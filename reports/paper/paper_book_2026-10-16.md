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
  A newer 4-hour chart keeps daily or weekly fibs from the prior session.
  Those carried fibs set the stop. They do not move the test or the target.
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
- Trade plans dated before 2026-10-14 are not the tape.
  A chart on or after that date stays live. The latest chart for that ticker is the plan.
  Each entry level is its own paper level. Spot within 1% of that level opens it.
  A farther entry level waits. One invalidation covers the name.
- TA older than one trading session is stale when it is also before that date.
  Stale levels do not arm and do not alert.

## This session

| Ticker | As of | Verdict | Status | Why |
|--------|-------|---------|--------|-----|

Tape starts 2026-10-14. No chart dated 2026-10-14 or later is in the checkout.

## If that tape had been fresh

| Ticker | Shadow | Entry zone | Test / fill | Invalidation | Target |
|--------|--------|------------|-------------|--------------|--------|

## Patterns in this tape

- Names on the latest confluence tape: 0.
- King-node targets on the sketch: 0.
- RSI called out in the thesis or the one-thing-to-verify: 0.
- Rug / reverse-rug passing the size check: none.
- Fresh shadow would paper-open: none.
- Fresh shadow would wait for the test: none.
- Fresh shadow stays flat: none.
- Fresh shadow watches: none.

## Alert path

Robinhood tool `create_alert` and a TradingView price alert share each level.
Create the TradingView alert only on rows marked create. Withheld means the tape is stale.
Paste the session Pine on each ticker's chart. It plots that ticker's levels.
Arm Any alert() function call. No webhook is configured.
The alert does not place an order.

| Ticker | Create | Condition | Role |
|--------|--------|-----------|------|

## Questions

1. No chart dated 2026-10-14 or later is in the checkout.
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
