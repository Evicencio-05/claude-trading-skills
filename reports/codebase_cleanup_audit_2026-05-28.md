# Codebase Cleanup Audit — 2026-05-28

**Mode:** audit-only (no deletions executed)
**Phase:** 1 — Audit & Activate
**Scope:** Whole repo

## Summary

| Metric | Count |
|--------|-------|
| Findings | **18** (P0: 4 / P1: 7 / P2: 7) |
| Estimated safe deletions | **2 scripts** (~800 lines) — after user confirms one-shots are done |
| Estimated doc edits | **~6 files** (links/index fixes, no behavior change) |
| Estimated merges | **1** (scenario-analyzer workflow — deferred, upstream touch) |

**Overall health:** Workflow architecture is sound. Thin-wrapper pattern is correctly applied for `deep-research`, `log-positions`, and `update-research`. Main gaps are **orphan one-shot scripts**, **routing table omissions**, **scenario-analyzer duplication**, and **one stale setup doc line**.

---

## A. Workflow & skill overlap

| Path | Duplicate of | Action | Risk |
|------|--------------|--------|------|
| `.cursor/skills/deep-research/SKILL.md` | `commands/deep-research.md` | **Keep** — thin wrapper (36 lines, links only) | None |
| `.cursor/skills/log-positions/SKILL.md` | `commands/log-positions.md` | **Keep** — thin wrapper (28 lines) | None |
| `.cursor/skills/update-research/SKILL.md` | `commands/update-research.md` | **Keep** — thin wrapper (13 lines) | None |
| `.cursor/skills/robinhood-portfolio-review/SKILL.md` | — (no `commands/` file) | **Keep** — distinct from `review-portfolio`; skill-only broker snapshot (79 lines) | Low — optional P2: add `commands/robinhood-portfolio-review.md` for parity |
| `commands/review-portfolio.md` | — | **Keep** — research watchlist batch refresh | None — do not merge with MCP review |
| `commands/scenario-analyzer.md` | `skills/scenario-analyzer/SKILL.md` | **Merge** (P2) — 104 vs 339 lines; both embed workflow; skill is Japanese, command is abbreviated | Medium — upstream skill edit deferred in `decisions.md` |
| `commands/options-strategy-planner.md` | — | **Keep** — valid workflow; missing from indexes only | None |
| `commands/intraday-options.md` | — | **Keep** — in routing table | None |

**Pass 1/Pass 2 fork check:** No skill copies the deep-research two-pass body inline. `trade-hypothesis-ideator` uses its own "Pass 1/2" naming (different skill, not a fork).

**Routing table vs files:**

| File | In `commands-workflows.mdc`? | In `commands/README.md`? |
|------|------------------------------|--------------------------|
| `deep-research.md` | Yes | Yes |
| `update-research.md` | Yes | Yes |
| `log-positions.md` | Yes | Yes |
| `intraday-options.md` | Yes | Yes |
| `review-portfolio.md` | Yes | Yes |
| `scenario-analyzer.md` | Yes | Yes |
| `options-strategy-planner.md` | **No** | **No** |
| `robinhood-portfolio-review` (skill) | Yes | Yes (Cursor row) |

**Naming confusion (document, don't merge):** `commands/README.md` Cursor row says "Portfolio review" → `robinhood-portfolio-review`, while Claude table has `/review-portfolio` for research batch. Add explicit labels in README.

---

## B. `.cursor/skills/` integrity

```text
Symlinks (10): breadth-chart-analyst, earnings-calendar, earnings-trade-analyzer,
  exposure-coach, ibd-distribution-day-monitor, market-breadth-analyzer,
  market-top-detector, position-sizer, sector-analyst, technical-analyst,
  trader-memory-core, uptrend-analyzer, us-stock-analysis

Wrapper dirs (4): deep-research, log-positions, update-research, robinhood-portfolio-review

Broken symlinks: none
Copied skill trees under .cursor/skills/: none
```

| Path | Duplicate of | Action | Risk |
|------|--------------|--------|------|
| 10 symlinks → `skills/<name>/` | Canonical `skills/` | **Keep** | None |
| 4 wrapper directories | `commands/` (+ CLI notes for RH review) | **Keep** per AGENTS.md | None |
| 41 skills not symlinked in Cursor | N/A | **Keep** — intentional subset; invoke by path or add symlinks on demand | None |

---

## C. Robinhood / MCP script overlap

| Path | Role | Action | Risk |
|------|------|--------|------|
| `scripts/robinhood_sync.py` | Scheduled Portfolio A → `pending_ingest.json` | **Keep** | — |
| `scripts/robinhood_mcp.py` | CLI: accounts, positions, `ingest-pending` | **Keep** | — |
| `scripts/robinhood_mcp_client.py` | Library for MCP subprocess | **Keep** | — |
| `scripts/robinhood_accounts.py` | YAML account map loader | **Keep** | — |
| `scripts/mcp_stdio_structured_content_proxy.py` | Cursor `structuredContent` compat | **Keep** | — |
| `scripts/run_robinhood_mcp_stdio.sh` | Stdio launcher (used by client, not Cursor URL) | **Keep** | — |
| `config/robinhood_accounts.yaml` | Canonical account map | **Keep** | — |
| `scripts/setup_robinhood_mcp.sh` | One-time setup | **Keep** | — |

**Superseded ingest scripts:** None found. `decisions.md` / `PENDING_WORK.md` confirm `ingest-pending` replaced any separate ingest script; grep shows no stale references.

**Hybrid stack:** Intentionally dual-path per `decisions.md` (A=sync, B/C=MCP). Do not consolidate.

---

## D. Documentation overlap

| Path | Issue | Action | Risk |
|------|-------|--------|------|
| `project-docs/reference/cursor-integration.md` §2 | Says every `.cursor/skills/` entry should symlink to `skills/` — **false** for 4 wrapper dirs | **Merge** → one sentence: wrappers + symlinks | None |
| `commands/README.md` | "Portfolio review" row ambiguous vs `/review-portfolio` | **Merge** → rename rows: "Broker snapshot (MCP)" vs "Research watchlist batch" | None |
| `.cursor/rules/commands-workflows.mdc` | Missing `options-strategy-planner` | **Merge** → add row | None |
| Robinhood setup | Repeated in `robinhood-mcp-integration.md`, `cursor-integration.md`, `setup_robinhood_mcp.sh`, `robinhood-mcp.mdc` | **Keep** — canonical = `robinhood-mcp-integration.md`; others should link, not copy full steps | Low |
| `project-router.mdc` vs `PROJECT.md` | Short charter repeat | **Keep** — by design for always-on context | None |
| `LOAD_GUIDE.md` "never load" list | Repeated in router | **Keep** — acceptable one-hop summary | None |
| `skills/scenario-analyzer/SKILL.md` | Japanese output; `commands/scenario-analyzer.md` also Japanese | **Keep** until rewrite; track in P2 | — |
| `phase-1-audit.md` | Still mentions `thesis_ingest.py` for position logging | **Merge** → align with `log-positions` / `thesis_store.register` | Low |

**Do not delete:** `docs/`, `CLAUDE.md`, `launchd/` (macOS reference per `decisions.md`).

---

## E. Dead / unnecessary files

| Path | Duplicate of | Action | Risk |
|------|--------------|--------|------|
| `scripts/log_manual_positions.py` | One-shot IRA/Lucid backfill (2026-05-09/10); **0 repo references** | **Delete** or move to `scripts/archive/` after user confirms backfill complete | **Medium** — re-run could duplicate theses |
| `scripts/normalize_research_filenames.py` | One-time filename migration; **0 references** | **Delete** or archive after user confirms migration done | **Low** |
| `package.json` + `package-lock.json` | `mcp-remote` dep for Robinhood bridge | **Keep** | — |
| `reports/` (102 files, ~1.1 MB) | User artifacts | **List only** — no delete without approval | — |
| `.cursor/prompts/` (untracked) | Meta prompts (`codebase-cleanup`, `prompt-engine`) | **Keep** — commit when user wants (not dead) | — |
| `launchd/*.plist` | macOS reference on Arch host | **Keep** per `decisions.md` | — |

---

## F. Fork policy check

- No proposed edits under `skills/<name>/` except **scenario-analyzer** thin-wrapper refactor (needs `decisions.md` entry + approval).
- `log-positions` correctly forbids `thesis_ingest.py` for manual/MCP positions; `phase-1-audit.md` checklist is stale on this point.

---

## P0 — Safe now (no behavior change)

| Action | Path | Reason | Verified by |
|--------|------|--------|-------------|
| Archive or delete | `scripts/normalize_research_filenames.py` | One-time migration utility; zero imports/refs | `rg` repo-wide |
| Archive or delete | `scripts/log_manual_positions.py` | One-shot backfill; zero refs; hardcoded 2026-05-09 data | File header + `rg` |
| Fix doc line | `project-docs/reference/cursor-integration.md` | Incorrect "all symlinks" claim | `ls -la .cursor/skills/` |
| Add index rows | `commands/README.md`, `.cursor/rules/commands-workflows.mdc` | `options-strategy-planner` exists but unlisted | File listing |

**User approval needed before P0 deletes:** Confirm research filenames are normalized and IRA/Lucid backfill will not be re-run.

---

## P1 — Merge / consolidate (small edits)

| Action | From → To | Reason |
|--------|-----------|--------|
| Clarify labels | `commands/README.md` | Distinguish `review-portfolio` vs `robinhood-portfolio-review` |
| Link-only trim | `cursor-integration.md`, `AGENTS.md` | Point Robinhood setup to single canonical doc |
| Stale checklist | `project-docs/phase-1-audit.md` | Position logging via `log-positions` / `thesis_store`, not `thesis_ingest` for open positions |
| Commit prompts | `.cursor/prompts/` | Useful meta-tooling; currently untracked |

---

## P2 — Needs approval (behavior or upstream touch)

| Action | Path | Risk | Ask user |
|--------|------|------|----------|
| Thin-wrapper refactor | `skills/scenario-analyzer/SKILL.md` → link `commands/scenario-analyzer.md` | Upstream skill edit; Japanese rewrite deferred | Approve fork change + `decisions.md` entry |
| Optional command file | `commands/robinhood-portfolio-review.md` + thin skill | Consistency with other workflows | Worth it? |
| Japanese → English | `scenario-analyzer` | Output language change | Per `decisions.md` deferral |
| Prune old reports | `reports/research/`, `reports/logs/` | Data loss | Which retention window? |
| Symlink more skills | `.cursor/skills/<name>` | Token/discovery tradeoff | Which daily stack additions? |
| Re-run hooks | `pre-commit run --all-files` | STATUS exit criterion | Ready to fix any latent issues? |

---

## Intentionally kept (looked redundant but isn't)

| Path | Why kept |
|------|----------|
| `commands/review-portfolio.md` vs `robinhood-portfolio-review` | Research watchlist batch ≠ live broker snapshot |
| `robinhood_sync.py` + `robinhood_mcp.py` | Portfolio A schedule vs IRA/Agentic MCP per `decisions.md` |
| `skills/economic-calendar-fetcher/` | Upstream skill; blocked on FMP but not deleted; use `fred_calendar.py` |
| `launchd/` | macOS reference; Linux uses copied units in `~/.config/systemd/user/` |
| `package.json` | Required for `mcp-remote` in MCP hybrid stack |
| `thesis_ingest.py` | Valid for **screener JSON** ingestion; distinct from `/log-positions` |
| `tools/thesis-manager/` | Human UI for IRA; complements MCP ingest |
| 41 skills without Cursor symlinks | Cost/context discipline; add symlinks only when needed |

---

## Not in scope

- Deleting or rewriting upstream `skills/*` bodies (except approved fixes in `decisions.md`)
- Merging `review-portfolio` and `robinhood-portfolio-review`
- Removing Robinhood hybrid (sync + MCP)
- Bulk `reports/` deletion
- `docs/` Jekyll site cleanup
- Enabling `launchd` skill-improvement/generation jobs (Phase 3+)
- FMP Starter activation (cost approval)

---

## Recommended execution order (audit-and-fix)

1. **Batch 1 (docs only):** P0 index fixes + `cursor-integration.md` — no tests required beyond pre-commit.
2. **Batch 2 (archive scripts):** After your OK on migration/backfill — move to `scripts/archive/` or delete; run `pytest scripts/tests/`.
3. **Batch 3 (scenario-analyzer):** Only if you want upstream skill touch this phase.

```bash
# After each batch
pre-commit run --all-files
uv run python3 -m pytest scripts/tests/ -v
```

---

## Execution log (2026-05-28)

All three batches completed per approved plan:

| Batch | Status | Changes |
|-------|--------|---------|
| 1 | Done | `commands/README.md`, `commands-workflows.mdc`, `cursor-integration.md`, `phase-1-audit.md`; `.cursor/prompts/` staged |
| 2 | Done | `scripts/archive/log_manual_positions.py`, `scripts/archive/normalize_research_filenames.py` + README |
| 3 | Done | `skills/scenario-analyzer/SKILL.md` thin wrapper; `decisions.md` entry |

Validation: `pre-commit run --all-files` and `uv run python3 -m pytest scripts/tests/ -v` (see session output).

---

*Generated by Phase 1 inventory. Execution completed 2026-05-28.*
