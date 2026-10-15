# Sentinel IAM: Team Playbook

*How each member does their part, and how we check that the work follows the plan · Team Bastion · Prepared Oct 8, 2026; updated Oct 15 for the 5-member team*

## 1. Why this document exists

You are joining mid-program, and you have been trusted with real ownership. That is a lot to pick up quickly, so this playbook is deliberately specific. It tells you what to do, what "done" looks like, what evidence to keep, and what a good example looks like. Aldo, the Team Lead, is handing the build over to you and will guide rather than build. His job is to set the acceptance criteria, make design calls, review at each checkpoint, and sign off.

Some of this may be familiar. The examples are here so that five people can work independently and still produce one coherent project. Where an example is only an illustration, it says so. Please adapt the examples, but do not skip the evidence steps. Those protect all of us.

Read the companion document, *Sentinel IAM: Current Build and Status*, and your role guide first. This playbook assumes you have.

## 2. Five rules that never bend

1. **Bob writes the code.** The program requires IBM Bob to be a core build tool, and every member exports their Bob task session reports into `bob_sessions/`. Without them, the project is not eligible for judging. Do not hand-write large pieces of code and then ask Bob to review them.
2. **One written task per Bob session.** Write the task and its done-when condition before you open Bob. Stop when the condition is met.
3. **Nothing executes without human approval.** Sentinel recommends. The analyst approves or rejects. Any behavior that runs an action on its own is a failed test, however good the idea.
4. **Fictional data only.** Use the seed users and documentation-range IPs (`203.0.113.x`, `198.51.100.x`, `192.0.2.x`). Never paste real customer, employer, or analyst data into the repo, Bob, or Slack.
5. **Do not invent numbers.** Every statistic we use comes from `research-evidence.md` or from our own measurement. If we do not have a figure, we say so.

## 3. How one task works, start to finish

Every task, for every member, follows the same loop:

1. **Read** the task in `docs/bob-tasks/` and the files it names.
2. **Write** a Bob prompt that states the files to read, what to build, and when to stop.
3. **Run** one Bob session.
4. **Check** the done-when condition yourself. Do not rely on Bob saying it worked.
5. **Capture evidence:** the passing test output or a screenshot, plus a screenshot of the Bob consumption summary exported to `bob_sessions/`.
6. **Post** a short status update in Slack (format in section 11).
7. **Commit** with a clear message that names the task number.

### A good Bob prompt versus a weak one

Weak: *Build the login risk endpoint for our banking project.*

This is vague, so Bob will scan the whole backend and spend credits guessing.

Good (illustrative):

```
Task 02. Read only: the FastAPI app entry file, tests/fixtures/iam_baselines.json,
and tests/scenarios.json. Do not scan other files.

Add POST /iam/assess-login. Request: user_id, ip, device_id, geo, timestamp.
Response: risk_score, risk_level, flags, baseline, explanation.

Scoring is deterministic, no LLM and no database. Impossible travel +35
(over 900 km/h since last login), IP on threat list +30, new device +25,
off-hours +10, capped at 100. Levels: 0-24 Low, 25-49 Medium, 50-79 High, 80+ Critical.
Unknown user returns 404.

Add pytest tests for scenarios A, B, C, D, F and G from scenarios.json.
Do not change any other endpoint. Stop when all tests pass.
```

This names the files, the contract, the rules, the tests, and the stop condition.

## 4. Technical Lead: the endpoint and the agent

You own the build: the new assess\_login endpoint, the Sentinel agent in Orchestrate, and the audit log. Your Bob sessions run on your own credits.

### Task 02: `assess_login` endpoint and tests

- **Done when:** all fixture scenarios pass (A, B, C, D, F, G).
- **Evidence:** pytest output showing all tests passing, and the Bob consumption screenshot.
- **Check yourself:** run scenario A by hand. Expected: score 100, Critical, flags for impossible travel, new device, off-hours and a threat-listed IP. Run scenario D (tkim, known device, home city, 1 AM). Expected: score 10, Low. If D comes back Medium or higher, the off-hours rule is too heavy.
- **Heads up:** the example response in the build spec shows a score of 87 with all four flags, but the rules add up to 100. The tests use 100. Please fix the example in the spec as part of this task.

### Task 05: the Sentinel agent in Orchestrate

The agent receives a goal, guardrails and tool descriptions, then decides its own path. It does not follow a fixed procedure. Illustrative instruction skeleton:

```
Goal: For each suspicious-login alert, reach a ranked, justified recommendation
with as little evidence-gathering as the case needs.

You own the case. After each tool result, state what you learned and what is
still unknown, then either call another tool or stop. You choose the tools and
the order.

Guardrails: You recommend. You never execute. The analyst approves or rejects.
If you reject-and-replan, present the next-best option with its reason.
If signals conflict or data is thin, gather more evidence or ask the analyst
one specific question before recommending.

Policy guidance: 2 failed attempts in 15 minutes triggers investigation.
4 or more means flag, review and manual approval.

Output: risk level, a plain-language explanation, and recommendations ranked
from best to lowest, each with a reason. State conclusions plainly.
```

Illustrative behavior to aim for (scenario F-style alert):

> **Learned:** `assess_login` returned 55, High, with a new device and a threat-listed IP. **Unknown:** whether this IP belongs to a current campaign. Calling `get_live_threats`.
>
> **Learned:** the IP matches a current credential-theft campaign. Evidence is sufficient; I am skipping `analyze_signal`.
>
> **Recommendations, best first:** 1. Revoke session, because the device is unrecognized and the IP is tied to an active campaign. 2. Step-up MFA, a weaker control that would leave an attacker's session alive if the credential is already stolen. 3. No action, ruled out by two independent risk signals.
>
> **Awaiting your approval.**

- **Done when:** scenario A is handled end to end, the investigate loop is visible in the output, and nothing is ever executed.
- **What failure looks like:** the agent always calls the same tools in the same order regardless of the case, uses words like "probably" or "most likely," or ends the conversation when the analyst rejects.

### Audit log

Banks need a record of every AI-assisted decision. Each time the agent makes a recommendation, log one record. Illustrative example:

```json
{
  "case_id": "case-0007",
  "timestamp": "2026-10-14T15:02:11Z",
  "alert": {"user_id": "mgarcia", "ip": "198.51.100.23"},
  "tools_called": ["assess_login", "get_live_threats"],
  "risk_level": "High",
  "recommendation": "revoke_session",
  "reason": "New device and threat-listed IP; IP matches a current credential-theft campaign.",
  "analyst_decision": "approved",
  "executed": false
}
```

- **Done when:** every recommendation and every approve or reject is logged, and no record shows an action executed without approval.

### Your deliverables

**Technology statement (with the Research & Documentation Lead).** You supply the technical detail; they own the final text. **Agent freeze.** No new features after **Nov 8**.

## 5. Technical Support / QA: tools, connectivity and testing

You connect the pieces and prove they work: the banking threat feed, the authentication-failure lookup, getting the tools into Orchestrate, the test pass and the baseline timing. You also check that `bob_sessions/` has a report for every Bob session across the team. Your Bob sessions run on your own credits.

### Task 03: banking threat feed and authentication-failure lookup

- **Done when:** `/threats/live` returns banking-relevant headlines (for example, credential theft, account takeover, phishing and MFA abuse), and the authentication-failure lookup returns the number of failures for a user in a 15-minute window.
- **Aldo's decisions you must respect:** the agent triggers after 2 failed attempts. Four or more failures means flag, review, and manual analyst approval. Do not use the earlier thresholds (7, 3 to 6, or 5 or more).
- **Open question to settle with Aldo and the Technical Lead first:** whether the lookup is its own tool or part of `assess_login`. Decide this at the start, write the decision in Slack, and then build it.
- **Evidence:** a sample response for 1, 2, 3 and 4 failures, with the expected behavior beside each.

### Task 04: OpenAPI spec and Orchestrate import

- **Done when:** `orchestrate tools list` shows the tools, and one real call to each tool succeeds from inside Orchestrate.
- **Reaching the backend:** Orchestrate runs outside the laptop, so `localhost:8000` will not work. Use `host.docker.internal:8000` with the local ADK Developer Edition, or a `cloudflared` tunnel for Orchestrate SaaS.
- **Evidence:** a screenshot of the tools list and a screenshot or log of one successful call per tool.
- **Deadline:** target **Oct 14**, because the Technical Lead cannot test the agent end to end until this is done.

### Task 06: test pass

Run the 7 original scenarios plus new ambiguous ones. Proposed additions (adapt as needed):

| # | Scenario | What it proves |
| --- | --- | --- |
| H | Known device, home city, business hours, but the IP is on the threat list (score 30, Medium) | The agent investigates conflicting signals and explains its choice |
| I | A user with very little login history | The agent asks one specific question or states the limit, rather than guessing |
| J | Scenario A, analyst rejects revoke and reset | The agent re-plans and offers the next-best option |
| K | 2 failed attempts in 15 minutes, then success from a known device | The agent triggers on the threshold and does not over-react |
| L | 4 or more failures in 15 minutes | The agent flags and requires manual approval |

Keep a test sheet with these columns: scenario, date, tester, input, tools called in order, the agent's stated reason for each tool, risk verdict, recommended action, expected action, executed without approval (must be No), explanation clear (Yes or No), pass or fail, notes, and Bob session reference.

- **Pass bar:** the right action is recommended, the evidence-gathering is justified, the explanation is clear, and nothing executes without approval. Because the agent now chooses its own tools, we judge the outcome and the reasoning, not an exact tool order.
- **Done when:** all scenarios pass and the repo is tagged `v1-tested` (target **Oct 18**). The test sheet is also evidence for the rubric.
- **When something fails:** fix the instructions first, then re-run every scenario, not just the failed one. Fixes can break earlier passes.

### Baseline timing

Our claim is that triage drops from about an hour of manual work to under a minute plus one approval. The hour comes from industry surveys, not from us. So we measure our own:

1. Time a person working through scenario A manually, using only the seed data and a simple runbook. Note the time for each phase.
2. Repeat at least three times and record the average.
3. Time Sentinel on the same alert, from alert to recommendation.
4. Report both numbers honestly as "in our test." Do not present them as industry figures.

## 6. Research & Documentation Lead: evidence and written deliverables

You validate the problem with real evidence and write the documents that explain Sentinel. Keep every finding tied to a source in `research-evidence.md`. Aldo opens the introductions for the analyst conversations. Take test results from Technical Support / QA for the effectiveness evidence.

### Your deliverables

**Technology statement.** One to two pages covering: how IBM Bob was used as a core tool (with reference to `bob_sessions/`), the watsonx Orchestrate agent and its tools, the reused backend and the one new tool, the human-approval guardrail, the synthetic data, and the limits of a proof of concept.

**White paper and manual procedure.** This is the instruction manual for Sentinel. Suggested outline: purpose and scope, who uses it, how Sentinel reaches a decision, the analyst's step-by-step procedure (receive the recommendation, review the evidence, approve or reject, what happens next), the 15-minute authentication-failure thresholds, how the audit trail works, limitations, and a glossary. Aldo wants the document to show that the agent owns the case and presents a complete solution, with the analyst approving it.

**Three to five analyst conversations.** Short (about 15 minutes), with people in security or IAM roles, ideally through Aldo's network and Raices Cyber. Ask about:

- The last suspicious login they handled and where the time went.
- Which responses they can take without escalating.
- What they would need to see from an AI recommendation before trusting it.
- What has to be logged for a decision to pass audit.
- What a wrong lockout costs in practice.

Get permission before quoting anyone, and anonymize quotes. Do not record confidential details about any employer.

**Written problem, solution and prototype link.** Plain language, for someone outside security. Include the persona, the as-is journey, the solution, the measured results, the limits, and the repo link.

## 7. Communications & Demo Lead: the story

You turn the tested agent into the story judges see: the 3-minute video, the demo script, the checkpoint and showcase presentations, and the team's Slack updates.

### Your deliverables

**3-minute video.** Illustrative storyboard:

| Time | Content |
| --- | --- |
| 0:00 to 0:20 | The problem, with one sourced statistic |
| 0:20 to 0:50 | Meet Sentinel and its human-approval guardrail |
| 0:50 to 1:50 | Scenario A live, with the investigate loop visible on screen |
| 1:50 to 2:20 | Analyst rejects and the agent re-plans; scenario D stays Low to show it does not over-lock customers |
| 2:20 to 2:45 | Audit log and our measured timing |
| 2:45 to 3:00 | Close: secure, inclusive, efficient |

**Demo script.** Write it from the test scenarios. Scenario A is the lead candidate; Scenario E (analyst rejects, nothing executes) shows the guardrail. Confirm the final pick with Aldo.

**Record only from the tested agent.** Wait until Technical Support / QA confirms the `v1-tested` tag, and re-record if the agent changes before the Nov 8 freeze.

**Checkpoint (Oct 25) and showcase (Nov 9 to 22).** Demo a tested agent, not a work in progress.

**Slack.** Keep a short running status post current for the coach, and use the same public team description in all materials.

**Final packaging for Nov 22.** Aldo approves and submits the package. Use the checklist in section 10.

## 8. Handoffs between roles

The roles depend on each other. Agree on these handoffs explicitly in Slack.

- **By Oct 14, Technical Support / QA gives the Technical Lead:** a backend reachable from Orchestrate, the tools imported, one recorded successful call per tool, the request and response shapes, and a list of known issues.
- **By the next day, the Technical Lead gives Technical Support / QA:** a list of any tool behavior that looks wrong or confusing to the agent, with the exact input.
- Until Oct 14, the Technical Lead can draft the agent instructions and Technical Support / QA can draft the test sheet against the tool contracts. You do not have to wait.
- **Technical Support / QA gives the Communications & Demo Lead:** confirmation of the `v1-tested` tag before any recording, and the scenario results to show on screen.
- **Technical Support / QA gives the Research & Documentation Lead:** the test sheet and timing numbers for the effectiveness evidence.
- **The Research & Documentation Lead and the Communications & Demo Lead** share one storyline so the written and video versions match.
- **The Technical Lead and the Research & Documentation Lead** write the technology statement together.
- Aldo is involved in any decision that changes a threshold, an action, a tool contract, or a guardrail.

## 9. Checkpoints and how Aldo will check the work

| Date | What Aldo checks | Evidence he expects |
| --- | --- | --- |
| Oct 9 | All five members on the roster; IBM Cloud request submitted | Roster confirmation |
| Oct 14 | Three tools live in Orchestrate | Tools list screenshot; one call per tool |
| Oct 18 | Agent tested; repo tagged | Test sheet; `v1-tested` tag; pytest output |
| Oct 25 | Checkpoint demo of a tested agent | Live demo; audit log; first timing numbers |
| Nov 8 | Agent frozen; deliverable drafts complete | Video draft; written statements |
| Nov 22 | Submission | Section 10 checklist |

## 10. Definition of done and the final checklist

A task is done only when the done-when condition is met, the evidence exists, the Bob session report is exported, the work is committed, and the status update is posted.

Before submitting on Nov 22, confirm:

- The 3-minute video is under three minutes and shows the full flow.
- The written problem, solution and prototype link are complete.
- The technology statement is complete.
- The test sheet is attached.
- `bob_sessions/` contains reports from **every** member.
- Every statistic has a source, or is labeled as our own measurement.
- No real data appears anywhere.
- Every member has finished the three courses and the credential requirements.

## 11. Status updates

Post in Slack after every task, and at least once a week even if nothing finished. Use this format:

- **Done:** what finished, with evidence.
- **Next:** the next task.
- **Blocked:** what you need and from whom, or none.
- **Bobcoins left:** your remaining balance.

Example:

> **Done:** Task 02. All 6 fixture scenarios pass (screenshot attached). Fixed the 87 versus 100 example in the spec. **Next:** Task 03, starting with the question of where the authentication-failure lookup lives. **Blocked:** Need Aldo's call on that question. **Bobcoins left:** 38.

## 12. When you are stuck

Being stuck is normal, and asking is cheap. Do not spend Bobcoins to work around a blocker.

1. Spend a short, fixed amount of time on it yourself.
2. Post in Slack with the task number, what you tried, and the exact error or question.
3. If it affects another member's work, say so in the same message.
4. If your balance drops near the 10-credit reserve, tell the team before starting another session.

## 13. Keeping the work fair

The work is split across four roles so that everyone carries a fair load, and the work-split spreadsheet tracks it. If you finish early, offer help before taking over someone else's task, and agree on it in Slack. The Bob session stays with the person who ran it, because each member's own reports are what count for eligibility. If the load turns out to be uneven, tell Aldo and we will rebalance. That is a planning problem, not a failing.

## 14. Common mistakes and what to do instead

| Mistake | Do this instead |
| --- | --- |
| Starting Bob without a written task | Write the task and done-when first |
| Writing code by hand | Have Bob write it; keep the session report |
| Skipping the consumption screenshot | Capture it after every session |
| Changing a threshold or action without asking | Raise it with Aldo first |
| Letting the agent execute an action | Recommend only; log the approval |
| Hedging language such as probably or most likely | State the conclusion plainly with its reason |
| Using real names, IPs or data | Use seed users and documentation-range IPs |
| Quoting a statistic from memory | Take it from `research-evidence.md` or measure it |
| Fixing a failed test and re-running only that test | Re-run every scenario after any fix |

Thank you for taking this on. If anything in this playbook is unclear or seems wrong, say so early. That is how we keep the project, and everyone's time, protected.
