# Bob task queue

Hand Bob **one file per session**. Each has a "Done when" condition, so stop there. After each session, screenshot the task consumption summary into `bob_sessions/` (`aldo-task-02-2026-09-29.png`).

| # | Task | Est. credits | Status |
|---|---|---|---|
| 01 | Repo scaffold + AGENTS.md | done (prepared outside Bob) | ✅ |
| 02 | `POST /iam/assess-login` + tests | medium | 🟨 Built in `CyberShield_IV` (uncommitted; 6/6 tests pass, checked Oct 15). No Bob session report in `bob_sessions/` yet. Aldo to confirm it was a Bob session |
| 03 | Re-point the live threat feed to banking | low | ⬜ |
| 03b | 5-minute failure flag inside `assess_login` | low | ⬜ Ready. Decisions (Oct 15): the count lives inside `assess_login`; 2 failures in 5 minutes flags the case |
| 04 | OpenAPI tool spec + import the 3 tools into Orchestrate | low–medium | ⬜ |
| 05 | Sentinel agent in Orchestrate | medium | ⬜ |
| 05b | Attach the response playbook as a knowledge base | low | ⬜ After Task 05 and once the playbook is marked ready |
| 06 | Run the scenarios through the agent + log results | low–medium | ⬜ |

Build-ahead target: 02–06 done by **Oct 18** (scenarios A to L in `tests/scenarios.json` and `docs/testing/test-sheet.md`), before the official build phase and the **Oct 25 checkpoint**.
