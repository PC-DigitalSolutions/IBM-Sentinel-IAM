# Sentinel IAM: Build Spec (v2, single agent)
### IBM SkillsBuild AI Experiential Learning Lab · Banking & Financial Services · Team Bastion

> **Changed Sept 25, 2026, after coach feedback:** the 4-agent design was too much. We're now building **one agent, for one problem, with one solution**, built around agentic tool calling. It reuses the existing backend and adds one new tool. The agent gets built **early** so we can test it before presenting. We don't waste Bob credits.
>
> **Updated Oct 15, 2026, to match the settled team decisions** (`docs/team/team-handoff.md` §4): ranked recommendations with reasons, a goal-driven agent instead of a fixed tool order, the authentication-failure flag (2 failures in 5 minutes, set by Aldo on Oct 15), the corrected `assess_login` example (100, Critical), and the 5-member roster.
>
> `AGENTS.md` in the repo root gives Bob persistent context. Section 5 is the list of tasks to hand Bob one at a time. **Bob builds the code** so the `bob_sessions/` reports stay legit.

---

## 1. One problem, one solution

**Problem.** A bank analyst gets a suspicious-login alert and spends about an hour investigating it by hand: 56 minutes before the first action and 70 minutes to fully investigate. Stolen credentials are the #1 way attackers get in (88% of basic web-app attacks). In the financial sector, a breach costs $6.08M on average. *(See `research-evidence.md`.)*

**Solution.** **Sentinel**, a single AI agent for SOC/IAM analysts at a bank. Given a suspicious-login alert, Sentinel **decides which tools to call**, correlates the results, explains the risk in plain language, and presents **ranked recommendations, best first, each with a reason**. The responses are *no action*, *step-up MFA*, *revoke session*, and *reset credential*. **A human approves the action before anything happens.**

**Target user.** A SOC/IAM analyst at a mid-to-large bank.

**Measurable impact.** Time to triage one suspicious login drops from about 60 minutes of manual correlation to under a minute of agent reasoning plus one approval.

---

## 2. The agent: Sentinel

| | |
|---|---|
| **Input** | A suspicious-login alert (user, IP, device, location, timestamp) |
| **Reasoning** | Calls its tools in whatever order it chooses and skips the ones it doesn't need |
| **Output** | Risk verdict (Low / Medium / High / Critical), a plain-language "why", and recommendations ranked best to lowest, each with a reason |
| **Guardrail** | Recommends only. The analyst approves or rejects, and Sentinel never runs the action itself |
| **Runs on** | watsonx Orchestrate, as a single native agent with 3 tools |
| **Knowledge** | One knowledge base: the bank IAM response playbook (`docs/knowledge/sentinel-response-playbook.md`), retrieved to ground and cite recommendations. Knowledge, not a tool (Aldo, Oct 15) |

The work that Watchtower, Gatekeeper and Custodian did in v1 is now **tools and steps inside Sentinel**. They are no longer separate agents.

---

## 3. Tools (agentic tool calling)

The backend is the existing FastAPI/Neon service in `C:\CyberLab\CyberShield_IV` on port 8000. Import the endpoints into Orchestrate as OpenAPI tools.

| Tool | Endpoint | Status | What Sentinel uses it for |
|---|---|---|---|
| `assess_login` | `POST /iam/assess-login` | **NEW, the one tool we add** | Scores the login itself for impossible travel, a new device, off-hours access, and IPs on the threat list |
| `get_live_threats` | `GET /threats/live?limit=` | Reuse | Checks whether the IP or technique matches current threats |
| `analyze_signal` | `GET /analyze?signal=` | Reuse | Runs the event through the existing gate + specialist engine to get a verdict |

### New tool: `assess_login` contract

**Request**
```json
{
  "user_id": "jdoe",
  "ip": "203.0.113.66",
  "device_id": "win-unknown-7f2",
  "geo": "Lagos, NG",
  "timestamp": "2026-10-02T03:14:00Z"
}
```

**Response**
```json
{
  "risk_score": 100,
  "risk_level": "Critical",
  "flags": ["impossible_travel", "new_device", "off_hours", "ip_on_threat_list"],
  "baseline": { "usual_geo": "Newark, US", "usual_hours": "08:00-19:00 ET", "known_devices": 2 },
  "explanation": "Login from Lagos 40 min after a Newark session; unrecognized device; 3:14 AM; IP seen in live threat feed."
}
```

**Logic (keep it simple and deterministic):** each flag adds points: impossible travel +35 (over 900 km/h since the last login), IP on the threat list +30, new device +25, off-hours +10, capped at 100. Levels: 0–24 Low, 25–49 Medium, 50–79 High, 80+ Critical. The seed data (3 fictional users, documentation-range IPs) lives in `sentinel-iam/tests/fixtures/iam_baselines.json`. No LLM, no DB, so the tool is fully testable (Section 6).

### Authentication-failure policy (set by Aldo, Oct 15, 2026)
Sentinel checks authentication failures for the account within a **5-minute window**.
- **2 or more failed attempts** in the window **flags the case**. Sentinel then investigates on its own (calls the tools the case needs) and has a ranked recommendation ready for the analyst's decision.
- A flagged case with a Low risk score ranks **step-up MFA** first (Aldo, Oct 15). At Medium or above, the default action for the level applies.
- Every action still needs the analyst's approval.
- This replaces the earlier 15-minute window with its 2-failure investigate tier and 4+ manual-approval tier. The older thresholds (7, 3 to 6, and 5 or more) also stay retired.

**Where the count lives (decided by Aldo, Oct 15):** inside `assess_login`, returned as `auth_failures_in_window`, `auth_failure_window_minutes` and `failure_flag` (Bob Task 03b). It keeps the settled "one new tool" rule and leaves the 35/30/25/10 scoring unchanged. The count is reported alongside the score and does not add points to it.

### How the agent decides (goes in the Orchestrate instructions)
Sentinel gets a goal, guardrails and tool descriptions, and chooses its own path. It does not follow a fixed if/then procedure. The full instructions are in `agents/sentinel.instructions.md`.
- `assess_login` is the starting evidence for every alert, because no other tool knows the user's baseline.
- After each tool result, Sentinel states what it learned and what is still unknown, then calls another tool or stops.
- `get_live_threats` adds context when the IP or the pattern could belong to a current campaign. `analyze_signal` gives a second opinion when the signals conflict or the case is close to a level boundary.
- Default action per level: Low → no action; Medium → step-up MFA; High → revoke session; Critical → revoke session + reset credential. Sentinel ranks the options best to lowest with a reason for each, then asks the analyst to approve.

---

## 4. Build ahead, then test

Coach's rule: **the agent has to be built and tested before we present.** So:

| When | Goal |
|---|---|
| **Wk 3 (Sep 28–Oct 4)** | Bob tasks 02–03: `assess_login` endpoint + tests, banking threat feed |
| **Wk 4 (Oct 5–11)** | Tasks 04–05: tools into Orchestrate, Sentinel agent working end to end. **Oct 9: roster locks + IBM Cloud request** |
| **Wk 5 (Oct 12–18)** | **Task 06: test pass.** All scenarios pass, tag `v1-tested` |
| **Wk 6 (Oct 19–25)** | **Checkpoint Oct 25:** demo a tested agent, not a work in progress |
| **Wks 7–8 (Oct 26–Nov 8)** | Polish: demo script, video draft, written statements. **Agent frozen Nov 8** |
| **Wks 9–10 (Nov 9–22)** | Showcase, final video. **Submit Nov 22** |

---

## 5. Bob build plan (50 credits per person)

Each of the 5 members has about **50 credits**. The 150-coin team account arrives a few days after the **Oct 9** IBM Cloud request. Hand Bob **one small task per session**.

Task prompts live in `sentinel-iam/docs/bob-tasks/`. Each is scoped to the files Bob should read, so it doesn't burn credits scanning the backend.

| # | Task | Est. cost | Done-when |
|---|---|---|---|
| 01 | Repo scaffold + `AGENTS.md` | Done | Single-agent AGENTS.md in repo |
| 02 | `POST /iam/assess-login` + pytest | Medium | All fixture scenarios pass |
| 03 | Re-point live threat feed to banking terms | Low | `/threats/live` shows banking headlines |
| 03b | 5-minute failure flag inside `assess_login` | Low | Failure tests for 1, 2, 3 and 4 failures and the window edges pass; A–H still pass |
| 04 | OpenAPI spec for the 3 tools → import into Orchestrate | Low–Med | `orchestrate tools list` shows 3 tools |
| 05 | Sentinel agent (instructions already drafted) | Medium | Scenario A handled end to end, investigate loop visible, nothing executed |
| 05b | Attach the response playbook as Sentinel's knowledge base | Low | Agent shows 3 tools + 1 knowledge base; scenario H cites the playbook section |
| 06 | Test pass + instruction fixes | Low–Med | Scenarios A–L pass, tag `v1-tested` |
| — | Export `bob_sessions/` screenshots after every task | Free | **Eligibility gate** |

**Reaching the backend:** Orchestrate runs outside your laptop, so `localhost:8000` won't work. Use `host.docker.internal:8000` with the local ADK Developer Edition, or a `cloudflared` tunnel for Orchestrate SaaS (Task 04).

**Credit rules:** don't start a Bob session without a written task, stop once the "done-when" condition is met, and screenshot the consumption summary after every session. Leave about 10 credits in reserve for fixes found in testing.

---

## 6. Test plan (run in Week 5, re-run before every demo)

Full inputs and expected outputs are in `sentinel-iam/tests/scenarios.json`. The expected scores were checked against a reference calculation.

| # | Scenario | Typical tools (not a required order) | Expected result |
|---|---|---|---|
| A | jdoe: Lagos 40 min after Newark, threat-listed IP, new device, 3:14 AM UTC | assess_login → get_live_threats | 100 Critical → revoke + reset |
| B | jdoe: home city, known laptop, 10 AM | assess_login | 0 Low → no action |
| C | mgarcia: new device, home city, business hours | assess_login | 25 Medium → step-up MFA |
| D | tkim: known device, home city, 1 AM | assess_login | 10 Low → no action, explains |
| F | mgarcia: threat-listed IP + new device | assess_login → get_live_threats (analyze_signal if the evidence is still insufficient) | 55 High → revoke session |
| E | Scenario A, analyst rejects | — | Nothing executed, offers a safer fallback |
| G | Unknown user | assess_login | 404 → asks analyst to check the user ID |

The ambiguous scenarios H to L (conflicting signals, thin history, re-plan after rejection, and the 5-minute failure flag inside and outside the window) are in `docs/testing/test-sheet.md`.

**Pass bar:** the right action is recommended, the evidence-gathering is justified, the explanation is clear, and nothing ever executes without approval. Because the agent chooses its own tools, we judge the outcome and the reasoning, not an exact tool order. Log every result in the test sheet; that sheet is also evidence for the rubric.

---

## 7. Team + roles (5 members, roster locked Oct 9)

| Role | Owns |
|---|---|
| Team Lead (Aldo) | Guidance, coach and program contact, design decisions, review and approval |
| Technical Lead | Task 02 (`assess_login`), Task 05 (Sentinel agent), audit log, agent freeze on Nov 8 |
| Technical Support / QA | Task 03 / 03b (threat feed and failure count), Task 04 (Orchestrate import), Task 06 (test pass, `v1-tested`), baseline timing, `bob_sessions/` check |
| Research & Documentation Lead | Analyst interviews, white paper and procedure manual, written problem and solution, technology statement |
| Communications & Demo Lead | 3-minute video, demo script, checkpoint and showcase presentations, Slack updates |

Each member runs Bob on their own credits and exports their own session reports. Details are in `docs/team/`.

---

## 8. Deliverables → rubric

| Deliverable | Rubric |
|---|---|
| 3-min video: one alert → Sentinel calls tools → recommends → analyst approves | Design & usability; Effectiveness |
| Written problem + solution + prototype link | Completeness & feasibility |
| Tech statement: Bob + watsonx Orchestrate agent + reused backend + new tool | Completeness; Creativity |
| Test results (Section 6) | Effectiveness |
| `bob_sessions/` screenshots | **Eligibility gate** |

*Owner: Aldo (Team Lead). Living doc.*
