# Sentinel IAM: Current Build and Status

*Team Bastion · IBM SkillsBuild AI Experiential Learning Lab · Banking & Financial Services · Prepared Oct 8, 2026; updated Oct 15 for the 5-member team*

## How to use this document

Welcome to the team. You are joining at a point where the thinking is done and the building is about to speed up. This document tells you what Sentinel IAM is, what exists today, what does not exist yet, and what we have to deliver and when. Read it start to finish once. After that, use it as a reference.

A note on honesty: where I could not confirm the status of something, this document says so. Please do not treat an "unconfirmed" item as done. Aldo, the Team Lead, will confirm those items with you at handoff.

## 1. The project in one paragraph

Sentinel IAM is a single AI agent that helps a bank's security analyst (a SOC or IAM analyst) deal with a suspicious login. Today, an analyst can spend about an hour pulling information from several tools by hand to decide whether a login is an attack. Sentinel takes the alert, decides which tools to call, combines what it finds, explains the risk in plain language, and recommends one response. A human analyst approves or rejects that response. Sentinel never executes an action on its own.

The point of the project is not to replace the analyst. It is to remove the slow, manual correlation work so the analyst can make a faster, better-informed decision.

## 2. The program and the rules we build under

This is a 10-week program. It is scored out of 20 for feedback, not ranked against other teams. A few rules are non-negotiable:

- **IBM Bob must be a core build tool.** Each member exports their Bob task session reports into a `bob_sessions/` folder in the repo. Without these reports, the project is not eligible for judging. This is the single most important rule in the program.
- **watsonx Orchestrate** is where the agent runs. It is optional in the program rules but "highly advised," and we are using it.
- **Bobcoins are limited.** Each person has about 50. The team account (150) arrives a few days after the IBM Cloud request, which is due **Oct 9**. We spend them carefully (see section 9).
- **Credential requirements for every member:** three self-paced courses (Enterprise Design Thinking Practitioner, Make Agentic Work for You, How IBM Bob...), attendance at the Thursday instructor-led sessions or the recordings, and the project plus presentation. Completing everything unlocks the IBM certificate, the digital credential, and the IBM Career Fair and mentoring.

## 3. The problem we are solving

When an account looks compromised, an analyst has to correlate three things by hand: the event itself, the current threat picture, and the right response. That correlation is slow and stressful, and slow response is where a suspicious event turns into a breach.

The public research we compiled supports this:

*(Updated Oct 19, 2026 with 2026 sources. Several older figures were outdated or unsourced; see the corrections table in `research-evidence.md`.)*

- An alert waits 55 minutes on average before an analyst picks it up, and a thorough investigation takes about 75 minutes. About 28% of alerts are never investigated (Prophet Security / ViB, 2026).
- Attackers break out in 29 minutes on average; the fastest took 27 seconds (CrowdStrike, 2026).
- Credential abuse appears in 39% of breaches (Verizon DBIR, 2026).
- A financial-services breach averages $6.3M; security AI and automation cut breach costs by almost $2M (IBM, 2026).
- No SOC team surveyed gives AI full unsupervised autonomy, and 44% use AI that recommends while a human executes (Prophet / ViB, 2026). That is why our design is recommend-then-approve.

The sources are in `docs/research/research-evidence.md`. Please cite them when you write anything for submission.

## 4. What Sentinel does

|  |  |
| --- | --- |
| **Input** | A suspicious-login alert: user, IP, device, location, timestamp |
| **Reasoning** | The agent chooses which tools to call, in what order, and when it has enough evidence to stop |
| **Output** | A risk verdict (Low, Medium, High, Critical), a plain-language explanation, and a ranked recommendation, each with a reason |
| **Guardrail** | Recommends only. The analyst approves or rejects. Sentinel never runs the action itself |
| **Runs on** | watsonx Orchestrate, as one native agent with its tools |

The possible responses are: no action, step-up MFA, revoke session, and reset credential.

## 5. Design decisions already made

These came from Aldo or from the coach. Please do not reopen them without talking to Aldo first.

1. **One agent, one problem, one solution.** The coach said our original 4-agent design was overreaching. Watchtower, Gatekeeper and Custodian became tools and steps inside Sentinel.
2. **Reuse the existing backend and add one new tool.** We do not build a new backend.
3. **Build and test early.** The coach's rule is that the agent must be built and tested before we present.
4. **Recommendations are ranked from best to lowest, and each has a reason why.**
5. **Sentinel is decisive.** It does not hedge with words like "probably" or "most likely." It owns the case and presents a complete solution, and the analyst approves it. A "devil's advocate" or hedging feature was rejected.
6. **Authentication failures are checked in a 15-minute window.** The agent triggers after 2 failed attempts. Four or more failures means flag, review, and manual analyst approval. Earlier thresholds (7, 3 to 6, and 5 or more) were rejected.
7. **More agentic, less scripted.** The agent receives a goal, guardrails and tool descriptions, and decides its own path. It does not follow a fixed if/then procedure. The detailed changes are in the work-split spreadsheet (tab: Agentic Changes) and in the Team Playbook.

## 6. Architecture

**The agent** runs in watsonx Orchestrate.

**The backend** is an existing FastAPI service (`CyberShield_IV`) on port 8000, located at `C:\CyberLab\CyberShield_IV` on Aldo's machine. It is signal-agnostic, which is why it can be re-pointed at banking and IAM signals without a rewrite. The endpoints are `GET /threats/live`, `GET /threats/history`, `GET /analyze?signal=`, `POST /analyze/file`, `POST /sentinel/chat`, and `GET /status`.

**The tools** the agent can call:

| Tool | Endpoint | Status | Purpose |
| --- | --- | --- | --- |
| `assess_login` | `POST /iam/assess-login` | **New, the one tool we add** | Scores the login for impossible travel, new device, off-hours access, and IPs on the threat list |
| `get_live_threats` | `GET /threats/live?limit=` | Reused | Checks whether the IP or technique matches current threats |
| `analyze_signal` | `GET /analyze?signal=` | Reused | Runs the event through the existing gate and specialist engine for a second opinion |

The 15-minute authentication-failure lookup is a decision Aldo made. Where it lives (a fourth tool or part of `assess_login`) is not yet settled. Aldo and the Technical Lead should decide this early in Task 02, before Technical Support / QA builds the lookup in Task 03.

### The `assess_login` contract

Request:

```json
{
  "user_id": "jdoe",
  "ip": "203.0.113.66",
  "device_id": "win-unknown-7f2",
  "geo": "Lagos, NG",
  "timestamp": "2026-10-02T03:14:00Z"
}
```

Response fields: `risk_score`, `risk_level`, `flags`, `baseline` (usual location, usual hours, known devices), and `explanation`.

### Scoring logic (deterministic, no LLM, no database)

Each flag adds points, capped at 100:

- Impossible travel: +35 (faster than 900 km/h since the last login)
- IP on the threat list: +30
- New device: +25
- Off-hours: +10

Levels: 0 to 24 is Low, 25 to 49 is Medium, 50 to 79 is High, 80 and above is Critical.

The seed data is three fictional users with documentation-range IPs, stored in `sentinel-iam/tests/fixtures/iam_baselines.json`. We never use real customer data.

**Important:** the scores are *evidence* for the agent, not the decision. The agent weighs them and explains its choice.

### Reaching the backend from Orchestrate

Orchestrate runs outside the laptop, so `localhost:8000` will not work. Use `host.docker.internal:8000` with the local ADK Developer Edition, or a `cloudflared` tunnel for Orchestrate SaaS.

## 7. Current status

This table separates what is confirmed from what is not.

| Item | Status | Notes |
| --- | --- | --- |
| Challenge framing, persona and as-is journey | Drafted | The empathy map and as-is journey are drafts and still need validation with real analysts |
| Secondary research | Re-verified Oct 19 with 2026 sources | `docs/research/research-evidence.md` |
| Build spec v2, single agent | Done (Sept 25) | `build-spec.md` |
| Coach feedback incorporated | Done | 4 agents reduced to 1 |
| Task 01: repo scaffold and `AGENTS.md` | Done | Single-agent `AGENTS.md` in the repo |
| GitHub repo | Done (Sept 30) | github.com/PC-DigitalSolutions/IBM-Sentinel-IAM |
| Aldo's course progress | In progress | Third module completed Oct 6 |
| Task 02: `assess_login` + tests | **Unconfirmed** | Last recorded as the next task (Sept 30) |
| Task 03: banking threat feed | **Unconfirmed** | Not recorded as started |
| Task 04: OpenAPI spec, import into Orchestrate | **Unconfirmed** | Not recorded as started |
| Task 05: Sentinel agent | **Unconfirmed** | Not recorded as started |
| Task 06: test pass, tag `v1-tested` | **Unconfirmed** | Not recorded as started |
| Primary research (analyst conversations) | Not started | No interviews recorded |
| Roster | 5 members | Locked on **Oct 9** |

Please treat Tasks 02 to 06 as not started until Aldo confirms otherwise.

## 8. Test scenarios

The full inputs and expected outputs are in `sentinel-iam/tests/scenarios.json`. The expected scores were checked against a reference calculation.

| # | Scenario | Expected result |
| --- | --- | --- |
| A | jdoe: Lagos 40 min after Newark, threat-listed IP, new device, 3 AM | 100, Critical: revoke session and reset credential |
| B | jdoe: home city, known laptop, 10 AM | 0, Low: no action |
| C | mgarcia: new device, home city, business hours | 25, Medium: step-up MFA |
| D | tkim: known device, home city, 1 AM | 10, Low: no action, explains why |
| F | mgarcia: threat-listed IP and new device | 55, High: revoke session |
| E | Scenario A, analyst rejects | Nothing executed; offers a safer fallback |
| G | Unknown user | 404; asks the analyst to check the user ID |

Because the agent is now goal-driven, the pass bar checks outcomes rather than an exact tool order: the right action is recommended, the evidence-gathering is justified, the explanation is clear, and nothing ever executes without approval. We are also adding ambiguous scenarios (conflicting signals, thin data) to prove the agent reasons rather than follows a script.

## 9. Bob and credit rules

- Do not start a Bob session without a written task.
- Give Bob **one small task per session**, scoped to the files it should read, so it does not burn credits scanning the backend.
- Stop when the "done-when" condition is met.
- Screenshot the consumption summary after every session and export it to `bob_sessions/`.
- Keep about 10 credits in reserve for fixes found in testing.
- Bob writes the code. This is what keeps the `bob_sessions/` reports legitimate. Please do not hand-write large sections of code and then ask Bob to "review" them.

Task prompts live in `sentinel-iam/docs/bob-tasks/`.

## 10. Timeline

| Date | Milestone |
| --- | --- |
| **Oct 9** | Roster locks; IBM Cloud request deadline |
| Oct 14 | Target: three tools live in Orchestrate |
| Oct 18 | Target: tested agent, tagged `v1-tested` |
| **Oct 25** | Mid-Program Checkpoint: demo a tested agent |
| Nov 4 (TBC) | IBM Career Fair |
| **Nov 8** | Build ends; agent frozen |
| Nov 9 to 22 | Showcase and final video |
| **Nov 22** | **Project submission** |

## 11. What we submit on Nov 22

| Deliverable | Why it matters |
| --- | --- |
| 3-minute video demo | Design and usability; Effectiveness |
| Written problem, solution and prototype link | Completeness and feasibility |
| Technology statement (Bob, Orchestrate agent, reused backend, new tool) | Completeness; Creativity |
| Test results | Effectiveness |
| `bob_sessions/` reports | **Eligibility gate** |

## 12. Known risks and open items

1. **Primary research is missing.** We have public data but no conversations with real analysts. Three to five short conversations would strengthen the persona and the problem.
2. **The "60 minutes down to under one minute" claim is not yet measured.** The 55 and 75 minute figures are industry survey averages. We need our own timing of a manual walkthrough versus Sentinel on the same alert.
3. **All data is synthetic.** That is acceptable for a proof of concept, but we must say so openly.
4. **A small inconsistency in the spec.** The `assess_login` example response shows a score of 87 with all four flags. By the scoring rules, all four flags add up to 100 (Scenario A). The tests use 100. Please correct the example in the spec.
5. **Scope.** Seven scenarios passing cleanly with a polished demo beats additional features.
6. **The bank-specific cost of a wrong customer lockout** has no solid public number yet. Do not invent one.

## 13. Where things live

- Repo: `sentinel-iam` (GitHub: PC-DigitalSolutions/IBM-Sentinel-IAM)
- `AGENTS.md` in the repo root: persistent context for Bob
- `docs/bob-tasks/`: the Bob task prompts
- `tests/scenarios.json` and `tests/fixtures/iam_baselines.json`: test inputs and seed data
- `bob_sessions/`: required session reports
- Project docs: `sentinel-iam-knowledge.md`, `research-evidence.md`, `build-spec.md`

## 14. Glossary for newer members

- **SOC (Security Operations Center):** the team that watches for and responds to security incidents.
- **IAM (Identity and Access Management):** the systems and processes that control who can log in to what.
- **Tier-2 analyst:** the person who investigates alerts that the first-line team escalates.
- **MFA and step-up MFA:** multi-factor authentication; "step-up" means asking for an extra verification only when a login looks risky.
- **Revoke session:** ending an active login session immediately.
- **Reset credential:** forcing a new password or key.
- **Impossible travel:** two logins from places too far apart to travel between in the time elapsed.
- **MTTR (mean time to respond):** the average time from alert to response.
- **Tool calling:** an AI agent deciding to use an external function or API to get information or take a step.
- **Human-in-the-loop:** a person must approve high-stakes decisions.
- **watsonx Orchestrate:** IBM's platform where the agent runs.
- **IBM Bob:** IBM's AI development environment that we use to build the code.
- **Bobcoins:** the credits Bob consumes.

## 15. What we need from you at handoff

In your first 24 hours, please do three things: read this document, the Team Playbook and your role guide, confirm with Aldo which Bob tasks are truly done, and tell the team early if anything here is unclear or looks wrong. Asking early is not a weakness here. It is the cheapest way to protect everyone's time and Bobcoins.

## 16. Who does what

| Role | Owns |
| --- | --- |
| Team Lead (Aldo) | Guidance, coach and program contact, design decisions, review and approval |
| Technical Lead | Task 02 (`assess_login`), Task 05 (Sentinel agent), audit log, agent freeze on Nov 8 |
| Technical Support / QA | Task 03 (threat feed and failure lookup), Task 04 (Orchestrate import and connectivity), Task 06 (test pass, `v1-tested`), baseline timing, `bob_sessions/` check |
| Research & Documentation Lead | Analyst interviews, research evidence, white paper and procedure manual, written problem and solution, technology statement (with the Technical Lead) |
| Communications & Demo Lead | 3-minute video, demo script, checkpoint and showcase presentations, Slack updates |

Each role has its own role guide with responsibilities and dates. The Team Playbook shows how each role does its tasks.
