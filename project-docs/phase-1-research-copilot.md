# Phase 1 — Research + Co-Pilot Trading

**Duration:** 4–6 weeks (active from 2026-05-29)
**Goal:** Reliable daily research → thesis → co-pilot execution on Robinhood Agentic; production-ready swing pipeline and thesis logging.

**Operator cadence:** [trading-pipeline-checklist.md](trading-pipeline-checklist.md) — daily, weekly, research, and per-trade steps.

**Prerequisites:** Phase 1 audit complete ([STATUS.md](STATUS.md), [skills_audit.md](audit/skills_audit.md)).

---

## Why this phase exists

The fork's stock/options skills and Robinhood MCP hybrid are built. The **swing research pipeline** and **thesis logging** are not yet production-ready for live Agentic trades. This phase closes that gap before advancing to the learning loop.

---

## Workstreams (parallel)

### 1. Research pipeline

| Item | Target |
|------|--------|
| FMP Starter | **Active** 2026-05-31 — watchlist vcp/canslim/earnings via `--universe`; full S&P 500 needs Professional ($79/mo) |
| Daily batch → PASS 0 | Run watchlist screeners once/day; per-ticker deep/update research reuses via [`scripts/research_preflight.py`](../../scripts/research_preflight.py) ([`commands/deep-research.md`](../../commands/deep-research.md) PASS 0) |
| Operator cadence | See checklist § [Daily](trading-pipeline-checklist.md#daily-trading-days), § [Weekly](trading-pipeline-checklist.md#weekly), § [Research](trading-pipeline-checklist.md#research-on-demand) |

**Watchlist state:** [config/research_watchlist.yaml](../config/research_watchlist.yaml) · [config/research_exclude.yaml](../config/research_exclude.yaml) · staleness in [STATUS.md](STATUS.md) or latest `reports/logs/research_staleness_*.md`

### 2. Thesis discipline

| Item | Target |
|------|--------|
| Trade count | 10+ logged across ≥2 types (stock, option; paper OK) |
| IRA | All open IRA positions in `trader-memory-core` via MCP `ingest-pending` + `log-positions` |
| Pending | Close/log expired: TSLA, PENG (POWL closed 2026-05-29) |
| Rules | Never write `state/theses/` directly — `thesis_store.py` / thesis-manager only |

### 3. Robinhood co-pilot (Agentic only)

See checklist § [Per-trade co-pilot](trading-pipeline-checklist.md#per-trade-co-pilot-agentic-only).

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync stays on `robinhood_sync.py`.

### 4. Cost & hygiene

- Anthropic spend tracking toward exit (&lt;$20)
- Pre-commit clean on commit
- New subscriptions → [decisions.md](../decisions.md) first

---

## Exit criteria (Phase 1 → Phase 2)

Progress detail: [docs_sync_2026-05-30.md](../reports/docs_sync_2026-05-30.md).

- [x] FMP Starter active; `vcp-screener` run on watchlist universe at least once (11 quotes, 2026-05-31)
- [ ] 14 consecutive trading days: `pre_market.py` + posture log (**12/14** unique days as of 2026-05-30)
- [x] 5+ deep-research or update-research reports on active watchlist (5 tickers on disk; 2 stale need update)
- [ ] 10+ trades logged across ≥2 types via `trader-memory-core`
- [ ] 3+ co-pilot trades on Agentic via MCP (user-confirmed each)
- [ ] IRA positions logged (MCP read + four questions)
- [ ] `reports/portfolio_review_*.md` for 2+ dates
- [ ] Anthropic spend cap met; pre-commit clean

---

## Explicitly NOT in Phase 1

- Autonomous MCP order placement (Phase 3 gate)
- MCP trades on IRA or taxable
- Upstream `skills/<name>/` rewrites except fixes in [decisions.md](../decisions.md)

---

## References

- [trading-pipeline-checklist.md](trading-pipeline-checklist.md)
- [robinhood-mcp-integration.md](reference/robinhood-mcp-integration.md)
- [playbook.md](playbook.md)
- [PENDING_WORK.md](../PENDING_WORK.md)

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 2. Read [phase-2-learning-loop.md](phase-2-learning-loop.md).
