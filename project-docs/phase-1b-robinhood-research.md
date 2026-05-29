# Phase 1B — Robinhood Research + Co-Pilot Trading

**Duration:** 4–6 weeks (starts 2026-05-28)
**Goal:** Reliable daily research → thesis → co-pilot execution on Robinhood Agentic; close remaining Phase 1 exit gaps without building futures skills.

**Prerequisites:** Phase 1 audit largely complete ([STATUS.md](STATUS.md), [skills_audit.md](audit/skills_audit.md)).

---

## Why this phase exists

Phase 1 proved the fork’s stock/options skills and Robinhood MCP hybrid. The **swing research pipeline** and **thesis logging** are not yet production-ready for live Agentic trades. **Futures skills** (old Phase 2) are deferred until this phase exits — see [decisions.md](../decisions.md) and [phase-2-futures-skills.md](phase-2-futures-skills.md).

Lucid eval continues **manually**; no `lucid-rules-engine`, `tradovate-integration`, or `/futures-setup` work in 1B.

---

## Workstreams (parallel)

### 1. Research pipeline

| Item | Target |
|------|--------|
| FMP Starter | Activate when budget approved; unblocks vcp/canslim/earnings batch screeners |
| Daily stack | `uv run python3 scripts/pre_market.py` every trading day (systemd `pre-market.timer`) |
| Exposure | Run `exposure-coach` weekly when upstream JSON saved |
| Deep / update | `/deep-research` or Cursor `deep-research` on watchlist; `/update-research` when report &gt;14d stale |
| Watchlist cadence | Weekly `commands/review-portfolio.md` — batch staleness + summary table |
| Macro calendar | `scripts/fred_calendar.py` (canonical; economic-calendar-fetcher remains blocked on free FMP) |

**Watchlist (`reports/research/`, latest report per ticker):**

| Ticker | Latest report | Stale (&gt;14d)? |
|--------|---------------|----------------|
| MRAM | 2026-05-27 | No |
| MU | 2026-05-27 | No |
| P | 2026-05-27 | No |
| FPS | 2026-05-13 | Yes |
| INO | 2026-05-10 | Yes |
| VECO | 2026-05-08 | Yes |

Maintain via weekly `commands/review-portfolio.md`. Counts toward 5+ exit include Phase 1 reports; **3 current**, 3 need update-research.

### 2. Thesis discipline

| Item | Target |
|------|--------|
| Trade count | 10+ logged across ≥2 types (stock, option; paper OK) |
| IRA | All open IRA positions in `trader-memory-core` via MCP `ingest-pending` + `log-positions` |
| Pending | Close/log expired: POWL, TSLA, PENG per PENDING_WORK |
| Rules | Never write `state/theses/` directly — `thesis_store.py` / thesis-manager only |

### 3. Robinhood co-pilot (Agentic only)

| Step | Action |
|------|--------|
| Read | All accounts: `robinhood_mcp.py` or skill `robinhood-portfolio-review` |
| Context | Same session: today’s `pre_market` + `exposure-coach` when sizing new risk |
| Size | `position-sizer` on Agentic buying power |
| Confirm | Present plan → **wait for user “confirm”** before any MCP order |
| Execute | MCP orders on **Portfolio C (Agentic) only** |
| Log | `log-positions` / thesis transition in same session |

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync stays on `robinhood_sync.py`.

### 4. Cost & hygiene

- Anthropic spend tracking toward Phase 1 exit (&lt;$20)
- Pre-commit clean on commit
- New subscriptions → [decisions.md](../decisions.md) first

---

## Per-trade checklist (co-pilot)

1. `robinhood-portfolio-review` (or CLI) — buying power, exposure
2. Today’s `pre_market` + exposure posture — new entry allowed?
3. `position-sizer` for Agentic account
4. Present: entry, stop, target, risk $, IRA N/A on Agentic
5. **Stop — user confirms**
6. MCP order on Agentic only
7. Log thesis + position same session

---

## Exit criteria (Phase 1B → revisit futures Phase 2)

Progress detail: [docs_sync_2026-05-28.md](../reports/docs_sync_2026-05-28.md).

- [ ] FMP Starter active; `vcp-screener` run on watchlist universe at least once
- [ ] 14 consecutive trading days: `pre_market.py` + posture log (**11/14** unique days as of 2026-05-28)
- [ ] 5+ deep-research or update-research reports on active watchlist (6 tickers; 3 stale — count includes Phase 1)
- [ ] 10+ trades logged across ≥2 types via `trader-memory-core`
- [ ] 3+ co-pilot trades on Agentic via MCP (user-confirmed each)
- [ ] IRA positions logged (MCP read + four questions)
- [ ] `reports/portfolio_review_*.md` for 2+ dates
- [ ] Phase 1 remaining exit items: spend cap, pre-commit clean

**Futures Phase 2 revisit (default):** Phase 1B exit **and** 20+ logged stock/options trades (user may override).

---

## Explicitly NOT in Phase 1B

- `lucid-rules-engine`, `futures-position-sizer`, `tradovate-integration`, `futures-pre-market-scan`, `futures-session-monitor`, `/futures-setup`
- Autonomous execution (Phase 5 gate)
- MCP trades on IRA or taxable
- Upstream `skills/<name>/` rewrites except fixes in [decisions.md](../decisions.md)

---

## References

- [robinhood-mcp-integration.md](reference/robinhood-mcp-integration.md)
- [playbook.md](playbook.md)
- [phase-1-audit.md](phase-1-audit.md)
- [PENDING_WORK.md](../PENDING_WORK.md)
