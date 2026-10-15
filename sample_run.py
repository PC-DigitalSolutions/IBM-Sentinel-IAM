"""
sample_run.py — end-to-end demonstration of Sentinel IAM
Run: python sample_run.py

Uses test scenarios from scenarios.json
"""

from __future__ import annotations

from sentinel_iam.agent import SentinelAgent

# Scenario A: Critical (impossible travel + threat IP + new device + off-hours)
login_event = {
    "user_id": "jdoe",
    "timestamp": "2026-10-02T14:00:00Z",
    "source_ip": "198.51.100.20",
    "geolocation": "Newark, US",
    "device_id": "win-jdoe-laptop",
    "auth_method": "password",
    "outcome": "success",
}
login_history = [
    {"user_id": "jdoe", "geolocation": "Newark, US", "device_id": "win-jdoe-laptop",
     "timestamp": "2026-10-01T14:00:00Z", "outcome": "success"},
]

login_event = {
    "user_id": "mgarcia",
    "timestamp": "2026-10-02T15:30:00Z",
    "source_ip": "198.51.100.45",
    "geolocation": "Miami, US",
    "device_id": "win-unknown-3c1",
    "auth_method": "password",
    "outcome": "success",
}
login_history = [
    {"user_id": "mgarcia", "geolocation": "Miami, US", "device_id": "mac-mgarcia",
     "timestamp": "2026-10-01T15:00:00Z", "outcome": "success"},
]

auth_failure_log = []

# ── Run agent ────────────────────────────────────────────────────────────────
agent = SentinelAgent()
result = agent.run(login_event, login_history, auth_failure_log)

print("=" * 70)
print("SENTINEL IAM - SAMPLE RUN")
print("=" * 70)
print(f"\nUser:          {result['user_id']}")
print(f"Risk Score:    {result['risk_score']}")
print(f"Risk Level:    {result['risk_level']}")
print(f"Tier:          {result['tier']}")
print(f"Flags:         {', '.join(result['flags']) if result['flags'] else 'none'}")

print("\n-- Ranked Actions --")
for item in result.get("ranked_actions", []):
    print(f"  {item['rank']}. {item['action']}")
    print(f"     {item['reason']}")

print("\n-- Agent Summary --")
print(result["agent_summary"])

# Simulate analyst approval
if result["tier"] == "APPROVAL_REQUIRED":
    print("\n── Simulating Analyst Approval ──")
    updated = agent.handle_analyst_decision(result, "approve")
    print(updated["execution_log"])