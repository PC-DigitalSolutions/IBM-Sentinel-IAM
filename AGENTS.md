# CyberShield — Sentinel IAM

Agentic AI access & threat-response copilot for banking. Built for the IBM SkillsBuild AI Experiential Learning Lab (Banking & Financial Services). IBM Bob is the core build tool; the multi-agent layer runs on watsonx Orchestrate.

## What this project is
A team of specialized agents watch threats, triage suspicious access events against the live threat picture, and **recommend** IAM responses to a human analyst who approves the action. Human-in-the-loop by design: agents propose, a person decides.

## Agents
- **Sentinel** — primary orchestrator + analyst-facing copilot. Delegates to the collaborators, explains every decision in plain language.
- **Watchtower** — threat-intelligence agent. Reports what's currently threatening the bank's stack.
- **Gatekeeper** — IAM/access triage. Risk-scores an auth/access event against Watchtower's current picture.
- **Custodian** — secrets & response. Proposes a concrete action (rotate credential / step-up auth / revoke token). **Never acts without human approval.**

## Backend (reused, do not rebuild)
The analysis + threat feed comes from an existing FastAPI service (`CyberShield_IV`, runs on port 8000). Agents call it as tools; it is signal-agnostic. Endpoints:
- `GET /threats/live?limit=` — live classified threat feed (Watchtower)
- `GET /threats/history?limit=&kind=` — durable archive (Watchtower)
- `GET /analyze?signal=` — verdict + specialist reports for a signal (Gatekeeper)
- `POST /analyze/file` — multimodal evidence analysis (Gatekeeper)
- `POST /sentinel/chat` — analyst conversation (Sentinel)
- `GET /status` — health

## Domain language
This is a **banking** context. Signals are auth events, credential exposures, fraud indicators, session anomalies — not physical-event or concert threats. Keep vocabulary financial-sector and IAM-focused.

## Conventions for Bob
- Small, single-purpose changes per task so each session closes cleanly.
- Prefer wiring real endpoints over mocking data.
- Any response action is **recommend-then-approve**; never auto-execute a credential change.
- Document new agents/tools here in AGENTS.md as they're added.
- Session reports are a graded deliverable — do not squash task history; export each task's session summary to `bob_sessions/`.
