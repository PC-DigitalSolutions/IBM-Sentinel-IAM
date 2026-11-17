# Sentinel IAM — Tool Registration

## Import command

```bash
orchestrate tools import -k openapi -f tools/sentinel-tools.openapi.yaml
```

Check all available flags with:

```bash
orchestrate tools import --help
```

## Default server

`https://cybershield-iv.onrender.com`

This is a free-tier Render deployment. **The service sleeps when idle; the first call after a sleep period can take up to a minute.** If the call times out, retry once before investigating further.

## Fallback servers

| Scenario | URL to use |
|---|---|
| Local ADK (Docker) | `http://host.docker.internal:8000` |
| SaaS Orchestrate + local backend via tunnel | The cloudflared tunnel URL (changes on every restart — update `servers` in the YAML and re-import) |

**Never use `localhost:8000`** — it resolves to the container itself, not the host machine.

To switch servers, edit the `servers.url` value in `tools/sentinel-tools.openapi.yaml` and re-run the import command.

## API key requirement

`analyze_signal` (`GET /analyze`) calls Gemini on the backend. The environment variable `CYBERSHIELD_API_KEY` must be set on the backend process before this tool will return results.
