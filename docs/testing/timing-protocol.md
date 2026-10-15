# Baseline Timing Protocol: Manual Triage vs Sentinel

*Owner: Technical Support / QA · Results go to the Research & Documentation Lead and the Communications & Demo Lead · First numbers due for the Oct 25 checkpoint*

## Why
Our claim is that triage drops from about an hour of manual work to under a minute plus one approval. The hour comes from industry surveys (`research-evidence.md`), not from us. This protocol produces **our own** numbers on the same alert, so we can report a measured result instead of only citing an average.

## What we measure
- **Manual time:** from the moment the tester reads the alert to the moment they write down a recommended action with a reason.
- **Sentinel time:** from sending the alert to Sentinel to the moment its ranked recommendation appears.
- **Approval time** (optional, recorded separately): how long the analyst takes to read Sentinel's answer and approve or reject.

The alert is **scenario A** (`tests/scenarios.json`):
> jdoe · IP 203.0.113.66 · device win-unknown-7f2 · Lagos, NG · 2026-10-02T03:14:00Z

## Manual runbook (give this to the tester, nothing else)
The tester may use only: `tests/fixtures/iam_baselines.json`, a web map or distance calculator, a calculator, and the backend's `GET /threats/live` (or a news search for current banking threats). No Sentinel, no `assess_login`.

| Phase | Step |
|---|---|
| 1. Baseline | Find jdoe in the seed file. Note the usual location, usual hours (UTC), known devices, and last login. |
| 2. Travel | Find the distance from the last-login city to the alert city. Divide by the hours between the two timestamps. Is the speed over 900 km/h? |
| 3. Device | Is the alert's device in the known-devices list? |
| 4. Hours | Is the alert's UTC hour outside the usual hours? |
| 5. Threat list | Is the IP in the seed file's threat list? |
| 6. Threat context | Check current threats for related credential-theft or account-takeover activity. |
| 7. Decide | Using the action map (Low: no action · Medium: step-up MFA · High: revoke session · Critical: revoke + reset), write the recommended action and a one-line reason. |

## How to run it
1. **Tester:** ideally someone who did not design the seed data or the scoring. Note who it was.
2. **Manual runs:** at least **3**, using a different tester for each run where possible. If the same person repeats it, note that, because they get faster from familiarity.
3. Time each phase with a stopwatch (lap per phase). Stop when the action and reason are written.
4. **Sentinel runs:** at least **3** on the same alert in Orchestrate. Use a stopwatch or the chat timestamps. Note the model and whether the backend was already warm.
5. Record everything below. Don't drop slow runs.

## Results template
**Manual**

| Run | Date | Tester | Repeat tester? | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Total | Action reached | Correct? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | | |
| **Average** | | | | | | | | | | | | | |

**Sentinel**

| Run | Date | Model | Backend warm? | Alert → recommendation | Approval time (optional) | Action recommended | Correct? |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| **Average** | | | | | | | |

## How to report it
- Always say **"in our test"**, and give the number of runs and the conditions: synthetic seed data, one alert, a simple runbook.
- Report both averages and the range (fastest and slowest run).
- Don't present our numbers as industry figures, and don't combine them with the survey figures into a single claim.
- Note the limits: a real analyst works with real tools, real data volumes and interruptions, so our manual time understates real-world effort in some ways and overstates it in others.

Example wording, with blanks to fill in (no numbers exist yet):
> "In our test, manual triage of one synthetic suspicious-login alert took an average of __ minutes across __ runs (range __ to __). Sentinel reached a ranked recommendation in an average of __ seconds across __ runs, followed by one analyst approval."
