# Phase 1B Kickoff — 2026-05-28

## Decision recorded

- [x] [decisions.md](../decisions.md) — [2026-05-28] futures Phase 2 deferred; Phase 1B active
- [x] [phase-1b-robinhood-research.md](../project-docs/phase-1b-robinhood-research.md) created
- [x] Routers updated: PROJECT.md, STATUS.md, LOAD_GUIDE.md, PENDING_WORK.md, project-router.mdc
- [x] [phase-2-futures-skills.md](../project-docs/phase-2-futures-skills.md) DEFERRED banner

**Futures revisit (default):** Phase 1B exit **and** 20+ logged stock/options trades (user may override).

---

## Research pipeline status

| Component | Status | Next action |
|-----------|--------|-------------|
| FMP API key | Set in env | Activate **Starter** billing when ready |
| vcp-screener | Smoke OK (`--universe MRAM`, 3 calls) | Full S&P500 screen after Starter |
| economic-calendar | Blocked on FMP | Keep `fred_calendar.py` |
| pre_market.py | Ran 2026-05-28; breadth 42.4, CAUTIOUS 50% | Continue daily; timer **active** |
| pre-market.timer | systemd **active** | None |
| exposure-coach | Schema fixed | Weekly when JSON saved |
| Deep research (watchlist) | MRAM/MU/P **2026-05-27**; FPS **2026-05-13** (stale) | Full `/deep-research FPS` or update-research |
| review-portfolio cadence | Documented in PENDING_WORK | Weekly; flag &gt;14d stale |
| P2 gaps (wrappers) | Documented | FMP chain, log-positions manual, `--static-basket` |

**Pre-flight MCP:**

```text
accounts:  OK (3 accounts mapped)
positions: OK (TE @ taxable)
```

---

## Robinhood MCP status

| Account | Maps to | Read | Trade MCP | Logged in thesis_store |
|---------|---------|------|-----------|------------------------|
| ••••7016 Agentic | `robinhood_agentic` | Yes | Yes (confirm) | N/A — no open equity |
| ••••9309 taxable | `robinhood_taxable` | Yes | **No** | TE **pending** |
| ••••3854 Roth IRA | `ira_robinhood` | Yes | **No** | Partial (legacy theses; reconcile) |

**Portfolio review:** [portfolio_review_2026-05-28.md](portfolio_review_2026-05-28.md)

**ingest-pending (dry-run):** 1 position TE → `state/pending_ingest.json` when applied.

---

## Phase 1 / 1B exit checklist

| Criterion | Done? |
|-----------|-------|
| Phase 1B decision + doc | Yes |
| FMP Starter active | No (approved, not billed) |
| vcp on watchlist | Partial (MRAM smoke) |
| 14 days pre_market | ~13+ in posture_history |
| 5+ deep/update watchlist | ~6 tickers total; FPS stale |
| 10+ trades, ≥2 types | No |
| 3+ Agentic co-pilot trades | No |
| IRA fully logged | No |
| 2+ portfolio reviews | 1 (today) |
| Anthropic &lt; $20 | Open |
| Pre-commit clean | Open |

---

## Co-pilot bootstrap (Phase C)

Completed this session:

1. Portfolio review saved
2. `ingest-pending --dry-run` — TE ready to merge
3. Pre-market + position-sizer run

**Not executed (by design):** MCP order — requires your **confirm**.

### Proposed next actions (pick one)

**A — Log only (recommended today)**

1. Run: `uv run python3 scripts/robinhood_mcp.py ingest-pending`
2. Invoke skill **log-positions** for TE (four questions)
3. No trade

**B — Agentic trade (only after confirm)**

Example plan aligned with research (not recommended at current prices):

| Field | Value |
|-------|-------|
| Account | Agentic ••••7016 only |
| Ticker | MRAM |
| Direction | Long |
| Entry | ~$31 |
| Stop | $27.50 |
| Risk | 2% of ~$50 |
| Shares | **0** (position-sizer: insufficient capital for 2% risk) |

**Verdict:** No Agentic equity entry today — capital too small for MRAM stop width; research says wait for $24–27.

If you want a **small confirmed Agentic trade**, reply with: ticker, limit/market, shares, and **confirm**. I will then call MCP order tools on Agentic only and log to trader-memory-core in the same session.

---

## Deferred (futures)

- [phase-2-futures-skills.md](../project-docs/phase-2-futures-skills.md) — lucid-rules-engine, tradovate-integration, futures-setup
- **Revisit when:** Phase 1B exit + 20+ stock/options trades (default)

---

## Session commands reference

```bash
# Daily
uv run python3 scripts/pre_market.py

# MCP read
uv run python3 scripts/robinhood_mcp.py accounts
uv run python3 scripts/robinhood_mcp.py positions --all

# Log pipeline
uv run python3 scripts/robinhood_mcp.py ingest-pending
# then log-positions skill

# Research
# Cursor: "deep research on FPS" or follow commands/deep-research.md
```
