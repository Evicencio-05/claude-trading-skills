---
name: deep-research
description: >-
  Comprehensive deep research report on a US stock ticker. Covers market
  context, competitive intelligence, financials, earnings, technicals, and
  trade planning with a Quick Glance summary. Use when the user asks for deep
  research, full ticker report, or comprehensive analysis on a symbol.
---

# Deep Research

Run the workflow in [commands/deep-research.md](../../../commands/deep-research.md).

Replace `{TICKER}` with the user's symbol (uppercase).

## Rules

1. **Pass 0 — Reuse check:** Run preflight manifest; collect per manifest (reuse-first), not blind re-runs.
2. **Pass 1 — Collect:** Execute only manifest `action=run` items plus ticker-specific always-run steps. Save new outputs under category dirs in `scripts/report_paths.py` (e.g. `reports/screeners/vcp/`). Do not write the final report yet.
3. **Pass 2 — Synthesize:** Read collected outputs only, then write the report.
4. On failure: one-sentence gap note, continue — partial data beats no report.
5. Output: `reports/research/{TICKER}_{YYYY-MM-DD}.md` (match naming in command file if specified).

## Pre-flight (zero LLM cost)

```bash
uv run python3 scripts/research_preflight.py --ticker {TICKER}
```

Add `--force-refresh` only if the user explicitly wants to ignore same-day cache.

Read `reports/logs/research_preflight_{TICKER}_{YYYY-MM-DD}.json` before Pass 1. If `market_context` action is `run`, run `uv run python3 scripts/pre_market.py` and re-run preflight.

Artifact paths in the manifest resolve via [`scripts/report_paths.py`](../../../scripts/report_paths.py) — see [trading-pipeline-checklist § Output quick-ref](../../../project-docs/trading-pipeline-checklist.md#output-quick-ref).

## Related workflows

- Update existing report: [commands/update-research.md](../../../commands/update-research.md)
- Log positions: [commands/log-positions.md](../../../commands/log-positions.md)
