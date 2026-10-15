# Sentinel IAM: Orchestrate Runbook (commands)

*For Technical Support / QA (Tasks 03, 03b, 04) and the Technical Lead (Task 05). Windows PowerShell. Prepared Oct 15, 2026.*

**Read first:**
- Bob writes the build files: `tools/sentinel-tools.openapi.yaml` (Task 04) and `agents/sentinel.agent.yaml` (Task 05). This runbook only runs and checks them.
- The ADK is not installed on Aldo's machine yet. Check every `orchestrate` command against `orchestrate <command> --help` on the installed version, because flags change between releases (AGENTS.md rule).
- Use only seed users and documentation-range IPs in every test call.

## 0. Pick the Orchestrate path
| Path | When | Backend URL Orchestrate uses |
|---|---|---|
| **A. Trial SaaS** (IBM Cloud → Resource list → AI / Machine Learning → "watsonx-Challenge Orchestrate" → Launch) | The program's provided instance, once the IBM Cloud access is active | A public tunnel URL (step 2) |
| **B. ADK Developer Edition** (local, runs in Docker) | Building and testing before SaaS access, or offline | `http://host.docker.internal:8000` |

## 1. Start the backend (both paths)
Run it in a real terminal window or detached. A backend hosted by a short-lived background job stops silently.
```powershell
cd C:\CyberLab\CyberShield_IV
.\.venv\Scripts\Activate.ps1
uvicorn src.api.main:app --port 8000
```
Check it in a second window:
```powershell
Invoke-RestMethod http://localhost:8000/status
Invoke-RestMethod -Method Post -Uri http://localhost:8000/iam/assess-login -ContentType 'application/json' -Body '{"user_id":"jdoe","ip":"203.0.113.66","device_id":"win-unknown-7f2","geo":"Lagos, NG","timestamp":"2026-10-02T03:14:00Z"}'
```
Expected: `risk_score` 100, `risk_level` Critical, all four flags. `analyze_signal` (`/analyze`) needs `CYBERSHIELD_API_KEY` in the backend `.env`. Never commit that file.

Run the unit tests:
```powershell
python -m pytest tests/test_assess_login.py -q
```

## 2. Path A only: expose the backend with a tunnel
```powershell
winget install --id Cloudflare.cloudflared
cloudflared tunnel --url http://localhost:8000
```
Copy the `https://….trycloudflare.com` URL into `servers:` in `tools/sentinel-tools.openapi.yaml`. **The URL changes every time the tunnel restarts**, so update the spec and re-import the tools after each restart. Stop the tunnel when you're not testing.

## 3. Install and connect the ADK
```powershell
python -m pip install --upgrade ibm-watsonx-orchestrate
orchestrate --help
```
**Path A (SaaS):** in the Orchestrate UI, open your profile settings and copy the service instance URL. Generate an API key and enter it when the CLI asks; never put it in the repo, Slack or a Bob prompt.
```powershell
orchestrate env add -n bastion-saas -u <SERVICE_INSTANCE_URL>
orchestrate env activate bastion-saas
```
**Path B (Developer Edition):** Docker Desktop must be running. The `.env` for the server holds your entitlement keys and stays out of git.
```powershell
orchestrate server start --env-file .env
orchestrate env activate local
```

## 4. Task 04: import the 3 tools
```powershell
cd "C:\CyberLab\IBM Experential ai\sentinel-iam"
orchestrate tools import -k openapi -f tools/sentinel-tools.openapi.yaml
orchestrate tools list
```
**Done when:** the list shows `assess_login`, `get_live_threats` and `analyze_signal`, and one test call to each succeeds from inside Orchestrate. Screenshot both for evidence.
*UI alternative (Path A):* Build → Tools → Add tool → OpenAPI → upload the same YAML.

## 5. Task 05: import the Sentinel agent
```powershell
orchestrate models list
orchestrate agents import -f agents/sentinel.agent.yaml
orchestrate agents list
```
Choose a model from `models list` that supports tool calling. The agent's instructions come from `agents/sentinel.instructions.md` (v2).
*UI alternative (Path A):* Build → Agents → Create agent → paste `sentinel.instructions.md` into Behavior → add the 3 tools.

## 6. Test in chat
- **Path A:** Orchestrate Chat → select `sentinel`.
- **Path B:** `orchestrate chat start`, then open the local chat UI it prints.

Paste scenario A as the first message:
```
Suspicious login alert: user_id jdoe, ip 203.0.113.66, device_id win-unknown-7f2, geo Lagos, NG, timestamp 2026-10-02T03:14:00Z
```
**Pass (Task 05):** Critical 100/100; revoke session + reset credential ranked first with reasons; the Learned / Unknown loop visible; "Awaiting your approval"; nothing described as executed. Then run every scenario A to L for Task 06 and log each run in `docs/testing/test-sheet.csv`.

## 7. After every Bob session
Screenshot the consumption summary into `bob_sessions/` (`<member>-task-<nn>-<date>.png`), commit with the task number in the message, and post the Slack status (Done / Next / Blocked / Bobcoins left).

## Troubleshooting
| Symptom | Check |
|---|---|
| Orchestrate can't reach a tool | Path A: is the tunnel running, and does the spec have the **current** URL? Path B: `host.docker.internal`, not `localhost` |
| `analyze_signal` errors | `CYBERSHIELD_API_KEY` set in the backend `.env`; backend restarted after setting it |
| `assess_login` returns 404 | The user ID isn't in the seed data (expected for scenario G) |
| A CLI flag is rejected | Check `orchestrate <command> --help` for the installed version |
