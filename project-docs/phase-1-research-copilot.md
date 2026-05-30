# Phase 1 — Research + Co-Pilot Trading

**Duration:** 4–6 weeks (active from 2026-05-29)
**Goal:** Reliable daily research → thesis → co-pilot execution on Robinhood Agentic; production-ready swing pipeline and thesis logging.

**Prerequisites:** Phase 1 audit complete ([STATUS.md](STATUS.md), [skills_audit.md](audit/skills_audit.md)).

---

## Why this phase exists

The fork's stock/options skills and Robinhood MCP hybrid are built. The **swing research pipeline** and **thesis logging** are not yet production-ready for live Agentic trades. This phase closes that gap before advancing to the learning loop.

---

## Workstreams (parallel)

### 1. Research pipeline

| Item | Target |
|------|--------|
| FMP Starter | Activate when budget approved; unblocks vcp/canslim/earnings batch screeners |
| Daily stack | `uv run python3 scripts/pre_market.py` every trading day (systemd `pre-market.timer`) |
| Exposure | Run `exposure-coach` weekly when upstream JSON saved |
| Deep / update | `/deep-research` or Cursor `deep-research` on watchlist; `/update-research` when report &gt;14d stale |
| Watchlist cadence | Weekly `scripts/update_stale_research.py` (systemd `research-staleness.timer`) → queue + summary; LLM via `update-research` |
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

Maintain via weekly `update_stale_research.py` (timer or `--dry-run`). Watchlist YAML: `config/research_watchlist.yaml`.

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
| Context | Same session: today's `pre_market` + `exposure-coach` when sizing new risk |
| Size | `position-sizer` on Agentic buying power |
| Confirm | Present plan → **wait for user "confirm"** before any MCP order |
| Execute | MCP orders on **Portfolio C (Agentic) only** |
| Log | `log-positions` / thesis transition in same session |

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync stays on `robinhood_sync.py`.

### 4. Cost & hygiene

- Anthropic spend tracking toward exit (&lt;$20)
- Pre-commit clean on commit
- New subscriptions → [decisions.md](../decisions.md) first

---

## Per-trade checklist (co-pilot)

1. `robinhood-portfolio-review` (or CLI) — buying power, exposure
2. Today's `pre_market` + exposure posture — new entry allowed?
3. `position-sizer` for Agentic account
4. Present: entry, stop, target, risk $, IRA N/A on Agentic
5. **Stop — user confirms**
6. MCP order on Agentic only
7. Log thesis + position same session

---

## Exit criteria (Phase 1 → Phase 2)

- [ ] FMP Starter active; `vcp-screener` run on watchlist universe at least once
- [ ] 14 consecutive trading days: `pre_market.py` + posture log
- [ ] 5+ deep-research or update-research reports on active watchlist
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

- [robinhood-mcp-integration.md](reference/robinhood-mcp-integration.md)
- [playbook.md](playbook.md)
- [PENDING_WORK.md](../PENDING_WORK.md)

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 2. Read [phase-2-learning-loop.md](phase-2-learning-loop.md).
