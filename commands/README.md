# Commands — Workflow Specs

Files in this directory define **multi-step workflows**, not executable code. They work in both Claude Code and Cursor.

## Claude Code

Install commands per [Claude Code docs](https://docs.claude.com/en/docs/claude-code/skills). Invoke with slash syntax:

| Command | File |
|---------|------|
| `/deep-research AAPL` | [deep-research.md](deep-research.md) |
| `/update-research AAPL` | [update-research.md](update-research.md) |
| `/log-positions` | [log-positions.md](log-positions.md) |
| `/log-trade-screenshot` | [log-trade-screenshot.md](log-trade-screenshot.md) |
| `/intraday-options` | [intraday-options.md](intraday-options.md) |
| `/review-portfolio` | [review-portfolio.md](review-portfolio.md) |
| `/options-strategy-planner TICKER` | [options-strategy-planner.md](options-strategy-planner.md) |
| `/scenario-analyzer` | [scenario-analyzer.md](scenario-analyzer.md) |
| `/tradewhisperer-charts TICKER` | [tradewhisperer-charts.md](tradewhisperer-charts.md) |
| `/gex-vex-maps TICKER\|SPX` | [gex-vex-maps.md](gex-vex-maps.md) |
| `/operator-charts TICKER` | [operator-charts.md](operator-charts.md) |
| `/ta-confluence [candle_first\|map_first]` | [ta-confluence.md](ta-confluence.md) |
| `/agentic-copilot-trade [TICKER]` | [agentic-copilot-trade.md](agentic-copilot-trade.md) |
| `/options-flow-tail` | [options-flow-tail.md](options-flow-tail.md) |

## Cursor

| Workflow | How to invoke |
|----------|----------------|
| Deep research | Skill: `.cursor/skills/deep-research` — or ask "deep research on AAPL" (`.cursor/rules/commands-workflows.mdc` links here) |
| Update research | Ask to follow [update-research.md](update-research.md) |
| Log positions | Skill `log-positions` — after sync and/or Robinhood MCP fetch |
| Trade screenshot backfill | Skill `log-trade-screenshot` — paste Robinhood confirmation images |
| Broker snapshot (MCP) | Skill `robinhood-portfolio-review` — live balances/positions; weekly before Agentic trades |
| TradeWhisperer charts | Skill `tradewhisperer-charts` — [tradewhisperer-charts.md](tradewhisperer-charts.md) |
| GEX/VEX maps | Skill `gex-vex-maps` — [gex-vex-maps.md](gex-vex-maps.md) |
| Operator charts | Skill `operator-charts` — [operator-charts.md](operator-charts.md) |
| TA confluence | Skill `ta-confluence` — [ta-confluence.md](ta-confluence.md) |
| Agentic co-pilot | Skill `agentic-copilot-trade` — [agentic-copilot-trade.md](agentic-copilot-trade.md) |
| Options flow tail | Skill `options-flow-tail` — [options-flow-tail.md](options-flow-tail.md) |
| Research watchlist batch | [review-portfolio.md](review-portfolio.md) — staleness &gt;14d → `/update-research`; not the MCP snapshot |
| Others | See table in `.cursor/rules/commands-workflows.mdc` |

**Rule:** For deep research, use Pass 0 preflight (`scripts/research_preflight.py`) reuse-first, then complete Pass 1 collection before writing the report in Pass 2. See [deep-research.md](deep-research.md).

## Editing workflows

Change the markdown in `commands/` only. Cursor skills and Claude slash commands both read these files; do not fork workflow text into multiple places.
