"""
get_live_threats — Sentinel IAM tool
Queries a (simulated) threat-intelligence feed for indicators matching
an IP address or geolocation.  Returns a list of threat records.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Simulated threat-intelligence database (synthetic data only)
# ---------------------------------------------------------------------------
# IPs match iam_baselines.json threat_ips list
_THREAT_DB: dict[str, dict[str, Any]] = {
    "203.0.113.66": {
        "ip": "203.0.113.66",
        "threat_type": "credential_stuffing",
        "confidence": "HIGH",
        "first_seen": "2026-01-10T08:00:00Z",
        "last_seen": "2026-10-01T14:22:00Z",
        "source": "IBM X-Force",
    },
    "203.0.113.91": {
        "ip": "203.0.113.91",
        "threat_type": "password_spray",
        "confidence": "HIGH",
        "first_seen": "2026-03-15T11:00:00Z",
        "last_seen": "2026-09-28T09:45:00Z",
        "source": "IBM X-Force",
    },
    "192.0.2.144": {
        "ip": "192.0.2.144",
        "threat_type": "brute_force",
        "confidence": "MEDIUM",
        "first_seen": "2026-05-01T00:00:00Z",
        "last_seen": "2026-09-30T18:00:00Z",
        "source": "IBM X-Force",
    },
}


def get_live_threats(source_ip: str) -> dict[str, Any]:
    """
    Look up live threat-intelligence records for *source_ip*.

    Parameters
    ----------
    source_ip : str
        The IP address to query.

    Returns
    -------
    dict with keys:
        ip          – queried IP
        threats     – list of matching threat records (may be empty)
        match_found – True when at least one threat record exists
        error       – present only on failure
    """
    if not source_ip or not isinstance(source_ip, str):
        return {"ip": source_ip, "threats": [], "match_found": False,
                "error": "invalid input: source_ip must be a non-empty string"}

    threats = [_THREAT_DB[source_ip]] if source_ip in _THREAT_DB else []
    return {
        "ip": source_ip,
        "threats": threats,
        "match_found": bool(threats),
    }
