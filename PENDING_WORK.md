# PENDING_WORK.md

> Persistent task queue across Cursor, Claude Code, and terminal sessions.
> **Last updated:** 2026-08-16
> **Active phase:** Phase 1 — TA + Co-Pilot Trading
> **Operator cadence:** [project-docs/trading-pipeline-checklist.md](project-docs/trading-pipeline-checklist.md)
> **Session load order:** [PROJECT.md](PROJECT.md) → [LOAD_GUIDE.md](LOAD_GUIDE.md) → [project-docs/STATUS.md](project-docs/STATUS.md) → [phase-1-research-copilot.md](project-docs/phase-1-research-copilot.md)

**Legend:** Auto-execute = agent can do without approval. Needs approval = money/architecture. Needs data = human-only input.

**Fork policy:** Do not modify upstream `skills/<name>/SKILL.md` or `skills/<name>/scripts/` except fixes listed in [decisions.md](decisions.md). Never write `state/theses/` directly — use `thesis_store.py` / thesis-manager.

**Account scope:** Log and trade-plan **Portfolio C (Agentic)** + **Portfolio A (taxable)**. **Do not log IRA (Portfolio B).**

---

## TA-first source foundations (primary)

User-supplied images/exports only; no news/FMP fetch for the core loop.

| Source | Skill / command | Output |
|--------|-----------------|--------|
| TradeWhisperer | `tradewhisperer-charts` | `reports/charts/tradewhisperer/` — **lists** (color SoT) + optional charts |
| GEX/VEX | `gex-vex-maps` | `reports/charts/gex_vex/` — Skylit Heatseeker screenshots |
| Operator charts | `operator-charts` | `reports/charts/operator/` — S/R, fibs, LuxAlgo VP, SMA 50/100/200 |

- [x] Skills + commands + `report_paths` keys
- [x] TradeWhisperer contract (charts + lists)
- [x] **List-first TW + HTF stack resolver** — `scripts/tw_list_resolve.py`; confluence uses `tw_stack` (2026-08-11)
- [x] GEX/VEX contract (Skylit docs)
- [x] Operator-charts contract (example `HOOD_operator_2026-08-08`)
- [x] **Fusion** — `ta-confluence` skill/command + rubric + judgment layer → `reports/charts/confluence/`
- [x] **Agentic co-pilot** — `agentic-copilot-trade` + `config/agentic_copilot.yaml.example`
- [x] **Charter TA-first + A+C** — IRA logging discontinued (2026-08-16)
- [x] Prediction log v1.5 **template** + seed (`prediction_log_2026-08-16`) + smoke inventory
- [ ] Live session smoke with **same-day** TW lists (daily+weekly) + GEX/VEX + operator (no stale TW gap)
- [ ] Prediction log **outcomes** after taken A/C trades
- [ ] First filled Agentic co-pilot trade (user `confirm`) on Portfolio C

---

## Robinhood co-pilot (A + C)

- [x] MCP CLI: `accounts`, `positions --all` verified (2026-05-30 smoke OK)
- [x] First `reports/portfolio/portfolio_review_2026-05-28.md`
- [x] **`ingest-pending`** + **`log-positions`** for TE — `th_te_grw_20260529_034d` ACTIVE (2026-05-29)
- [ ] **First Agentic (C) trade** — user must reply **confirm** on presented plan
- [ ] **2nd portfolio review** — A+C focus (skip IRA four-questions)
- [ ] Enable `robinhood-sync.timer` when Portfolio A sync should stay automatic

**Per-trade:** see [checklist § Per-trade co-pilot](project-docs/trading-pipeline-checklist.md#per-trade-co-pilot-agentic-only).

**Discontinued:** IRA positions — MCP four questions / thesis logging.

---

## Research pipeline (optional / demoted)

Not Phase 1 exit-blocking. Run on demand only.

**Watchlist (`reports/research/`, latest only):** HOOD/IBM/TSM/VECO @ 2026-05-31 | MRAM/MU/P @ 2026-05-27 | FPS @ 2026-05-13 (stale)

- [x] FMP Starter + watchlist vcp/canslim (2026-05-31)
- [x] Deep research Phase 1 minimum on disk
- [ ] Update research — FPS (optional)
- [ ] Weekly research watchlist batch (optional)
- [ ] Deep-research news strip — deferred / parked

---

## Parked research debt (do not prioritize)

Touch only if it blocks commits or the Agentic path.

| Item | Notes |
|------|--------|
| `institutional-flow-tracker` FMP v3 403 | Skip in deep-research; migrate later if research revived |
| Nine forked `fmp_client.py` copies | Contract tests exist; consolidation later |
| CI subset vs `run_all_tests.sh` | Pre-push runner is SoT; expand CI when convenient |
| `theme-detector` / canslim `bs4` skips | Documented KNOWN_SKIP |
| thesis-manager `utils` pytest collection clash | Avoid bulk pytest; use per-dir runner |
| FMP Premium ($69/mo) | Needs approval — not required for TA path |

---

## Done (do not redo)

- [x] Phase 1 audit Tier 1–2, exposure-coach P2, pre_market systemd
- [x] Robinhood MCP hybrid, account discovery table in decisions.md
- [x] Deep research Phase 1 minimum (MRAM, MU, P, VECO, FPS on disk)
- [x] Equity-only roadmap docs + decisions [2026-05-29]
- [x] `reports/portfolio/portfolio_review_2026-05-28.md` (2026-05-28)
- [x] TE thesis logged — `th_te_grw_20260529_034d` (2026-05-29)
- [x] POWL thesis closed — `th_powl_pvt_20260509_db36` CLOSED (2026-05-29)
- [x] FMP Starter + stable API fixes — verification 2026-05-31
- [x] Thesis Manager CRUD consolidation (2026-05-31)
- [x] TA intakes + confluence + list-first TW HTF (2026-08-09–11)

---

## Needs approval

- [ ] **FMP Premium ($69/mo)** — full S&P 500 universe only; not needed for TA-first Phase 1

---

## Needs data (human only)

- [ ] First Agentic (C) `confirm` on a PLAY plan
- [ ] Close expired A/C theses if still open: TSLA, PENG $55C x3
- [ ] Verify HOOD/ICHR June expiries (if still relevant)
