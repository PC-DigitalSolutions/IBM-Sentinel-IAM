# Analyst Interview Guide

*Owner: Research & Documentation Lead · Aldo opens the introductions (his network, Raíces Cyber) · Target: 3 to 5 conversations, about 15 minutes each, before the Oct 25 checkpoint*

## Why we are doing this
Our persona and as-is journey are drafts built from public research. Three to five short conversations with people in security or IAM roles turn them into findings we can cite. Use them to check our assumptions, not to sell Sentinel.

## Who to talk to
People who have handled suspicious-login or account-compromise alerts: SOC analysts (tier 1 or tier 2), IAM engineers or administrators, incident responders, or security managers. Banking or financial-services experience is a plus, not a requirement. Note which applies, in general terms only.

## Before the call: consent script
Read this at the start, or send it in writing beforehand:

> "Thanks for your time. We're a student team in the IBM SkillsBuild AI Experiential Learning Lab, building a proof-of-concept AI assistant that helps security analysts triage suspicious logins. We'd like about 15 minutes of your experience. We won't record your name, your employer, or any confidential details. Please don't share anything your employer would consider confidential. If we'd like to quote you, we'll use an anonymous description such as 'a tier-2 SOC analyst at a financial institution', and we'll ask you first. Is that OK?"

Record only "consent given: yes or no" and "OK to quote anonymously: yes or no".

## Questions (15 minutes)
Keep to five questions. Follow up with "Can you walk me through that?" rather than suggesting answers.

1. **Last suspicious login (4 min).** "Think of the last suspicious-login alert you handled. Walk me through it from the alert to the decision. Where did the time go?"
   *Listen for:* the tools they opened, data they gathered by hand, waiting on other people, and rough time per step.
2. **Responses without escalation (3 min).** "Which responses can you take on your own, and which need someone else's sign-off? For example, step-up MFA, ending a session, or resetting a credential."
3. **Trusting an AI recommendation (3 min).** "If a tool recommended an action, what would you need to see before you trusted it?"
   *Listen for:* evidence shown, reasoning, confidence, track record, the ability to override.
4. **Audit (2 min).** "What has to be recorded for a decision like this to pass an audit or review?"
5. **Wrong lockouts (3 min).** "What happens when a legitimate customer or employee gets locked out by mistake? What does it cost in practice: time, complaints, anything else?"
   *Note:* we have no public figure for this. Record what they describe. Use a number only if they give one, and label it as one practitioner's estimate, not a statistic.

**Close:** "Is there anything about this problem we haven't asked that we should have?"

## Notes template (one per conversation)
| Field | Entry |
|---|---|
| Interview # | |
| Date | |
| Interviewer | |
| Role (general) | e.g. "tier-2 SOC analyst, financial services" |
| Consent given / OK to quote anonymously | Yes/No · Yes/No |
| Q1: where the time went | |
| Q2: responses without escalation | |
| Q3: what builds trust | |
| Q4: audit requirements | |
| Q5: cost of a wrong lockout | |
| Anything else | |
| Approved anonymous quote (if any) | |

## Rules
- No names, employers, internal tool names, customer details or incident specifics in notes, Slack or the repo.
- Only quote someone after they agree to that exact wording.
- Report what was said. Don't round it up into a trend: three conversations are three data points.
- Store the notes outside the public repo (for example, the team's shared drive). Only the anonymized summary goes into the white paper.

## After all conversations: summary for the white paper
One page covering:
- Patterns that **confirm** the persona and as-is journey.
- Anything that **contradicts** them, and what we changed as a result.
- What analysts said they need in order to trust a recommendation, compared with what Sentinel shows (ranked reasons, the investigate loop, the audit log).
- A labeled list of approved quotes.
