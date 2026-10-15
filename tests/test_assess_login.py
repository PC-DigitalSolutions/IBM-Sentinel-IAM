"""
Tests for assess_login — Sentinel IAM Tool
Validates the flag-based risk-score system defined in scenarios.json
and iam_baselines.json. All data is synthetic.
"""

from __future__ import annotations

import re
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from sentinel_iam.tools.assess_login import (
    assess_login,
    FAILURE_WINDOW_MINUTES,
    AGENT_TRIGGER_FAILURES,
    APPROVAL_GATE_FAILURES,
    TIER_NORMAL,
    TIER_INVESTIGATE,
    TIER_APPROVAL_REQUIRED,
    CANDIDATE_ACTIONS,
    FLAG_WEIGHTS,
)
from sentinel_iam.agent import SentinelAgent, TOOLS

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_TS = datetime(2026, 10, 2, 14, 0, 0, tzinfo=timezone.utc)   # 14:00 UTC = business hours


def ts(offset_minutes: float = 0) -> str:
    return (BASE_TS + timedelta(minutes=offset_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")


# Profiles from iam_baselines.json
JDOE_PROFILE = {"usual_hours_utc": [12, 23], "known_devices": ["win-jdoe-laptop", "iphone-jdoe"], "home_geo": "Newark, US"}
MGARCIA_PROFILE = {"usual_hours_utc": [13, 22], "known_devices": ["mac-mgarcia"], "home_geo": "Miami, US"}
TKIM_PROFILE = {"usual_hours_utc": [14, 23], "known_devices": ["win-tkim-desk"], "home_geo": "Chicago, US"}

# jdoe's last login was Newark, US
JDOE_HISTORY = [
    {"user_id": "jdoe", "geolocation": "Newark, US", "device_id": "win-jdoe-laptop",
     "timestamp": "2026-10-02T02:34:00Z", "outcome": "success"},
]
MGARCIA_HISTORY = [
    {"user_id": "mgarcia", "geolocation": "Miami, US", "device_id": "mac-mgarcia",
     "timestamp": "2026-10-01T21:10:00Z", "outcome": "success"},
]
TKIM_HISTORY = [
    {"user_id": "tkim", "geolocation": "Chicago, US", "device_id": "win-tkim-desk",
     "timestamp": "2026-10-01T22:45:00Z", "outcome": "success"},
]


def make_event(
    user_id: str = "jdoe",
    source_ip: str = "198.51.100.20",
    geolocation: str = "Newark, US",
    device_id: str = "win-jdoe-laptop",
    auth_method: str = "password",
    outcome: str = "success",
    timestamp: str | None = None,
) -> dict:
    return {
        "user_id": user_id,
        "timestamp": timestamp or ts(0),
        "source_ip": source_ip,
        "geolocation": geolocation,
        "device_id": device_id,
        "auth_method": auth_method,
        "outcome": outcome,
    }


HEDGING_PATTERN = re.compile(
    r"\b(probably|likely|might|maybe|perhaps|possibly|could be|seems|appears)\b",
    re.IGNORECASE,
)


def assert_no_hedging(text: str) -> None:
    m = HEDGING_PATTERN.search(text)
    assert m is None, f"Hedging word found: {m.group()!r}\n\nFull text:\n{text}"


# ---------------------------------------------------------------------------
# Scenario A — impossible_travel + ip_on_threat_list + new_device + off_hours
#   score = 35+30+25+10 = 100, Critical, APPROVAL_REQUIRED
# ---------------------------------------------------------------------------

def test_scenario_a_critical():
    """Account takeover: impossible travel from threat-listed IP at 3 AM."""
    event = make_event(
        user_id="jdoe",
        source_ip="203.0.113.66",       # in threat_ips
        geolocation="Lagos, NG",         # different from last login Newark, US
        device_id="win-unknown-7f2",     # not in jdoe known_devices
        timestamp="2026-10-02T03:14:00Z",  # 03:14 UTC, outside [12,23)
        outcome="failure",
    )
    result = assess_login(event, JDOE_HISTORY, [], user_profile=JDOE_PROFILE)

    assert set(result["flags"]) == {"impossible_travel", "ip_on_threat_list", "new_device", "off_hours"}
    assert result["risk_score"] == 100
    assert result["risk_level"] == "Critical"
    assert result["tier"] == TIER_APPROVAL_REQUIRED
    assert "approval_gate_output" in result


# ---------------------------------------------------------------------------
# Scenario B — no flags, score=0, Low, NORMAL
# ---------------------------------------------------------------------------

def test_scenario_b_normal():
    """Normal login: known device, home city, business hours."""
    event = make_event(
        user_id="jdoe",
        source_ip="198.51.100.20",
        geolocation="Newark, US",
        device_id="win-jdoe-laptop",
        timestamp="2026-10-02T14:00:00Z",  # 14:00 UTC, inside [12,23)
        outcome="success",
    )
    result = assess_login(event, JDOE_HISTORY, [], user_profile=JDOE_PROFILE)

    assert result["flags"] == []
    assert result["risk_score"] == 0
    assert result["risk_level"] == "Low"
    assert result["tier"] == TIER_NORMAL
    assert "approval_gate_output" not in result


# ---------------------------------------------------------------------------
# Scenario C — new_device only, score=25, Medium, INVESTIGATE
# ---------------------------------------------------------------------------

def test_scenario_c_medium_investigate():
    """New device, home city, business hours."""
    event = make_event(
        user_id="mgarcia",
        source_ip="198.51.100.45",
        geolocation="Miami, US",
        device_id="win-unknown-3c1",     # not in mgarcia known_devices
        timestamp="2026-10-02T15:30:00Z",  # 15:30 UTC, inside [13,22)
        outcome="success",
    )
    result = assess_login(event, MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE)

    assert result["flags"] == ["new_device"]
    assert result["risk_score"] == 25
    assert result["risk_level"] == "Medium"
    assert result["tier"] == TIER_INVESTIGATE
    assert "approval_gate_output" not in result


# ---------------------------------------------------------------------------
# Scenario D — off_hours only, score=10, Low, NORMAL
# ---------------------------------------------------------------------------

def test_scenario_d_off_hours_low():
    """Off-hours login from known device and home city."""
    event = make_event(
        user_id="tkim",
        source_ip="198.51.100.77",
        geolocation="Chicago, US",
        device_id="win-tkim-desk",
        timestamp="2026-10-02T06:00:00Z",  # 06:00 UTC, outside [14,23)
        outcome="success",
    )
    result = assess_login(event, TKIM_HISTORY, [], user_profile=TKIM_PROFILE)

    assert result["flags"] == ["off_hours"]
    assert result["risk_score"] == 10
    assert result["risk_level"] == "Low"
    assert result["tier"] == TIER_NORMAL


# ---------------------------------------------------------------------------
# Scenario F — ip_on_threat_list + new_device, score=55, High, APPROVAL_REQUIRED
# ---------------------------------------------------------------------------

def test_scenario_f_high_approval_required():
    """Threat-listed IP plus new device."""
    event = make_event(
        user_id="mgarcia",
        source_ip="203.0.113.66",         # in threat_ips
        geolocation="Miami, US",
        device_id="android-unknown-9a2",  # not in mgarcia known_devices
        timestamp="2026-10-02T16:00:00Z",  # 16:00 UTC, inside [13,22)
        outcome="failure",
    )
    result = assess_login(event, MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE)

    assert set(result["flags"]) == {"ip_on_threat_list", "new_device"}
    assert result["risk_score"] == 55
    assert result["risk_level"] == "High"
    assert result["tier"] == TIER_APPROVAL_REQUIRED
    assert "approval_gate_output" in result


# ---------------------------------------------------------------------------
# Score arithmetic
# ---------------------------------------------------------------------------

def test_score_capped_at_100():
    """Score must not exceed 100 even if all flags fire."""
    total = sum(FLAG_WEIGHTS.values())
    assert total >= 100, "test precondition: weights sum >= 100"
    event = make_event(
        user_id="jdoe",
        source_ip="203.0.113.66",
        geolocation="Lagos, NG",
        device_id="win-unknown-7f2",
        timestamp="2026-10-02T03:14:00Z",
        outcome="failure",
    )
    result = assess_login(event, JDOE_HISTORY, [], user_profile=JDOE_PROFILE)
    assert result["risk_score"] <= 100


def test_score_zero_no_flags():
    event = make_event(timestamp="2026-10-02T14:00:00Z")
    result = assess_login(event, JDOE_HISTORY, [], user_profile=JDOE_PROFILE)
    assert result["risk_score"] == 0
    assert result["flags"] == []


# ---------------------------------------------------------------------------
# Tier boundaries
# ---------------------------------------------------------------------------

def test_medium_score_is_investigate():
    """Score 25 (new_device only) → Medium → INVESTIGATE."""
    result = assess_login(
        make_event(user_id="mgarcia", device_id="win-unknown-3c1",
                   timestamp="2026-10-02T15:30:00Z"),
        MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE,
    )
    assert result["tier"] == TIER_INVESTIGATE
    assert "approval_gate_output" not in result


def test_high_score_is_approval_required():
    """Score >=50 → High → APPROVAL_REQUIRED with gate."""
    result = assess_login(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE,
    )
    assert result["tier"] == TIER_APPROVAL_REQUIRED
    assert "approval_gate_output" in result
    gate = result["approval_gate_output"]
    assert "AWAITING ANALYST APPROVAL" in gate
    assert "[Approve]" in gate
    assert "[Override]" in gate
    assert "[Reject]" in gate
    assert "SENTINEL DECISION:" in gate
    assert "SOLUTION READY:" in gate


# ---------------------------------------------------------------------------
# Tool failure → always escalates, never auto-approves
# ---------------------------------------------------------------------------

def test_tool_failure_escalates():
    with patch(
        "sentinel_iam.tools.assess_login.get_live_threats",
        side_effect=RuntimeError("simulated outage"),
    ):
        result = assess_login(make_event(), JDOE_HISTORY, [])

    assert result["tier"] == TIER_APPROVAL_REQUIRED
    assert "tool_failure" in result["flags"]
    assert "error" in result
    assert "approval_gate_output" in result
    assert "AWAITING ANALYST APPROVAL" in result["approval_gate_output"]


def test_analyze_signal_failure_escalates():
    with patch(
        "sentinel_iam.tools.assess_login.analyze_signal",
        side_effect=RuntimeError("simulated outage"),
    ):
        result = assess_login(make_event(), JDOE_HISTORY, [])

    assert result["tier"] == TIER_APPROVAL_REQUIRED
    assert "tool_failure" in result["flags"]
    assert "approval_gate_output" in result


# ---------------------------------------------------------------------------
# Approval gate format
# ---------------------------------------------------------------------------

def test_approval_gate_format_fields():
    result = assess_login(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE,
    )
    gate = result["approval_gate_output"]
    assert "CASE:" in gate
    assert "SENTINEL DECISION:" in gate
    assert "WHY:" in gate
    assert "SOLUTION READY:" in gate
    assert "STATUS: AWAITING ANALYST APPROVAL" in gate


# ---------------------------------------------------------------------------
# No hedging words
# ---------------------------------------------------------------------------

def test_no_hedging_in_normal():
    result = assess_login(make_event(timestamp="2026-10-02T14:00:00Z"),
                          JDOE_HISTORY, [], user_profile=JDOE_PROFILE)
    for item in result.get("ranked_actions", []):
        assert_no_hedging(item["reason"])


def test_no_hedging_in_investigate():
    result = assess_login(
        make_event(user_id="mgarcia", device_id="win-unknown-3c1",
                   timestamp="2026-10-02T15:30:00Z"),
        MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE,
    )
    for item in result.get("ranked_actions", []):
        assert_no_hedging(item["reason"])


def test_no_hedging_in_approval():
    result = assess_login(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [], user_profile=MGARCIA_PROFILE,
    )
    for item in result.get("ranked_actions", []):
        assert_no_hedging(item["reason"])
    if "approval_gate_output" in result:
        assert_no_hedging(result["approval_gate_output"])


def test_no_hedging_in_agent_summary():
    agent = SentinelAgent()
    result = agent.run(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [],
    )
    assert_no_hedging(result["agent_summary"])


# ---------------------------------------------------------------------------
# Agent registry and analyst decision flow
# ---------------------------------------------------------------------------

def test_tools_registered_in_agent():
    assert "get_live_threats" in TOOLS
    assert "analyze_signal" in TOOLS
    assert "assess_login" in TOOLS


def test_analyst_approve_executes_top_action():
    agent = SentinelAgent()
    assessment = agent.run(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [],
    )
    assert assessment["tier"] == TIER_APPROVAL_REQUIRED
    updated = agent.handle_analyst_decision(assessment, "approve")
    assert updated["analyst_decision"] == "approve"
    assert updated["executed_action"] == "Block session and force credential reset"
    assert "[APPROVED]" in updated["execution_log"]


def test_analyst_override_reranks():
    agent = SentinelAgent()
    assessment = agent.run(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [],
    )
    override = "Require step-up authentication (MFA)"
    updated = agent.handle_analyst_decision(assessment, "override", override_action=override)
    assert updated["analyst_decision"] == "override"
    assert updated["executed_action"] == override
    assert updated["ranked_actions"][0]["action"] == override
    assert "[OVERRIDE]" in updated["execution_log"]


def test_analyst_reject_takes_no_action():
    agent = SentinelAgent()
    assessment = agent.run(
        make_event(user_id="mgarcia", source_ip="203.0.113.66",
                   device_id="android-unknown-9a2",
                   timestamp="2026-10-02T16:00:00Z"),
        MGARCIA_HISTORY, [],
    )
    updated = agent.handle_analyst_decision(assessment, "reject")
    assert updated["analyst_decision"] == "reject"
    assert updated["executed_action"] is None
    assert "[REJECTED]" in updated["execution_log"]


def test_ranked_actions_complete_and_ordered():
    """ranked_actions must contain all CANDIDATE_ACTIONS in rank order 1..N."""
    result = assess_login(make_event(), JDOE_HISTORY, [])
    assert len(result["ranked_actions"]) == len(CANDIDATE_ACTIONS)
    assert [a["rank"] for a in result["ranked_actions"]] == list(range(1, len(CANDIDATE_ACTIONS) + 1))
