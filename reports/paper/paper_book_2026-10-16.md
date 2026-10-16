# Paper book — 2026-10-16

No brokerage order was sent. Robinhood Agentic places live orders on Portfolio C,
and this book only records paper options. Alerts below are unpushed
`robinhood_create_alert` payloads.

**Open:** 0 · **Armed:** 0 · **Live alerts:** 0

## Rules encoded from the operator read

- Daily direction comes from the confluence verdict. A fresh `NO_TRADE` stays flat.
- Enter at the test (discount 40% of the zone for longs, premium 40% for shorts).
- A bar moving more than 4% does not get a paper fill.
- Add on a claim through the far side of the zone. Trim that add if price
  crosses back through the paper entry. The core stays until invalidation or the target.
- Target prefers a king node over the first fib when both are on the sketch.
- Contract is weekly or shorter, ATM to slightly ITM, sized for 0 (premium is the risk).
- Weekly expiry is this Friday for a Mon–Wed decision, and the next Friday after that.
- TA older than one trading session is stale. Stale levels do not arm and do not alert.

## This session

| Ticker | As of | Verdict | Status | Why |
|--------|-------|---------|--------|-----|
| BE | 2026-08-15 | NO_TRADE | stale | stale_ta |
| CRDO | 2026-08-09 | PLAY | stale | stale_ta |
| CRWD | 2026-08-16 | NO_TRADE | stale | stale_ta |
| HIMS | 2026-08-09 | WATCH | stale | stale_ta |
| HOOD | 2026-08-08 | NO_TRADE | stale | stale_ta |
| ONDS | 2026-08-09 | WATCH | stale | stale_ta |
| RIVN | 2026-08-10 | WATCH | stale | stale_ta |
| TSEM | 2026-08-09 | PLAY | stale | stale_ta |
| UMAC | 2026-08-09 | WATCH | stale | stale_ta |

## If that tape had been fresh

| Ticker | Shadow | Entry zone | Test / fill | Invalidation | Target |
|--------|--------|------------|-------------|--------------|--------|
| BE | flat | 228-232 | - | 220.7 | 250 |
| CRDO | armed_wait | 240-250 | 240 | 236 | 300 |
| CRWD | flat | 220-227 | - | 227.08 | 187.5 |
| HIMS | watch | 27.42-28.5 | 28.5 | 26.5 | 35 |
| HOOD | flat | 93-95 | - | 90.83 | - |
| ONDS | watch | 9.25-9.5 | 9.25 | 8.75 | 10 |
| RIVN | watch | 15.95-16.45 | 15.95 | 15.29 | 20 |
| TSEM | armed_wait | 248-255 | 248 | 236.75 | 300 |
| UMAC | watch | 24.5-26.5 | 24.5 | 22.93 | 30 |

## Patterns in this tape

- Names on the latest confluence tape: 9.
- King-node targets on the sketch: 5.
- RSI called out in the thesis or the one-thing-to-verify: 3.
- Named rug / reverse-rug setups: none.
- Fresh shadow would paper-open: none.
- Fresh shadow would wait for the test: CRDO, TSEM
- Fresh shadow stays flat: BE, CRWD, HOOD
- Fresh shadow watches: HIMS 28.5, ONDS 9.25, RIVN 15.95, UMAC 24.5

## Alert path

Robinhood tool `create_alert` and a TradingView price alert share each level.
Create the TradingView alert only on rows marked create. Withheld means the tape is stale.
No webhook is configured. The alert does not place an order.

| Ticker | Create | Condition | Role |
|--------|--------|-----------|------|
| BE | no | - | - |
| CRDO | withheld | Crossing down 240 | entry_test |
| CRDO | withheld | Crossing down 236 | invalidation |
| CRWD | no | - | - |
| HIMS | withheld | Crossing down 28.5 | entry_test |
| HOOD | no | - | - |
| ONDS | withheld | Crossing up 9.25 | entry_test |
| RIVN | withheld | Crossing down 15.95 | entry_test |
| TSEM | withheld | Crossing down 248 | entry_test |
| TSEM | withheld | Crossing down 236.75 | invalidation |
| UMAC | withheld | Crossing down 24.5 | entry_test |

## Questions

1. Newest confluence `as_of` in this book is 2026-08-16. If that is not last night or this pre-market, where is the later TA paste?
2. A claim through the far side adds at that edge in the same session and stays
   open. A cross back through the paper entry trims the add and keeps the core.
   Say if you want that add only after you confirm the claim held.
3. Invalidation is now the nearest fib/shelf/SMA/trend/S/R cluster against the trade.
   Should that flatten the weekly on an intraday break, or only on a daily close?
4. 4H agreement is not in the operator JSON. Should a missing 4H note block a
   paper open, or only the scalp add?
5. Robinhood `create_alert` can notify the Agentic account without an order.
   MCP trade approvals default off, which lets a connected agent place live
   orders. Confirm approvals stay on, and confirm the next fresh book may push
   price alerts only.
6. Earnings: sell immediately on the open. Should any name with earnings inside
   the contract life be an automatic pass?
7. A target that is not larger than a negative node between spot and the target
   stays a watch. Confirm that size check is the rug rule you want.
