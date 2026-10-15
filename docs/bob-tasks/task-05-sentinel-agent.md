# Task 05: build the Sentinel agent in Orchestrate

**Read only:** `AGENTS.md`, `agents/sentinel.instructions.md`.

## Build
1. Create `agents/sentinel.agent.yaml` as a native ADK agent named `sentinel`, with the instructions copied from `agents/sentinel.instructions.md` and the tools `assess_login`, `get_live_threats`, `analyze_signal`. Pick an available watsonx model that supports tool calling (check `orchestrate models list`). Verify the YAML fields against the installed ADK version.
2. Import it: `orchestrate agents import -f agents/sentinel.agent.yaml`.
3. In the Orchestrate chat, paste scenario A's alert as a message.

## Done when
For scenario A, Sentinel:
- reaches Critical (100/100) and ranks revoke session + reset credential first, with a reason for each option;
- shows the investigate loop (what it learned and what is still unknown after each tool call) and why it called each tool;
- asks the analyst to approve, and never says or implies that an action has been executed.

The tool order is Sentinel's choice. We judge the outcome and the reasoning, not a fixed sequence.

## Failure looks like
The same tools in the same order for every case, hedging words ("probably", "most likely"), or the conversation ending when the analyst rejects.
