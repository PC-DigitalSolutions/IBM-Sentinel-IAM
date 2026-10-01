# Task 05: build the Sentinel agent in Orchestrate

**Read only:** `AGENTS.md`, `agents/sentinel.instructions.md`.

## Build
1. Create `agents/sentinel.agent.yaml` as a native ADK agent named `sentinel`, with the instructions copied from `agents/sentinel.instructions.md` and the tools `assess_login`, `get_live_threats`, `analyze_signal`. Pick an available watsonx model that supports tool calling (check `orchestrate models list`). Verify the YAML fields against the installed ADK version.
2. Import it: `orchestrate agents import -f agents/sentinel.agent.yaml`.
3. In the Orchestrate chat, paste scenario A's alert as a message.

## Done when
For scenario A, Sentinel calls `assess_login` then `get_live_threats`, answers Critical 100/100, recommends revoke + reset, and asks for approval.
