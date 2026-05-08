# Risk Register

> **Read this when:** designing a new component that touches risk, executing a phase transition, or doing the monthly review.
> **Review cadence:** Monthly minimum. Update after any near-miss or actual incident.

---

## Critical Risks (could end the project or lose meaningful money)

| # | Risk | Mitigation | Phase relevance |
|---|---|---|---|
| C1 | Lucid rule violation kills account | Hard-coded constraints in `lucid-rules-engine`, separate from agent logic. Pre-trade check mandatory. | All |
| C2 | Catastrophic loss on single trade | Hard position size limits in rules engine. Mandatory stop on every trade. Max 1 contract in 5B. | 5+ |
| C3 | Agent self-modifies risk controls | `rules.py` is read-only at runtime. Mtime check on startup. Separate auth required for changes. | 2+ |
| C4 | Autonomous bug places unintended order | Pre-flight checklist must pass. Order matches recommendation in logs. Quarterly audit of all autonomous orders. | 5+ |
| C5 | API outage during live trade | Server-side bracket orders (broker holds the stop). Kill switch available offline. Reconnect logic with backoff. | 5+ |
| C6 | Lucid platform issue (their auto-flatten fails) | Agent force-flatten at 4:35 PM ET. 10-min buffer before Lucid's 4:45. Daily reconciliation. | 5+ |

---

## High Risks (would set the project back significantly)

| # | Risk | Mitigation | Phase relevance |
|---|---|---|---|
| H1 | Overfitting to small trade sample | Walk-forward analysis. Minimum n=30 for any playbook rule. Out-of-sample validation. | 3+ |
| H2 | Strategy decay (worked then, doesn't now) | Rolling performance windows. Auto-pause rules with declining edge. Quarterly regime check. | 4+ |
| H3 | Runaway API costs from agent loop | Hard $40/mo cap. Daily cost report. Max retries on every API call. Cost ledger per call. | All |
| H4 | LLM hallucinated rationale | Structured tool outputs over freeform reasoning. Require data citations. Human review of recommendations. | All |
| H5 | Data provider rate limit kills daily job | Caching layer. Fallback sources (Yahoo → FMP → Alpaca). Graceful degradation. | All |
| H6 | Auto-PR pipeline merges bad changes | Branch protection on main. Required PR review. No auto-merge. | 3+ |
| H7 | Buying paid tools without ROI validation | Subscription decision framework in `cost-discipline.md`. Pre-committed cancel triggers. | All |

---

## Medium Risks (operationally annoying, recoverable)

| # | Risk | Mitigation | Phase relevance |
|---|---|---|---|
| M1 | Local Ollama produces garbage outputs | Spot-check 10% of outputs. Route to Sonnet on uncertainty. Don't use for high-stakes tasks. | All |
| M2 | Trade journal data loss | Daily encrypted backup. Git commit state files where appropriate. | All |
| M3 | Burnout from over-scoping | Phase exit criteria are non-negotiable. Strict scope per phase doc. Time-boxed work weeks. | All |
| M4 | Skill quality degradation from auto-improvements | Dual-axis reviewer scoring. Rollback on score drop. Manual review of every PR. | 3+ |
| M5 | Tradovate auth expiry mid-trade | Auto-refresh on 401. Health check every 15 min during market hours. Alert on failure. | 2+ |
| M6 | DST transitions break time-of-day logic | Use ET timezone-aware datetimes everywhere. Test cases include DST switch days. | 2+ |
| M7 | Holiday-shortened CME sessions confuse rules | Hard-coded CME holiday calendar. Tested with last 3 years of holidays. | 2+ |

---

## Personal Risks (about you, not the system)

| # | Risk | Mitigation |
|---|---|---|
| P1 | Trading addiction / overtrading | `behavioral-pattern-detector` flags overtrading. Daily trade limit. Mandatory cooldowns. |
| P2 | Loss-chasing / revenge trading | Pattern detector flags revenge trades. 30-min mandatory cooldown after 2 losses. |
| P3 | Funding the project beyond budget | Hard $100/mo project ceiling. No drawing on personal capital for tools. |
| P4 | College workload conflict | Phase docs are calendar-flexible. Pause autonomous mode during exam weeks. |
| P5 | Treating this as primary income too soon | Prop firm income is uncertain. Don't reduce other income sources based on prop performance. |
| P6 | Confirmation bias from AI agreement | Explicitly seek disconfirming evidence. Use `strategy-reviewer` (existing skill) for second opinions. |

---

## Regulatory / Compliance Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | Lucid is a young firm (launched 2025) — could shut down | Don't concentrate all eval/funded accounts at one firm long-term. After Phase 5C, consider parallel evaluation at TopStep or Apex. |
| R2 | IRS treatment of prop firm income (1099-MISC vs. trader status) | Consult tax professional before first $10K in payouts. Track every payout, every fee. |
| R3 | Personal liability for any execution by agent | All accounts in user's name. User is legally responsible for every trade regardless of who placed it. Document this in `decisions.md`. |
| R4 | International compliance (if traveling abroad) | Don't trade autonomously while outside the US — broker T&Cs may require US presence. |

---

## Near-Miss Log

Document every situation where a risk was nearly realized but mitigated. This is more valuable than the risk register itself because it's evidence-based.

Format:
```
## YYYY-MM-DD: <Brief description>

- **Risk category:** <C/H/M/P/R##>
- **What almost happened:**
- **What prevented it:**
- **What changed in the system as a result:**
- **Tests added (if any):**
```

---

## Monthly Review Checklist

Last day of every month:

- [ ] Read every Critical risk — is the mitigation still in place and working?
- [ ] Review near-miss log entries from the last 30 days
- [ ] Check `decisions.md` for new decisions that might add or remove risks
- [ ] Update phase relevance for any risk based on current phase
- [ ] Identify any new risks discovered during the month
- [ ] Document the review in `decisions.md`: `[YYYY-MM-DD] Risk register monthly review: <summary>`

---

## Risk Threshold for Pausing the Project

**Pause autonomous operation immediately if any of these occur:**

- Any Lucid rule violation (intentional or not)
- Any unintended order placement by the agent
- Catastrophic loss > 25% of any account in a single day
- Any near-miss in a Critical risk category
- The kill switch fails when tested

Pausing means: revert to manual co-pilot mode, root-cause the incident, document in near-miss log, fix the underlying cause (with tests), then resume after 1 week of clean co-pilot operation.

**Pause is the default response. Resuming requires evidence the issue is fixed.**
