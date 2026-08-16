# Risk Register

> **Read this when:** designing a new component that touches risk, executing a phase transition, or doing the monthly review.
> **Review cadence:** Monthly minimum. Update after any near-miss or actual incident.

---

## Critical Risks (could end the project or lose meaningful money)

| # | Risk | Mitigation | Phase relevance |
|---|---|---|---|
| C1 | Catastrophic loss on single trade | Hard position size limits in config. Mandatory stop on every trade. Small allocation in Phase 3B autonomous test. | 3+ |
| C2 | Agent self-modifies risk controls | Risk config is read-only at runtime. Separate auth required for changes. | 2+ |
| C3 | Autonomous bug places unintended MCP order | Pre-flight checklist must pass. Order matches recommendation in logs. Quarterly audit of autonomous orders. | 3+ |
| C4 | API/broker outage during live trade | Bracket orders where supported. Kill switch available offline. Reconnect logic with backoff. | 3+ |
| C5 | IRA rule violation (non-eligible options) | Flag IRA-ineligible strategies before actionable advice. Never MCP trade IRA. | All |

---

## High Risks (would set the project back significantly)

| # | Risk | Mitigation | Phase relevance |
|---|---|---|---|
| H1 | Overfitting to small trade sample | Walk-forward analysis. Minimum n=30 for any playbook rule. Out-of-sample validation. | 2+ |
| H2 | Strategy decay (worked then, doesn't now) | Rolling performance windows. Auto-pause rules with declining edge. Quarterly regime check. | 2+ |
| H3 | Runaway API costs from agent loop | Hard $40/mo cap. Daily cost report. Max retries on every API call. Cost ledger per call. | All |
| H4 | LLM hallucinated rationale | Structured tool outputs over freeform reasoning. Require data citations. Human review of recommendations. | All |
| H5 | Data provider rate limit kills daily job | Caching layer. Fallback sources (Yahoo → FMP). Graceful degradation. | All |
| H6 | Auto-PR pipeline merges bad changes | Branch protection on main. Required PR review. No auto-merge. | 2+ |
| H7 | Buying paid tools without ROI validation | Subscription decision framework in `cost-discipline.md`. Pre-committed cancel triggers. | All |

---

## Medium Risks (operationally annoying, recoverable)

| # | Risk | Mitigation | Phase relevance |
|---|---|---|---|
| M1 | Local Ollama produces garbage outputs | Spot-check 10% of outputs. Route to Sonnet on uncertainty. Don't use for high-stakes tasks. | All |
| M2 | Trade journal data loss | Daily encrypted backup. Git commit state files where appropriate. | All |
| M3 | Burnout from over-scoping | Phase exit criteria are non-negotiable. Strict scope per phase doc. Time-boxed work weeks. | All |
| M4 | Skill quality degradation from auto-improvements | Dual-axis reviewer scoring. Rollback on score drop. Manual review of every PR. | 2+ |
| M5 | Robinhood MCP auth expiry mid-session | Re-auth flow documented. Health check before trade sessions. Alert on failure. | 1+ |
| M6 | DST transitions break time-of-day logic | Use ET timezone-aware datetimes everywhere. Test cases include DST switch days. | All |

---

## Personal Risks (about you, not the system)

| # | Risk | Mitigation |
|---|---|---|
| P1 | Trading addiction / overtrading | Playbook max trades/day + Phase 2 lightweight process flags (confluence missing, ignored invalidation). Optional later script. Daily trade limit. Mandatory cooldowns. |
| P2 | Loss-chasing / revenge trading | Pattern detector flags revenge trades. 30-min mandatory cooldown after 2 losses. |
| P3 | Funding the project beyond budget | Hard $100/mo project ceiling. No drawing on personal capital for tools. |
| P4 | College workload conflict | Phase docs are calendar-flexible. Pause autonomous mode during exam weeks. |
| P5 | Treating this as primary income too soon | Robinhood account is small; don't reduce other income sources based on early wins. |
| P6 | Confirmation bias from AI agreement | Explicitly seek disconfirming evidence. Use `strategy-reviewer` for second opinions. |

---

## Regulatory / Compliance Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | Personal liability for any execution by agent | All accounts in user's name. User is legally responsible for every trade regardless of who placed it. Document this in `decisions.md`. |
| R2 | IRA contribution limits and drawdown | IRA capital not easily replenished. Size for max loss; defined-risk structures where possible. |
| R3 | International compliance (if traveling abroad) | Don't trade autonomously while outside the US — broker T&Cs may require US presence. |

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

- Any unintended MCP order placement by the agent
- Catastrophic loss > 25% of Agentic account in a single day
- Any near-miss in a Critical risk category
- The kill switch fails when tested
- IRA-ineligible trade recommended as actionable for Portfolio B

Pausing means: revert to manual co-pilot mode, root-cause the incident, document in near-miss log, fix the underlying cause (with tests), then resume after 1 week of clean co-pilot operation.

**Pause is the default response. Resuming requires evidence the issue is fixed.**
