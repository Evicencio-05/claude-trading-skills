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
| Robinhood portfolio read / log positions | **Cursor** + Robinhood MCP | Skills: `robinhood-portfolio-review`, `log-positions`; see [Robinhood MCP](#robinhood-mcp) |
| Robinhood scheduled sync (Portfolio A) | **Terminal** | `robinhood_sync.py` + `robinhood-sync.timer` |
| Alpaca portfolio-manager | **Claude Code** (optional) | See [Portfolio MCP](#portfolio-mcp) below |
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
| `.cursor/skills/` | Symlinks to `skills/` plus workflow skills (`deep-research`, `log-positions`, `robinhood-portfolio-review`) |
| `.cursor/mcp.json.example` | Copy to `.cursor/mcp.json` for Robinhood MCP (gitignored) |
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

## Robinhood MCP

Official **Robinhood Agentic Trading MCP** for this fork (primary in Cursor).

| Item | Detail |
|------|--------|
| URL | `https://agent.robinhood.com/mcp/trading` |
| Setup | `bash scripts/setup_robinhood_mcp.sh` → `.cursor/mcp.json` (gitignored) |
| Cursor compat | [project-docs/reference/mcp-cursor-compat.md](project-docs/reference/mcp-cursor-compat.md) |
| Read | All accounts (positions, balances, history) |
| Trade | Agentic account only; Phase 5+ with user confirmation |
| Guide | [project-docs/reference/robinhood-mcp-integration.md](project-docs/reference/robinhood-mcp-integration.md) |
| Rules | [.cursor/rules/robinhood-mcp.mdc](.cursor/rules/robinhood-mcp.mdc) |

**Workflows:** `robinhood-portfolio-review` → `reports/portfolio_review_*.md`; `log-positions` → trader-memory-core.

## Portfolio MCP (Alpaca)

**portfolio-manager** expects Alpaca MCP (`get_positions`, `get_account_info`, …). Optional in Claude Code — not required for Robinhood workflows.

Do not duplicate API keys in committed files. Use `.env` at repo root (gitignored).

## Single source of truth

- Skill bodies: `skills/<name>/` only
- `.cursor/skills/<name>` → symlink, not a copy
- `~/.claude/skills/<name>` → symlink for Claude Code, not a forked copy

## Cost discipline

- **Cursor subscription:** code edits, refactors, test fixes
- **Anthropic API:** synthesis-heavy workflows (deep research final pass, postmortems) — see `project-docs/reference/cost-discipline.md`
- **Scripts/cron:** default for repeatable daily data — no LLM
