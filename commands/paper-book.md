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
2. Also read `reports/charts/operator/{TICKER}_operator_*.json`. A fresh operator plan, or one newer than that ticker's confluence, is the tape. It keeps GEX/VEX nodes from a confluence file that is still within one trading session. Older maps do not follow the new chart. A daily chart is the direction. A 4-hour or weekly plan stays a watch until the daily direction is stated. The prior session's daily chart supplies that direction when this chart does not. An older daily does not follow. Daily holding above is up. Daily holding below is down. A name the thesis puts in chop stays a watch. An explicit 4H fight withholds the scalp add and leaves the daily swing on. A missing 4H note does not block the open. A 20, 50, 100, or 200 followed by SMA is the moving average, not a price. Blue is the 20 SMA, green is the 50, orange is the 200. A chart that keys the SMA by those color names is read the same way, and a labeled period wins when both are present.
3. If the newest `as_of` is older than one trading session, say so. A stale tape is a flat book. Do not invent levels from memory.
4. Ask for the missing day-before or pre-market TA (operator charts, and GEX/VEX when you have a paste) before treating any name as live.

## PASS 2 — Record

```bash
uv run python3 scripts/paper_book.py \
  --session-date YYYY-MM-DD \
  --confluence-dir reports/charts/confluence \
  --output-dir reports/paper
```

Read `reports/paper/paper_book_YYYY-MM-DD.md`.

- `paper_open` is a recorded option intent: weekly or shorter, ATM to slightly ITM, sized for 0. Expiry is this Friday for a Monday–Wednesday decision and the next Friday for Thursday–Sunday. The fill is at the test. A level more than 3% of price past that test is the target, not a wider entry zone. A gap, a volume print, or an A/D print is confluence, not the entry.
- `armed_wait` and `watch` are alerts at the test. They are not fills.
- `flat` / `stale` means no position and no alert.
- Invalidation is the nearest fib / volume-shelf / SMA / trendline / S/R cluster against the trade when the operator chart is on file. A labeled volume-profile POC is a shelf. The price inside that cluster is the longer-timeframe fib, then the shelf, then the higher-period SMA, then the trendline. A channel note's tilde price counts as that trendline when it is labeled as a bound, rail, or midline. A newer 4-hour chart keeps daily or weekly fibs from the prior session.
- A long with RSI white under 50, white under the yellow signal, buyer_strength false, a 4H fight, price under the green 50, or a target smaller than the negative GEX in the path stays a watch. A marked buyer_strength true holds through a yellow cross. A scalp add uses the 20 and 50 SMA on the 1-minute options chart. A blank 50 price still blocks when `price_vs_sma.50` is `below`. The blue 20 and the orange 200 do not block a long that is holding the green 50.
- On a new operator chart, a starred positive king above replaces the chart target for a long, and a starred negative king below replaces it for a short, when that king is larger than the negative GEX in the path. A VEX negative does not count. A negative node at a long target is not a reverse-rug. A negative king does not become a long target.
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
