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

- `paper_open` is a recorded option intent: weekly or shorter, ATM to slightly ITM, sized for 0. Expiry is this Friday for a Monday–Wednesday decision and the next Friday for Thursday–Sunday.
- `armed_wait` and `watch` are alerts at the test. They are not fills.
- `flat` / `stale` means no position and no alert.
- Invalidation is the nearest fib / volume-shelf / SMA / trendline / S/R cluster against the trade when the operator chart is on file.
- A long with RSI white under 50, a 4H fight, or a target smaller than a negative node in the path stays a watch.
- The markdown lists the TradingView condition (`Crossing up` / `Crossing down`) beside the Robinhood `create_alert` level. Create those alerts only when the row says create.
- `reports/paper/paper_book_YYYY-MM-DD.pine` is the same live levels. Paste it on a chart and arm Any alert() function call. A stale tape has no `alert()` calls.
- A `paper_open` from an earlier book carries forward until invalidation, the target, contract expiry, the earnings open, or a newer confluence tape. A stale tape does not open a new name.

## PASS 2b — Mark fresh levels

After a fresh book exists, a quote file can advance it. Stale rows stay unchanged.

```bash
uv run python3 scripts/paper_book.py \
  --session-date YYYY-MM-DD \
  --confluence-dir reports/charts/confluence \
  --output-dir reports/paper \
  --quotes reports/paper/quotes_YYYY-MM-DD.json
```

`quotes_YYYY-MM-DD.json` is `{"TICKER": 123.45}`. `--fetch-quotes` loads the last regular-session price instead. A tagged test on `armed_wait` records `paper_open` at the level. A tagged test on `watch` records the touch and does not open. Invalidation or the target flattens an open paper position. A claim through the far side of the zone adds at that edge. A cross back through the paper entry trims the add and keeps the core. A dated earnings session flattens a carried position and does not open a new one. Stale rows ignore both sources.

Robinhood `create_alert` is sent only after the operator allows the push, the book is fresh, and the live tool schema lists the argument names. The paper book does not call an order tool.

## PASS 3 — Stop

Do not register these rows in `trader-memory-core`. They are not Portfolio A or C fills.

Do not push `create_alert` unless the operator asked, the book is fresh, and the payload is the entry, claim, invalidation, or target from that book.
