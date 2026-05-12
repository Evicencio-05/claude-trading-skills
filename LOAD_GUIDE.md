# Load Guide — For Claude Code Sessions

> Read this file after PROJECT.md at the start of every session.
> It tells you exactly what to load, when, and what to skip.
> Keeping context lean is a project non-negotiable.

## Every Session (always load these three)

1. PROJECT.md — project charter, goals, constraints
2. LOAD_GUIDE.md — this file
3. project-docs/STATUS.md — current state and blockers

## Phase-Conditional (load only the active phase doc)

| Phase | Load | Skip |
|-------|------|------|
| Phase 1 | project-docs/phase-1-audit.md | All other phase docs |
| Phase 2 | project-docs/phase-2-futures-skills.md | All other phase docs |
| Phase 3 | project-docs/phase-3-learning-loop.md | All other phase docs |
| Phase 4 | project-docs/phase-4-backtesting.md | All other phase docs |
| Phase 5 | project-docs/phase-5-live-execution.md | All other phase docs |

## Load When Relevant (on-demand only)

| File | Load when |
|------|-----------|
| project-docs/playbook.md | Planning a trade, reviewing a position, running a command |
| project-docs/audit/skills_audit.md | Checking skill status, ratings, or operational notes |
| project-docs/audit/skills_audit_detail.md | Investigating a specific skill in detail |
| project-docs/reference/lucid-rules.md | Any futures-related work |
| project-docs/reference/cost-discipline.md | Evaluating API costs or model routing |
| project-docs/reference/existing-skills-map.md | Considering building something new |
| project-docs/reference/tech-stack.md | Architecture decisions |
| project-docs/reference/risk-register.md | Risk assessment or safety review |
| decisions.md | A prior decision is being questioned or revisited |
| commands/deep-research.md | Running /deep-research |
| commands/intraday-options.md | Running /intraday-options |
| commands/update-research.md | Running /update-research |
| CLAUDE.md (specific section) | Working on a specific skill's internals only |
| commands/log-positions.md | After running robinhood_sync.py to log new positions to trader-memory-core |

## Never Load Routinely

| File/Directory | Why |
|----------------|-----|
| CLAUDE.md (full file) | 933 lines, upstream reference — load sections only |
| project-docs/audit/skills_audit_detail.md | 1200+ lines, load per-skill only |
| docs/ (any) | Jekyll site docs, not session context |
| examples/ | Reference only, Phase 3 Streamlit study |
| README.md | Upstream project README, not session context |
| skills/[name]/ (full dir) | Load specific SKILL.md only when working on that skill |

## Key Operational Facts (do not look these up elsewhere)

- Active phase: Phase 1 (check STATUS.md for current focus)
- economic-calendar-fetcher: BLOCKED — use scripts/fred_calendar.py
- exposure-coach: Schema mismatch FIXED 2026-05-10 — check STATUS.md for current state
- vcp-screener: BLOCKED on free FMP — FMP Starter upgrade pending
- market-top-detector: use --static-basket flag
- Portfolio B is a Robinhood IRA — IRA options rules apply
- AutoLiq = daily profit target hit ($625), not a rule violation
- Full operational rules: project-docs/playbook.md
