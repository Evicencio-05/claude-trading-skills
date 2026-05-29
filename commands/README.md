# Commands — Workflow Specs

Files in this directory define **multi-step workflows**, not executable code. They work in both Claude Code and Cursor.

## Claude Code

Install commands per [Claude Code docs](https://docs.claude.com/en/docs/claude-code/skills). Invoke with slash syntax:

| Command | File |
|---------|------|
| `/deep-research AAPL` | [deep-research.md](deep-research.md) |
| `/update-research AAPL` | [update-research.md](update-research.md) |
| `/log-positions` | [log-positions.md](log-positions.md) |
| `/intraday-options` | [intraday-options.md](intraday-options.md) |
| `/review-portfolio` | [review-portfolio.md](review-portfolio.md) |
| `/scenario-analyzer` | [scenario-analyzer.md](scenario-analyzer.md) |

## Cursor

| Workflow | How to invoke |
|----------|----------------|
| Deep research | Skill: `.cursor/skills/deep-research` — or ask "deep research on AAPL" (`.cursor/rules/commands-workflows.mdc` links here) |
| Update research | Ask to follow [update-research.md](update-research.md) |
| Log positions | Skill `log-positions` — after sync and/or Robinhood MCP fetch |
| Portfolio review | Skill `robinhood-portfolio-review` (requires Robinhood MCP) |
| Others | See table in `.cursor/rules/commands-workflows.mdc` |

**Rule:** For deep research, always use the two-pass flow in [deep-research.md](deep-research.md) — collect everything in Pass 1 before writing the report in Pass 2.

## Editing workflows

Change the markdown in `commands/` only. Cursor skills and Claude slash commands both read these files; do not fork workflow text into multiple places.
