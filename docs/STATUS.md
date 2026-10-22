# Project status

**Last updated:** Oct 21, 2026 · **Updated by:** _(your name)_

This is the one place to check what's done and what's next. **When you finish, start or get blocked on something, update this file in the same commit.** Older status docs in `docs/team/` are history; this file replaces them.

---

## Team

Fill in your name when you claim a role.

| Role | Name | Slack handle |
|---|---|---|
| Team Lead / Advisor | Aldo | |
| Technical Lead | | |
| Technical Support / QA | | |
| Research & Documentation Lead | | |
| Communications & Demo Lead | | |

---

## Build tasks

Each task has a prompt file in [bob-tasks/](bob-tasks/). Do them in order: later tasks depend on earlier ones.

| # | Task | Repo | Owner | Target | Status | Evidence |
|---|---|---|---|---|---|---|
| 01 | Repo scaffold + `AGENTS.md` | this | Aldo | Sep 30 | ✅ Done | Commit history |
| 02 | `POST /iam/assess-login` + tests | CyberShield_IV | Aldo | Oct 3 | ✅ Done (6/6 tests, live on Render) | `bob_sessions/aldo-task-02-2026-10-03.png` |
| — | Local prototype `sentinel_iam/` | this | Aldo | Oct 4 | ✅ Done (21/21 tests) | `bob_sessions/aldo-task-02-prototype-2026-10-04.png` |
| 03 | Re-point threat feed to banking | CyberShield_IV | QA | Oct 21 | ⬜ To do | |
| 03b | 5-minute failure flag in `assess_login` (backend **and** prototype) | both | QA | Oct 22 | ⬜ To do | |
| 04 | OpenAPI spec + import 3 tools into Orchestrate | this | QA | Oct 23 | ⬜ To do. **Blocks 05** | |
| 05 | Sentinel agent in Orchestrate | this | Tech Lead | Oct 27 | ⬜ To do | |
| — | Audit log record format | this | Tech Lead | Oct 29 | ⬜ To do | |
| 05b | Attach response playbook as knowledge base | this | Tech Lead | Oct 29 | ⬜ To do | |
| 06 | Run scenarios A–L, fix, tag `v1-tested` | this | QA | **Nov 1** | ⬜ To do | `docs/testing/test-sheet.csv` |
| — | Baseline timing: manual vs Sentinel | — | QA | Nov 4 | ⬜ To do | `docs/testing/timing-protocol.md` |

Status key: ⬜ To do · 🟦 In progress · ⛔ Blocked · ✅ Done

---

## Deliverables

| Deliverable | Owner | Draft | Final | Status |
|---|---|---|---|---|
| Demo script | Comms | Oct 23 | | ⬜ |
| Oct 25 checkpoint deck | Comms | Oct 24 | Oct 25 | ⬜ |
| 3–5 analyst interviews | Research | Oct 21 start | Nov 1 | ⬜ |
| Persona + as-is journey (updated with interviews) | Research | | Nov 3 | ⬜ |
| White paper / procedure manual | Research | Nov 8 | Nov 20 | ⬜ |
| Technology statement | Research + Tech Lead | Nov 8 | Nov 20 | ⬜ |
| Written problem + solution + prototype link | Research | Nov 8 | Nov 20 | ⬜ |
| 3-minute video (record only after `v1-tested`) | Comms | Nov 8 | Nov 20 | ⬜ |
| `bob_sessions/` screenshots from **every** member | Everyone (QA checks) | ongoing | Nov 21 | 🟦 Aldo's done; 4 members to go |

---

## Everyone's program requirements

| Member | 6 SkillsBuild courses + W6 deliverable (due Oct 25) | At least 1 Bob session exported |
|---|---|---|
| Aldo | 🟦 | ✅ |
| | ⬜ | ⬜ |
| | ⬜ | ⬜ |
| | ⬜ | ⬜ |
| | ⬜ | ⬜ |

---

## Timeline

| Date | Milestone |
|---|---|
| Oct 20 | Roles claimed |
| Oct 23 | 3 tools live in Orchestrate (Task 04) |
| **Oct 25** | **Mid-program checkpoint**: demo the Orchestrate agent if ready, otherwise the prototype (labeled as such). All courses + W6 deliverable due |
| Oct 27 | Agent handles scenario A end to end (Task 05) |
| **Nov 1** | All scenarios pass, tag `v1-tested`. Interviews done |
| Nov 4 | Timing numbers in. Career Fair (TBC) |
| **Nov 8** | **Agent frozen.** All drafts done |
| Nov 21 | Final checklist review, Aldo signs off |
| **Nov 22** | **Submission** |

---

## Known issues

| Issue | Where | Fix in |
|---|---|---|
| Prototype uses retired 15-minute / 4-failure rule | `sentinel_iam/tools/assess_login.py` | Task 03b |
| Prototype ranks "Block session" above step-up MFA for Medium | same file | Task 03b |
| Plain `pytest` fails if a stray nested copy of the repo exists locally; use `pytest tests` | local folders | Delete the stray copy |
| Older team docs mention 4 agents, 3 members, 15-minute window | `docs/sentinel-iam-knowledge.md`, `docs/team/*` | Marked historical in [docs/README.md](README.md) |
| No primary research yet (no analyst interviews) | — | Research Lead |
| "60 min → under 1 min" not yet measured by us | — | Baseline timing |

---

## Open decisions

None right now. Add a row when something needs Aldo's sign-off (thresholds, actions, tool contracts, guardrails).

| Date raised | Question | Raised by | Decision | Decided on |
|---|---|---|---|---|
