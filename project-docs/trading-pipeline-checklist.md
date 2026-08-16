# Trading Pipeline Checklist

> **Last updated:** 2026-08-16 (TA-first + A+C logging; IRA log discontinued)
> **Active phase:** [Phase 1 — TA + Co-Pilot](phase-1-research-copilot.md)
>
> Canonical operator cadence for TA session → confluence → co-pilot execution.
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
| Screeners (optional) | `reports/screeners/{vcp,canslim,earnings,pead,breakout}/` |
| Deep research (on demand) | `reports/research/{TICKER}_{YYYY-MM-DD}.md` |
| Broker snapshot (A+C focus) | `reports/portfolio/portfolio_review_YYYY-MM-DD.md` |
| Position sizing | `reports/portfolio/position_sizer_{YYYY-MM-DD}_{HHMMSS}.{json,md}` |
| TradeWhisperer list intake (color SoT) | `reports/charts/tradewhisperer/list_tw_{daily\|weekly\|monthly}_DATE` |
| TradeWhisperer chart intake (optional structure) | `reports/charts/tradewhisperer/{TICKER}_tw_{1D\|1W\|1M}_DATE` |
| TW HTF color stack | `uv run python3 scripts/tw_list_resolve.py stack TICKER --as-of DATE` |
| TW HTF overlap + sector compare | `uv run python3 scripts/tw_list_resolve.py overlap --as-of DATE --bias either --write-pending` → `overlap_tw_DATE` · map `config/tw_sector_map.yaml` |
| GEX/VEX map intake | `reports/charts/gex_vex/{TICKER}_gex_DATE` · `{TICKER}_vex_DATE` |
| Operator chart intake | `reports/charts/operator/{TICKER}_operator_DATE.{md,json}` |
| TA confluence brief | `reports/charts/confluence/session_confluence_{period}_DATE` · `{TICKER}_confluence_DATE` |
| Prediction log v1.5 | `reports/charts/confluence/prediction_log_YYYY-MM-DD.{md,json}` |
| Agentic co-pilot plan | `reports/logs/agentic_copilot_plan_{TICKER}_DATE.json` |
| Prompt retros / digests | `reports/prompts/prompt_run_retro_*.md`, `reports/prompts/prompt_learning_digest_*.md` |
| Meta / audit session outputs | `reports/meta/` |
| Theses (A+C only) | `state/theses/` (via `thesis_store.py` only) |

Path registry: [`scripts/report_paths.py`](../scripts/report_paths.py)

---

## Daily (trading days)

- [ ] Run `uv run python3 scripts/pre_market.py` (timer: `pre-market.timer` — see [launchd/README.md](../launchd/README.md)) — **context only**
- [ ] Read `reports/logs/market_context_YYYY-MM-DD.json` (or `.md`) — posture, ceiling, position flags
- [ ] **TW lists (prefer text)** — ingest via `/tradewhisperer-charts` → `list_tw_daily_DATE` (+ weekly/monthly when posted). Charts only for finalists (structure). Then run PHASE 3 overlap (`tw_list_resolve.py overlap`) and note vs-benchmark + unmapped.
- [ ] **TA session** — `/ta-confluence candle_first` (or map_first) after lists + maps + operator chart ([ta-confluence.md](../commands/ta-confluence.md))
- [ ] If PLAY → optional `/agentic-copilot-trade` on Portfolio C (user `confirm`)
- [ ] After session — append prediction log row ([prediction_log_v15.md](../.cursor/skills/ta-confluence/references/prediction_log_v15.md))

---

## Weekly

- [ ] Ingest TW **weekly** (and monthly if posted) candle lists → `list_tw_weekly_*` / `list_tw_monthly_*` for HTF stacks
- [ ] **Broker snapshot (A+C)** — skill `robinhood-portfolio-review` → `reports/portfolio/portfolio_review_*.md` (skip IRA four-questions)
- [ ] **`exposure-coach`** — weekly posture synthesis when upstream JSON exists ([playbook.md](playbook.md))
- [ ] Optional: `update_stale_research.py` / research batch — **not required** for Phase 1 exit

> **Posture policy:** Daily posture = `pre_market.py` (zero LLM). TA session = primary idea path. Research = on demand.

---

## Research (on demand — optional)

| Situation | Workflow |
|-----------|----------|
| Fundamentals needed | [commands/deep-research.md](../commands/deep-research.md) |
| Report >14d stale | [commands/update-research.md](../commands/update-research.md) |
| Closed trade backfill (A/C) | [commands/log-trade-screenshot.md](../commands/log-trade-screenshot.md) |

**Screeners (optional):** `vcp-screener`, `canslim-screener` — `--universe` from watchlist on Starter.

---

## Per-trade co-pilot (Agentic C only)

Use [commands/agentic-copilot-trade.md](../commands/agentic-copilot-trade.md) (skill `agentic-copilot-trade`). Summary:

- [ ] Prefer a same-day PLAY from `/ta-confluence` (link artifact)
- [ ] **Broker snapshot** — `robinhood-portfolio-review` (A+C) — buying power, exposure
- [ ] Today's `pre_market` posture — new entry allowed?
- [ ] Size — `position-sizer` within `config/agentic_copilot.yaml` caps
- [ ] Present plan — entry, stop, target, risk $
- [ ] **Stop — user replies `confirm` / `confirm plan and order`**
- [ ] MCP `review_equity_order` then `place_equity_order` — **Portfolio C (Agentic) only**
- [ ] Write plan JSON + log thesis to `robinhood_agentic` — [commands/log-positions.md](../commands/log-positions.md)

**Never MCP trade:** IRA (`ira_robinhood`), taxable (`robinhood_taxable`). Taxable sync → `robinhood_sync.py`. **Never log IRA.**

---

## End of day (optional)

- [ ] `uv run python3 scripts/robinhood_sync.py` (Portfolio A taxable) → `/log-positions` for **A only** if `PENDING_THESIS` in `state/pending_ingest.json`

---

## Gates (rules — detail in playbook)

- **Co-pilot only** — no autonomous MCP orders before Phase 3B ([PROJECT.md](../PROJECT.md))
- **Log A+C only** — IRA (B) logging discontinued
- **FTD vs breadth** — lower exposure ceiling governs ([playbook.md](playbook.md))
- **Thesis writes** — `thesis_store.py` / thesis-manager only; never edit `state/theses/` YAML directly
- **FMP** — optional; calendar → `scripts/fred_calendar.py`; screeners via `--universe` on Starter

---

## Changelog

- **2026-08-16** — TA-first cadence; A+C logging only; IRA log discontinued; prediction log path
- **2026-08-11** — TW list-first cadence; `scripts/tw_list_resolve.py` HTF stacks; confluence requires period list for PLAY
- **2026-08-09** — TA-first chart intakes + `ta-confluence`; `agentic-copilot-trade` gates; TW filenames include `1D|1W|1M`
- **2026-05-31** — Reports layout v2: category-grouped subdirs; `scripts/report_paths.py` registry
- **2026-05-31** — Initial checklist; consolidated steps from phase-1, PENDING_WORK, LOAD_GUIDE
