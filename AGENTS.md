# Sentinel IAM: Agent Context for Bob

Built for the IBM SkillsBuild AI Experiential Learning Lab (Fall 2026), Banking & Financial Services track, by Team Bastion. IBM Bob is the core build tool, and the agent runs on watsonx Orchestrate.

## Scope (read first)
**One agent. One problem. One solution.** (Coach direction, Sept 25 2026.) Do not add more agents.

- **Problem:** a bank SOC/IAM analyst needs about an hour to investigate one suspicious login by hand. Stolen credentials are the #1 initial access vector.
- **Solution:** **Sentinel**, a single agent. Given a suspicious-login alert, it chooses which tools to call, explains the risk in plain language, and presents recommendations ranked best to lowest, each with a reason. A human approves every action, and Sentinel never executes it.

## The agent: Sentinel
- Input: login alert `{user_id, ip, device_id, geo, timestamp}`
- Output: risk level (Low/Medium/High/Critical) + why + tools it called and why + ranked recommendations with a reason each + a request for approval
- Default action per level: Low → no action · Medium → step-up MFA · High → revoke session · Critical → revoke session + reset credential
- Goal-driven, not scripted: Sentinel chooses which tools to call and when it has enough evidence. There is no fixed tool order.
- Decisive: no hedging words ("probably", "most likely"). Sentinel states its conclusion and the reason.
- Authentication-failure policy: failures for the account are counted in a 5-minute window. 2 or more failures flags the case; Sentinel then investigates and has a ranked recommendation ready for the analyst. A flagged case with a Low score ranks step-up MFA first. Every action still needs approval.
- Instructions: `agents/sentinel.instructions.md`

## Tools (3 total)
The backend is the existing FastAPI service in `C:\CyberLab\CyberShield_IV` (run with `uvicorn src.api.main:app --port 8000`). Reuse it. Do not rebuild it.

| Tool | Endpoint | Status |
|---|---|---|
| `assess_login` | `POST /iam/assess-login` | **NEW**: built in Task 02; failure count added in Task 03b |
| `get_live_threats` | `GET /threats/live?limit=` | Existing |
| `analyze_signal` | `GET /analyze?signal=` | Existing (calls Gemini; needs `CYBERSHIELD_API_KEY`) |

Other existing endpoints (`/sentinel/chat`, `/analyze/file`, `/threats/history`) are **out of scope**. Don't wire them.

## Test data
- `tests/fixtures/iam_baselines.json`: user baselines, city coordinates, threat-listed IPs (RFC 5737 documentation IPs only, never real ones)
- `tests/scenarios.json`: scenarios A to G plus H and J, with expected flags, score, level and action. **This is the definition of done.** `expect.tools` is the typical path, not a required order.

## Conventions for Bob (credits are limited)
- One small task per session. Task prompts are in `docs/bob-tasks/`. Stop when the "Done when" condition is met.
- Only read the files a task names. Don't scan the whole backend.
- `assess_login` is **deterministic**: no LLM calls, no network, no database. It reads the JSON seed data.
- Never auto-execute a credential change. Responses are always recommend-then-approve.
- Don't commit secrets. `.env` stays gitignored.
- Session reports are graded: export each task's summary screenshot to `bob_sessions/`.
