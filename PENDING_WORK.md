# PENDING_WORK.md

> Persistent task queue across Cursor, Claude Code, and terminal sessions.
> **Last updated:** 2026-05-28
> **Active phase:** Phase 1B — Robinhood Research + Co-Pilot Trading
> **Session load order:** [PROJECT.md](PROJECT.md) → [LOAD_GUIDE.md](LOAD_GUIDE.md) → [project-docs/STATUS.md](project-docs/STATUS.md) → [phase-1b-robinhood-research.md](project-docs/phase-1b-robinhood-research.md)

**Legend:** Auto-execute = agent can do without approval. Needs approval = money/architecture. Needs data = human-only input.

**Fork policy:** Do not modify upstream `skills/<name>/SKILL.md` or `skills/<name>/scripts/` except fixes listed in [decisions.md](decisions.md). Never write `state/theses/` directly — use `thesis_store.py` / thesis-manager.

---

## Research pipeline (Phase 1B P0–P2)

### P0 — Unblock screeners

- [ ] **Activate FMP Starter ($29/mo)** — needs approval / billing
- [x] vcp-screener smoke: `--universe MRAM` (2026-05-28, 3 API calls)
- [ ] Full watchlist vcp/canslim pass after Starter active
- [ ] **Deep research — FPS** (stale 2026-05-13; MRAM/MU/P current 2026-05-27)

### P1 — Daily stack

- [x] `pre-market.timer` active (systemd user)
- [x] `pre_market.py` run 2026-05-28
- [ ] **Weekly `review-portfolio`** — Mondays or before sizing new risk
  - Staleness rule: flag tickers with report &gt;14 days (currently **FPS**)
  - Save summary: `reports/logs/portfolio_summary_YYYY-MM-DD.md`

### P2 — Audit gaps (wrappers only; no upstream skill edits)

| Gap | Wrapper / doc fix |
|-----|-------------------|
| vcp → breakout pipeline | Document FMP Starter + `commands/deep-research.md` chain in phase-1b doc |
| Manual thesis / non-screener sources | Use `log-positions` + `thesis_store.py register` with `source: manual` via CLI |
| market-top-detector ETFs | Always pass `--static-basket` in commands/pre_market notes |

---

## Robinhood co-pilot (Phase 1B)

- [x] MCP CLI: `accounts`, `positions --all` verified
- [x] First `portfolio_review_2026-05-28.md`
- [ ] **`ingest-pending`** (non–dry-run) + **`log-positions`** for TE (taxable)
- [ ] **IRA positions** — MCP read + four questions each
- [ ] **First Agentic trade** — user must reply **confirm** on presented plan (see kickoff report)

**Per-trade:** portfolio review → pre_market/exposure → position-sizer → confirm → MCP Agentic only → log thesis.

---

## Done (do not redo)

- [x] Phase 1 audit Tier 1–2, exposure-coach P2, pre_market systemd
- [x] Robinhood MCP hybrid, account discovery table in decisions.md
- [x] Deep research Phase 1 minimum (MRAM, MU, P, VECO, INO, FPS)
- [x] Phase 1B roadmap docs + decisions [2026-05-28]

---

## Needs approval

- [ ] **FMP Starter ($29/mo)** — activate in FMP dashboard, confirm key tier

---

## Needs data (human only)

- [ ] Log IRA open positions (four questions)
- [ ] Close expired theses: POWL, TSLA, PENG $55C x3
- [ ] Verify HOOD/ICHR June expiries

---

## Deferred — Futures Phase 2 (do not start)

See [project-docs/phase-2-futures-skills.md](project-docs/phase-2-futures-skills.md) (DEFERRED banner).
Revisit when Phase 1B exit + 20+ stock/options trades logged (or user override).

- lucid-rules-engine, tradovate-integration, futures-setup — **not in queue**
