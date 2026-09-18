# Sentinel IAM — Master Knowledge Doc
### Team Bastion · IBM SkillsBuild AI Experiential Learning Lab · Banking & Financial Services

> This is the single source of truth for the project. Upload it as Project knowledge in Claude.ai. Some sections (empathy map, as-is scenario) are **drafts to validate with real research** — they're marked.

---

## 1. Program context (the rules we build under)

- **Program:** IBM SkillsBuild AI Experiential Learning Lab (Fall 2026), a 10-week program to build a proof-of-concept **agentic AI** solution for a real industry challenge. Not a competition — scored /20 for *feedback*, not ranking.
- **Hard requirement:** IBM Bob (IBM's AI dev IDE) must be a *core* build tool; each member exports **Bob task session reports** into a `bob_sessions/` folder in the repo. Without it, the project isn't eligible for judging.
- **watsonx Orchestrate** is optional-but-"highly advised" — we're using it for the agent layer.
- **Bobcoins:** ~50 initial; **150 per team account** land a few days after the Oct 9 IBM Cloud request.
- **Credential requirements (all mandatory):** 3 self-paced courses (Enterprise Design Thinking Practitioner 3h, Make Agentic Work for You 4h, How IBM Bob… 30min); attend Thursday instructor-led sessions (or watch recordings); deliver the project + presentation. Completion unlocks an IBM certificate + digital credential + a bonus **IBM Career Fair & mentoring**.
- **Key dates:** Solution Design (Wks 1–5) Sept 17–Oct 18 · IBM Cloud request deadline **Oct 9** · Mid-Program Checkpoint **Oct 25** · Build (Wks 6–8) Oct 19–Nov 8 · Career Fair Nov 4 (TBC) · Showcase (Wks 9–10) Nov 9–22 · **Project Submission Nov 22** · Team roster locks **Oct 9**.
- **Final deliverables:** 3-min video demo, written problem+solution+prototype link, technology statement, `bob_sessions/` reports.
- **Team:** Team Bastion — 3 members. Lead (Aldo, IAM/cybersecurity engineer) + a beginner SNHU teammate (Research Lead) + a 3rd member (Communications Lead).

---

## 2. The challenge

**IBM's banking prompt:**
> How might we use Agentic AI to create more secure, inclusive, and efficient financial experiences for customers and institutions?

**Our sharpened framing:**
> How might we help a bank's security team respond to suspicious access events faster and more confidently — without taking the human out of high-stakes decisions?

**The problem underneath:** When an account looks compromised — a strange login, a token from nowhere, a leaked credential — a security analyst must *manually* correlate the event, the current threat landscape, and the right response. That correlation is slow and stressful, and slow response is where an anomaly becomes a breach.

---

## 3. The solution — Sentinel IAM

An agentic AI copilot for a bank's security analyst. A team of agents watch, triage, and **recommend** a response; a human approves the action.

**The four agents:**
| Agent | Role |
|---|---|
| **Sentinel** | Orchestrates the others + talks to the analyst, explaining every decision in plain language |
| **Watchtower** | Watches the live threat landscape; flags what's relevant to the bank |
| **Gatekeeper** | Risk-scores a suspicious access event *against the current threat picture* |
| **Custodian** | Proposes the fix — rotate a credential, step up auth, revoke a token — **never acts without human approval** |

**One-sentence pitch:**
> Sentinel IAM turns minutes of manual threat-correlation into seconds of agent reasoning plus one human approval — so a bank stops breaches faster without ever letting AI make an irreversible call on its own.

**POC scope:** One live end-to-end flow — suspicious event → Watchtower/Gatekeeper triage → Custodian recommends → analyst approves → Sentinel explains. Built with IBM Bob, orchestrated on watsonx Orchestrate, on top of an existing FastAPI threat-analysis backend (reused as tools). Not a production platform — a proof the agentic loop adds value.

**Why it fits the prompt:** secure (faster breach response), inclusive (fewer wrongful customer lockouts), efficient (analyst does more with less) — and human-in-the-loop by design, which is non-negotiable in banking.

---

## 4. Opportunity framing

**Who experiences the problem (primary user):** the Tier-2 SOC / IAM analyst. On the hook when access looks wrong; measured on speed + accuracy. We design for them.

**Who else is involved (stakeholders):**
- SOC / IR Manager — accountable for mean-time-to-respond
- Tier-3 / senior responders — escalation target
- IAM / Identity team — owns the systems Custodian would act on
- The bank customer — collateral of a wrong action (the "inclusive" angle)
- Compliance / audit / risk — need the decision trail; care about explainability
- CISO — owns org-level risk; the buyer
- Fraud team — adjacent (account takeover overlaps)
- Regulators (indirect) — the reason human-in-the-loop + auditability matter

**What we're taking for granted (assumptions):**
- Detection already works; the gap is correlation + response, not spotting
- The analyst's real bottleneck is manual correlation (not staffing/tool access)
- Analysts will trust an AI recommendation if it's explained + reversible
- Human-in-the-loop is *required* in banking, not just preferred
- Recommended actions map cleanly to real IAM controls
- Seconds-level agent reasoning is fast enough to matter
- Bank events can be represented as signals our backend can analyze

⚠️ **Riskiest assumptions to validate first:** "correlation is the real bottleneck" and "analysts will trust + act on an AI recommendation."

**What we still need to learn (open questions):**
- Real alert queue/volume (validates the pain)
- Current MTTR and where the time goes (impact baseline)
- Which responses an analyst can take without escalation (defines Custodian's action set + approval gate)
- How much explanation earns trust vs. becomes noise
- The real cost of a wrong action (customer lockout, support surge)
- Which threat-intel sources banks actually use
- What must be logged for an AI-assisted decision to pass audit
- Integration reality: can agents touch IAM systems, or strictly recommend?

*Note: Aldo can answer several of these from his IAM/cybersecurity experience; the rest (threat-intel sources, MTTR benchmarks) are public research for the teammates.*

---

## 5. Empathy snapshot *(DRAFT — validate)*

**Persona:** "Maya," Tier-2 SOC / IAM analyst at a mid-size retail bank. 3 years' experience. Lives in a queue of alerts. Not a developer.

- **Says:** "I get more alerts than I can chase." · "By the time I've pieced it together, the window's half closed." · "I can't just auto-lock a customer — if I'm wrong, that's a support storm."
- **Thinks:** *Is this tied to today's phishing wave?* · *Escalate and be wrong = slow; ignore and be wrong = on me.*
- **Does:** Triages the queue; pivots between SIEM, IAM console, threat feeds; copies indicators between tools by hand; follows a runbook; documents for audit.
- **Feels:** Overloaded, anxious about missing the real one, second-guessing high-stakes calls, drained by repetition.
- **Goals:** Close the *right* incidents fast; never be the one who missed the breach; keep customers unblocked.
- **Pains:** Alert fatigue; manual correlation; fear of a wrong irreversible action; documentation burden.
- **Gains valued:** A correlated risk read she trusts; a recommended, reversible, *explained* next step; less write-up time.

---

## 6. As-is scenario *(DRAFT — validate)*

Maya handles one suspicious access event **today**, with no Sentinel IAM.

| Phase | Doing | Feeling |
|---|---|---|
| 1. Detect | Alert lands: login from new device on a privileged account | Alert, skeptical |
| 2. Triage | Opens alert, checks account + recent activity | Cautious, time-pressured |
| 3. Correlate | Pivots to threat feeds + SIEM; copies indicators by hand | **Frustrated — the slow manual part** |
| 4. Decide | Weighs risk; consults runbook for the response | Anxious, second-guessing |
| 5. Respond | Executes the action in the IAM console | Tense — the irreversible moment |
| 6. Document | Writes up what she saw/decided/did, for audit | Tired, box-checking |

**Pain points Sentinel IAM attacks:**
- Phase 3 (Correlate) — biggest, most manual time sink → *Watchtower + Gatekeeper automate it*
- Phase 4 (Decide) — high-anxiety, error-prone → *Custodian gives an explained recommendation*
- Phase 5 (Respond) — fear of irreversible mistakes → *recommend-then-approve keeps the human in control*
- Phase 6 (Document) — repetitive burden → *the agents' rationale becomes the audit trail*

---

## 7. Technical shape (see build-spec.md for detail)

The agents run on watsonx Orchestrate and call an existing FastAPI service (`CyberShield_IV`, port 8000) as tools — it's signal-agnostic, so it re-points at banking/IAM signals without a rewrite. Endpoints: `GET /threats/live`, `GET /threats/history`, `GET /analyze?signal=`, `POST /analyze/file`, `POST /sentinel/chat`, `GET /status`. Bob-heavy build starts Week 6 (Oct 19).
