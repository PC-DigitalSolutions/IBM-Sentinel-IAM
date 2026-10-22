# How we work

Short version: **write the task → one Bob session → check it yourself → save evidence → update STATUS → commit → post in Slack.**

---

## Five rules that never bend

1. **Bob writes the code.** IBM requires Bob as the core build tool. Don't hand-write large pieces of code and then ask Bob to review them.
2. **Every Bob session gets a screenshot in [`bob_sessions/`](bob_sessions/README.md).** No screenshots from every member means the project can't be judged.
3. **Sentinel recommends; it never executes.** Any change that lets it take an action on its own is a failed test.
4. **Fictional data only.** Seed users and IPs from `203.0.113.x`, `198.51.100.x`, `192.0.2.x`. No real names, IPs, employers or customer data, anywhere: repo, Bob, Slack.
5. **No invented numbers.** Every statistic comes from [`docs/research/research-evidence.md`](docs/research/research-evidence.md) or from our own measurement, labeled "in our test."

---

## The task loop

Every task, for every role, follows the same steps.

1. **Pick** the task from [docs/STATUS.md](docs/STATUS.md). Set it to 🟦 In progress with your name.
2. **Read** its prompt in [docs/bob-tasks/](docs/bob-tasks/) and only the files it names.
3. **Run one Bob session.** Paste or adapt the task prompt. It should name the files to read, what to build, and when to stop. (Example of a good prompt: [team-playbook.md §3](docs/team/team-playbook.md).)
4. **Stop** when the task's "Done when" condition is met.
5. **Check it yourself.** Run the tests or the scenario. Don't rely on Bob saying it worked.
6. **Save evidence:**
   - Bob screenshot: Bob → Tasks → All → click the task header → screenshot → save as `bob_sessions/<name>-task-<nn>-<yyyy-mm-dd>.png` and add a row to the table in [bob_sessions/README.md](bob_sessions/README.md).
   - Test output or a screenshot of the result.
7. **Update** [docs/STATUS.md](docs/STATUS.md): status ✅ and the evidence link.
8. **Commit** with the task number in the message (see below).
9. **Post** a status update in Slack (format below).

No Bob task? Non-code work (interviews, writing, video) skips steps 3 and 6, but still updates STATUS and posts in Slack.

---

## Bob credits (Bobcoins)

- About 50 each. Keep about **10 in reserve** for fixes found in testing. Tell the team **before** you drop below that.
- No session without a written task. One small task per session.
- Point Bob only at the files the task names. [`.bobignore`](.bobignore) already hides the noisy folders.

---

## Git

```bash
git pull
# ...make your change...
git add <files>
git commit -m "Task 03b: add 5-minute failure flag to assess_login"
git push
```

- Start commit messages with the task number when there is one.
- Pull before you start, so you don't overwrite a teammate.
- Never commit `.env` or any key. It's in `.gitignore`; keep it there.
- After Task 06 passes, QA tags the release: `git tag v1-tested && git push origin v1-tested`.

---

## Changing a rule

Thresholds, actions, tool contracts and guardrails are settled. To change one:

1. Add a row under **Open decisions** in [docs/STATUS.md](docs/STATUS.md).
2. Ask Aldo in Slack.
3. Once approved, update **all** of: [`docs/build-spec.md`](docs/build-spec.md), [`agents/sentinel.instructions.md`](agents/sentinel.instructions.md), [`docs/knowledge/sentinel-response-playbook.md`](docs/knowledge/sentinel-response-playbook.md), [`AGENTS.md`](AGENTS.md), and the scenarios if expected results change.
4. Re-run every test scenario.

---

## Testing

- **Prototype unit tests:** `py -m pytest tests -q` (should say 21 passed).
- **Backend tests:** in CyberShield_IV, `python -m pytest tests/test_assess_login.py -q`.
- **Agent tests:** run scenarios A to L in Orchestrate chat; log **one row per run** in [`docs/testing/test-sheet.csv`](docs/testing/test-sheet.csv). Pass bar: [`docs/testing/test-sheet.md`](docs/testing/test-sheet.md).
- After **any** fix, re-run **every** scenario, not just the one that failed.

---

## Slack status update

Post after every task, and at least once a week even if nothing finished.

> **Done:** what finished, with evidence
> **Next:** your next task
> **Blocked:** what you need and from whom (or "none")
> **Bobcoins left:** your balance

---

## Keeping docs useful

- If you change how something works, update the doc that describes it in the same commit.
- If a doc is out of date and you're not sure how to fix it, add a note at the top: `> ⚠️ Out of date: <what's wrong>` and tell the team.
- New doc? Add it to [docs/README.md](docs/README.md).
