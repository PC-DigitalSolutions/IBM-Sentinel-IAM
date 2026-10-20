# Sentinel IAM: Research Evidence

*Team Bastion · Verified Oct 19, 2026 · Owner: Research & Documentation Lead*

Every number we use in the white paper, the written statement, the slides and the video must come from this file, with its source. If a number isn't here, don't use it. If you add one, add the source link and the date you checked it.

**Status of each figure:**
- ✅ **Verified:** checked against the publisher's own page or report
- 🟡 **Secondary:** reported consistently by reputable coverage, but the original PDF wasn't opened. Open the original before the final submission
- ⚠️ **Older or narrow:** real, but dated or from a small or vendor sample. Use it as supporting evidence only, never as the headline

---

## 1. The story in five numbers (use these first)

| # | Claim | Number | Source | Status |
|---|---|---|---|---|
| 1 | Analysts are too slow to reach the alert | **55 minutes** on average from alert to analyst pickup; **~75 minutes** for a thorough investigation; **over 2 hours** from alert to finished investigation | Prophet Security / ViB, *State of AI in the SOC 2026*, n=250, Aug 2026 | ✅ |
| 2 | Attackers move faster than that | Average eCrime **breakout time 29 minutes** in 2025; the fastest took **27 seconds** | CrowdStrike, *2026 Global Threat Report* | ✅ |
| 3 | Alerts get dropped | **~28%** of alerts are never investigated (average), and **60%** of teams say an ignored alert later turned out to matter | Prophet Security / ViB 2026 | ✅ |
| 4 | Breaches in banking are expensive | Financial-services breach averages **$6.3M** vs. a global average of **$4.99M** | IBM / Ponemon, *Cost of a Data Breach 2026*, 602 organizations, breaches Mar 2025 to Feb 2026 | ✅ (see note in §3) |
| 5 | Credentials are everywhere in breaches | Credential abuse appears in **39% of all breaches** at some point in the attack | Verizon, *2026 Data Breach Investigations Report*, 22,000+ confirmed breaches | 🟡 |

**The pitch line these support:** *An attacker using stolen credentials can break out in 29 minutes. The average analyst doesn't pick up the alert for 55. Sentinel closes that gap by doing the evidence-gathering in seconds and handing the analyst a ranked, approval-ready decision.*

---

## 2. ⚠️ Corrections: claims in our older docs that are now wrong or outdated

Fix these everywhere they appear (build spec, team docs, white paper, slides).

| Old claim in our docs | Problem | Use instead |
|---|---|---|
| "Stolen credentials are the **#1** way attackers get in" | True in the 2025 DBIR (22%), **no longer true** in the 2026 DBIR. Exploited vulnerabilities are now #1 at 31%; credential abuse fell to 13% as the *first* step (16% after a reclassification) | "Credential abuse appears in **39% of breaches**" (DBIR 2026), and "Adversaries aren't breaking in, they're logging in" (CrowdStrike 2026, valid-account abuse = 35% of cloud incidents) |
| "A financial-sector breach averages **$6.08M**" | That's the IBM **2024** figure. 2025 was $5.56M | **$6.3M** (IBM 2026) |
| "**960 alerts/day**, **40%** never investigated, **56 min** to first action, **70 min** to investigate" | Real (Prophet Security 2025 survey, ~300 respondents), but superseded by the 2026 edition | **55 min / ~75 min / ~28%** (Prophet 2026). Volume: median ~100 alerts/day; the largest environments pull the mean close to 1,000 |
| "Teams with extensive security AI resolve breaches **about 80 days faster**" | That's the IBM **2025** figure ($1.9M saved) | IBM 2026: **65 days faster** and **$1.93M** saved per breach; only **36%** of breached organizations use AI across prevention, detection, investigation and response 🟡 |
| "**86%** of practitioners won't let AI carry out even minor remediation without human oversight" | **No source found.** We could not trace this number to any survey. Do not use it | **0%** of SOC teams give AI full unsupervised autonomy; **44%** use AI that *recommends* while a human executes; **57%** require a human to review every AI verdict (Prophet 2026) |

---

## 3. Full evidence by topic

### 3.1 The analyst's time problem (why Sentinel exists)
| Finding | Source | Status |
|---|---|---|
| Average **55 min** from alert to analyst pickup (median 23 min); 60% say pickup takes more than 15 min | Prophet / ViB, State of AI in the SOC 2026 (n=250) | ✅ |
| Thorough investigation averages **~75 min** (median ~45); 64% report a mean time to investigate of 30+ min; **over 2 hours** from alert to completed investigation | Prophet / ViB 2026 | ✅ |
| **~28%** of alerts left uninvestigated (median 22%); 39% of teams leave 30%+ untouched | Prophet / ViB 2026 | ✅ |
| **60%** say an ignored alert later proved material; 34% had three or more such incidents in 12 months | Prophet / ViB 2026 | ✅ |
| Median org ~100 alerts/day; 74% receive 50+ per day, 27% receive 500+ per day | Prophet / ViB 2026 | ✅ |
| Prior year: 960 alerts/day average, 40% uninvestigated, 56 min before action, 70 min to investigate | Prophet Security, State of AI in SOC 2025 (~300 respondents), reported by The Hacker News, Sept 2025 | ⚠️ older edition |
| **71%** of SOC analysts report some level of burnout | Tines, *Voice of the SOC Analyst* (n=468), 2022 | ⚠️ older |

### 3.2 The attacker's speed (why minutes matter)
| Finding | Source | Status |
|---|---|---|
| Average eCrime breakout time **29 minutes** in 2025 (65% faster than the prior year); fastest **27 seconds** | CrowdStrike 2026 Global Threat Report | ✅ |
| Adversaries operate "through valid credentials, trusted identity flows"; **valid account abuse = 35% of cloud incidents** | CrowdStrike 2026 Global Threat Report | ✅ |

### 3.3 Credentials and account takeover (why we focus on suspicious logins)
| Finding | Source | Status |
|---|---|---|
| Credential abuse in **39% of breaches** at any point in the attack chain, the most pervasive technique | Verizon 2026 DBIR | 🟡 |
| As the *initial* vector: credential abuse 13% (16% before pretexting was split out); exploited vulnerabilities 31% | Verizon 2026 DBIR | 🟡 |
| **50%** of ransomware victims had a credential or infostealer event in the 95 days before the attack | Verizon 2026 DBIR | 🟡 |
| 2025 DBIR: credential abuse was the top initial vector (22%); **88%** of basic web-application attacks used stolen credentials | Verizon 2025 DBIR | 🟡 older edition |
| Account takeover was the **costliest fraud type** in 2025: **$15B+** in losses, about **6 million** US victims (up 18% from 5.1M), **17 hours** on average for a victim to resolve | Javelin Strategy & Research, Identity Fraud Study (Apr 2026, 2025 data) | 🟡 |
| FBI IC3 flagged account takeover as a growing threat for the first time: about **4,700 complaints** and **$359.7M** in losses in 2025. Attackers posed as bank staff to get **login credentials and MFA codes**, then moved funds out fast | FBI IC3 2025 Internet Crime Report (via SpyCloud and Expert Insights coverage) | 🟡 |

### 3.4 The cost of getting it wrong (why banks care)
| Finding | Source | Status |
|---|---|---|
| Global average breach cost **$4.99M**, a record, up 12% | IBM / Ponemon, Cost of a Data Breach 2026 | ✅ |
| Financial-services breach average **$6.3M** (2025 edition: $5.56M) | IBM 2026 press release | ✅ *Note: one summary attributes $6.29M to AI-driven breaches in finance specifically. Confirm the wording in the full report before final use* |
| Organizations using security AI and automation cut breach costs by **almost $2M** | IBM 2026 press release | ✅ |
| Extensive security AI shortened the breach timeline by **65 days**, saved **$1.93M**; only **36%** use it across the full lifecycle | IBM 2026 (via Varonis summary) | 🟡 |
| Financial services and energy identify and contain breaches about four weeks faster than average | IBM 2026 (via Varonis summary) | 🟡 |

### 3.5 Why step-up MFA is a strong recommendation
| Finding | Source | Status |
|---|---|---|
| MFA reduces the risk of account compromise by **99.22%** overall, and by **98.56%** even when the credentials were already leaked | Microsoft Research, Meyer et al., *How effective is multifactor authentication at deterring cyberattacks?* (arXiv 2305.00945, 2023) | ✅ |
| But attackers now social-engineer MFA codes (FBI IC3 2025 account-takeover alert). That's why Sentinel ranks **revoke session** above step-up MFA when the evidence shows active compromise | FBI IC3 2025 | 🟡 |

### 3.6 Why human approval (recommend-then-approve) is the right design
| Finding | Source | Status |
|---|---|---|
| **0%** of SOC teams using AI grant it full unsupervised autonomy | Prophet / ViB 2026 | ✅ |
| **44%** run AI that recommends while a human executes, the most common model and exactly Sentinel's design | Prophet / ViB 2026 | ✅ |
| **57%** require a human to review every AI verdict | Prophet / ViB 2026 | ✅ |
| **41%** cite lack of explainability as a barrier to AI adoption, which is why Sentinel explains every tool call and every ranked option | Prophet / ViB 2026 | ✅ |
| **9 in 10** security leaders need to see how AI reaches its decisions before trusting it | Torq / Sapio Research, 2026 AI SOC Leadership Report (450+ leaders) | 🟡 |
| **72%** of AI users cut investigation time by 25% or more (about one-third on average) | Prophet / ViB 2026 | ✅ |

---

## 4. What we still need (primary research)

Everything above is **secondary** research: real, published, and current, but not from our own users. Judges and the coach will also ask what *real analysts* told us. We still need:

1. **3 to 5 analyst conversations** (guide: `analyst-interview-guide.md`). Even 2 before the Oct 25 checkpoint changes the story.
2. **Our own timing:** manual triage of scenario A vs. Sentinel on the same alert (`docs/testing/timing-protocol.md`). Report it as "in our test."
3. **The cost of a wrongful customer lockout:** no solid public figure found. Ask analysts about it, and don't invent one.

---

## 5. Rules for using these numbers

- Always name the source in the same sentence or on the same slide ("IBM, 2026").
- Use the **2026** figures. Use older editions only when labeled as such.
- Industry averages are not our results. Our own measurements are labeled "in our test."
- Don't round in our favor (55 minutes is "55 minutes," not "an hour").
- Before Nov 22, open the original report for every 🟡 item and upgrade it to ✅, or drop it.

---

## 6. Sources

- Prophet Security / ViB, *State of AI in the SOC 2026* (Aug 3, 2026): https://www.prophetsecurity.ai/blog/state-of-ai-in-the-soc-2026
- Prophet Security, *State of AI in SOC 2025*, as reported by The Hacker News (Sept 2025): https://thehackernews.com/2025/09/the-state-of-ai-in-soc-2025-insights.html
- CrowdStrike, *2026 Global Threat Report*: https://www.crowdstrike.com/global-threat-report/ (saved copy: `C:\CyberLab\CrowdStrike 2026 Global Threat Report.html`)
- IBM, *Cost of a Data Breach 2026* press release (Jul 29, 2026): https://newsroom.ibm.com/2026-07-29-ibm-study-one-in-four-malicious-breaches-are-ai-enabled,-costing-companies-6-million-on-average
- Varonis summary of IBM 2026: https://www.varonis.com/blog/ibm-cost-of-a-data-breach-report-2026
- IBM, *Cost of a Data Breach 2025* (PDF via Baker Donelson): https://www.bakerdonelson.com/webfiles/Publications/20250822_Cost-of-a-Data-Breach-Report-2025.pdf
- Verizon, *2026 Data Breach Investigations Report*: https://www.verizon.com/business/resources/T343/reports/2026-dbir-data-breach-investigations-report.pdf
- Push Security review of the 2026 DBIR: https://pushsecurity.com/blog/verizon-dbir-2026-review
- Javelin Strategy & Research, Identity Fraud Study (Apr 2026): https://javelinstrategy.com/node/35385
- FBI IC3 2025 report coverage: https://spycloud.com/blog/fbi-internet-crime-report-2025/ and https://expertinsights.com/news/262-million-lost-to-account-takeover-fraud-in-2025
- Microsoft Research, MFA effectiveness (arXiv 2305.00945): https://arxiv.org/abs/2305.00945
- Torq, *2026 AI SOC Leadership Report*: https://torq.io/blog/ai-soc-leadership-report/
- Tines, *Voice of the SOC Analyst* (2022): https://tines.com/reports/voice-of-the-soc-analyst
