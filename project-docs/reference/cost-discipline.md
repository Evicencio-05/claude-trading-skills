# Cost Discipline & Model Routing

> **Read this when:** considering a new paid subscription, evaluating Anthropic API spend, or deciding which model tier to use for a new skill.

---

## Monthly Budget

| Category | Target | Hard Cap |
|---|---|---|
| Cursor subscription | (user plan) | Use for code/tests/refactors — not synthesis |
| Anthropic API | $20 | $40 |
| Data sources | $0–30 | $30 |
| Reserve | $30 | — |
| **Total** | **$50** | **$100** |

---

## Anthropic Spend Controls

- **Hard cap:** $40/month via Anthropic console budget alert
- **Soft cap:** $20/month — review usage if exceeded
- **Daily monitoring:** every API call logged with token count + estimated cost
- **Cache aggressively:** same ticker, same day, same workflow = use cached report. Deep/update research: run [`scripts/research_preflight.py`](../../scripts/research_preflight.py) (PASS 0) and obey manifest `action=reuse` before re-running batch skills — see [`commands/deep-research.md`](../../commands/deep-research.md).
- **Batch overnight:** queue Sonnet jobs for off-peak processing where applicable

### Cost tracking pattern

Every skill that calls the Claude API should log to a shared cost ledger:

```python
# src/shared/cost_ledger.py
def log_api_call(
    skill: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    estimated_cost_usd: float,
) -> None: ...

def daily_spend_total() -> float: ...
def alert_if_over_threshold(threshold: float = 1.50) -> None: ...
```

Wire this into every skill that makes API calls. Set up a cron to email/notify if daily spend exceeds $1.50 (which projects to >$45/mo).

---

## Model Routing Rules

| Tier | Model | When to use | Approximate cost per call |
|---|---|---|---|
| **Heavy** | Claude Opus 4.7 | Final thesis synthesis, post-trade reviews on losing trades, weekly playbook reviews, edge-pipeline-orchestrator | $$$ |
| **Default** | Claude Sonnet 4.6 | Most existing skills, daily research workflows, structured extraction | $$ |
| **Bulk** | Claude Haiku 4.5 | High-volume classification (sentiment on 200 headlines), simple extraction tasks | $ |
| **Free** | Ollama (qwen2.5:7b) local | Optional: log parsing, anomaly detection, embedding pre-processing | $0 |

### When to use which (cost-conscious version)

**Use Opus for:**
- Final thesis synthesis (`/deep-research` last step)
- Post-trade reviews (especially losing trades — get the lesson right)
- Weekly playbook reviews
- `edge-pipeline-orchestrator` final synthesis
- Anything where a wrong answer costs money

**Use Sonnet for:**
- Default for most existing skills (they're tuned for Sonnet)
- `/intraday-options`
- Daily research and screening workflows
- Earnings transcript parsing
- Most everyday analysis

**Use Haiku for:**
- Headline sentiment classification at volume
- News categorization
- Simple structured extraction where 90% accuracy is acceptable

**Use Ollama (local) for:**
- Log parsing and anomaly detection
- Bulk embedding pre-processing (or use `sentence-transformers` directly)
- Prompt retro drafts, edge hints, distill suggestions, commit message drafts
- Anything where you can spot-check 10% of outputs and correct errors

**Implementation:** [local-model-integration.md](local-model-integration.md) — `scripts/local_llm_cli.py`, Cursor rule `.cursor/rules/local-model-routing.mdc`.

**NEVER use any LLM for:**
- Web scraping (use traditional tools — `httpx`, `BeautifulSoup`, or APIs)
- Math computations (use Python directly)
- Data fetching (use API clients)
- Code formatting (use `ruff`)
- Type checking (use `mypy`)

---

## Free Tools That Replace Paid Services

| If you'd consider paying for... | Use instead |
|---|---|
| Code formatting | `ruff` (free) |
| Type checking | `mypy` (free) |
| Embeddings API | `sentence-transformers` local (free) |
| News sentiment API | Ollama + qwen2.5 (free) or NewsAPI free tier |
| Charts/dashboards | `plotly`, `matplotlib`, `streamlit` (all free) |
| Vector DB | Chroma local (free) |
| Backtesting platform | `vectorbt` or `backtrader` (free) |
| Time-series DB | SQLite or DuckDB (free) |
| Task scheduling | `cron` or Python `schedule` (free) |
| Logging | `structlog` + local JSON (free) |

---

## Subscription Decision Framework

Before subscribing to ANY paid service, write the answer to all five questions in `decisions.md`:

1. **What specific use case requires this?** ("Curiosity" or "might be useful" = NO)
2. **Have I extracted what edge I can from free alternatives?**
3. **What's the monthly cost? Is it under 30% of my project budget?** (If not, stop here.)
4. **Could the use case realistically pay for the subscription within 2 months?**
5. **What is my pre-committed cancel trigger?** (e.g., "Cancel if I haven't used it 3x weekly after 6 weeks")

If you can't answer all five clearly, don't subscribe.

---

## Specific Tools: Subscribe vs. Defer

### FMP API
- **Verdict:** **Starter ($29/mo) active** as of 2026-05-31 — 300 API calls/minute; watchlist screening via `--universe`.
- **Premium ($69/mo):** Defer until full S&P 500 universe screening is justified and budget approved ([decisions.md](../../decisions.md) [2026-05-31]).
- Basic (free) tier is insufficient for this fork (legacy v3 blocked; stable API required).

### FINVIZ Elite ($40/mo)
- **Verdict:** Defer indefinitely.
- Public FINVIZ screener works for most skills.
- Only subscribe if a specific equity/options strategy needs Elite features (rare).

### Skylit ($99/mo)
- **Verdict:** Defer until Phase 2 decision gate.
- GEX/dark pool data most useful for equity options strategies.
- The decision gate is in `phase-2-learning-loop.md` section 2.8.

### Polygon.io ($30+/mo)
- **Verdict:** Defer until Phase 4+ if at all.
- Yahoo Finance + Alpaca free tier covers Phase 1-3 needs.
- Only subscribe if Yahoo's data gaps become a backtesting blocker.

### Unusual Whales ($50+/mo)
- **Verdict:** Defer indefinitely.
- Equity options flow value unproven at current scale.
- Don't subscribe based on YouTube hype.

### Alpaca Markets
- **Verdict:** Free tier indefinitely.
- Paper trading API is free.
- Optional for portfolio-manager skill; Robinhood MCP is primary for this fork.

---

## Cost Postmortem (run monthly)

Last day of every month:
1. Pull total Anthropic spend from console
2. Compare to soft cap ($20) and hard cap ($40)
3. If over soft cap: identify the top 3 spending skills/workflows
4. Decide: optimize prompts? Switch to cheaper tier? Reduce frequency?
5. Document changes in `decisions.md`

Track the trend. If spend is climbing month over month without commensurate value, something's wrong.
