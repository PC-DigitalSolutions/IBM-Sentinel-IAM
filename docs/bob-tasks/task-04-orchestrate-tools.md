# Task 04: expose the 3 tools to watsonx Orchestrate

**Read only:** `AGENTS.md` and the three route definitions in `CyberShield_IV/src/api/main.py` (`/iam/assess-login`, `/threats/live`, `/analyze`).

## Build
1. Write `sentinel-iam/tools/sentinel-tools.openapi.yaml` (OpenAPI 3.0) with exactly 3 operations: `assess_login`, `get_live_threats`, `analyze_signal`. Give each one a clear description written for the agent. Put the server URL in `servers: - url: <BACKEND_URL>`.
2. Decide how Orchestrate reaches the backend:
   - **Local ADK / Developer Edition** (for build and testing): `http://host.docker.internal:8000`
   - **Orchestrate SaaS** (after the IBM Cloud access lands): a public tunnel, e.g. `cloudflared tunnel --url http://localhost:8000`, then use that https URL. Note in `tools/README.md` that the URL changes on every restart.
3. Import: `orchestrate tools import -k openapi -f tools/sentinel-tools.openapi.yaml` (check the flags against the installed ADK's `--help`).

## Done when
`orchestrate tools list` shows all 3 tools, and a manual test call of `assess_login` with scenario A returns 100/Critical.
