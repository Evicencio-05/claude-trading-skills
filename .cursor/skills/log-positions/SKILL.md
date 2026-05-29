---
name: log-positions
description: >-
  Log Robinhood-synced positions into trader-memory-core with thesis questions.
  Use after robinhood_sync.py or when the user asks to log positions, register
  theses, or update position memory.
---

# Log Positions

Follow [commands/log-positions.md](../../../commands/log-positions.md).

**Prerequisite:** Run sync first if needed:

```bash
uv run python3 scripts/robinhood_sync.py
```

Then complete the four thesis questions per position as specified in the command file.
