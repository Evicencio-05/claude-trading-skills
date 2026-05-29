# Agent Routing — Hybrid Claude + Cursor

This repo supports **two AI harnesses** over one portable core (`skills/`, `scripts/`, `reports/`, `state/`). Use the right tool for the job to control cost.

## Which tool when

| Task | Tool | Notes |
|------|------|-------|
| Edit skill Python, tests, refactors | **Cursor** | Included in Cursor subscription; use `.cursor/rules/` |
| Daily pre-market (breadth, uptrend, sector) | **Terminal** | `uv run python3 scripts/pre_market.py` — zero LLM cost |
| Screeners, thesis CLI, FRED calendar | **Terminal** | Run `skills/*/scripts/*.py` directly |
| Deep research, multi-skill synthesis | **Cursor or Claude Code** | `commands/deep-research.md` or `.cursor/skills/deep-research` |
| Chart image analysis (technical/sector/breadth) | **Cursor or Claude Code** | Invoke skill by name; provide images |
| Portfolio via Alpaca MCP | **Claude Code** (default) | See [Portfolio MCP](#portfolio-mcp) below |
| Robinhood position sync | **Terminal** | `scripts/robinhood_sync.py` then `commands/log-positions.md` |
| Automated skill-improvement PRs | **Claude CLI** | `scripts/run_skill_improvement_loop.py` |
| Scheduled automation | **systemd/cron** | IDE-independent |

## Session start (any agent)

1. [PROJECT.md](PROJECT.md)
2. [LOAD_GUIDE.md](LOAD_GUIDE.md)
3. [project-docs/STATUS.md](project-docs/STATUS.md)
4. Active phase doc only (see STATUS.md)

Cursor loads (1)–(3) automatically via `.cursor/rules/project-router.mdc`.

## Cursor-specific

| Resource | Purpose |
|----------|---------|
| `.cursor/rules/` | Always-on project router + Python conventions + command workflows |
| `.cursor/skills/` | Symlinks to `skills/` plus `deep-research` workflow skill |
| [commands/README.md](commands/README.md) | How slash commands map to Cursor |

**Invoke a skill:** Ask by name (e.g. "run market-breadth-analyzer") or reference `skills/<name>/SKILL.md`.

**Add a skill to Cursor:** `ln -sfn ../../skills/<name> .cursor/skills/<name>`

## Claude Code-specific

| Resource | Purpose |
|----------|---------|
| `~/.claude/skills/` | Global skill install (symlink from repo `skills/` preferred) |
| `commands/*.md` | Slash commands (`/deep-research`, `/log-positions`, …) |
| `.mcp.json` (gitignored) | Alpaca MCP and other servers |

Install pattern (from repo root):

```bash
ln -sfn "$(pwd)/skills/<name>" ~/.claude/skills/<name>
```

## Portfolio MCP

**portfolio-manager** expects Alpaca MCP tools (`get_positions`, `get_account_info`, …).

| Environment | Status |
|-------------|--------|
| Claude Code + `.mcp.json` | Supported — [skills/portfolio-manager/references/alpaca-mcp-setup.md](skills/portfolio-manager/references/alpaca-mcp-setup.md) |
| Cursor MCP | Optional — same Alpaca MCP server can be added in Cursor Settings → MCP if you want portfolio review in Cursor |
| No MCP | Use `scripts/robinhood_sync.py` + [commands/log-positions.md](commands/log-positions.md) for Robinhood; manual entry for other accounts |

Do not duplicate API keys in committed files. Use `.env` at repo root (gitignored).

## Single source of truth

- Skill bodies: `skills/<name>/` only
- `.cursor/skills/<name>` → symlink, not a copy
- `~/.claude/skills/<name>` → symlink for Claude Code, not a forked copy

## Cost discipline

- **Cursor subscription:** code edits, refactors, test fixes
- **Anthropic API:** synthesis-heavy workflows (deep research final pass, postmortems) — see `project-docs/reference/cost-discipline.md`
- **Scripts/cron:** default for repeatable daily data — no LLM
