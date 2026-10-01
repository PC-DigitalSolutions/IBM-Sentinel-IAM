# Task 02: add `POST /iam/assess-login` to the backend

**Repo:** `C:\CyberLab\CyberShield_IV` (FastAPI). **Read only:** `src/api/main.py`, plus the two fixture files named below from the `sentinel-iam` repo. Don't scan anything else.

## Build
1. Copy `sentinel-iam/tests/fixtures/iam_baselines.json` to `CyberShield_IV/data/iam/baselines.json`.
2. Create `src/iam/__init__.py` and `src/iam/assess.py` with a **pure function** `assess_login(req: dict, seed: dict) -> dict`. No LLM, no network, no database.
   - `impossible_travel`: haversine distance between `last_login.geo` and `req.geo` (coordinates from `seed.cities`), divided by the hours between `last_login.timestamp` and `req.timestamp`. Flag it if the speed is over `scoring.impossible_travel_kmh` and the hours are > 0.
   - `ip_on_threat_list`: `req.ip` is in `seed.threat_ips`
   - `new_device`: `req.device_id` isn't in the user's `known_devices`
   - `off_hours`: the UTC hour of `req.timestamp` is outside `[usual_hours_utc[0], usual_hours_utc[1])`
   - Flags go in that order. `risk_score` = the sum of their points, capped at `max_score`. `risk_level` = the first entry in `scoring.levels` whose `min` ≤ score.
   - Return `{risk_score, risk_level, flags, baseline: {usual_geo, usual_hours_utc, known_devices: <count>}, explanation}`. `explanation` is one plain sentence built from the flags (e.g. "Login from Lagos, NG 40 min after a Newark, US session; unrecognized device; outside usual hours; IP is on the threat list.").
   - Unknown user → raise `KeyError`. Unknown city → treat as no travel data (no impossible_travel flag).
3. In `src/api/main.py`: add a Pydantic model `LoginAlert {user_id, ip, device_id, geo, timestamp}` and a route `POST /iam/assess-login`. Load the seed once at import time. Map `KeyError` → HTTP 404 `{"detail": "Unknown user"}`. Give it `operation_id="assess_login"` and a clear docstring, because Orchestrate reads these.
4. Create `tests/test_assess_login.py`. Load `sentinel-iam/tests/scenarios.json` (copy it to `CyberShield_IV/tests/scenarios.json`). For every scenario that has `expect.flags`, assert that flags, risk_score and risk_level match. Also add one route test for scenario G → 404. Use `TestClient(app)` **without** a `with` block so the background news monitor doesn't start.

## Done when
`python -m pytest tests/test_assess_login.py -q` passes. (`pip install pytest` first if it's missing.) Expected results: A=100 Critical, B=0 Low, C=25 Medium, D=10 Low, F=55 High, G=404.

## Don't
Touch other endpoints, add dependencies beyond pytest, or call Gemini.
