# PENDING_WORK.md

> Persistent task queue across Cursor, Claude Code, and terminal sessions.
> **Last updated:** 2026-05-30
> **Active phase:** Phase 1 — Research + Co-Pilot Trading
> **Session load order:** [PROJECT.md](PROJECT.md) → [LOAD_GUIDE.md](LOAD_GUIDE.md) → [project-docs/STATUS.md](project-docs/STATUS.md) → [phase-1-research-copilot.md](project-docs/phase-1-research-copilot.md)

**Legend:** Auto-execute = agent can do without approval. Needs approval = money/architecture. Needs data = human-only input.

**Fork policy:** Do not modify upstream `skills/<name>/SKILL.md` or `skills/<name>/scripts/` except fixes listed in [decisions.md](decisions.md). Never write `state/theses/` directly — use `thesis_store.py` / thesis-manager.

---

## Research pipeline (Phase 1 P0–P2)

**Watchlist (`reports/research/`, latest only):** MRAM/MU/P @ 2026-05-27 | FPS @ 2026-05-13 (stale) | VECO @ 2026-05-08 (stale)

### P0 — Unblock screeners

- [ ] **Activate FMP Starter ($29/mo)** — needs approval / billing
- [x] vcp-screener smoke: `--universe MRAM` (2026-05-28, 3 API calls)
- [ ] Full watchlist vcp/canslim pass after Starter active
- [ ] **Update research — stale watchlist** (FPS, VECO; MRAM/MU/P current 2026-05-27)

### P1 — Daily stack

- [x] `pre-market.timer` active (systemd user)
- [x] `pre_market.py` run 2026-05-28, 2026-05-29 (`reports/logs/market_context_2026-05-29.md`)
- [ ] **Weekly stale research scan** — `research-staleness.timer` (Sun 6 PM local) or manual:
  `uv run python3 scripts/update_stale_research.py`
  - Queue: `state/research_update_queue.json` | Summary: `reports/logs/research_staleness_YYYY-MM-DD.md`
  - Staleness rule: &gt;14 days (currently **FPS, VECO**); run `update-research` / Cursor from queue
- [ ] **Weekly `review-portfolio`** — optional batch LLM refresh after queue review

### P2 — Audit gaps (wrappers only; no upstream skill edits)

| Gap | Wrapper / doc fix |
|-----|-------------------|
| vcp → breakout pipeline | Document FMP Starter + `commands/deep-research.md` chain in phase-1 doc |
| Manual thesis / non-screener sources | Use `log-positions` + `thesis_store.py register` with `source: manual` via CLI |
| market-top-detector ETFs | Always pass `--static-basket` in commands/pre_market notes |

---

## Robinhood co-pilot (Phase 1)

- [x] MCP CLI: `accounts`, `positions --all` verified (2026-05-30 smoke OK)
- [x] First `portfolio_review_2026-05-28.md`
- [x] **`ingest-pending`** + **`log-positions`** for TE — `th_te_grw_20260529_034d` ACTIVE (2026-05-29)
- [ ] **IRA positions** — MCP read + four questions each
- [ ] **First Agentic trade** — user must reply **confirm** on presented plan

**Per-trade:** portfolio review → pre_market/exposure → position-sizer → confirm → MCP Agentic only → log thesis.

---

## Done (do not redo)

- [x] Phase 1 audit Tier 1–2, exposure-coach P2, pre_market systemd
- [x] Robinhood MCP hybrid, account discovery table in decisions.md
- [x] Deep research Phase 1 minimum (MRAM, MU, P, VECO, FPS on disk)
- [x] Equity-only roadmap docs + decisions [2026-05-29]
- [x] `reports/portfolio_review_2026-05-28.md` (2026-05-28)
- [x] `reports/vcp_screener_2026-05-28_204543.md` — MRAM smoke (2026-05-28)
- [x] TE thesis logged — `th_te_grw_20260529_034d` (2026-05-29)
- [x] POWL thesis closed — `th_powl_pvt_20260509_db36` CLOSED (2026-05-29)

---

## Needs approval

- [ ] **FMP Starter ($29/mo)** — activate in FMP dashboard, confirm key tier

---

## Needs data (human only)

- [ ] Log IRA open positions (four questions)
- [ ] Close expired theses: TSLA, PENG $55C x3
- [ ] Verify HOOD/ICHR June expiries
