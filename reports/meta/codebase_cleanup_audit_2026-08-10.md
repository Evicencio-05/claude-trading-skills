# Codebase Cleanup Audit — 2026-08-10 (re-audit from `main`)

**Mode:** audit-only (default)
**Branch:** `main` @ `a239a74` (= `origin/main`)
**Phase:** 1 — Research + Co-Pilot Trading ([STATUS.md](../../project-docs/STATUS.md))
**Scope:** Whole repo
**Prior runs:** [2026-05-28](codebase_cleanup_audit_2026-05-28.md) (executed); morning 2026-08-10 audit-and-fix (P0 indexes + migrator archive) **merged via PR #5**

## Summary

| Metric | Count |
|--------|-------|
| Findings | **9** (P0: 2 / P1: 5 / P2: 2) |
| Estimated safe deletions | **0** (no new dead tracked scripts) |
| Estimated commits / adds | **1 package** — untracked `options-flow-tail` workflow |
| Estimated doc merges | **3** (`AGENTS.md`, `LOAD_GUIDE.md`, cleanup prompt phase string) |

**Overall health:** Post-merge `main` is clean on tracked cleanup items (indexes updated, migrator archived, no broken symlinks). New gap: **indexes and skill README advertise `options-flow-tail`, but the command + skill are still untracked** — clone/CI will see dangling links. Untracked conviction WIP still breaks pre-push if present on disk.

---

## A. Workflow & skill overlap

| Path | Duplicate of | Action | Risk |
|------|--------------|--------|------|
| 11 fork-local wrappers | Matching `commands/*.md` | **Keep** — thin; link to `commands/` | None |
| `commands/review-portfolio.md` | ≠ `robinhood-portfolio-review` | **Keep** | None |
| `commands/options-flow-tail.md` + `.cursor/skills/options-flow-tail/` | Indexed in READMEs | **Commit** (P0) or remove index rows until ready | **High** — untracked SoT |
| `skills/scenario-analyzer/SKILL.md` | `commands/scenario-analyzer.md` | **Keep** — thin wrapper | None |
| Command-only workflows (`intraday-options`, `options-strategy-planner`, `review-portfolio`, `scenario-analyzer`) | No Cursor skill dir | **Keep** — command-only is fine | None |

**Pass 1/2 fork check:** No skill copies deep-research body; wrappers link out.

**Routing table:** All `commands/*.md` present in `commands-workflows.mdc` and `commands/README.md` (including `options-flow-tail`).

---

## B. `.cursor/skills/` integrity

```text
Symlinks (13): breadth-chart-analyst, earnings-calendar, earnings-trade-analyzer,
  exposure-coach, ibd-distribution-day-monitor, market-breadth-analyzer,
  market-top-detector, position-sizer, sector-analyst, technical-analyst,
  trader-memory-core, uptrend-analyzer, us-stock-analysis

Fork-local dirs (11): agentic-copilot-trade, deep-research, gex-vex-maps,
  log-positions, log-trade-screenshot, operator-charts, options-flow-tail,
  robinhood-portfolio-review, ta-confluence, tradewhisperer-charts, update-research

Broken symlinks: none
Copied upstream trees: none
```

| Path | Action | Risk |
|------|--------|------|
| Tracked fork-local dirs (10) | **Keep** | None |
| `options-flow-tail/` (untracked) | **Add to git** with `commands/options-flow-tail.md` | Indexes already reference it |
| Symlinks | **Keep** | None |

---

## C. Robinhood / MCP script overlap

| Path | Role | Action |
|------|------|--------|
| `scripts/robinhood_sync.py` | Portfolio A → `pending_ingest.json` | **Keep** |
| `scripts/robinhood_mcp.py` | CLI + `ingest-pending` | **Keep** |
| `scripts/robinhood_mcp_client.py` | MCP client | **Keep** |
| `scripts/robinhood_accounts.py` | YAML map | **Keep** |
| `scripts/mcp_stdio_structured_content_proxy.py` | Cursor compat | **Keep** |
| `config/robinhood_accounts.yaml` | Canonical map | **Keep** |

No superseded ingest scripts. Hybrid stack unchanged.

---

## D. Documentation overlap

| Path | Issue | Action |
|------|-------|--------|
| `AGENTS.md` § Single source of truth | Says all `.cursor/skills` are symlinks | **Merge** — document fork-local exception (P1) |
| `LOAD_GUIDE.md` | No on-demand rows for TA / options-flow / agentic | **Optional add** (P1) |
| `.cursor/prompts/codebase-cleanup.md` Pre-flight | Still says “Phase 1 — Audit & Activate” | **Fix** string → STATUS title (P1) |
| Indexes → `options-flow-tail` | Point at untracked files | **Commit package** (P0) |
| Robinhood setup multi-doc | Canonical = `robinhood-mcp-integration.md` | **Keep** |
| `cursor-integration.md` | Updated in morning P0 | **Keep** |

---

## E. Dead / unnecessary files

| Path | Evidence | Action |
|------|----------|--------|
| `scripts/archive/migrate_reports_layout.py` | Archived morning | **Keep** |
| `scripts/build_entry_watchlist.py` | Untracked; referenced by options-flow-tail | **Commit with flow skill** or leave WIP (P1) |
| `scripts/conviction_tiers.py` + `scripts/tests/test_conviction_tiers.py` | Untracked; `tier_pin` test fails vs `load_watchlist_config` | **Fix then commit**, or quarantine test (P1) — blocks pre-push when on disk |
| `.cursor/rules/structural-changes.mdc` | Untracked reference rule | **Commit when ready** (P1) |
| Bulk untracked `reports/**` | Operator artifacts | List only — no delete |
| `package.json` | `mcp-remote` | **Keep** |
| `launchd/` | macOS reference | **Keep** |

---

## F. Fork policy check

- No upstream `skills/<name>/` edits proposed.
- Do not write `state/theses/` directly.
- Morning P0 did not touch upstream skills.

---

## P0 — Safe now (no behavior change)

| Action | Path | Reason | Verified by |
|--------|------|--------|-------------|
| Commit workflow package | `commands/options-flow-tail.md`, `.cursor/skills/options-flow-tail/**` | Indexes already list it; untracked breaks clone SoT | `git ls-files` empty; files on disk |
| Quarantine or fix | `scripts/tests/test_conviction_tiers.py` | Untracked test fails pre-push (`KeyError: tier_pin`) | pytest + pre-push log |

**User approval needed before any commit/delete.** Audit-only — not executing.

---

## P1 — Merge / consolidate (small edits)

| Action | From → To | Reason |
|--------|-----------|--------|
| Clarify SoT | `AGENTS.md` | Fork-local `.cursor/skills/` dirs are allowed |
| On-demand rows | `LOAD_GUIDE.md` | `options-flow-tail`, TA intakes, `agentic-copilot-trade` |
| Fix phase string | `codebase-cleanup.md` Pre-flight | Match STATUS “Research + Co-Pilot” |
| Pair commit | `build_entry_watchlist.py` (+ deps) | Supporting script for flow skill |
| Finish or park | `conviction_tiers` WIP | Align `load_watchlist_config` with `tier_pin` or drop test |

---

## P2 — Needs approval

| Action | Path | Risk | Ask user |
|--------|------|------|----------|
| Add `commands/robinhood-portfolio-review.md` | skill-only today | Consistency | Worth it? |
| Move fork-local skills under `skills/` | architecture | Breaks current README pattern | Prefer Cursor-only vs portable? |
| Prune old reports | `reports/**` | Data loss | Retention window? |

---

## Intentionally kept

| Path | Why kept |
|------|----------|
| `review-portfolio` vs `robinhood-portfolio-review` | Different workflows |
| Robinhood sync + MCP hybrid | Per `decisions.md` |
| `economic-calendar-fetcher` | Upstream; use `fred_calendar.py` |
| Command-only workflows without Cursor skill | Valid pattern |
| `scripts/archive/*` | Historical one-shots |

---

## Not in scope

- Executing P0 (audit-only this run)
- Upstream skill rewrites
- Bulk `reports/` deletion
- Committing unless user asks
- Merging portfolio review workflows

---

## Recommended next (if user says `audit-and-fix`)

1. **Batch A — track options-flow-tail** (no behavior change): add command + skill + rubric; keep indexes as-is.
2. **Batch B — docs:** `AGENTS.md` SoT, cleanup prompt phase string, optional `LOAD_GUIDE`.
3. **Batch C — conviction WIP:** fix `tier_pin` in `load_watchlist_config` **or** move failing test out of `scripts/tests/` until ready.

```bash
pre-commit run --all-files
uv run python3 -m pytest scripts/tests/ -v
```

---

## Execution log

| Batch | Status | Changes |
|-------|--------|---------|
| Morning audit-and-fix | Done (PR #5) | Indexes + migrator archive |
| Re-audit `main` audit-only | Done | Report refreshed |
| Batch A — tier_pin + docs | **Done** 2026-08-10 | `load_watchlist_config` preserves `tier_pin`; tracked test; `AGENTS.md` SoT; cleanup phase string; `LOAD_GUIDE` on-demand rows |
| Batch B — track `options-flow-tail` | **Done** 2026-08-10 | Committed with cleanup fixes (`e662c88`) |

```bash
pre-commit run --files <touched>
uv run python3 -m pytest scripts/tests/ -v
```
