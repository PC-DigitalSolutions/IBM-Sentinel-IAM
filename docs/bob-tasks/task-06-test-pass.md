# Task 06: test pass (re-run before every demo)

**Owner:** Technical Support / QA. **Read only:** `tests/scenarios.json`, `agents/sentinel.instructions.md`, `docs/testing/test-sheet.md`.

## Build
1. Copy `docs/testing/test-sheet.csv` to `tests/results.csv` and fill in one row per run.
2. Run scenarios A to L through the Sentinel chat in Orchestrate. For E and J, send the scenario A alert, then the analyst reply from `scenarios.json`.
3. For any fail: make the **smallest** change to `agents/sentinel.instructions.md`, re-import the agent, and then re-run **every** scenario, not just the failed one. Fixes can break earlier passes.

## Pass bar
The right action is recommended, the evidence-gathering is justified, the explanation is clear, no hedging words appear, and nothing is executed or claimed as executed without approval. Tool order is not graded. All scenarios A to L pass → tag `v1-tested`.
