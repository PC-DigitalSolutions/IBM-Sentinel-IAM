# Team docs (Team Bastion)

> **Update, Oct 15, 2026 (Aldo):** the authentication-failure rule changed after these docs were exported. The rule is now **2 failed attempts within 5 minutes flags the case**; Sentinel then investigates and has a ranked recommendation ready, and a flagged case with a Low score ranks step-up MFA first. The 15-minute window and the 4+ tier described below are retired. The failure count lives inside `assess_login` (Task 03b). Where these docs differ, `docs/build-spec.md` and `agents/sentinel.instructions.md` are current.

Exported from the team's Claude docs on Oct 15, 2026. All docs reflect the 5-member team. Read in this order:

1. `team-handoff.md` - project summary, settled design decisions, roster and roles
2. `current-build-and-status.md` - architecture, `assess_login` contract, test scenarios, status, who does what
3. `team-playbook.md` - how each role does its tasks, evidence, handoffs, checkpoints

Roles: Team Lead (Aldo), Technical Lead, Technical Support / QA, Research & Documentation Lead, Communications & Demo Lead.
