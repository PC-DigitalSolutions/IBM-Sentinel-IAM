"""
assess_login — Sentinel IAM tool

Scores a login event using the flag-based risk system defined in
tests/fixtures/iam_baselines.json and tests/scenarios.json.

Flag weights (from iam_baselines.json)
---------------------------------------
  impossible_travel  +35
  ip_on_threat_list  +30
  new_device         +25
  off_hours          +10
  cap                100

Risk levels → tiers
-------------------
  Critical (>=80)  → APPROVAL_REQUIRED
  High     (>=50)  → APPROVAL_REQUIRED
  Medium   (>=25)  → INVESTIGATE
  Low      ( >=0)  → NORMAL
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from sentinel_iam.tools.get_live_threats import get_live_threats
from sentinel_iam.tools.analyze_signal import analyze_signal

# ---------------------------------------------------------------------------
# Tier labels
# ---------------------------------------------------------------------------
TIER_NORMAL = "NORMAL"
TIER_INVESTIGATE = "INVESTIGATE"
TIER_APPROVAL_REQUIRED = "APPROVAL_REQUIRED"

# ---------------------------------------------------------------------------
# Flag weights — mirror iam_baselines.json scoring block exactly
# ---------------------------------------------------------------------------
FLAG_WEIGHTS: dict[str, int] = {
    "impossible_travel":  35,
    "ip_on_threat_list":  30,
    "new_device":         25,
    "off_hours":          10,
}
MAX_SCORE: int = 100

# Risk-level thresholds (descending order)
RISK_LEVELS: list[tuple[int, str]] = [
    (80, "Critical"),
    (50, "High"),
    (25, "Medium"),
    (0,  "Low"),
]

# Business hours fallback when user profile is unknown (UTC)
DEFAULT_HOURS_START: int = 9
DEFAULT_HOURS_END: int = 17

# Kept for backward-compat and for the failure-window evidence block
FAILURE_WINDOW_MINUTES: int = 15
AGENT_TRIGGER_FAILURES: int = 2   # not used for tier, kept for tests that read it
APPROVAL_GATE_FAILURES: int = 4   # not used for tier, kept for tests that read it

# Candidate actions (ordered Critical→Low)
CANDIDATE_ACTIONS = [
    "Block session and force credential reset",
    "Require step-up authentication (MFA)",
    "Escalate to analyst",
    "Allow and monitor",
    "Allow",
]

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_ts(ts: str) -> datetime | None:
    """Parse an ISO-8601 UTC timestamp; return None on failure."""
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _score_flags(flags: list[str]) -> int:
    """Sum flag weights, capped at MAX_SCORE."""
    return min(sum(FLAG_WEIGHTS.get(f, 0) for f in flags), MAX_SCORE)


def _risk_level(score: int) -> str:
    for threshold, level in RISK_LEVELS:
        if score >= threshold:
            return level
    return "Low"


def _tier_from_level(level: str) -> str:
    if level in ("Critical", "High"):
        return TIER_APPROVAL_REQUIRED
    if level == "Medium":
        return TIER_INVESTIGATE
    return TIER_NORMAL


def _is_off_hours(timestamp: str, user_profile: dict[str, Any] | None) -> bool:
    """
    Return True when the login hour (UTC) falls outside the user's usual hours.
    Falls back to DEFAULT_HOURS_START–DEFAULT_HOURS_END when no profile exists.
    usual_hours_utc is [start, end) — end is exclusive.
    """
    dt = _parse_ts(timestamp)
    if dt is None:
        return False
    hour = dt.hour
    if user_profile:
        hours = user_profile.get("usual_hours_utc", [DEFAULT_HOURS_START, DEFAULT_HOURS_END])
    else:
        hours = [DEFAULT_HOURS_START, DEFAULT_HOURS_END]
    start, end = hours[0], hours[1]
    return not (start <= hour < end)


def _count_failures_in_window(
    records: list[dict[str, Any]],
    anchor_ts: datetime,
    window_minutes: int,
    key_field: str,
    key_value: str,
) -> int:
    """Count failure records within window_minutes before anchor_ts."""
    count = 0
    for record in records:
        if str(record.get("outcome", "")).lower() == "success":
            continue
        if record.get(key_field) != key_value:
            continue
        ts = _parse_ts(record.get("timestamp", ""))
        if ts is None:
            continue
        delta = (anchor_ts - ts).total_seconds() / 60
        if 0 <= delta <= window_minutes:
            count += 1
    return count


def _rank_actions(tier: str, flags: list[str]) -> list[dict[str, str]]:
    """Return CANDIDATE_ACTIONS with per-tier reasons."""
    ranked = []
    for i, action in enumerate(CANDIDATE_ACTIONS):
        if tier == TIER_NORMAL:
            if action == "Allow":
                reason = "Risk score is Low; no flags triggered."
            elif action == "Allow and monitor":
                reason = "No flags active; passive monitoring only."
            elif action == "Require step-up authentication (MFA)":
                reason = "Optional precaution for borderline cases."
            elif action == "Block session and force credential reset":
                reason = "Reserved for Critical/High risk."
            else:
                reason = "Not warranted at Low risk."
        elif tier == TIER_INVESTIGATE:
            if action == "Require step-up authentication (MFA)":
                reason = "Medium risk detected; step-up reduces exposure without locking the account."
            elif action == "Block session and force credential reset":
                reason = "Stronger option if step-up fails or additional signals emerge."
            elif action == "Escalate to analyst":
                reason = "Engage analyst if automated step-up is inconclusive."
            elif action == "Allow and monitor":
                reason = "Permit with enhanced logging if step-up is unavailable."
            else:
                reason = "Only if all other options are exhausted."
        else:  # APPROVAL_REQUIRED
            flag_str = ", ".join(flags) if flags else "risk threshold exceeded"
            if action == "Block session and force credential reset":
                reason = f"Critical/High risk. Flags: {flag_str}. Session blocked; credential reset required."
            elif action == "Require step-up authentication (MFA)":
                reason = "Lower-impact alternative if analyst overrides block."
            elif action == "Escalate to analyst":
                reason = "Fallback when block cannot be executed automatically."
            elif action == "Allow and monitor":
                reason = "Only if analyst explicitly downgrades risk."
            else:
                reason = "Not recommended at Critical/High risk."
        ranked.append({"action": action, "reason": reason, "rank": i + 1})
    return ranked


def _build_approval_gate_output(
    user_id: str,
    risk_score: int,
    risk_level: str,
    outcome: str,
    ranked_actions: list[dict[str, str]],
    flags: list[str],
) -> str:
    """Format the approval-gate block."""
    top_action = ranked_actions[0]["action"]
    flag_str = ", ".join(flags) if flags else "none"
    why = f"Risk score {risk_score} ({risk_level}); flags: {flag_str}; outcome: {outcome}."

    steps = [
        f"1. Immediately block active session for account {user_id}.",
        "2. Invalidate all existing session tokens.",
        "3. Lock account pending credential reset.",
        "4. Send secure reset link via registered out-of-band channel.",
        "5. Notify account holder and log incident in SIEM.",
        "6. Re-evaluate after successful reset and MFA enrollment.",
    ]

    lines = [
        f"CASE: {user_id} | score {risk_score} ({risk_level}), {outcome}",
        f"SENTINEL DECISION: {top_action}",
        f"WHY: {why}",
        "SOLUTION READY:",
        *[f"  {s}" for s in steps],
        "STATUS: AWAITING ANALYST APPROVAL [Approve] [Override] [Reject]",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public tool function
# ---------------------------------------------------------------------------

def assess_login(
    login_event: dict[str, Any],
    login_history: list[dict[str, Any]],
    auth_failure_log: list[dict[str, Any]],
    user_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Assess the risk of a login event using the flag/score system.

    Parameters
    ----------
    login_event : dict with keys
        user_id, timestamp, source_ip, geolocation, device_id,
        auth_method, outcome
    login_history     : previous successful logins for this user
    auth_failure_log  : recent auth events (for supplemental evidence)
    user_profile      : optional dict from iam_baselines users block
                        (keys: usual_hours_utc, known_devices, home_geo, etc.)

    Returns
    -------
    dict with keys
        user_id              – str
        tier                 – NORMAL | INVESTIGATE | APPROVAL_REQUIRED
        risk_score           – int  (0–100)
        risk_level           – Low | Medium | High | Critical
        flags                – list[str] of triggered flag names
        escalation_signals   – same as flags (alias kept for compatibility)
        ranked_actions       – list of {rank, action, reason}
        approval_gate_output – str (only when tier == APPROVAL_REQUIRED)
        evidence             – dict of supporting data
        failure_count        – int, failures in the rolling window (supplemental)
        account_failures     – int
        ip_failures          – int
        trigger_dimension    – "account" | "ip" | None
        error                – str (only on tool failure)
        missing_evidence     – list[str] (only when tools fail)
    """
    # --- validate required fields -------------------------------------------
    required = ("user_id", "timestamp", "source_ip", "geolocation",
                 "device_id", "auth_method", "outcome")
    missing_fields = [f for f in required if f not in login_event]
    if missing_fields:
        return {
            "user_id": login_event.get("user_id", "UNKNOWN"),
            "tier": TIER_APPROVAL_REQUIRED,
            "risk_score": MAX_SCORE,
            "risk_level": "Critical",
            "flags": ["tool_failure"],
            "escalation_signals": ["tool_failure"],
            "error": f"missing required fields in login_event: {missing_fields}",
            "missing_evidence": missing_fields,
            "ranked_actions": _rank_actions(TIER_APPROVAL_REQUIRED, ["tool_failure"]),
        }

    user_id: str   = login_event["user_id"]
    timestamp: str = login_event["timestamp"]
    source_ip: str = login_event["source_ip"]
    geolocation: str = login_event["geolocation"]
    device_id: str = login_event["device_id"]
    auth_method: str = login_event["auth_method"]
    outcome: str   = login_event["outcome"]

    anchor_ts = _parse_ts(timestamp)
    if anchor_ts is None:
        return {
            "user_id": user_id,
            "tier": TIER_APPROVAL_REQUIRED,
            "risk_score": MAX_SCORE,
            "risk_level": "Critical",
            "flags": ["tool_failure"],
            "escalation_signals": ["tool_failure"],
            "error": f"unparseable timestamp: {timestamp!r}",
            "missing_evidence": ["timestamp"],
            "ranked_actions": _rank_actions(TIER_APPROVAL_REQUIRED, ["tool_failure"]),
        }

    # --- supplemental failure counts (evidence only) ------------------------
    account_failures = _count_failures_in_window(
        auth_failure_log, anchor_ts, FAILURE_WINDOW_MINUTES,
        key_field="user_id", key_value=user_id,
    )
    ip_failures = _count_failures_in_window(
        auth_failure_log, anchor_ts, FAILURE_WINDOW_MINUTES,
        key_field="source_ip", key_value=source_ip,
    )
    failure_count = max(account_failures, ip_failures)
    trigger_dimension: str | None = None
    if failure_count > 0:
        trigger_dimension = "ip" if ip_failures >= account_failures else "account"

    # --- call tools ---------------------------------------------------------
    tool_errors: list[str] = []
    missing_evidence: list[str] = []
    threat_result: dict[str, Any] = {}
    signal_result: dict[str, Any] = {}

    try:
        threat_result = get_live_threats(source_ip)
        if "error" in threat_result:
            tool_errors.append(f"get_live_threats: {threat_result['error']}")
            missing_evidence.append("live_threat_data")
    except Exception as exc:  # noqa: BLE001
        tool_errors.append(f"get_live_threats raised: {exc}")
        missing_evidence.append("live_threat_data")
        threat_result = {"match_found": None}

    try:
        signal_result = analyze_signal(
            user_id=user_id,
            source_ip=source_ip,
            geolocation=geolocation,
            device_id=device_id,
            timestamp=timestamp,
            login_history=login_history,
        )
        if "error" in signal_result:
            tool_errors.append(f"analyze_signal: {signal_result['error']}")
            missing_evidence.append("signal_analysis")
    except Exception as exc:  # noqa: BLE001
        tool_errors.append(f"analyze_signal raised: {exc}")
        missing_evidence.append("signal_analysis")
        signal_result = {"new_device": None, "new_country": None, "impossible_travel": None}

    if tool_errors:
        log.warning("assess_login: tool failure(s) for %s: %s", user_id, tool_errors)
        err_actions = _rank_actions(TIER_APPROVAL_REQUIRED, ["tool_failure"])
        result: dict[str, Any] = {
            "user_id": user_id,
            "tier": TIER_APPROVAL_REQUIRED,
            "risk_score": MAX_SCORE,
            "risk_level": "Critical",
            "flags": ["tool_failure"],
            "escalation_signals": ["tool_failure"],
            "failure_count": failure_count,
            "account_failures": account_failures,
            "ip_failures": ip_failures,
            "trigger_dimension": trigger_dimension,
            "ranked_actions": err_actions,
            "error": (
                "Tool failure(s) detected — evidence incomplete. "
                f"Escalating to analyst. Details: {'; '.join(tool_errors)}"
            ),
            "missing_evidence": missing_evidence,
            "evidence": {
                "login_event": login_event,
                "threat_result": threat_result,
                "signal_result": signal_result,
            },
        }
        result["approval_gate_output"] = _build_approval_gate_output(
            user_id, MAX_SCORE, "Critical", outcome, err_actions, ["tool_failure"],
        )
        return result

    # --- build flags --------------------------------------------------------
    flags: list[str] = []

    if signal_result.get("impossible_travel"):
        flags.append("impossible_travel")
    if threat_result.get("match_found"):
        flags.append("ip_on_threat_list")
    if signal_result.get("new_device"):
        flags.append("new_device")
    if _is_off_hours(timestamp, user_profile):
        flags.append("off_hours")

    # --- score and tier -----------------------------------------------------
    risk_score = _score_flags(flags)
    risk_level = _risk_level(risk_score)
    tier = _tier_from_level(risk_level)

    ranked_actions = _rank_actions(tier, flags)

    evidence = {
        "login_event": login_event,
        "flags": flags,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "account_failures_in_window": account_failures,
        "ip_failures_in_window": ip_failures,
        "failure_window_minutes": FAILURE_WINDOW_MINUTES,
        "trigger_dimension": trigger_dimension,
        "threat_intelligence": threat_result,
        "signal_analysis": signal_result,
    }

    result = {
        "user_id": user_id,
        "tier": tier,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "flags": flags,
        "escalation_signals": flags,   # alias for backward compat
        "failure_count": failure_count,
        "account_failures": account_failures,
        "ip_failures": ip_failures,
        "trigger_dimension": trigger_dimension,
        "ranked_actions": ranked_actions,
        "evidence": evidence,
    }

    if tier == TIER_APPROVAL_REQUIRED:
        result["approval_gate_output"] = _build_approval_gate_output(
            user_id, risk_score, risk_level, outcome, ranked_actions, flags,
        )

    log.info(
        "assess_login: user=%s score=%d level=%s tier=%s flags=%s",
        user_id, risk_score, risk_level, tier, flags,
    )
    return result
