# PENDING_WORK.md

> Persistent task queue across Cursor, Claude Code, and terminal sessions.
> **Last updated:** 2026-08-09
> **Active phase:** Phase 1 — Research + Co-Pilot Trading
> **Operator cadence:** [project-docs/trading-pipeline-checklist.md](project-docs/trading-pipeline-checklist.md)
> **Session load order:** [PROJECT.md](PROJECT.md) → [LOAD_GUIDE.md](LOAD_GUIDE.md) → [project-docs/STATUS.md](project-docs/STATUS.md) → [phase-1-research-copilot.md](project-docs/phase-1-research-copilot.md)

**Legend:** Auto-execute = agent can do without approval. Needs approval = money/architecture. Needs data = human-only input.

**Fork policy:** Do not modify upstream `skills/<name>/SKILL.md` or `skills/<name>/scripts/` except fixes listed in [decisions.md](decisions.md). Never write `state/theses/` directly — use `thesis_store.py` / thesis-manager.

---

## TA-first source foundations (2026-08-09)

User-supplied images/exports only; no news/FMP fetch; fusion next.

| Source | Skill / command | Output |
|--------|-----------------|--------|
| TradeWhisperer | `tradewhisperer-charts` | `reports/charts/tradewhisperer/` — charts + lists |
| GEX/VEX | `gex-vex-maps` | `reports/charts/gex_vex/` — Skylit Heatseeker screenshots |
| Operator charts | `operator-charts` | `reports/charts/operator/` — S/R, fibs, LuxAlgo VP, SMA 50/100/200 |

- [x] Skills + commands + `report_paths` keys
- [x] TradeWhisperer contract (charts + lists)
- [x] GEX/VEX contract (Skylit docs)
- [x] Operator-charts contract (example `HOOD_operator_2026-08-08`)
- [x] **Fusion** — `ta-confluence` skill/command + rubric + judgment layer → `reports/charts/confluence/`
- [ ] Live session smoke with full TW list + GEX/VEX + operator chart
- [ ] Deep-research news strip — deferred
- [ ] v1.5 prediction log / process retro (after real sessions)

---

## Research pipeline (Phase 1 P0–P2)

**Watchlist (`reports/research/`, latest only):** HOOD/IBM/TSM/VECO @ 2026-05-31 | MRAM/MU/P @ 2026-05-27 | FPS @ 2026-05-13 (stale)

### P0 — Unblock screeners

- [x] **Activate FMP Starter ($29/mo)** — active 2026-05-31 ([decisions.md](decisions.md) [2026-05-31])
- [x] vcp-screener smoke: `--universe MRAM` (2026-05-28, 3 API calls)
- [x] Full watchlist vcp/canslim pass — vcp 11 quotes + canslim MRAM/MU (2026-05-31)
- [x] **Deep research HOOD/IBM/TSM + update VECO** (2026-05-31)
- [ ] **Update research — stale watchlist** (FPS only; MRAM/MU/P/VECO current)

### P1 — Cadence (see [checklist § Weekly](project-docs/trading-pipeline-checklist.md#weekly))

- [x] `pre-market.timer` active (systemd user)
- [x] `pre_market.py` run 2026-05-28, 2026-05-29 (`reports/logs/market_context_2026-05-29.md`)
- [x] **Weekly stale research scan** — run 2026-05-31 (`reports/logs/research_staleness_2026-05-31.md`; **FPS** + 8 others still need deep research)
- [ ] **Weekly research watchlist batch** — optional after queue review

### P2 — Audit gaps (wrappers only; no upstream skill edits)

| Gap | Wrapper / doc fix |
|-----|-------------------|
| vcp → breakout pipeline | [x] Documented in phase-1 + deep-research PASS 0 preflight (2026-05-31) |
| Manual thesis / non-screener sources | Use `log-positions` + `thesis_store.py register` with `source: manual` via CLI |
| Full S&P 500 vcp/canslim | FMP Premium ($69/mo) for `sp500-constituent`; watchlist `--universe` works on Starter |

---

## Robinhood co-pilot (Phase 1)

- [x] MCP CLI: `accounts`, `positions --all` verified (2026-05-30 smoke OK)
- [x] First `reports/portfolio/portfolio_review_2026-05-28.md`
- [x] **`ingest-pending`** + **`log-positions`** for TE — `th_te_grw_20260529_034d` ACTIVE (2026-05-29)
- [ ] **IRA positions** — MCP read + four questions each
- [ ] **First Agentic trade** — user must reply **confirm** on presented plan

**Per-trade:** see [checklist § Per-trade co-pilot](project-docs/trading-pipeline-checklist.md#per-trade-co-pilot-agentic-only).

---

## Done (do not redo)

- [x] Phase 1 audit Tier 1–2, exposure-coach P2, pre_market systemd
- [x] Robinhood MCP hybrid, account discovery table in decisions.md
- [x] Deep research Phase 1 minimum (MRAM, MU, P, VECO, FPS on disk)
- [x] Equity-only roadmap docs + decisions [2026-05-29]
- [x] `reports/portfolio/portfolio_review_2026-05-28.md` (2026-05-28)
- [x] `reports/screeners/vcp/vcp_screener_2026-05-28_204543.md` — MRAM smoke (2026-05-28)
- [x] TE thesis logged — `th_te_grw_20260529_034d` (2026-05-29)
- [x] POWL thesis closed — `th_powl_pvt_20260509_db36` CLOSED (2026-05-29)
- [x] FMP Starter + stable API fixes — verification 2026-05-31
- [x] Thesis Manager CRUD consolidation — removed Add Thesis tab; Theses page owns sync ingest + lifecycle (2026-05-31)

---

## Needs approval

- [ ] **FMP Premium ($69/mo)** — full S&P 500 universe only; Starter sufficient for watchlist screening

---

## Needs data (human only)

- [ ] Log IRA open positions (four questions)
- [ ] Close expired theses: TSLA, PENG $55C x3
- [ ] Verify HOOD/ICHR June expiries
