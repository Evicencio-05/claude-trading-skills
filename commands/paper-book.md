---
description: "Record a paper options book from the latest TA confluence. No brokerage orders."
argument-hint: "[YYYY-MM-DD]"
---

# Paper book

> **Record only.** Do not call Robinhood `place_equity_order`, `place_option_order`, or `review_*` from this workflow.
>
> Robinhood Agentic executes live orders on Portfolio C. MCP trade approvals default off for external agents, so a connected session can place real orders unless approvals are on. This book never does that.
>
> Alerts are unpushed `create_alert` payloads. Push them only after the operator confirms a fresh book and asks for alerts.

Replace the session date with the trading session being recorded. Default it to today (US/Eastern) when the operator omits it.

## PASS 1 — Tape

1. Read the latest `reports/charts/confluence/{TICKER}_confluence_*.json` files.
2. If the newest `as_of` is older than one trading session, say so. A stale tape is a flat book. Do not invent levels from memory.
3. Ask for the missing day-before or pre-market TA (TradeWhisperer lists, GEX/VEX, operator charts) before treating any name as live.

## PASS 2 — Record

```bash
uv run python3 scripts/paper_book.py \
  --session-date YYYY-MM-DD \
  --confluence-dir reports/charts/confluence \
  --output-dir reports/paper
```

Read `reports/paper/paper_book_YYYY-MM-DD.md`.

- `paper_open` is a recorded option intent: weekly or shorter, ATM to slightly ITM, sized for 0.
- `armed_wait` and `watch` are alerts at the test. They are not fills.
- `flat` / `stale` means no position and no alert.

## PASS 3 — Stop

Do not register these rows in `trader-memory-core`. They are not Portfolio A or C fills.

Do not push `create_alert` unless the operator asked, the book is fresh, and the payload is the entry, invalidation, or target from that book.
