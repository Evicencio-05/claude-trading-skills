# Load Guide — For AI Sessions (Claude Code & Cursor)

> Read this file after PROJECT.md at the start of every session.
> It tells you exactly what to load, when, and what to skip.
> Keeping context lean is a project non-negotiable.
>
> **Tool routing:** See [AGENTS.md](AGENTS.md) for which IDE to use per task.
> **Product center:** TA three sources → `ta-confluence` → playbook learning. Fundamentals/deep-research = optional backup.

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
| project-docs/trading-pipeline-checklist.md | Daily/weekly/TA session / trade operator cadence |
| project-docs/playbook.md | Planning a trade, reviewing a position, playbook distill |
| `.cursor/prompts/ta-first-session.md` | Standing TA-first session instructions |
| `skills/tradewhisperer-charts/SKILL.md` or command | Ingesting TW lists/charts |
| `skills/gex-vex-maps/SKILL.md` or command | Ingesting GEX/VEX maps |
| `skills/operator-charts/SKILL.md` or command | Ingesting operator TradingView markups |
| `commands/ta-confluence.md` / skill | Fusing three sources → PLAY/WATCH/NO_TRADE |
| `commands/agentic-copilot-trade.md` | Portfolio C co-pilot place flow |
| project-docs/audit/skills_audit.md | Checking skill status, ratings, or operational notes |
| project-docs/audit/skills_audit_detail.md | Investigating a specific skill in detail |
| project-docs/reference/cost-discipline.md | Evaluating API costs or model routing |
| project-docs/reference/local-model-integration.md | Ollama setup, local LLM CLI, Cursor delegation |
| project-docs/reference/existing-skills-map.md | Considering building something new |
| project-docs/reference/tech-stack.md | Architecture decisions |
| project-docs/reference/risk-register.md | Risk assessment or safety review |
| decisions.md | A prior decision is being questioned or revisited |
| commands/deep-research.md | **Only** on PLAY, verge-of-confluence (user OK), or explicit ask |
| commands/update-research.md | Same gate as deep-research; run `scripts/research_preflight.py` first |
| commands/intraday-options.md | Running /intraday-options |
| scripts/research_preflight.py | PASS 0 manifest before gated deep/update research |
| scripts/update_stale_research.py | Zero-LLM staleness scan (optional backup watchlist hygiene) |
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
| reports/research/*.md | Load specific report only when needed (gated backup) |
| reports/logs/ | Load specific log only when needed |
| scripts/report_paths.py | Resolving artifact output dirs under `reports/` |
| project-docs/trading-pipeline-checklist.md § Output quick-ref | Full reports layout map |
| launchd/ | macOS only — use systemd on this system |
| tools/thesis-manager/ | Streamlit app — run directly, never load into context |

## Key Operational Facts (do not look these up elsewhere)

- Active phase: **Phase 1 — TA Confluence + Co-pilot** (check STATUS.md)
- Default path: TW lists → GEX/VEX → operator charts → `ta-confluence` → thesis / Agentic co-pilot
- Deep-research: PLAY / verge / explicit ask only
- economic-calendar-fetcher: BLOCKED on v3 — use scripts/fred_calendar.py (stable calendar available but FRED is primary)
- exposure-coach: Schema mismatch FIXED 2026-05-10 — check STATUS.md for current state
- vcp-screener / canslim / earnings-trade-analyzer: **optional backup** — `--universe` watchlist on Starter; full S&P 500 needs FMP Premium
- market-top-detector: works on Starter stable API (no `--static-basket` required)
- Portfolio B is a Robinhood IRA — IRA options rules apply
- Full operational rules: project-docs/playbook.md

## Cursor sessions

Same load order as above. Cursor applies `.cursor/rules/project-router.mdc` automatically.

1. Open repo in Cursor — rules load PROJECT charter constraints without pasting them each chat.
2. Read `project-docs/STATUS.md` for this week's focus (or ask the agent to read it).
3. Operator cadence: [project-docs/trading-pipeline-checklist.md](project-docs/trading-pipeline-checklist.md).
4. Prefer TA skills by name (`tradewhisperer-charts`, `gex-vex-maps`, `operator-charts`, `ta-confluence`) before deep-research.
5. Standing prompt: [`.cursor/prompts/ta-first-session.md`](.cursor/prompts/ta-first-session.md).

**Portfolio:** In Cursor, connect Robinhood MCP (see `project-docs/reference/robinhood-mcp-integration.md`). Use skills `robinhood-portfolio-review` and `log-positions`. Scheduled taxable sync still uses `robinhood_sync.py`.

## Claude Code sessions

1. Read PROJECT.md, this file, STATUS.md (same as Cursor).
2. Use slash commands in `commands/` when available (`/ta-confluence`, `/agentic-copilot-trade`, `/log-positions`).
3. Symlink `skills/<name>` → `~/.claude/skills/<name>` so the repo stays the single source of truth.
