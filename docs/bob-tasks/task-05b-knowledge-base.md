# Task 05b: attach the response playbook to Sentinel as a knowledge base

**Owner:** Technical Lead (on your own Bob credits). **Run after:** Task 05 (agent imported) and once the Research & Documentation Lead marks the playbook ready for import.
**Decision (Aldo, Oct 15, 2026):** Sentinel gets one knowledge base, the bank IAM response playbook. It is **knowledge, not a tool**: the agent still has exactly 3 tools (`assess_login`, `get_live_threats`, `analyze_signal`).

**Read only:** `AGENTS.md`, `agents/sentinel.agent.yaml`, `docs/knowledge/sentinel-response-playbook.md`. Don't scan anything else.

## Build
1. Create `agents/sentinel-playbook.knowledge.yaml`, a knowledge-base definition for the installed ADK, with:
   - name `sentinel_response_playbook`
   - a description written for the agent: "Bank policy for suspicious-login response: risk levels, default responses, the 5-minute failure rule, special cases, analyst procedure and audit requirements."
   - one document: `docs/knowledge/sentinel-response-playbook.md`
   Check the YAML fields and the import command against `orchestrate knowledge-bases --help` on the installed version.
2. In `agents/sentinel.agent.yaml`, attach the knowledge base to the `sentinel` agent. **Do not add, remove or rename any tool.**
3. Import:
   ```
   orchestrate knowledge-bases import -f agents/sentinel-playbook.knowledge.yaml
   orchestrate agents import -f agents/sentinel.agent.yaml
   ```
   *UI alternative (Trial SaaS):* Build → Agents → `sentinel` → Knowledge → upload the playbook file.

## Done when
- `orchestrate agents list` (or the agent's page) shows `sentinel` with 3 tools and 1 knowledge base.
- In chat, scenario H gets a recommendation that names the playbook section it follows (section 6, conflicting signals) and still ends with "Awaiting your approval".
- Scenario A is unchanged: Critical 100, revoke + reset ranked first, nothing executed.

## Don't
Add a tool, change any threshold or response, or upload any other document. The playbook only restates settled rules; a playbook change goes through Aldo first (playbook section 9).

## After the session
Screenshot the Bob consumption summary into `bob_sessions/` and post the Slack status update. Then QA re-runs every scenario A to L (Task 06).
