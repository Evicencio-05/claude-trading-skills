# Commands — Workflow Specs

Files in this directory define **multi-step workflows**, not executable code. They work in both Claude Code and Cursor.

**Daily core (TA-first):** intakes → `/ta-confluence` → optional `/agentic-copilot-trade` (Portfolio C). Deep research is on demand.

## Claude Code

Install commands per [Claude Code docs](https://docs.claude.com/en/docs/claude-code/skills). Invoke with slash syntax:

| Command | File |
|---------|------|
| `/tradewhisperer-charts [list\|TICKER]` | [tradewhisperer-charts.md](tradewhisperer-charts.md) — lists preferred |
| `/gex-vex-maps TICKER\|SPX` | [gex-vex-maps.md](gex-vex-maps.md) |
| `/operator-charts TICKER` | [operator-charts.md](operator-charts.md) |
| `/ta-confluence [candle_first\|map_first]` | [ta-confluence.md](ta-confluence.md) |
| `/agentic-copilot-trade [TICKER]` | [agentic-copilot-trade.md](agentic-copilot-trade.md) |
| `/options-flow-tail` | [options-flow-tail.md](options-flow-tail.md) |
| `/log-positions` | [log-positions.md](log-positions.md) — **A+C only** |
| `/log-trade-screenshot` | [log-trade-screenshot.md](log-trade-screenshot.md) |
| `/intraday-options` | [intraday-options.md](intraday-options.md) |
| `/review-portfolio` | [review-portfolio.md](review-portfolio.md) — research batch (optional) |
| `/options-strategy-planner TICKER` | [options-strategy-planner.md](options-strategy-planner.md) |
| `/scenario-analyzer` | [scenario-analyzer.md](scenario-analyzer.md) |
| `/deep-research AAPL` | [deep-research.md](deep-research.md) — on demand |
| `/update-research AAPL` | [update-research.md](update-research.md) — on demand |

## Cursor

| Workflow | How to invoke |
|----------|----------------|
| TradeWhisperer lists/charts | Skill `tradewhisperer-charts` — HTF: `scripts/tw_list_resolve.py` |
| GEX/VEX maps | Skill `gex-vex-maps` |
| Operator charts | Skill `operator-charts` |
| TA confluence | Skill `ta-confluence` (+ prediction log v1.5) |
| Agentic co-pilot | Skill `agentic-copilot-trade` — Portfolio C; user `confirm` |
| Options flow tail | Skill `options-flow-tail` |
| Log positions | Skill `log-positions` — A+C only; skip IRA |
| Trade screenshot backfill | Skill `log-trade-screenshot` |
| Broker snapshot (MCP) | Skill `robinhood-portfolio-review` — A+C focus |
| Deep research | Skill `deep-research` — on demand |
| Update research | [update-research.md](update-research.md) — on demand |
| Research watchlist batch | [review-portfolio.md](review-portfolio.md) — optional; not MCP snapshot |
| Others | See table in `.cursor/rules/commands-workflows.mdc` |

**Rule:** For optional deep research, use Pass 0 preflight (`scripts/research_preflight.py`) reuse-first, then Pass 1 before Pass 2. See [deep-research.md](deep-research.md).

## Editing workflows

Change the markdown in `commands/` only. Cursor skills and Claude slash commands both read these files; do not fork workflow text into multiple places.
