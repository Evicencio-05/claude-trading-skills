# Codebase Cleanup Audit — 2026-08-10

**Mode:** audit-and-fix
**Phase:** 1 — Research + Co-Pilot
**Scope:** Whole repo
**Prior audit:** [codebase_cleanup_audit_2026-05-28.md](codebase_cleanup_audit_2026-05-28.md) (all batches done)

## Summary

| Metric | Count |
|--------|-------|
| Findings | **12** (P0: 5 / P1: 4 / P2: 3) |
| Estimated safe deletions | **1 script** → `scripts/archive/` (~227 lines) |
| Estimated doc/index edits | **5 files** |
| Estimated merges | **0** (no workflow body forks) |

**Overall health:** May 2026 cleanup held. New fork workflows (TA intakes, confluence, Agentic co-pilot, options-flow-tail) follow the thin-wrapper pattern. Main gaps are **index drift** (especially `options-flow-tail`) and one **finished one-shot migrator** still under `scripts/`.

---

## A. Workflow & skill overlap

| Path | Duplicate of | Action | Risk |
|------|--------------|--------|------|
| `.cursor/skills/*/SKILL.md` (11 wrappers) | Matching `commands/*.md` | **Keep** — all link to `commands/`; no Pass 1/2 body copies | None |
| `commands/review-portfolio.md` | ≠ `robinhood-portfolio-review` | **Keep** — research batch vs broker snapshot | None |
| `commands/options-flow-tail.md` | skill + `references/tail_rubric.md` | **Keep** — command is SoT; skill thin; rubric correctly under skill refs | None |
| `skills/scenario-analyzer/SKILL.md` | `commands/scenario-analyzer.md` | **Keep** — already thin wrapper (2026-05-28) | None |
| `gex-vex-maps` / `tradewhisperer-charts` | skill slightly longer than command | **Keep** — skill = discovery + load table; command = phases | Low |

**Pass 1/Pass 2 fork check:** `deep-research` skill summarizes Pass 0–2 rules but points at `commands/deep-research.md` as SoT — acceptable thin wrapper, not a fork.

**Routing table vs files (gaps only):**

| File / skill | `commands-workflows.mdc` | `commands/README.md` | `.cursor/skills/README.md` |
|--------------|--------------------------|----------------------|----------------------------|
| `options-flow-tail` | **Missing** | **Missing** | **Missing** |
| `log-trade-screenshot` | Yes | Yes | **Missing** |
| All other `commands/*.md` | Yes | Yes | Yes (workflow rows) |

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
Copied upstream skill trees: none (no skills/<name> twin for fork-local dirs)
```

| Path | Action | Risk |
|------|--------|------|
| 13 symlinks → `skills/<name>/` | **Keep** | None |
| 11 fork-local wrappers | **Keep** — documented in `.cursor/skills/README.md` | None |
| Prompt keep-list (4 wrappers only) | **Update** `.cursor/prompts/codebase-cleanup.md` — stale vs reality | Doc only |

---

## C. Robinhood / MCP script overlap

| Path | Role | Action |
|------|------|--------|
| `scripts/robinhood_sync.py` | Portfolio A schedule → `pending_ingest.json` | **Keep** |
| `scripts/robinhood_mcp.py` | CLI + `ingest-pending` | **Keep** |
| `scripts/robinhood_mcp_client.py` | MCP client library | **Keep** |
| `scripts/robinhood_accounts.py` | YAML account map | **Keep** |
| `scripts/mcp_stdio_structured_content_proxy.py` | Cursor compat | **Keep** |
| `config/robinhood_accounts.yaml` | Canonical map | **Keep** |

**Superseded ingest scripts:** None. Hybrid stack unchanged per `decisions.md`.

---

## D. Documentation overlap

| Path | Issue | Action |
|------|-------|--------|
| `commands/README.md` + routing table + skills README | `options-flow-tail` unlisted | **Fix** (P0) |
| `.cursor/skills/README.md` | Missing `log-trade-screenshot`, `options-flow-tail` | **Fix** (P0) |
| `project-docs/reference/cursor-integration.md` | Wrapper list still names only 4 dirs | **Fix** → point at skills README (P0) |
| `AGENTS.md` § Single source of truth | Says all `.cursor/skills` are symlinks | **Merge** note for fork-local wrappers (P1) |
| `.cursor/prompts/codebase-cleanup.md` | Keep-list outdated (4 wrappers) | **Fix** (P0) |
| `config/agentic_copilot.yaml` markdown link | File absent until user copies `.example` | **Keep** — intentional; procedural fallback documented |
| Robinhood setup docs | Still multi-file | **Keep** — canonical = `robinhood-mcp-integration.md` |

---

## E. Dead / unnecessary files

| Path | Evidence | Action |
|------|----------|--------|
| `scripts/migrate_reports_layout.py` | Header: one-time; **0 repo refs**; category dirs present; no flat leftovers; no tests | **Archive** (P0, needs OK) |
| `scripts/archive/*` | Prior P0 leftovers | **Keep** |
| `scripts/fmp_verify_starter.py` | Referenced in `decisions.md` | **Keep** |
| `package.json` | `mcp-remote` | **Keep** |
| `reports/` bulk | User artifacts | List only — no delete |
| `launchd/` | macOS reference | **Keep** |

---

## F. Fork policy check

- No upstream `skills/<name>/` edits proposed.
- Fork-local skills correctly live under `.cursor/skills/` + `commands/` (not copied into `skills/`).
- No direct `state/theses/` write paths found in cleanup scope.

---

## P0 — Safe now (no behavior change)

| Action | Path | Reason | Verified by |
|--------|------|--------|-------------|
| Add index rows | `commands/README.md`, `.cursor/rules/commands-workflows.mdc`, `.cursor/skills/README.md` | `options-flow-tail` exists but unlisted | `rg` + file listing |
| Add skill row | `.cursor/skills/README.md` | `log-trade-screenshot` missing from skills README | `rg` |
| Doc pointer | `project-docs/reference/cursor-integration.md` | Stale 4-wrapper list | `ls .cursor/skills/` |
| Update keep-list | `.cursor/prompts/codebase-cleanup.md` | Prompt contradicted fork-local pattern | Compare to skills README |
| Archive | `scripts/migrate_reports_layout.py` → `scripts/archive/` | Finished one-shot; zero refs | `rg` + reports layout check |

---

## P1 — Merge / consolidate (small edits)

| Action | From → To | Reason |
|--------|-----------|--------|
| Clarify SoT exception | `AGENTS.md` § Single source of truth | Document fork-local `.cursor/skills/` dirs |
| On-demand row | `LOAD_GUIDE.md` | Optional: `options-flow-tail` / TA commands when relevant |
| Soften bare yaml link | `commands/agentic-copilot-trade.md` | Prefer `.example` as primary clickable target |
| Optional command file | `commands/robinhood-portfolio-review.md` | Parity with other workflows (still deferred) |

---

## P2 — Needs approval (behavior or upstream touch)

| Action | Path | Risk | Ask user |
|--------|------|------|----------|
| Move fork-local skills into `skills/` | e.g. `options-flow-tail` | Architecture change vs current README | Prefer Cursor-only vs portable `skills/`? |
| Prune old reports | `reports/**` | Data loss | Retention window? |
| Symlink more upstream skills | `.cursor/skills/` | Discovery vs token cost | Which daily stack? |

---

## Intentionally kept (looked redundant but isn't)

| Path | Why kept |
|------|----------|
| `review-portfolio` vs `robinhood-portfolio-review` | Different workflows |
| Robinhood sync + MCP hybrid | Portfolios A vs B/C per `decisions.md` |
| `economic-calendar-fetcher` | Upstream; use `fred_calendar.py` |
| `thesis_ingest.py` | Screener JSON only; ≠ `/log-positions` |
| Chart skill refs under `.cursor/skills/*/references/` | Contracts/rubrics; commands link in |
| `config/agentic_copilot.yaml` absent | Gitignored user copy of `.example` |

---

## Not in scope

- Upstream skill body rewrites
- Merging portfolio review workflows
- Removing Robinhood hybrid stack
- Bulk `reports/` deletion
- `docs/` / `CLAUDE.md` / `launchd/` removal
- Committing unless user asks

---

## Execution log

| Batch | Status | Changes |
|-------|--------|---------|
| 1 — indexes + docs | **Done** 2026-08-10 | `commands/README.md`, `commands-workflows.mdc`, `.cursor/skills/README.md`, `cursor-integration.md`, `codebase-cleanup.md` keep-list |
| 2 — archive migrator | **Done** 2026-08-10 | `scripts/migrate_reports_layout.py` → `scripts/archive/`; archive README updated |

Validation after each batch:

```bash
pre-commit run --all-files
uv run python3 -m pytest scripts/tests/ -v
```
