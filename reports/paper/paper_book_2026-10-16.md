# Paper book — 2026-10-16

No brokerage order was sent. Robinhood Agentic places live orders on Portfolio C,
and this book only records paper options. Alerts below are unpushed
`robinhood_create_alert` payloads.

**Open:** 0 · **Armed:** 0 · **Live alerts:** 0

## Rules encoded from the operator read

- Daily direction comes from the confluence verdict. A fresh `NO_TRADE` stays flat.
- Enter at the test (discount 40% of the zone for longs, premium 40% for shorts).
- A bar moving more than 4% does not get a paper fill.
- Add/roll is a later claim through the zone, not the first fill at the high.
- Target prefers a king node over the first fib when both are on the sketch.
- Contract is weekly or shorter, ATM to slightly ITM, sized for 0 (premium is the risk).
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
| CRDO | armed_wait | 240-250 | 240 | 232 | 300 |
| CRWD | flat | 220-227 | - | 227.08 | 187.5 |
| HIMS | watch | 27.42-28.5 | 28.5 | 24 | 35 |
| HOOD | flat | 93-95 | - | 90.83 | - |
| ONDS | watch | 9.25-9.5 | 9.25 | 8.45 | 10 |
| RIVN | watch | 15.95-16.45 | 15.95 | 15 | 20 |
| TSEM | armed_wait | 248-255 | 248 | 230 | 300 |
| UMAC | watch | 24.5-26.5 | 24.5 | 22.9 | 30 |

## Patterns in this tape

- Names on the latest confluence tape: 9.
- King-node targets on the sketch: 5.
- RSI called out in the thesis or the one-thing-to-verify: 3.
- Named rug / reverse-rug setups: none.
- Fresh shadow would paper-open: none.
- Fresh shadow would wait for the test: CRDO, TSEM
- Fresh shadow stays flat: BE, CRWD, HOOD
- Fresh shadow watches: HIMS 28.5, ONDS 9.25, RIVN 15.95, UMAC 24.5

## Questions

1. Newest confluence `as_of` in this book is 2026-08-16. If that is not last night or this pre-market, where is the later TA paste?
2. A paper fill requires the discount/premium 40% of the zone and a bar inside
   4% absolute. Should a claim through the far side open
   an add the same day, or only after you say the claim held?
3. Invalidation in these artifacts is a daily-close level. For weeklies, do you
   want the paper book to flatten on an intraday break instead?
4. 4H agreement is not in the operator JSON. Should a missing 4H note block a
   paper open, or only the scalp add?
5. Robinhood `create_alert` can notify the Agentic account without an order.
   MCP trade approvals default off, which lets a connected agent place live
   orders. Confirm approvals stay on, and confirm the next fresh book may push
   price alerts only.
6. Earnings: sell immediately on the open. Should any name with earnings inside
   the contract life be an automatic pass?
7. Rug and reverse-rug need a target node larger than the opposing -GEX node.
   Mark that node on the next map paste so the book can require it.
