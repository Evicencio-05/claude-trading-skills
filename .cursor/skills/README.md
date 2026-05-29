# Cursor Project Skills

Symlinks point at the canonical skill tree in [`skills/`](../../skills/). **Edit files under `skills/`**, not here.

## Symlinked skills (daily + research stack)

- `market-breadth-analyzer`, `uptrend-analyzer`, `sector-analyst`
- `breadth-chart-analyst`, `market-top-detector`, `ibd-distribution-day-monitor`
- `us-stock-analysis`, `technical-analyst`, `earnings-trade-analyzer`, `earnings-calendar`
- `exposure-coach`, `position-sizer`, `trader-memory-core`

## Workflow skills (repo-local)

- `deep-research` — wraps [commands/deep-research.md](../../commands/deep-research.md)
- `log-positions` — [commands/log-positions.md](../../commands/log-positions.md) (sync + MCP)
- `robinhood-portfolio-review` — MCP read-only portfolio report
- `update-research` — [commands/update-research.md](../../commands/update-research.md)

## Add another skill

From repo root:

```bash
ln -sfn ../../skills/<skill-name> .cursor/skills/<skill-name>
```

Commit the symlink. Cursor discovers `SKILL.md` inside the linked directory.

## Claude Code parity

Mirror the same symlink under `~/.claude/skills/` so both IDEs use one source tree. See [AGENTS.md](../../AGENTS.md).
