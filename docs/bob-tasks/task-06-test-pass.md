# Task 06: test pass (re-run before every demo)

**Read only:** `tests/scenarios.json`, `agents/sentinel.instructions.md`.

## Build
1. Create `tests/results.md` with a table: scenario | tools called | verdict | action | pass/fail | notes.
2. Run scenarios A, B, C, D, F, E and G through the Sentinel chat (E: send the scenario A alert, then the analyst's reject reply). Fill in the table.
3. For any fail: make the **smallest** change to `agents/sentinel.instructions.md`, re-import the agent, and re-run only that scenario.

## Pass bar
Right tools, right action, clear explanation, and nothing ever claims to be executed without approval. All 7 pass → freeze the agent (tag `v1-tested`).
