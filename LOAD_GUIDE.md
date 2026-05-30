# Load Guide — For AI Sessions (Claude Code & Cursor)

> Read this file after PROJECT.md at the start of every session.
> It tells you exactly what to load, when, and what to skip.
> Keeping context lean is a project non-negotiable.
>
> **Tool routing:** See [AGENTS.md](AGENTS.md) for which IDE to use per task.

## Every Session (always load these three)

1. PROJECT.md — project charter, goals, constraints
2. LOAD_GUIDE.md — this file
3. project-docs/STATUS.md — current state and blockers

## Phase-Conditional (load only the active phase doc)

| Phase | Load | Skip |
|-------|------|------|
| **Phase 1** | project-docs/phase-1-research-copilot.md | All other phase docs |
| Phase 2 | project-docs/phase-2-learning-loop.md | All other phase docs |
| Phase 3 | project-docs/phase-3-agentic-execution.md | All other phase docs |

## Load When Relevant (on-demand only)

| File | Load when |
|------|-----------|
| project-docs/playbook.md | Planning a trade, reviewing a position, running a command |
| project-docs/audit/skills_audit.md | Checking skill status, ratings, or operational notes |
| project-docs/audit/skills_audit_detail.md | Investigating a specific skill in detail |
| project-docs/reference/cost-discipline.md | Evaluating API costs or model routing |
| project-docs/reference/existing-skills-map.md | Considering building something new |
| project-docs/reference/tech-stack.md | Architecture decisions |
| project-docs/reference/risk-register.md | Risk assessment or safety review |
| decisions.md | A prior decision is being questioned or revisited |
| commands/deep-research.md | Deep research workflow (Claude `/deep-research` or Cursor `deep-research` skill) |
| commands/intraday-options.md | Running /intraday-options |
| commands/update-research.md | Update research workflow |
| scripts/update_stale_research.py | Zero-LLM staleness scan; queue at state/research_update_queue.json |
| AGENTS.md | Choosing Cursor vs Claude Code vs terminal |
| project-docs/reference/cursor-integration.md | Cursor setup, MCP, symlinks |
| project-docs/reference/robinhood-mcp-integration.md | Robinhood Agentic MCP in Cursor, portfolio review, log-positions |
| project-docs/reference/mcp-cursor-compat.md | Cursor MCP structuredContent wrapper (Robinhood, future servers) |
| .cursor/rules/ | Cursor auto-loads project-router; read on-demand if debugging rules |
| CLAUDE.md (specific section) | Working on a specific skill's internals only |
| commands/log-positions.md | After running robinhood_sync.py to log new positions to trader-memory-core |

## Never Load Routinely

| File/Directory | Why |
|----------------|-----|
| CLAUDE.md (full file) | 933 lines, upstream reference — load sections only |
| project-docs/archive/ | Superseded futures/Lucid docs — historical only |
| project-docs/audit/skills_audit_detail.md | 1200+ lines, load per-skill only |
| docs/ (any) | Jekyll site docs, not session context |
| examples/ | Reference only, Phase 2 Streamlit study |
| README.md | Upstream project README, not session context |
| skills/[name]/ (full dir) | Load specific SKILL.md only when working on that skill |
| reports/research/*.md | Load specific report only when needed |
| reports/logs/ | Load specific log only when needed |
| launchd/ | macOS only — use systemd on this system |
| tools/thesis-manager/ | Streamlit app — run directly, never load into context |

## Key Operational Facts (do not look these up elsewhere)

- Active phase: **Phase 1** (check STATUS.md)
- economic-calendar-fetcher: BLOCKED — use scripts/fred_calendar.py
- exposure-coach: Schema mismatch FIXED 2026-05-10 — check STATUS.md for current state
- vcp-screener: BLOCKED on free FMP — FMP Starter upgrade pending
- market-top-detector: use --static-basket flag
- Portfolio B is a Robinhood IRA — IRA options rules apply
- Full operational rules: project-docs/playbook.md

## Cursor sessions

Same load order as above. Cursor applies `.cursor/rules/project-router.mdc` automatically.

1. Open repo in Cursor — rules load PROJECT charter constraints without pasting them each chat.
2. Read `project-docs/STATUS.md` for this week's focus (or ask the agent to read it).
3. For market context before research: `uv run python3 scripts/pre_market.py` (zero LLM cost).
4. Invoke skills by name (`market-breadth-analyzer`, `deep-research on AAPL`, etc.) — see `.cursor/skills/README.md`.
5. For workflows: use `.cursor/skills/deep-research`, `update-research`, `log-positions`, or `commands/*.md` directly.

**Portfolio:** In Cursor, connect Robinhood MCP (see `project-docs/reference/robinhood-mcp-integration.md`). Use skills `robinhood-portfolio-review` and `log-positions`. Scheduled taxable sync still uses `robinhood_sync.py`.

## Claude Code sessions

1. Read PROJECT.md, this file, STATUS.md (same as Cursor).
2. Use slash commands in `commands/` when available (`/deep-research`, `/log-positions`).
3. Symlink `skills/<name>` → `~/.claude/skills/<name>` so the repo stays the single source of truth.
