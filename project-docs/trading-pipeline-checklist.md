# Trading Pipeline Checklist

> **Last updated:** 2026-05-31 (reports layout v2)
> **Active phase:** [Phase 1 — Research + Co-Pilot](phase-1-research-copilot.md)
>
> Canonical operator cadence for research → thesis → co-pilot execution.
> Update this file when cadence changes; link to `commands/` for workflow detail — do not copy Pass 1/Pass 2 steps here.

---

## Output quick-ref

| Artifact | Path |
|----------|------|
| Daily market context | `reports/logs/market_context_YYYY-MM-DD.md` |
| Daily market context (structured) | `reports/logs/market_context_YYYY-MM-DD.json` |
| Posture history | `reports/logs/posture_history.log` |
| Market breadth | `reports/market/breadth/market_breadth_{YYYY-MM-DD}_{HHMMSS}.{json,md}` |
| Uptrend analysis | `reports/market/uptrend/uptrend_analysis_{YYYY-MM-DD}_{HHMMSS}.{json,md}` |
| Sector rotation | `reports/market/sector/sector_rotation_{YYYY-MM-DD}.{md,json}` |
| Market top / exposure | `reports/market/top/`, `reports/market/exposure/` |
| Screeners (VCP, CANSLIM, earnings, PEAD, breakout) | `reports/screeners/{vcp,canslim,earnings,pead,breakout}/` |
| Deep research reports | `reports/research/{TICKER}_{YYYY-MM-DD}.md` |
| Deep research preflight manifest | `reports/logs/research_preflight_{TICKER}_{YYYY-MM-DD}.json` |
| Research staleness summary | `reports/logs/research_staleness_YYYY-MM-DD.md` |
| Stale-research queue | `state/research_update_queue.json` |
| Broker snapshot | `reports/portfolio/portfolio_review_YYYY-MM-DD.md` |
| Position sizing | `reports/portfolio/position_sizer_{YYYY-MM-DD}_{HHMMSS}.{json,md}` |
| Watchlist batch summary | `reports/logs/portfolio_summary_YYYY-MM-DD.md` |
| Prompt retros / digests | `reports/prompts/prompt_run_retro_*.md`, `reports/prompts/prompt_learning_digest_*.md` |
| Meta / audit session outputs | `reports/meta/` |
| Theses | `state/theses/` (via `thesis_store.py` only) |

Path registry: [`scripts/report_paths.py`](../scripts/report_paths.py)

---

## Daily (trading days)

- [ ] Run `uv run python3 scripts/pre_market.py` (timer: `pre-market.timer` — see [launchd/README.md](../launchd/README.md))
- [ ] Read `reports/logs/market_context_YYYY-MM-DD.json` (or `.md`) — posture, ceiling, position flags

---

## Weekly

- [ ] Run `uv run python3 scripts/update_stale_research.py` → queue + `reports/logs/research_staleness_*.md`
- [ ] **Research watchlist batch** — [commands/review-portfolio.md](../commands/review-portfolio.md) or per-ticker [commands/update-research.md](../commands/update-research.md) from queue
- [ ] **Broker snapshot** — skill `robinhood-portfolio-review` → `reports/portfolio/portfolio_review_*.md`
- [ ] **`exposure-coach`** — weekly posture synthesis when upstream JSON exists ([playbook.md](playbook.md))

> **Posture policy:** Daily posture = `pre_market.py` (zero LLM). `exposure-coach` = weekly synthesis **or** runs inside deep-research Pass 1 when researching a ticker — not a separate daily LLM call.

---

## Research (on demand)

| Situation | Workflow |
|-----------|----------|
| New ticker | [commands/deep-research.md](../commands/deep-research.md) |
| Report >14d stale or thesis changed | [commands/update-research.md](../commands/update-research.md) |
| Screener hit | `thesis_ingest.py` (screener JSON) → deep-research → `thesis_store.link_report()` |
| Closed trade backfill | [commands/log-trade-screenshot.md](../commands/log-trade-screenshot.md) |

**Live state:** [config/research_watchlist.yaml](../config/research_watchlist.yaml) · [config/research_exclude.yaml](../config/research_exclude.yaml) · staleness in [STATUS.md](STATUS.md) or latest `research_staleness_*.md`

**Screeners (FMP Starter active):** `vcp-screener`, `canslim-screener`, `earnings-trade-analyzer` → `pead-screener` — pass `--universe` from [config/research_watchlist.yaml](../config/research_watchlist.yaml); full S&P 500 needs Premium tier — see [phase-1-research-copilot.md](phase-1-research-copilot.md) exit criteria. Daily watchlist screener runs feed deep-research Pass 0 — do not re-run per ticker when same-day JSON exists.

---

## Per-trade co-pilot (Agentic only)

Before any new Agentic MCP order:

- [ ] **Broker snapshot** — `robinhood-portfolio-review` (or `scripts/robinhood_mcp.py`) — buying power, exposure
- [ ] Today's `pre_market` posture — new entry allowed?
- [ ] **`position-sizer`** — Agentic buying power ([skills/position-sizer/SKILL.md](../skills/position-sizer/SKILL.md))
- [ ] Present plan — entry, stop, target, risk $ (IRA N/A on Agentic)
- [ ] **Stop — user confirms**
- [ ] MCP order — **Portfolio C (Agentic) only**
- [ ] Log thesis + position same session — [commands/log-positions.md](../commands/log-positions.md)

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync → `robinhood_sync.py`.

---

## End of day (optional)

- [ ] `uv run python3 scripts/robinhood_sync.py` (Portfolio A taxable) → `/log-positions` if `PENDING_THESIS` in `state/pending_ingest.json`

---

## Gates (rules — detail in playbook)

- **Co-pilot only** — no autonomous MCP orders before Phase 3B ([PROJECT.md](../PROJECT.md))
- **IRA options** — flag eligibility before actionable advice ([playbook.md](playbook.md) § IRA)
- **FTD vs breadth** — lower exposure ceiling governs ([playbook.md](playbook.md))
- **Thesis writes** — `thesis_store.py` / thesis-manager only; never edit `state/theses/` YAML directly
- **FMP blocks** — `economic-calendar-fetcher` v3 → `scripts/fred_calendar.py`; vcp/canslim watchlist via `--universe` on Starter; full S&P 500 → FMP Premium ($69/mo)

---

## Changelog

- **2026-05-31** — Reports layout v2: category-grouped subdirs (`market/`, `screeners/`, `portfolio/`, etc.); `scripts/report_paths.py` registry
- **2026-05-31** — Initial checklist; consolidated steps from phase-1, PENDING_WORK, LOAD_GUIDE
