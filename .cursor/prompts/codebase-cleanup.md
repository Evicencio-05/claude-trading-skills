# Codebase Cleanup — Overlap & Dead Code Audit

## Goal
Audit this fork for duplicated workflows, forked copies, stale docs, and unused code; produce a prioritized cleanup plan and execute **safe, approved removals only** — no behavior changes without tests.

## Inputs
- Scope: whole repo (default) or user-specified path
- Mode: `audit-only` (default) or `audit-and-fix` (user must approve each deletion batch)

## Pre-flight
- [ ] Read `PROJECT.md`, `LOAD_GUIDE.md`, `project-docs/STATUS.md`, `PENDING_WORK.md`, `decisions.md`
- [ ] Read `AGENTS.md` § Single source of truth
- [ ] Confirm active phase: **Phase 1 — Research + Co-Pilot** per `project-docs/STATUS.md` (no upstream skill rewrites except fixes logged in `decisions.md`)

## Phase 1 — Inventory (read-only)

Map every overlap category. For each finding, record: **path**, **duplicate of**, **keep/delete/merge**, **risk**.

### A. Workflow & skill overlap
- Compare `commands/*.md` vs `.cursor/skills/*/SKILL.md` — workflow logic must live in `commands/`; skills are thin wrappers only
- Flag skills that **copy** Pass 1/Pass 2 steps instead of linking (see `commands/deep-research.md` as the pattern)
- Distinguish similarly named workflows:
  - `commands/review-portfolio.md` = research watchlist batch update
  - `robinhood-portfolio-review` = live broker snapshot via MCP/CLI
- Check `.cursor/rules/commands-workflows.mdc` routing table matches actual files

### B. `.cursor/skills/` integrity
```bash
ls -la .cursor/skills/
```
- **Keep as directories (fork-local wrappers):** any skill that has no twin under `skills/` — currently `deep-research`, `log-positions`, `log-trade-screenshot`, `robinhood-portfolio-review`, `update-research`, `tradewhisperer-charts`, `gex-vex-maps`, `operator-charts`, `ta-confluence`, `agentic-copilot-trade`, `options-flow-tail` (see `.cursor/skills/README.md`)
- **Must be symlinks:** every entry that mirrors `skills/<name>` → `../../skills/<name>`
- Flag any **copied** upstream skill trees under `.cursor/skills/` (directory that also exists under `skills/` and is not a symlink)

### C. Robinhood / MCP script overlap
Review for duplicate responsibilities:
- `scripts/robinhood_sync.py` — scheduled Portfolio A (robin_stocks)
- `scripts/robinhood_mcp.py` — CLI data plane (accounts, positions, ingest-pending)
- `scripts/robinhood_mcp_client.py` — MCP client library
- `scripts/robinhood_accounts.py` — account map from YAML
- `scripts/mcp_stdio_structured_content_proxy.py` — Cursor compat proxy
- `config/robinhood_accounts.yaml` — canonical account map

Per `decisions.md`: ingest lives in `robinhood_mcp.py ingest-pending` — flag any superseded ingest scripts or docs referencing them.

### D. Documentation overlap
| Canonical | May duplicate |
|-----------|---------------|
| `PROJECT.md` | charter only |
| `LOAD_GUIDE.md` | load order only |
| `AGENTS.md` | tool routing only |
| `.cursor/rules/project-router.mdc` | short router; must not re-copy full charter |
| `project-docs/STATUS.md` | current focus/blockers |
| `PENDING_WORK.md` | task queue (not skill docs) |
| `decisions.md` | binding architecture decisions |
| `commands/README.md` | command index |

Flag: stale cross-links, duplicate Robinhood setup instructions, docs that repeat `LOAD_GUIDE.md` "never load" lists inline.

**Do not delete:** `docs/` (Jekyll upstream site), `CLAUDE.md` (upstream reference), `launchd/` (macOS reference per `decisions.md`).

### E. Dead / unnecessary files
- Untracked or orphaned scripts with zero imports and no references in docs/skills
- Stale reports under `reports/` (list only — do not delete without user approval)
- `package.json` / `package-lock.json` — required for `mcp-remote`; do not remove unless MCP setup moves elsewhere
- macOS-only paths referenced on Linux host — note, don't delete reference files

### F. Fork policy check
Before proposing changes under `skills/<name>/`:
- Is this a **fix** listed in `decisions.md`? If not → **defer** (extend via wrapper/command, not upstream edit)
- Never write `state/theses/` directly — only via `thesis_store.py`

## Phase 2 — Deliverable

Write audit report to `reports/meta/codebase_cleanup_audit_YYYY-MM-DD.md`:

```markdown
# Codebase Cleanup Audit — YYYY-MM-DD

## Summary
- Findings: N (P0 / P1 / P2)
- Estimated deletions: X files, Y lines
- Estimated merges: Z

## P0 — Safe now (no behavior change)
| Action | Path | Reason | Verified by |
|--------|------|--------|-------------|

## P1 — Merge / consolidate (small edits)
| Action | From → To | Reason |

## P2 — Needs approval (behavior or upstream touch)
| Action | Path | Risk | Ask user |

## Intentionally kept (looked redundant but isn't)
| Path | Why kept |

## Not in scope
- [List deferred items]
```

## Phase 3 — Execute (only if user said `audit-and-fix`)

Apply **P0 only** in one PR-sized batch:
1. Remove dead files confirmed by grep + pytest
2. Consolidate docs: replace duplication with links to canonical file
3. Fix broken symlinks under `.cursor/skills/`
4. Update index files: `commands/README.md`, `.cursor/skills/README.md`, `commands-workflows.mdc` if routing changed

After each batch:
```bash
pre-commit run --all-files
uv run python3 -m pytest scripts/tests/ -v
```

## Rules
- **Audit before delete** — grep for imports, doc links, and skill references
- **One source of truth** — merge into canonical path, leave a link at most one hop away
- **No secrets** — never commit `.cursor/mcp.json`, `.env`, credentials
- **No upstream skill rewrites** without explicit user approval + `decisions.md` entry
- On ambiguity: list in P2 and ask — do not guess

## Do not
- Delete `skills/`, `state/theses/`, or user reports without explicit approval
- Merge `review-portfolio` and `robinhood-portfolio-review` (different workflows)
- Remove Robinhood hybrid stack (`sync` + `mcp` serve different portfolios per `decisions.md`)
- Commit cleanup changes unless user explicitly asks
- Refactor working code for style during cleanup

## After run
Paste [prompt-complete.md](prompt-complete.md) with `codebase-cleanup.md`.
