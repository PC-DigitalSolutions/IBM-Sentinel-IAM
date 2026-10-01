# Task 03: re-point the live threat feed to banking

**Repo:** `C:\CyberLab\CyberShield_IV`. **Read only:** `src/core/live_monitor.py` (the `QUERIES` list near the top and the docstring).

## Build
Replace the `QUERIES` list with banking and identity search terms, keeping the interleaved-domain pattern the comments describe. Use these 14 terms:
`"bank account takeover"`, `"credential stuffing attack"`, `"banking phishing campaign"`, `"MFA fatigue attack"`, `"stolen credentials dark web bank"`, `"session hijacking"`, `"bank data breach"`, `"SIM swap fraud bank"`, `"infostealer malware credentials"`, `"business email compromise wire fraud"`, `"banking trojan"`, `"deepfake bank fraud"`, `"password spraying"`, `"financial sector ransomware"`.
Update the module docstring and comments so they say banking/IAM instead of concert/event. Don't change any logic.

## Done when
The backend starts and `GET /threats/live?limit=10` returns banking/identity headlines after the first poll.
