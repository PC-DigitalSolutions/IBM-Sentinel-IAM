"""
Sentinel IAM Agent
==================
A single AI agent that triages suspicious logins for a bank.

Registered tools
----------------
1. get_live_threats  – live threat-intelligence lookup by IP
2. analyze_signal    – enrich a login signal (device, country, travel)
3. assess_login      – full risk assessment with tiered decision + ranked actions

Usage (prototype / simulation)
-------------------------------
    from sentinel_iam.agent import SentinelAgent
    agent = SentinelAgent()
    result = agent.run(login_event, login_history, auth_failure_log)
"""

from __future__ import annotations

import logging
from typing import Any

from sentinel_iam.tools.get_live_threats import get_live_threats
from sentinel_iam.tools.analyze_signal import analyze_signal
from sentinel_iam.tools.assess_login import (
    assess_login,
    TIER_NORMAL,
    TIER_INVESTIGATE,
    TIER_APPROVAL_REQUIRED,
)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Tool registry — all three tools in declaration order
# ---------------------------------------------------------------------------
TOOLS: dict[str, Any] = {
    "get_live_threats": get_live_threats,
    "analyze_signal": analyze_signal,
    "assess_login": assess_login,
}


class SentinelAgent:
    """
    Sentinel IAM: triage agent for suspicious bank logins.

    The agent owns each case end-to-end:
    - It calls assess_login to obtain a tiered risk assessment.
    - For INVESTIGATE cases it calls get_live_threats and analyze_signal
      directly and summarises findings.
    - For APPROVAL_REQUIRED cases it presents the approval-gate block and
      waits for analyst action (simulated via handle_analyst_decision).
    - All recommendations, evidence, and analyst decisions are logged.
    """

    def __init__(self) -> None:
        self._case_log: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(
        self,
        login_event: dict[str, Any],
        login_history: list[dict[str, Any]],
        auth_failure_log: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Triage one login event.  Returns the full assessment dict produced
        by assess_login, augmented with an 'agent_summary' key.
        """
        assessment = assess_login(login_event, login_history, auth_failure_log)
        tier = assessment.get("tier", TIER_APPROVAL_REQUIRED)

        summary_lines: list[str] = [
            f"Sentinel decision: {tier}",
            f"Failure count: {assessment.get('failure_count', '?')} "
            f"(trigger: {assessment.get('trigger_dimension', 'none')})",
        ]

        if assessment.get("escalation_signals"):
            summary_lines.append(
                f"Escalation signals: {', '.join(assessment['escalation_signals'])}"
            )

        if tier == TIER_INVESTIGATE:
            summary_lines.append(
                "Agent investigates: tools called, actions ranked — no analyst required "
                "unless signals escalate."
            )
        elif tier == TIER_APPROVAL_REQUIRED:
            summary_lines.append(
                "Solution ready: top action held for analyst approval."
            )
            if assessment.get("error"):
                summary_lines.append(
                    f"Evidence gap: {assessment['error']} — escalating to analyst."
                )
        else:  # NORMAL
            summary_lines.append("Failures are evidence only; no immediate action required.")

        if assessment.get("ranked_actions"):
            summary_lines.append("Ranked actions:")
            for item in assessment["ranked_actions"]:
                summary_lines.append(
                    f"  {item['rank']}. {item['action']} — {item['reason']}"
                )

        assessment["agent_summary"] = "\n".join(summary_lines)
        self._log_case(assessment)
        return assessment

    # ------------------------------------------------------------------
    # Analyst decision handling (simulated)
    # ------------------------------------------------------------------

    def handle_analyst_decision(
        self,
        assessment: dict[str, Any],
        decision: str,
        override_action: str | None = None,
    ) -> dict[str, Any]:
        """
        Process an analyst decision for an APPROVAL_REQUIRED case.

        Parameters
        ----------
        assessment     : dict returned by run()
        decision       : "approve" | "override" | "reject"
        override_action: required when decision == "override"; the analyst's
                         chosen action string from CANDIDATE_ACTIONS.

        Returns
        -------
        Updated assessment dict with 'analyst_decision' and 'execution_log'.
        """
        user_id = assessment.get("user_id", "UNKNOWN")
        decision_l = decision.lower()

        if decision_l == "approve":
            top = assessment["ranked_actions"][0]["action"]
            execution_log = (
                f"[APPROVED] Executing: {top} for account {user_id}. "
                f"Action confirmed and logged."
            )
            assessment["analyst_decision"] = "approve"
            assessment["executed_action"] = top
            assessment["execution_log"] = execution_log
            log.info("Analyst approved action '%s' for %s", top, user_id)

        elif decision_l == "override":
            if not override_action:
                assessment["analyst_decision"] = "override_error"
                assessment["execution_log"] = (
                    "Override requires override_action to be specified."
                )
                return assessment
            # Re-rank with override action first
            original_ranked = assessment.get("ranked_actions", [])
            reranked = [r for r in original_ranked if r["action"] == override_action]
            reranked += [r for r in original_ranked if r["action"] != override_action]
            assessment["ranked_actions"] = [
                {**r, "rank": i + 1} for i, r in enumerate(reranked)
            ]
            execution_log = (
                f"[OVERRIDE] Analyst chose: {override_action} for account {user_id}. "
                f"Re-ranked and executed. Original top action was: "
                f"{original_ranked[0]['action'] if original_ranked else 'unknown'}."
            )
            assessment["analyst_decision"] = "override"
            assessment["executed_action"] = override_action
            assessment["execution_log"] = execution_log
            log.info("Analyst overrode to '%s' for %s", override_action, user_id)

        elif decision_l == "reject":
            execution_log = (
                f"[REJECTED] Analyst rejected all actions for account {user_id}. "
                f"No action taken. Logged for audit."
            )
            assessment["analyst_decision"] = "reject"
            assessment["executed_action"] = None
            assessment["execution_log"] = execution_log
            log.info("Analyst rejected action for %s", user_id)

        else:
            assessment["analyst_decision"] = "unknown"
            assessment["execution_log"] = f"Unknown decision: {decision!r}"

        self._log_case(assessment)
        return assessment

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _log_case(self, assessment: dict[str, Any]) -> None:
        """Append to in-memory case log (replace with persistent store in prod)."""
        self._case_log.append(assessment)
        log.debug("Case logged for user=%s tier=%s",
                  assessment.get("user_id"), assessment.get("tier"))

    def get_case_log(self) -> list[dict[str, Any]]:
        """Return all logged cases (read-only copy)."""
        return list(self._case_log)
