# Cursor Project Skills

Two kinds of entries live here:

1. **Upstream / shared skills** — symlinks into [`skills/`](../../skills/). Edit under `skills/`, not the symlink.
2. **Fork workflow skills** — real directories under `.cursor/skills/` (no `skills/` copy). Edit here; authoritative steps live in [`commands/`](../../commands/).

## Symlinked skills (daily + research stack)

- `market-breadth-analyzer`, `uptrend-analyzer`, `sector-analyst`
- `breadth-chart-analyst`, `market-top-detector`, `ibd-distribution-day-monitor`
- `us-stock-analysis`, `technical-analyst`, `earnings-trade-analyzer`, `earnings-calendar`
- `exposure-coach`, `position-sizer`, `trader-memory-core`

## Workflow skills (fork-local under `.cursor/skills/`)

| Skill | Status | Command |
|-------|--------|---------|
| `deep-research` | Active | [deep-research.md](../../commands/deep-research.md) |
| `log-positions` | Active | [log-positions.md](../../commands/log-positions.md) |
| `log-trade-screenshot` | Active | [log-trade-screenshot.md](../../commands/log-trade-screenshot.md) |
| `robinhood-portfolio-review` | Active | MCP portfolio report |
| `update-research` | Active | [update-research.md](../../commands/update-research.md) |
| `tradewhisperer-charts` | Contract active | [tradewhisperer-charts.md](../../commands/tradewhisperer-charts.md) |
| `gex-vex-maps` | Contract active | [gex-vex-maps.md](../../commands/gex-vex-maps.md) |
| `operator-charts` | Contract active | [operator-charts.md](../../commands/operator-charts.md) |
| `ta-confluence` | Active (candle_first / map_first) | [ta-confluence.md](../../commands/ta-confluence.md) |
| `agentic-copilot-trade` | Co-pilot gates (confirm before place) | [agentic-copilot-trade.md](../../commands/agentic-copilot-trade.md) |
| `options-flow-tail` | Active (user-supplied screener) | [options-flow-tail.md](../../commands/options-flow-tail.md) |

## Add a symlinked upstream skill

From repo root:

```bash
ln -sfn ../../skills/<skill-name> .cursor/skills/<skill-name>
```

Commit the symlink. Cursor discovers `SKILL.md` inside the linked directory.

## Claude Code parity

For symlinked skills, mirror under `~/.claude/skills/`. Fork workflow skills are invoked via `commands/*.md` in both harnesses. See [AGENTS.md](../../AGENTS.md).
