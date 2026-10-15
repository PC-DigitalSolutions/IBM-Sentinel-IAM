# Task 03b: add the 5-minute authentication-failure flag to `assess_login`

**Owner:** Technical Support / QA (on your own Bob credits).
**Decisions (Aldo, Oct 15, 2026):**
- The failure count lives **inside `assess_login`**, not in a fourth tool. This keeps the settled "reuse the backend, add one new tool" rule. The count is reported next to the score and **does not change the 35/30/25/10 scoring**.
- **2 failed attempts within 5 minutes flags the case.** This replaces the earlier 15-minute window, the 2-failure investigate tier and the 4+ manual-approval tier.

**Repo:** `C:\CyberLab\CyberShield_IV`. **Read only:** `src/iam/assess.py`, `data/iam/baselines.json`, `tests/test_assess_login.py`, `tests/scenarios.json`. Don't scan anything else. Don't touch `src/api/main.py` unless a test proves the route needs it.

## Policy (do not change the numbers)
- Count authentication failures **for the account** (`user_id`) in the **5 minutes up to and including** the alert timestamp: `alert_ts - 5 min <= failure_ts <= alert_ts`. Failures after the alert don't count.
- 0 or 1 failures → `failure_flag: false`
- 2 or more failures → `failure_flag: true`. The agent then investigates and prepares a ranked recommendation for the analyst. Approval is still required for every action.
- No other thresholds. The earlier ones (15-minute window, 4 or more, 7, 3 to 6, 5 or more) are all retired.

## Build
1. In `data/iam/baselines.json`, add:
   - Under `scoring`: `"auth_failure_window_minutes": 5, "auth_failure_flag_threshold": 2`.
   - A top-level `"auth_failures"` list. Each record is `{"user_id", "ip", "timestamp"}`. Add exactly these fictional records:
     - jdoe, `198.51.100.20`, `2026-10-02T16:56:00Z` (inside K's window)
     - jdoe, `198.51.100.20`, `2026-10-02T16:58:00Z` (inside K's window)
     - mgarcia, `198.51.100.45`, `2026-10-02T17:50:00Z` (outside L's window)
     - mgarcia, `198.51.100.45`, `2026-10-02T17:54:00Z` (outside L's window, 6 minutes before the alert)
   - A fourth user with thin history: `"sbrooks": {"display_name": "S. Brooks (Commercial Lending)", "home_geo": "Miami, US", "usual_hours_utc": [13, 22], "known_devices": ["mac-sbrooks"], "last_login": null}`.
2. In `src/iam/assess.py`:
   - Count failures with the rule above, reading the window and threshold from `seed.scoring`. A missing `auth_failures` list means 0.
   - Add three response fields: `auth_failures_in_window` (int), `auth_failure_window_minutes` (int, 5), and `failure_flag` (bool).
   - Add `last_login_known` (bool) to `baseline`. A `null` `last_login` means no travel data, so no `impossible_travel` flag, and the function must not crash.
   - When `failure_flag` is true, append one plain sentence to `explanation`, for example "2 failed sign-in attempts in the last 5 minutes." No hedging words.
   - Keep `assess_login(req, seed)` pure: no LLM, no network, no database.
3. Copy the updated `baselines.json` back to `sentinel-iam/tests/fixtures/iam_baselines.json` so both copies match.
4. Copy `sentinel-iam/tests/scenarios.json` (it now includes H and J) over `CyberShield_IV/tests/scenarios.json`. Then append scenarios I, K and L to `tests/scenarios.json` in **both** repos:
   - **I:** `sbrooks`, `198.51.100.88`, `mac-sbrooks`, `Miami, US`, `2026-10-02T16:00:00Z` → flags `[]`, score 0, Low, `baseline.last_login_known` false.
   - **K:** `jdoe`, `198.51.100.20`, `win-jdoe-laptop`, `Newark, US`, `2026-10-02T17:00:00Z` → flags `[]`, score 0, Low, `auth_failures_in_window` 2, `failure_flag` true, `action` `"step_up_mfa"` (agent expectation: flagged + Low ranks step-up MFA first).
   - **L:** `mgarcia`, `198.51.100.45`, `mac-mgarcia`, `Miami, US`, `2026-10-02T18:00:00Z` → flags `[]`, score 0, Low, `auth_failures_in_window` 0, `failure_flag` false (2 failures exist, but both fall outside the 5-minute window).
5. In `tests/test_assess_login.py`, add:
   - Scenario tests for I, K and L (the existing loop over `expect.flags` can cover score and level; assert the new fields too).
   - Pure-function tests that pass a modified seed with 1, 2, 3 and 4 failures inside the window → `failure_flag` false, true, true, true.
   - Window-edge tests: a failure exactly 5:00 before the alert counts; one 5:01 before doesn't; one after the alert doesn't.
   - A check that scenarios A to H still return the same flags, score and level as before.

## Done when
`python -m pytest tests/test_assess_login.py -q` passes, including A, B, C, D, F, G, H and the new tests. Save the output for evidence: the 1, 2, 3 and 4 failure results with the expected behavior beside each (playbook §5, Task 03).

## Don't
Change the scoring points or levels, add a new endpoint or tool, add dependencies, call Gemini, or use any IP outside `203.0.113.x`, `198.51.100.x`, `192.0.2.x`.

## After the session
Screenshot the Bob consumption summary into `sentinel-iam/bob_sessions/` (e.g. `qa-task-03b-2026-10-16.png`) and post the Slack status update.
