# Suspicious-Login Response Playbook (Sentinel knowledge base)

*Version 0.1 draft, Oct 15, 2026 · Owner: Research & Documentation Lead · Policy owner: Aldo (Team Lead) · Fictional policy for a proof of concept. It describes no real bank.*

This playbook is the written policy Sentinel retrieves to ground and cite its recommendations. It restates the team's settled rules; it does not add new ones. Any change to a threshold, an action or a guardrail needs Aldo's approval first (section 9).

Writing rules for this file: one topic per section, short sections with clear headings (the agent retrieves by section), no statistics, no real names, IPs only from `203.0.113.x`, `198.51.100.x`, `192.0.2.x`.

## 1. Purpose and scope
- Applies to one alert type: a suspicious sign-in to a bank account or workforce identity.
- Sentinel recommends a response. A SOC or IAM analyst approves, rejects or chooses another option. Sentinel never executes a response.
- Out of scope: other alert types, fraud decisions on transactions, and any automatic action.

## 2. Roles and authority
| Role | Can do | Cannot do |
| --- | --- | --- |
| Sentinel (AI agent) | Gather evidence, assign a risk level, rank responses with reasons, record the case | Execute, or say it executed, any response |
| SOC / IAM analyst | Approve, reject, or choose another option; record the reason | Skip the audit record |
| Bank operations team | Carry out an approved response through the bank's own systems | Act on a recommendation that no analyst approved |

## 3. Risk levels and default responses
The login risk score comes from `assess_login`: impossible travel +35, IP on the threat list +30, new device +25, off-hours +10, capped at 100.

| Risk level | Score | Default first response |
| --- | --- | --- |
| Low | 0 to 24 | No action; keep monitoring |
| Medium | 25 to 49 | Step-up MFA on the next sensitive action |
| High | 50 to 79 | Revoke the active session |
| Critical | 80 to 100 | Revoke the active session and force a credential reset |

The score is evidence, not the decision. Sentinel starts from the default and explains any difference.

## 4. Response definitions
### 4.1 No action, keep monitoring
- **What it does:** leaves the session active; the case stays on record.
- **Use when:** the risk is Low and no rule in section 5 or 6 applies.
- **Customer impact:** none.
- **Risk left open:** if the signals were wrong, the session continues.

### 4.2 Step-up MFA
- **What it does:** asks the user for an extra verification on the next sensitive action.
- **Use when:** the risk is Medium, or a Low-risk case is flagged under section 5.
- **Customer impact:** one extra verification step; no lockout.
- **Risk left open:** if the credential and the second factor are both compromised, the attacker passes.

### 4.3 Revoke the active session
- **What it does:** ends the current session immediately; the user signs in again.
- **Use when:** the risk is High.
- **Customer impact:** the user is signed out once.
- **Risk left open:** a stolen password still works for the next sign-in.

### 4.4 Revoke the session and reset the credential
- **What it does:** ends the session and forces a new password or key.
- **Use when:** the risk is Critical.
- **Customer impact:** the highest: sign-out plus a reset through a verified channel.
- **Risk left open:** lowest of the four.

## 5. Authentication-failure rule
- Failed sign-ins for the account are counted in the **5 minutes** up to the alert.
- **2 or more failures flags the case.** Sentinel investigates and has a ranked recommendation ready for the analyst.
- A flagged case with a **Low** risk score ranks **step-up MFA** first. At Medium or above, the default for the level applies.
- A flag never removes the approval step.

## 6. Special cases
| Case | What Sentinel does | Test scenario |
| --- | --- | --- |
| Off-hours sign-in only, known device, home city | Stays Low; explains why off-hours alone does not justify a lockout | D |
| Normal baseline but a threat-listed IP | Names the conflict, checks the IP against current threats, ranks step-up MFA above revoke and says why | H |
| Little or no sign-in history | States the limit or asks the analyst one specific question; never invents history | I |
| Unknown user | Says the user is unknown, asks the analyst to check the user ID, assigns no risk level | G |
| Analyst rejects (for example, the customer is traveling) | Records the reason, keeps the case open, offers the next-best option and the risk it leaves open | E, J |

## 7. Analyst procedure
*[Research & Documentation Lead: complete from the analyst interviews. Steps below are the current draft.]*
1. Read Sentinel's verdict, its reasons and the evidence it gathered.
2. Approve, reject, or choose another option. Give a one-line reason for a reject or an override.
3. If approved, hand the response to the operations team. Sentinel does not execute it.
4. Confirm the audit record is complete (section 8).

## 8. Audit record
One record per recommendation and per analyst decision, with: case ID, timestamp, alert fields, tools called, risk level, recommended response, reason, analyst decision, analyst reason (if any), and `executed: false` for Sentinel.

## 9. Change control
Thresholds, responses and guardrails change only with Aldo's approval. When they change, update this playbook, `docs/build-spec.md` and `agents/sentinel.instructions.md` together, re-import the knowledge base, and re-run every test scenario.
