# Trading Pipeline Checklist

> **Last updated:** 2026-08-16 (TA-first charter)
> **Active phase:** [Phase 1 — TA Confluence + Co-Pilot](phase-1-research-copilot.md)
>
> Canonical operator cadence for three-source TA → confluence → thesis → co-pilot.
> Fundamentals / deep-research are optional backup (PLAY / verge / explicit ask).
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
| TradeWhisperer list intake (color SoT) | `reports/charts/tradewhisperer/list_tw_{daily\|weekly\|monthly}_DATE` |
| TradeWhisperer chart intake (optional structure) | `reports/charts/tradewhisperer/{TICKER}_tw_{1D\|1W\|1M}_DATE` |
| TW HTF color stack | `uv run python3 scripts/tw_list_resolve.py stack TICKER --as-of DATE` |
| TW HTF overlap + sector compare | `uv run python3 scripts/tw_list_resolve.py overlap --as-of DATE --bias either --write-pending` → `overlap_tw_DATE` · map `config/tw_sector_map.yaml` |
| GEX/VEX map intake | `reports/charts/gex_vex/{TICKER}_gex_DATE` · `{TICKER}_vex_DATE` |
| Operator chart intake | `reports/charts/operator/{TICKER}_operator_DATE.{md,json}` |
| TA confluence brief | `reports/charts/confluence/session_confluence_{period}_DATE` · `{TICKER}_confluence_DATE` |
| Agentic co-pilot plan | `reports/logs/agentic_copilot_plan_{TICKER}_DATE.json` |
| Entry watchlist (optional) | `reports/logs/entry_watchlist_DATE.{json,md}` |
| Prompt retros / digests | `reports/prompts/prompt_run_retro_*.md`, `reports/prompts/prompt_learning_digest_*.md` |
| Meta / audit session outputs | `reports/meta/` |
| Theses | `state/theses/` (via `thesis_store.py` only) |

Path registry: [`scripts/report_paths.py`](../scripts/report_paths.py)

---

## Daily (trading days)

- [ ] Run `uv run python3 scripts/pre_market.py` (timer: `pre-market.timer` — see [launchd/README.md](../launchd/README.md))
- [ ] Read `reports/logs/market_context_YYYY-MM-DD.json` (or `.md`) — posture, ceiling, position flags
- [ ] **TW lists (prefer text)** — when posted, ingest via `/tradewhisperer-charts` → `list_tw_daily_DATE` (+ weekly/monthly when available). Charts only for finalists (structure). Then run overlap (`tw_list_resolve.py overlap`) and note vs-benchmark + unmapped.
- [ ] **TA session (primary)** — paste/provide GEX/VEX + operator chart → `/ta-confluence` ([ta-confluence.md](../commands/ta-confluence.md)). Ask for any missing source before scoring. Standing prompt: [ta-first-session.md](../.cursor/prompts/ta-first-session.md)

---

## Weekly

- [ ] Ingest TW **weekly** (and monthly if posted) candle lists → `list_tw_weekly_*` / `list_tw_monthly_*` for HTF stacks
- [ ] **TA pattern distill** — review confluence notes; propose playbook / charting-coach deltas for human approve ([playbook.md](playbook.md), [phase-2-learning-loop.md](phase-2-learning-loop.md))
- [ ] **Broker snapshot** — skill `robinhood-portfolio-review` → `reports/portfolio/portfolio_review_*.md`
- [ ] **`exposure-coach`** — weekly posture synthesis when upstream JSON exists ([playbook.md](playbook.md))
- [ ] Optional backup: `uv run python3 scripts/update_stale_research.py` only for tickers already in play from confluence / open theses

> **Posture policy:** Daily posture = `pre_market.py` (zero LLM). `exposure-coach` = weekly synthesis — not a separate daily LLM call. Deep-research is not a weekly default.

---

## TA session → thesis (primary)

| Situation | Workflow |
|-----------|----------|
| Lists + maps + operator chart ready | [commands/ta-confluence.md](../commands/ta-confluence.md) → PLAY / WATCH / NO_TRADE |
| PLAY or strong WATCH | Draft thesis (trader-memory) with three-domain invalidation |
| PLAY or verge of confluence (user OK) | Optional [commands/deep-research.md](../commands/deep-research.md) stress-test |
| Agentic entry | [commands/agentic-copilot-trade.md](../commands/agentic-copilot-trade.md) |
| Closed trade backfill | [commands/log-trade-screenshot.md](../commands/log-trade-screenshot.md) |

---

## Research backup (gated — on demand)

| Situation | Workflow |
|-----------|----------|
| PLAY / verge / explicit ask — new ticker | [commands/deep-research.md](../commands/deep-research.md) |
| Same gate — report stale or thesis changed | [commands/update-research.md](../commands/update-research.md) |
| Optional screener shortlist | `thesis_ingest.py` → gated deep-research if still pursuing |

**Live state (backup watchlist):** [config/research_watchlist.yaml](../config/research_watchlist.yaml) · [config/research_exclude.yaml](../config/research_exclude.yaml)

**Screeners (optional backup):** `vcp-screener`, `canslim-screener`, `earnings-trade-analyzer` → `pead-screener` — `--universe` from watchlist; not the daily center of gravity.

---

## Per-trade co-pilot (Agentic only)

Use [commands/agentic-copilot-trade.md](../commands/agentic-copilot-trade.md) (skill `agentic-copilot-trade`). Summary:

- [ ] **Broker snapshot** — `robinhood-portfolio-review` (or `scripts/robinhood_mcp.py`) — buying power, exposure
- [ ] Today's `pre_market` posture — new entry allowed?
- [ ] Confluence + size — cite TW/maps/operator invalidation; `position-sizer` within `config/agentic_copilot.yaml` caps; deep-research only if PLAY/verge gate met
- [ ] Present plan — entry, stop, target, risk $ (IRA N/A on Agentic)
- [ ] **Stop — user replies `confirm` / `confirm plan and order`**
- [ ] MCP `review_equity_order` then `place_equity_order` — **Portfolio C (Agentic) only**
- [ ] Write plan JSON + log thesis — [commands/log-positions.md](../commands/log-positions.md)

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

- **2026-08-16** — TA-first charter: confluence primary; deep-research gated; weekly playbook distill
- **2026-08-11** — TW list-first cadence; `scripts/tw_list_resolve.py` HTF stacks; confluence requires period list for PLAY
- **2026-08-09** — TA-first chart intakes + `ta-confluence`; `agentic-copilot-trade` gates; TW filenames include `1D|1W|1M`
- **2026-05-31** — Reports layout v2: category-grouped subdirs (`market/`, `screeners/`, `portfolio/`, etc.); `scripts/report_paths.py` registry
- **2026-05-31** — Initial checklist; consolidated steps from phase-1, PENDING_WORK, LOAD_GUIDE
