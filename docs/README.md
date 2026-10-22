# Documentation index

Every doc in the repo, what it's for, and whether you can trust it today.

**Current** = matches today's design. **Historical** = kept for the record; parts are out of date. Don't build from historical docs.

---

## Start here

| Doc | What it's for | State |
|---|---|---|
| [guides/](guides/) | Seven Word guides: Team Guide, Setup and Coding Standards, Backend, Tools, Agent, Frontend, Testing | Current, **start with 00-team-guide.docx** |
| [../README.md](../README.md) | Front door: what, why, status, repo map | Current |
| [ONBOARDING.md](ONBOARDING.md) | Step-by-step for new members | Current |
| [STATUS.md](STATUS.md) | Live tracker: tasks, owners, dates, known issues | Current, **update it** |
| [ARCHITECTURE.md](ARCHITECTURE.md) | How the agent, tools, backend and prototype fit together | Current |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | How we work: Bob, evidence, git, Slack | Current |

## Design and build (source of truth)

| Doc | What it's for | State |
|---|---|---|
| [build-spec.md](build-spec.md) | Technical spec: agent, tools, scoring, failure rule, test plan | Current, **wins on conflicts** |
| [../agents/sentinel.instructions.md](../agents/sentinel.instructions.md) | The agent's instructions for Orchestrate | Current, **wins on conflicts** |
| [../AGENTS.md](../AGENTS.md) | Short context file that IBM Bob reads automatically | Current |
| [architecture-incident-flow.svg](architecture-incident-flow.svg) | Flow diagram | Current |
| [bob-tasks/](bob-tasks/README.md) | One prompt per Bob session, Tasks 02 to 06 | Current. Live status is in STATUS.md |
| [orchestrate-runbook.md](orchestrate-runbook.md) | Exact commands: backend, tunnel, ADK, import tools and agent | Current |
| [knowledge/sentinel-response-playbook.md](knowledge/sentinel-response-playbook.md) | The bank response policy the agent cites (knowledge base) | Current, v0.1 draft |

## Testing

| Doc | What it's for | State |
|---|---|---|
| [../tests/scenarios.json](../tests/scenarios.json) | Inputs and expected results for each scenario | Current (I, K, L added in Task 03b) |
| [testing/test-sheet.md](testing/test-sheet.md) | Pass bar and all 12 scenarios explained | Current |
| [testing/test-sheet.csv](testing/test-sheet.csv) | Blank log, one row per run | Current |
| [testing/timing-protocol.md](testing/timing-protocol.md) | How to measure manual vs Sentinel time | Current |

## Research

| Doc | What it's for | State |
|---|---|---|
| [research/research-evidence.md](research/research-evidence.md) | **The only allowed source of statistics**, verified Oct 19 | Current |
| [research/analyst-interview-guide.md](research/analyst-interview-guide.md) | Script for analyst interviews | Current |

## Team and history

| Doc | What it's for | State |
|---|---|---|
| [team/team-playbook.md](team/team-playbook.md) | Detailed how-to for each role | Mostly current. Says 15-minute window; the rule is now **5 minutes** |
| [team/current-build-and-status.md](team/current-build-and-status.md) | Oct 8 briefing, glossary | Historical. Status section replaced by STATUS.md |
| [team/team-handoff.md](team/team-handoff.md) | Oct 9 handoff summary | Historical |
| [team/slack-handoff-2026-10-18.txt](team/slack-handoff-2026-10-18.txt) | The Slack handoff and role sign-up | Historical, but has the latest timeline |
| [team/slack-backend-design-2026-10-19.txt](team/slack-backend-design-2026-10-19.txt) | Slack post: system design | Historical |
| [team/slack-backend-code-2026-10-19.txt](team/slack-backend-code-2026-10-19.txt) | Slack post: backend code summary | Historical |
| [sentinel-iam-knowledge.md](sentinel-iam-knowledge.md) | Early master doc (4 agents, 3 members) | **Historical. Outdated design** |
| [project-instructions.md](project-instructions.md) | Old Claude.ai project prompt (4 agents) | **Historical. Outdated design** |

## Graded evidence

| Folder | What it's for |
|---|---|
| [../bob_sessions/](../bob_sessions/README.md) | Bob session screenshots from every member. **Required for judging** |
| [brand/](brand/) | Team Bastion banner and icon |
