# CyberShield — Sentinel IAM
### IBM SkillsBuild AI Experiential Learning Lab · Banking & Financial Services · Build Spec

> **How to use this doc:** This is the plan *you* work from and feed into Bob. Section 6 (`AGENTS.md`) is the file you paste at the root of the new repo so Bob has persistent context. Sections 4–5 are the tasks you hand Bob one at a time. I (Claude) keep this doc and the written deliverables current; **Bob builds the code** so the `bob_sessions/` reports stay legit and your Bobcoins stretch.

---

## 1. Concept (the pitch)

**Problem.** A bank's security operations team drowns in access events and threat noise. When a suspicious login, token use, or credential exposure happens, an analyst has to manually correlate it against the current threat landscape, decide the risk, and figure out the right response — rotate a secret? step up auth? revoke a session? That correlation is slow, and slow response is where breaches happen.

**Solution.** **Sentinel IAM** — an agentic AI copilot where a team of specialized agents continuously watch threats, triage access events against that live threat picture, and *recommend* concrete IAM responses to a human analyst who approves the action. Human-in-the-loop by design: the agents reason and propose; a person decides.

**Target user.** SOC / IAM analyst at a mid-to-large bank.

**Measurable impact.** Mean-time-to-triage and mean-time-to-respond on access incidents drop from minutes-of-manual-correlation to seconds-of-agent-reasoning-plus-one-approval.

---

## 2. The agent cast (built in Bob, run on watsonx Orchestrate)

A **primary orchestrator** delegates to three specialist collaborator agents — the exact multi-agent delegation pattern watsonx Orchestrate rewards.

| Agent | Role | Human-facing? |
|---|---|---|
| **Sentinel** | Orchestrator + analyst copilot. Routes work, explains every decision in plain language, holds the conversation with the analyst. | ✅ Yes |
| **Watchtower** | Threat-intelligence agent. Pulls the live threat feed and assesses what's relevant to the bank's stack. | No |
| **Gatekeeper** | IAM/access triage agent. Given a suspicious auth/access event, scores its risk *against Watchtower's current threat picture*. | No |
| **Custodian** | Secrets & response agent. Proposes concrete actions (rotate credential, step-up auth, revoke token) — **recommends only; a human approves.** | No (proposes to human) |

*(Naming is bank-appropriate and demo-friendly. "Sentinel" carries over from your existing copilot; the rest are new.)*

---

## 3. What we reuse vs. build new

**Reuse — the existing FastAPI/Neon backend (`C:\CyberLab\CyberShield_IV`, port 8000) becomes a set of *tools* the watsonx agents call.** It's signal-agnostic (the CNS gate engine is keyword-driven), so it re-points at banking/IAM signals with no rewrite.

**Build new in Bob:**
- The banking multi-agent orchestration on watsonx Orchestrate (Sentinel → Watchtower/Gatekeeper/Custodian)
- Banking-tuned signals & specialist logic (fraud / access / secrets vocabulary and gates)
- A thin demo surface (a screen or the Orchestrate chat) showing an access incident flow end-to-end
- The `bob_sessions/` reports as you go

---

## 4. Tool definitions (map agents → real backend endpoints)

Build these as watsonx Orchestrate tools (OpenAPI import is easiest since these are real HTTP endpoints). All are live in `src/api/main.py`.

| Tool | Endpoint | Used by | Purpose |
|---|---|---|---|
| `get_live_threats` | `GET /threats/live?limit=` | Watchtower | Rolling classified threat feed |
| `get_threat_history` | `GET /threats/history?limit=&kind=` | Watchtower | Durable archive for trend context |
| `analyze_signal` | `GET /analyze?signal=` | Gatekeeper | Run an event/signal through the analysis engine → verdict + specialist reports |
| `analyze_evidence` | `POST /analyze/file` | Gatekeeper | Multimodal: assess an attached artifact (screenshot, PDF) |
| `sentinel_chat` | `POST /sentinel/chat` | Sentinel | Analyst-facing conversational reasoning |
| `health` | `GET /status` | Sentinel | Backend liveness |

> **Note for the tech statement:** the backend's own "gates + specialist agents" (El Guardián pattern) become the *analysis engine* underneath `analyze_signal`. You're layering a banking multi-agent orchestration on top of a working intel core — that's the "reuse backend, new agents" story stated cleanly.

---

## 5. Bob build plan (Bobcoin-aware task breakdown)

Hand Bob **one task per session**, each scoped small so a session closes cleanly (cheaper coins, cleaner reports). Spread Bob-heavy tasks **across team members' accounts** — each account has 40 coins; don't let one hit 100%.

**LEARN → BUILD sequence:**

1. **Scaffold** — `Bob /init` on the new repo to generate the base `AGENTS.md`, then replace it with Section 6 below. *(cheap)*
2. **Point backend at banking signals** — small config/prompt change so `/analyze` and `/threats` speak fraud/IAM, not concerts. *(cheap–medium)*
3. **Watchtower tool wiring** — import `get_live_threats` / `get_threat_history` as Orchestrate tools; build the Watchtower agent that summarizes current threats. *(medium)*
4. **Gatekeeper agent** — takes a sample access event, calls `analyze_signal`, risk-scores it against Watchtower's output. *(medium — core)*
5. **Custodian agent** — maps a Gatekeeper verdict to a recommended action with a human-approval gate. *(medium — core)*
6. **Sentinel orchestrator** — wires the three collaborators and the analyst chat; this is the demo spine. *(medium–heavy)*
7. **Demo surface + seed data** — one clean incident walkthrough for the 3-min video. *(medium)*
8. **Export `bob_sessions/`** — screenshot each task's session-consumption summary; commit to repo. *(free, mandatory)*

**Checkpoint gate (Week 6):** items 1–5 working = a defensible mid-program deliverable. Items 6–8 are the Weeks 7–10 polish toward final.

---

## 6. `AGENTS.md` to paste at the new repo root

See the separate `AGENTS.md` file I'm sending alongside this — drop it in the new repo before Bob's second session.

---

## 7. Team roles + Bobcoin split

Five roles from the guide; adapt to your headcount.

| Role | Owns | Bob usage |
|---|---|---|
| **Team Lead** (you) | Submission, timeline, the vision above | Light — reviews |
| **Technical Lead** | Tasks 3–6 (agent build) | Heavy — primary Bob account |
| **Solution Designer** | Demo surface, incident UX (task 7) | Medium |
| **Research Lead** | Banking threat/IAM signals for task 2, empathy map | Light |
| **Communications Lead** | Video, written statements, `bob_sessions/` collation | Light |

**Coin rule:** route tasks 4–6 (the expensive ones) across *two* accounts so neither Technical-Lead account tanks before Week 10.

---

## 8. Deliverable checklist → rubric

| Deliverable | Maps to rubric points |
|---|---|
| 3-min video (problem → Sentinel resolves an incident live) | Design & usability; Effectiveness |
| Written problem + solution + prototype link | Completeness & feasibility |
| Technology statement (Bob core + watsonx multi-agent + reused intel core) | Completeness; Creativity |
| `bob_sessions/` screenshots | **Eligibility gate** — without this you're not judged |

---

*Owner: Aldo (Team Lead). Living doc — I'll keep it and the written deliverables current as Bob's build lands.*
