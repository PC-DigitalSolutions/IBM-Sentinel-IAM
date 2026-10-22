# Onboarding: your first days on Sentinel IAM

This guide takes you from "just joined" to "working on my first task." Follow the steps in order. Each step says how long it takes and how you know you're done.

If something here is wrong or unclear, fix it in this file or ask in Slack. A confused newcomer means the docs need work, not that you missed something.

---

## Day 1: understand the project (about 1 hour)

### Step 1. Read the front door (10 min)
Read the repo [README](../README.md) from top to bottom.

**Done when** you can explain in one sentence what Sentinel does and why a human has to approve.

### Step 2. Read the spec (20 min)
Read [build-spec.md](build-spec.md), sections 1 to 3 and section 6. This is the technical source of truth.

**Done when** you can name the three tools and say what each one is for.

### Step 3. Read how the agent thinks (10 min)
Read [agents/sentinel.instructions.md](../agents/sentinel.instructions.md). This is the text the agent receives in watsonx Orchestrate. It decides how Sentinel behaves.

### Step 4. Look at the test cases (10 min)
Skim the table in [testing/test-sheet.md](testing/test-sheet.md). Every scenario, A to L, is one fake alert with the answer we expect. If the agent gets these right, the project works.

### Step 5. See where we are (10 min)
Read [STATUS.md](STATUS.md). It tells you what is done, what is next, and who owns it.

---

## Day 1: set up your machine (about 30 min)

### Step 6. Get the code
You need [Git](https://git-scm.com/downloads) and [Python 3.10+](https://www.python.org/downloads/).

```bash
git clone https://github.com/PC-DigitalSolutions/IBM-Sentinel-IAM.git
cd IBM-Sentinel-IAM
```

If you will work on the backend (Tasks 02, 03, 03b), also clone it next to this repo:

```bash
git clone https://github.com/PC-DigitalSolutions/CyberShield_IV.git
```

Ask in Slack for push access if you don't have it.

### Step 7. Run the prototype

On Windows use `py`. On Mac or Linux use `python3`.

```bash
py -m pip install pytest
py sample_run.py
py -m pytest tests -q
```

**Done when** you see the sample output (a risk level, ranked actions, an approval block) and `21 passed`.

> **Run `pytest tests`, not plain `pytest`.** A stray copy of the project in some local folders makes plain `pytest` fail with "import file mismatch". Pointing it at `tests` avoids that.

### Step 8. Set up IBM Bob
1. Install Bob and sign in with your IBM SkillsBuild account (see the program guide from the coach).
2. Open this repo folder in Bob. Bob reads [AGENTS.md](../AGENTS.md) automatically, so it already knows the project rules.
3. Check your Bobcoin balance. You start with about 50.

**Don't start a Bob session yet.** Every session needs a written task first (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

### Step 9. Check the backend is up (optional)
Open `https://cybershield-iv.onrender.com/status` in a browser. A JSON response means it's running. The free Render tier sleeps when idle, so the first request can take up to a minute.

---

## Day 2: start contributing

### Step 10. Confirm your role
Check that your name is next to your role in [STATUS.md](STATUS.md#team). If not, add it.

### Step 11. Read your role's section
| Your role | Read |
|---|---|
| Technical Lead | [team-playbook.md §4](team/team-playbook.md), [bob-tasks/task-05](bob-tasks/task-05-sentinel-agent.md), [task-05b](bob-tasks/task-05b-knowledge-base.md), [orchestrate-runbook.md](orchestrate-runbook.md) |
| Technical Support / QA | [team-playbook.md §5](team/team-playbook.md), [bob-tasks/task-03](bob-tasks/task-03-banking-feed.md), [task-03b](bob-tasks/task-03b-failure-window.md), [task-04](bob-tasks/task-04-orchestrate-tools.md), [task-06](bob-tasks/task-06-test-pass.md), [orchestrate-runbook.md](orchestrate-runbook.md), [testing/](testing/) |
| Research & Documentation Lead | [team-playbook.md §6](team/team-playbook.md), [research/research-evidence.md](research/research-evidence.md), [research/analyst-interview-guide.md](research/analyst-interview-guide.md), [knowledge/sentinel-response-playbook.md](knowledge/sentinel-response-playbook.md) |
| Communications & Demo Lead | [team-playbook.md §7](team/team-playbook.md), [testing/test-sheet.md](testing/test-sheet.md) (scenarios to demo), [research/research-evidence.md](research/research-evidence.md) (numbers you may quote) |

Note: the team playbook was written before Oct 15. Where it mentions a **15-minute** failure window or a **4+ failures** tier, the current rule is **2 failures in 5 minutes**.

### Step 12. Pick up your task
1. Find your next task in [STATUS.md](STATUS.md).
2. Follow the task loop in [CONTRIBUTING.md](../CONTRIBUTING.md#the-task-loop).
3. When done, update [STATUS.md](STATUS.md) and post in Slack.

---

## Program requirements for everyone

These are separate from your role, and they decide whether you get the certificate.

- [ ] Finish all **6 IBM SkillsBuild courses** and upload the **W6 deliverable** by **Sun Oct 25**
- [ ] Attend the Thursday sessions or watch the recordings
- [ ] Run **at least one real Bob session** and save its screenshot in [`bob_sessions/`](../bob_sessions/README.md). **Without screenshots from every member, the project can't be judged.**

---

## Words you'll see a lot

| Term | Meaning |
|---|---|
| SOC / IAM analyst | The bank security person who handles the alert. Our user |
| Step-up MFA | Ask for an extra verification code only because the login looks risky |
| Revoke session | Log the user out right now |
| Reset credential | Force a new password |
| Impossible travel | Two logins too far apart to travel between in the time elapsed |
| Tool | An API the agent can choose to call to get information |
| Knowledge base | A document the agent can search (our response playbook). Not a tool |
| IBM Bob | IBM's AI coding assistant. We must use it to build. Its credits are Bobcoins |
| watsonx Orchestrate | IBM's platform where the agent actually runs |
| `v1-tested` | The git tag we add once every scenario passes |

More terms: [team/current-build-and-status.md §14](team/current-build-and-status.md).

---

## Who to ask

| Question about | Ask |
|---|---|
| Design, thresholds, guardrails, "is this allowed?" | Aldo (advisor), in Slack |
| Program rules, deadlines, Bob access | The coach, in Slack |
| A task someone else owns | That role's owner (see [STATUS.md](STATUS.md#team)) |

Rule of thumb: if you're stuck for 30 minutes, post the task number, what you tried and the exact error. Don't spend Bobcoins trying to work around a blocker.
