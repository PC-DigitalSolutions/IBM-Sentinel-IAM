# CyberShield — Sentinel IAM

An agentic AI access & threat-response copilot for banking.

Built for the **IBM SkillsBuild AI Experiential Learning Lab** (Fall 2026) — Banking & Financial Services theme. Core build tool: **IBM Bob**. Multi-agent layer: **watsonx Orchestrate**.

## The idea
A bank's security team drowns in access events and threat noise. Sentinel IAM puts a team of specialized agents on it: they watch the threat landscape, triage suspicious access events against it, and **recommend** an IAM response to a human analyst who approves the action. Agents propose; a person decides.

## Agents
| Agent | Role |
|---|---|
| **Sentinel** | Orchestrator + analyst copilot |
| **Watchtower** | Threat intelligence |
| **Gatekeeper** | IAM/access triage |
| **Custodian** | Secrets & response (recommend-then-approve) |

## Architecture (short)
The agents run on watsonx Orchestrate and call an existing FastAPI threat-analysis service (`CyberShield_IV`) as tools. See `AGENTS.md` for the endpoint map and build conventions.

## Repo layout
- `agents/` — agent definitions built in Bob
- `tools/` — watsonx Orchestrate tool specs (OpenAPI imports of the backend endpoints)
- `bob_sessions/` — exported IBM Bob task session reports (**graded submission deliverable**)

## Status
Scaffolding stage. Build plan lives in the team's BUILD_SPEC.
