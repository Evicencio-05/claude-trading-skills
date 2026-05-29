---
name: deep-research
description: >-
  Comprehensive deep research report on a US stock ticker. Covers market
  context, competitive intelligence, financials, earnings, technicals, and
  trade planning with a Quick Glance summary. Use when the user asks for deep
  research, full ticker report, or comprehensive analysis on a symbol.
---

# Deep Research

Run the two-pass workflow in [commands/deep-research.md](../../../commands/deep-research.md).

Replace `{TICKER}` with the user's symbol (uppercase).

## Rules

1. **Pass 1 — Collect:** Run every applicable skill and script listed in the command file. Save outputs under `reports/`. Do not write the final report yet.
2. **Pass 2 — Synthesize:** Read collected outputs only, then write the report.
3. On failure: one-sentence gap note, continue — partial data beats no report.
4. Output: `reports/research/{TICKER}_{YYYY-MM-DD}.md` (match naming in command file if specified).

## Pre-flight (zero LLM cost)

If today's market context is missing, run:

```bash
uv run python3 scripts/pre_market.py
```

Read `reports/logs/market_context_YYYY-MM-DD.md` before Pass 1 market-context steps.

## Related workflows

- Update existing report: [commands/update-research.md](../../../commands/update-research.md)
- Log positions: [commands/log-positions.md](../../../commands/log-positions.md)
