---
name: update-research
description: >-
  Refresh an existing ticker research report with new data while preserving
  structure. Use when the user asks to update research, refresh a report, or
  re-run analysis on a ticker with a prior report.
---

# Update Research

Follow [commands/update-research.md](../../../commands/update-research.md).

Replace `{TICKER}` with the user's symbol.

## Pre-flight (zero LLM cost)

```bash
uv run python3 scripts/research_preflight.py --ticker {TICKER}
```

Read `reports/logs/research_preflight_{TICKER}_{YYYY-MM-DD}.json` before Step 2. If `market_context` action is `run`, run `uv run python3 scripts/pre_market.py` and re-run preflight.

Reuse/run artifact paths resolve under category dirs in [`scripts/report_paths.py`](../../../scripts/report_paths.py) (see [trading-pipeline-checklist § Output quick-ref](../../../project-docs/trading-pipeline-checklist.md#output-quick-ref)).

Read the latest `reports/research/{TICKER}_*.md` in Step 1 before collecting new data.
