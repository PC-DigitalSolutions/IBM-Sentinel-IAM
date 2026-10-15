"""
analyze_signal — Sentinel IAM tool
Analyses a raw authentication signal and returns enriched context:
device familiarity, country change, and impossible-travel detection.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def analyze_signal(
    user_id: str,
    source_ip: str,
    geolocation: str,
    device_id: str,
    timestamp: str,
    login_history: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Enrich a login signal with contextual risk indicators.

    Parameters
    ----------
    user_id      : account identifier
    source_ip    : IP address of the current attempt
    geolocation  : country/region string, e.g. "US" or "RU"
    device_id    : device fingerprint
    timestamp    : ISO-8601 UTC timestamp of the current attempt
    login_history: list of previous successful login records for this user,
                   each a dict with at least 'geolocation', 'device_id',
                   'timestamp' keys.

    Returns
    -------
    dict with keys:
        new_device        – bool, device not seen in history
        new_country       – bool, geolocation not seen in history
        impossible_travel – bool, physically impossible move since last login
        last_known_geo    – str or None
        last_login_ts     – str or None
        error             – present only on failure
    """
    if not user_id or not isinstance(login_history, list):
        return {
            "new_device": None,
            "new_country": None,
            "impossible_travel": None,
            "last_known_geo": None,
            "last_login_ts": None,
            "error": "invalid input",
        }

    known_devices = {r.get("device_id") for r in login_history if r.get("device_id")}
    known_geos = {r.get("geolocation") for r in login_history if r.get("geolocation")}

    new_device = device_id not in known_devices if known_devices else False
    new_country = geolocation not in known_geos if known_geos else False

    # Impossible travel: >800 km in <2 hours (simplified: different country
    # within 30 minutes of last login counts as impossible in this prototype).
    impossible_travel = False
    last_known_geo = None
    last_login_ts = None

    if login_history:
        sorted_hist = sorted(
            login_history, key=lambda r: r.get("timestamp", ""), reverse=True
        )
        last = sorted_hist[0]
        last_known_geo = last.get("geolocation")
        last_login_ts = last.get("timestamp")

        if last_login_ts and new_country:
            try:
                t_last = datetime.fromisoformat(last_login_ts.replace("Z", "+00:00"))
                t_now = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                delta_minutes = abs((t_now - t_last).total_seconds()) / 60
                if delta_minutes < 60:
                    impossible_travel = True
            except ValueError:
                pass

    return {
        "new_device": new_device,
        "new_country": new_country,
        "impossible_travel": impossible_travel,
        "last_known_geo": last_known_geo,
        "last_login_ts": last_login_ts,
    }
