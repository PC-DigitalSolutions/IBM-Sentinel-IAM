# Sentinel IAM: Team Handoff

Team Bastion · IBM SkillsBuild AI Experiential Learning Lab · Banking & Financial Services Prepared by Aldo (Team Lead) · Oct 9, 2026

## 1. What we're building

Challenge from IBM: *How might we use Agentic AI to create more secure, inclusive, and efficient financial experiences for customers and institutions?*

Our framing: *How might we help a bank's security team respond to suspicious access events faster and more confidently, without taking the human out of high-stakes decisions?*

**Sentinel IAM** is one AI agent, for one problem, with one solution. A SOC/IAM analyst at a bank gets a suspicious-login alert. Sentinel decides which tools to call, correlates the results, explains the risk in plain language, and recommends one response. The analyst approves before anything happens.

This is a proof of concept, not a production platform. It shows the agentic loop adds value.

## 2. Why it matters (evidence)

- An alert waits 55 minutes before an analyst picks it up, and a thorough investigation takes about 75 minutes (Prophet Security / ViB, 2026).
- Attackers break out in 29 minutes on average (CrowdStrike, 2026).
- Credential abuse appears in 39% of breaches (Verizon DBIR, 2026).
- A financial-services breach averages $6.3M (IBM, 2026).
- 0% of SOC teams give AI full unsupervised autonomy; 44% use AI that recommends while a human executes (Prophet / ViB, 2026). That is why Sentinel only recommends.

Full sources are in the research evidence doc.

## 3. How Sentinel works

|  |  |
| --- | --- |
| Input | Suspicious-login alert (user, IP, device, location, timestamp) |
| Tools | `assess_login` (NEW), `get_live_threats` (reuse), `analyze_signal` (reuse) |
| Output | Risk verdict (Low / Medium / High / Critical), a plain-language reason, one recommended action |
| Guardrail | Recommends only. The analyst approves or rejects. Sentinel never runs the action itself |
| Runs on | watsonx Orchestrate, single native agent |
| Built with | IBM Bob (required) |
| Backend | Existing FastAPI service (CyberShield\_IV, port 8000) |

**Decision order:** always call `assess_login` first. If flags include `ip_on_threat_list` or `impossible_travel`, call `get_live_threats`. If the score is borderline (40-70), call `analyze_signal`. Map the result to one action: Low = no action; Medium = step-up MFA; High = revoke session; Critical = revoke session + reset credential. Explain which tools were called and why, then ask the analyst to approve.

**`assess_login` scoring:** impossible travel +35, IP on threat list +30, new device +25, off-hours +10, capped at 100. Levels: 0-24 Low, 25-49 Medium, 50-79 High, 80+ Critical. Deterministic, no LLM, no database.

## 4. Design decisions already made

These are settled. Please don't reopen them without talking to Aldo.

1. **One agent, not four.** The coach said four agents was overreaching. Watchtower, Gatekeeper and Custodian from v1 are now tools and steps inside Sentinel.
2. **Recommendations are ranked best to lowest, each with a reason why.**
3. **Sentinel owns the case.** It gives concrete, decisive recommendations and presents a complete solution; the analyst approves it. No hedging language such as "probably" or "most likely." A "devil's advocate" feature was considered and rejected.
4. **Authentication-failure logic:** Sentinel checks authentication-failure logs within a 15-minute window. The tool-calling agent triggers after 2 failed attempts. 4 or more failures means flag, review, and manual analyst approval.
5. **Human approval is non-negotiable.** Nothing executes without it.

**Open item to reconcile:** the failure-window logic in decision 4 is newer than the build spec's scoring table. The spec doesn't yet include it. The Technical Lead and Aldo should decide where it lives (inside `assess_login` or as a separate check) before Bob Task 02 is finalized.

## 5. Current status

Confirmed from our records:

- Repo exists: github.com/PC-DigitalSolutions/IBM-Sentinel-IAM (pushed Sept 30)
- Repo scaffold and `AGENTS.md` done (Bob Task 01)
- Single-agent plan, test plan and scenarios written
- Team is 5 members

**Aldo to confirm before handoff:** whether Bob Tasks 02 and 03 have been started or completed, and how many Bob credits Aldo has used.

## 6. Roster and roles

| Role | Owns |
| --- | --- |
| Team Lead (Aldo) | Guidance, coach and program contact, final calls on design, approvals |
| Technical Lead | Bob Tasks 02, 05; the `assess_login` endpoint and the Sentinel agent |
| Technical Support / QA | Bob Tasks 03, 04, 06; threat feed, tool import and connectivity, test pass |
| Research & Documentation Lead | White paper, procedure manual, written statements, analyst interviews |
| Communications & Demo Lead | 3-minute video, demo script, Slack updates, showcase |

Each role has its own doc with responsibilities, deliverables and dates. Everyone does the shared requirements in section 7.

## 7. Requirements for every member

- Complete the 3 self-paced courses: Enterprise Design Thinking Practitioner (3h), Make Agentic Work for You (4h), How IBM Bob... (30 min)
- Attend the Thursday instructor-led sessions, or watch the recordings
- Export Bob task session reports into `bob_sessions/` after every Bob session. **Without these, the project is not eligible for judging.**
- Contribute to the project and presentation

Completing everything earns an IBM certificate, a digital credential, and a bonus IBM Career Fair and mentoring.

## 8. Key dates

| Date | Milestone |
| --- | --- |
| Oct 9 | Team roster locks; IBM Cloud request deadline |
| Oct 12-18 | Test pass (Bob Task 06). All scenarios pass, tag `v1-tested` |
| Oct 25 | Mid-Program Checkpoint: demo a tested agent |
| Nov 4 | Career Fair (to be confirmed) |
| Nov 8 | Agent frozen. End of build phase |
| Nov 9-22 | Showcase and final video |
| Nov 22 | Project submission |

## 9. Bob rules

- Bob is a core build tool and must be used for the build.
- Credits: about 50 per person to start. The team account of 150 arrives a few days after the IBM Cloud request.
- One small task per Bob session. Task prompts live in `sentinel-iam/docs/bob-tasks/`.
- Don't start a Bob session without a written task. Stop once the task's done-when condition is met.
- Screenshot the consumption summary after every session.
- Keep about 10 credits in reserve for fixes found in testing.

## 10. Final deliverables

- 3-minute video demo: one alert, Sentinel calls tools, recommends, analyst approves
- Written problem, solution and prototype link
- Technology statement: Bob + watsonx Orchestrate agent + reused backend + new tool
- Test results sheet
- `bob_sessions/` reports

## 11. Aldo's role from here

Aldo hands over the build and provides guidance only. Questions on design go to Aldo. Questions on the program go to the coach through Slack.
