# Agent Routing — Hybrid Claude + Cursor

This repo supports **two AI harnesses** over one portable core (`skills/`, `scripts/`, `reports/`, `state/`). Use the right tool for the job to control cost.

## Which tool when

| Task | Tool | Notes |
|------|------|-------|
| Edit skill Python, tests, refactors | **Cursor** | Included in Cursor subscription; use `.cursor/rules/` |
| Daily pre-market (breadth, uptrend, sector) | **Terminal** | `uv run python3 scripts/pre_market.py` — zero LLM cost; posture **context** |
| TA session (TW / GEX / operator → confluence) | **Cursor or Claude Code** | `commands/ta-confluence.md` + intake skills; primary daily loop |
| Agentic co-pilot place (Portfolio C) | **Cursor** + Robinhood MCP | `commands/agentic-copilot-trade.md` — user `confirm` |
| Research preflight (optional) | **Terminal** | `uv run python3 scripts/research_preflight.py --ticker TICKER` |
| Screeners, thesis CLI, FRED calendar | **Terminal** | On demand — not daily core |
| Deep research (optional fundamentals) | **Cursor or Claude Code** | Pass 0 preflight first; then `commands/deep-research.md` |
| Chart image analysis (technical/sector/breadth) | **Cursor or Claude Code** | Invoke skill by name; provide images |
| Robinhood portfolio read / log A+C | **Cursor** + Robinhood MCP | Skills: `robinhood-portfolio-review`, `log-positions` (skip IRA) |
| Robinhood scheduled sync (Portfolio A) | **Terminal** | `robinhood_sync.py` + `robinhood-sync.timer` |
| Alpaca portfolio-manager | **Claude Code** (optional) | See [Portfolio MCP](#portfolio-mcp) below |
| Automated skill-improvement PRs | **Claude CLI** | `scripts/run_skill_improvement_loop.py` |
| Bulk text / retro draft / edge hints | **Terminal + Ollama** | `scripts/local_llm_cli.py` — see [local-model-integration.md](project-docs/reference/local-model-integration.md) |
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
| `.cursor/skills/` | Symlinks to `skills/` plus fork-local workflow dirs (see [.cursor/skills/README.md](.cursor/skills/README.md)) |
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
| Read | All accounts (discovery OK) |
| Trade | Agentic (C) only; Phase 3B+ with user confirmation |
| Log | Portfolio A + C only — **skip IRA (B)** |
| Guide | [project-docs/reference/robinhood-mcp-integration.md](project-docs/reference/robinhood-mcp-integration.md) |
| Rules | [.cursor/rules/robinhood-mcp.mdc](.cursor/rules/robinhood-mcp.mdc) |

**Workflows:** `robinhood-portfolio-review` → `reports/portfolio/portfolio_review_*.md`; `log-positions` → trader-memory-core.

## Portfolio MCP (Alpaca)

**portfolio-manager** expects Alpaca MCP (`get_positions`, `get_account_info`, …). Optional in Claude Code — not required for Robinhood workflows.

Do not duplicate API keys in committed files. Use `.env` at repo root (gitignored).

## Single source of truth

- Upstream skill bodies: `skills/<name>/` only
- `.cursor/skills/<name>` → symlink to `../../skills/<name>` when mirroring an upstream skill
- Fork-local workflow skills (no `skills/` twin) live as real dirs under `.cursor/skills/` and link to `commands/` — see [.cursor/skills/README.md](.cursor/skills/README.md)
- `~/.claude/skills/<name>` → symlink for Claude Code, not a forked copy

## Cost discipline

- **Cursor subscription:** code edits, refactors, test fixes
- **Anthropic API:** synthesis-heavy workflows (deep research final pass, postmortems) — see `project-docs/reference/cost-discipline.md`
- **Scripts/cron:** default for repeatable daily data — no LLM

## Cursor Cloud specific instructions

Dependencies are installed by the startup update script (`uv sync --extra dev` + `npm install`); `uv` lives at `~/.local/bin` and is on PATH in login shells. Run everything through `uv run` (e.g. `uv run python3 scripts/pre_market.py`). This is a **scripts-only** Python project (no installable package, no long-running server) — "running the app" means invoking `scripts/*.py` or `skills/*/scripts/*.py` CLIs.

- **Tests — use the per-skill runner:** `bash scripts/run_all_tests.sh` (the pre-push gate). A single bulk `uv run pytest` over all `testpaths` fails at *collection* because skills share module basenames (`utils.py`, `scorer.py`, `helpers.py`); the `tools/thesis-manager` tests under `scripts/tests` are the usual trigger. Run one directory at a time (e.g. `uv run pytest skills/vcp-screener/scripts/tests -q`) or use the runner. `theme-detector` and `canslim-screener` are intentionally skipped (need optional `bs4`/extra deps).
- **Lint parity:** CI and pre-commit pin **ruff 0.9.6**, but `uv sync` installs a newer ruff that can report spurious `ruff format` diffs. For CI-accurate results run `uvx ruff@0.9.6 check skills/ scripts/` and `uvx ruff@0.9.6 format --check skills/ scripts/`. Codespell: `uv run codespell --toml pyproject.toml skills/ scripts/`.
- **Local Python is 3.12** though CI targets 3.9 (`ruff target-version = py39`); keep code 3.9-compatible.
- **Fastest end-to-end smoke test (no keys):** `uv run python3 scripts/pre_market.py --dry-run --force` — computes the daily breadth/uptrend/sector posture from free public data (needs outbound network; drop `--dry-run` to write `reports/logs/`).
- **API keys are optional for most dev/testing:** offline tools (`position-sizer`, `data-quality-checker`, `edge-*`, `trader-memory-core` core, most fixture-backed tests) need none. FMP-backed screeners need `FMP_API_KEY`; Robinhood MCP / FINVIZ / Alpaca need their own creds. Provide via repo-root `.env` (gitignored) or env vars.
