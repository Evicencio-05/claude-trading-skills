# Paper book — 2026-10-16

No brokerage order was sent. Robinhood Agentic places live orders on Portfolio C,
and this book only records paper options. Alerts below are unpushed
`robinhood_create_alert` payloads.

**Open:** 0 · **Armed:** 0 · **Live alerts:** 0

## Rules encoded from the operator read

- Daily direction comes from the confluence verdict or a daily operator chart.
  A 4-hour or weekly chart stays a watch until the daily direction is stated.
  The prior session's daily chart supplies that direction when this chart does not.
  An older daily does not follow.
  Daily holding above is up. Daily holding below is down.
  A thesis that puts the name in chop stays a watch.
  A 4H fight does not flat the daily swing. It withholds the scalp add.
  A fresh `NO_TRADE` stays flat.
- Enter at the test (discount 40% of the zone for longs, premium 40% for shorts).
  A level more than 3% of price away is the target, not a wider entry.
  A gap, a volume print, or an A/D print is confluence. It is not the entry.
- A bar moving more than 4% does not get a paper fill.
- Add on a claim through the far side of the zone. Trim that add if price
  crosses back through the paper entry. The core stays until invalidation or the target.
- Invalidation is the nearest opposing cluster. Its price is the fib, then the
  volume shelf, then the higher-period SMA (200, then 100, then 50, then 20).
  A labeled volume-profile POC is a shelf.
  A longer-timeframe fib beats a shorter one in that same cluster.
  A channel bound written with a tilde price joins that cluster.
  A stacked price beats a lone nearer level of that same kind.
- Target prefers a king node over the first fib when both are on the sketch.
  On a new operator chart, a starred positive king above is the long target,
  and a starred negative king below is the short target, when that king is
  larger than the negative GEX in the path. A VEX negative does not count.
  A negative node at a long target is not a reverse-rug.
  A newer operator chart keeps GEX/VEX nodes from the prior session. A target
  that is not larger than the negative GEX in the path stays a watch.
- Contract is weekly or shorter, ATM to slightly ITM, sized for 0 (premium is the risk).
- Weekly expiry is this Friday for a Mon–Wed decision, and the next Friday after that.
- An open paper position carries until invalidation, the target, expiry, or a newer tape.
- A dated earnings session does not open. A carried position flattens that morning.
- A long with RSI white under 50, white under the yellow signal, or
  buyer_strength false stays a watch. A marked buyer_strength true holds.
- Operator SMA colors: blue 20, green 50, orange 200. Those color names fill a
  blank period. A labeled 50 wins over green. A long under the green 50
  stays a watch, including when that price is blank and the chart says below.
  A long under the blue 20 or the orange 200 still opens while it holds the green 50.
  A blank 50 on a shorter chart uses the prior session's longer-timeframe 50.
  A chart with no RSI uses that prior session's RSI. Its own RSI wins.
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
| RIVN | watch | 15.95-16.45 | 15.95 | 15.34 | 20 |
| TSEM | armed_wait | 248-255 | 248 | 236.75 | 300 |
| UMAC | watch | 24.5-26.5 | 24.5 | 23.46 | 30 |

## Patterns in this tape

- Names on the latest confluence tape: 9.
- King-node targets on the sketch: 5.
- RSI called out in the thesis or the one-thing-to-verify: 3.
- Rug / reverse-rug passing the size check: CRDO reverse rug, ONDS reverse rug, RIVN reverse rug
- Fresh shadow would paper-open: none.
- Fresh shadow would wait for the test: CRDO, TSEM
- Fresh shadow stays flat: BE, CRWD, HOOD
- Fresh shadow watches: HIMS 28.5, ONDS 9.25, RIVN 15.95, UMAC 24.5

## Alert path

Robinhood tool `create_alert` and a TradingView price alert share each level.
Create the TradingView alert only on rows marked create. Withheld means the tape is stale.
Paste the session Pine on each ticker's chart. It plots that ticker's levels.
Arm Any alert() function call. No webhook is configured.
The alert does not place an order.

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

1. Newest confluence `as_of` in this book is 2026-08-16. Newest operator chart on disk is 2026-08-16. Paste the day-before or pre-market charts if that is not the live plan.
2. A claim through the far side adds at that edge in the same session and stays
   open. A cross back through the paper entry trims the add and keeps the core.
   Say if you want that add only after you confirm the claim held.
3. Invalidation is the nearest cluster. Inside it, a fib beats a shelf, and a
   200 SMA beats a 20. Should that flatten the weekly on an intraday break,
   or only on a daily close?
4. A missing 4H note does not block the paper open. An explicit 4H fight
   withholds the scalp add and leaves the daily swing on. Say if a 4H fight
   should flat the swing too.
5. Robinhood `create_alert` can notify the Agentic account without an order.
   MCP trade approvals default off, which lets a connected agent place live
   orders. Confirm approvals stay on, and confirm the next fresh book may push
   price alerts only.
6. A dated earnings session does not open, and a carried position flattens that
   morning. A later ISO earnings date stays open until that open. Vague text
   such as early September does not count. Say if the whole earnings week
   should be a pass instead.
7. A target node has to point with the trade, and it has to be larger than
   the negative GEX between spot and the target. A negative node at a long
   target is not a reverse-rug. Confirm that size check is the rug rule.
