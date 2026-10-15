# CyberShield — Sentinel IAM

An agentic AI access & threat-response copilot for banking.

Built for the **IBM SkillsBuild AI Experiential Learning Lab** (Fall 2026) — Banking & Financial Services theme. Core build tool: **IBM Bob**. The agent runs on **watsonx Orchestrate** (single native agent).

## The idea
A bank analyst needs about an hour to investigate one suspicious login. **Sentinel** is a single AI agent that takes the alert, decides which tools to call, explains the risk in plain language, and ranks its recommended responses (no action, step-up MFA, revoke the session, reset the credential), each with a reason. **A human approves every action. Sentinel never executes one itself.**

## Architecture (short)
Sentinel runs on watsonx Orchestrate and calls 3 tools on the existing FastAPI backend (`CyberShield_IV`): the new `assess_login`, plus `get_live_threats` and `analyze_signal`. See `AGENTS.md`.

## Repo layout
- `agents/` — Sentinel agent instructions + Orchestrate definition
- `docs/bob-tasks/` — one Bob task per session (the build queue)
- `tests/` — seed data + scenarios (definition of done)
- `tools/` — watsonx Orchestrate tool specs (OpenAPI imports of the backend endpoints)
- `bob_sessions/` — exported IBM Bob task session reports (**graded submission deliverable**)

## Status
Build queue in `docs/bob-tasks/`. Team docs in `docs/team/`. Test sheet and timing protocol in `docs/testing/`. Build + test target: Oct 18 (`v1-tested`).
