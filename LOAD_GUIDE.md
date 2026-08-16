# Load Guide — For AI Sessions (Claude Code & Cursor)

> Read this file after PROJECT.md at the start of every session.
> It tells you exactly what to load, when, and what to skip.
> Keeping context lean is a project non-negotiable.
>
> **Tool routing:** See [AGENTS.md](AGENTS.md) for which IDE to use per task.
> **Product center:** TA three sources → `ta-confluence` → playbook learning. Fundamentals/deep-research = gated optional backup. Log **A + C** only.

## Every Session (always load these three)

1. PROJECT.md — project charter, goals, constraints
2. LOAD_GUIDE.md — this file
3. project-docs/STATUS.md — current state and blockers

## Phase-Conditional (load only the active phase doc)

| Phase | Load | Skip |
|-------|------|------|
| **Phase 1** | project-docs/phase-1-research-copilot.md (TA Confluence + Co-pilot) | All other phase docs |
| Phase 2 | project-docs/phase-2-learning-loop.md | All other phase docs |
| Phase 3 | project-docs/phase-3-agentic-execution.md | All other phase docs |

## Load When Relevant (on-demand only)

| File | Load when |
|------|-----------|
| project-docs/trading-pipeline-checklist.md | Daily/weekly/TA session / trade operator cadence |
| project-docs/playbook.md | Planning a trade, reviewing a position, playbook distill |
| `.cursor/prompts/ta-first-session.md` | Standing TA-first session instructions |
| commands/ta-confluence.md | TA fusion session (candle_first / map_first) |
| commands/tradewhisperer-charts.md · gex-vex-maps · operator-charts | Chart / list intakes |
| commands/agentic-copilot-trade.md | Agentic (C) co-pilot place flow |
| .cursor/skills/ta-confluence/references/prediction_log_v15.md | After confluence — prediction / process log |
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
| commands/options-flow-tail.md | Options flow screener → primary tail |
| scripts/research_preflight.py | PASS 0 before gated deep/update research |
| scripts/update_stale_research.py | Zero-LLM staleness scan (optional backup hygiene) |
| AGENTS.md | Choosing Cursor vs Claude Code vs terminal |
| project-docs/reference/cursor-integration.md | Cursor setup, MCP, symlinks |
| project-docs/reference/robinhood-mcp-integration.md | Robinhood Agentic MCP, portfolio review, log-positions (A+C) |
| project-docs/reference/mcp-cursor-compat.md | Cursor MCP structuredContent wrapper |
| .cursor/rules/ | Cursor auto-loads project-router; read on-demand if debugging rules |
| CLAUDE.md (specific section) | Working on a specific skill's internals only |
| commands/log-positions.md | After robinhood_sync (A) or Agentic fill (C) — **not IRA** |

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
- Deep-research: PLAY / verge / explicit ask only — not exit-blocking
- Log theses for **Portfolio A + C only** — IRA (B) logging discontinued
- Trade MCP: **Portfolio C (Agentic) only**
- economic-calendar-fetcher: use `scripts/fred_calendar.py` if macro timing matters
- vcp/canslim: optional backup — Starter + `--universe`; Premium not required for TA path
- Full operational rules: project-docs/playbook.md

## Cursor sessions

Same load order as above. Cursor applies `.cursor/rules/project-router.mdc` automatically.

1. Open repo in Cursor — rules load PROJECT charter constraints without pasting them each chat.
2. Read `project-docs/STATUS.md` for this week's focus (or ask the agent to read it).
3. Operator cadence (daily TA + posture, weekly A/C review, per-trade co-pilot): [project-docs/trading-pipeline-checklist.md](project-docs/trading-pipeline-checklist.md).
4. Prefer TA skills by name (`tradewhisperer-charts`, `gex-vex-maps`, `operator-charts`, `ta-confluence`) — see `.cursor/skills/README.md`.
5. Standing prompt: [`.cursor/prompts/ta-first-session.md`](.cursor/prompts/ta-first-session.md).
6. Gated fundamentals: `.cursor/skills/deep-research` / `update-research` only on PLAY / verge / ask.

**Portfolio:** Connect Robinhood MCP. Skills `robinhood-portfolio-review` and `log-positions` for **A + C**. Scheduled taxable sync: `robinhood_sync.py`. Do not run IRA four-questions logging.

## Claude Code sessions

1. Read PROJECT.md, this file, STATUS.md (same as Cursor).
2. Use slash commands in `commands/` (`/ta-confluence`, `/agentic-copilot-trade`, `/log-positions`).
3. Symlink `skills/<name>` → `~/.claude/skills/<name>` so the repo stays the single source of truth.
