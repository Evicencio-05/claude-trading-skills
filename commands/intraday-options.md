---
description: "Run a focused intraday options swing analysis on a ticker with allocated capital. Covers market pulse, technical setup, options environment, and trade setups for same-day or next-day execution."
argument-hint: "<TICKER> <CAPITAL>"
---

Run a focused intraday options swing analysis on {TICKER} with {CAPITAL}
allocated. Be concise — this is for same-day or next-day execution.
Fetch live data only. Complete all phases in one pass.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1 — MARKET PULSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run market-breadth-analyzer and exposure-coach. One sentence:
is the tape supportive of intraday longs, shorts, or neither?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2 — TECHNICAL SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using technical-analyst, pull:
  • Current price, today's range, premarket activity.
  • Key intraday levels: yesterday's close, today's open,
    premarket high/low, VWAP, gap levels.
  • Nearest support and resistance (2 each max).
  • RSI on 15-min and 1-hour.
  • Volume vs 20-day average.
  • Daily trend and stage.
  • Any pattern on 15-min or 1-hour chart.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 — OPTIONS ENVIRONMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using options-strategy-advisor, pull:
  • Current IV rank and IV percentile.
  • 30-day IV vs 30-day HV — is premium rich or cheap?
  • ATM bid-ask spread — is this name liquid enough for intraday options?
    If spread > 5% of premium, flag as illiquid and recommend caution.
  • Expected move for today (0DTE or nearest expiry).
  • Skew: are calls or puts bid up? What does that signal?
  • Earnings today or tomorrow? (earnings-calendar) — if yes, flag
    IV crush risk prominently.
  • Any macro events today? (economic-calendar-fetcher).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 4 — TRADE SETUPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Define up to 2 setups — one bullish, one bearish — if both sides have
merit. If only one side has edge, define that one only.

For each setup, use options-strategy-advisor to select the structure.
Prefer simple, liquid structures for intraday: long calls/puts or
vertical spreads. Avoid multi-leg structures with >2 strikes.

Selection logic:
  • HIGH IV rank (>50): favor debit spreads over naked long options
    to reduce premium cost and vega drag.
  • LOW IV rank (<30): favor long calls/puts — buying cheap vol.
  • VERY HIGH IV (>80): consider tight credit spreads fading the move.
  • Earnings within 1 day: avoid buying premium; flag and skip
    unless there is a specific event play rationale.

For EACH setup provide:
  • Structure: (e.g., long call, bull call spread, long put, bear put spread).
  • Strike(s) and expiration: anchored to support/resistance and the
    expected move. Prefer 0-2 DTE for pure intraday, 3-5 DTE for
    overnight swing. Delta target: 0.40-0.55 for directional plays.
  • Entry trigger: exact stock price or condition that activates the trade.
  • Entry price: target premium (mid or slight debit to mid).
  • Number of contracts: calculated from {CAPITAL}.
    - For long options: contracts = floor({CAPITAL} / (premium × 100)).
      Do not exceed {CAPITAL} total outlay.
    - For debit spreads: contracts = floor({CAPITAL} / (net debit × 100)).
    - Always reserve at least 10% of {CAPITAL} as buffer — do not use
      the full amount.
  • Stop: exit if premium drops to 40% of entry cost (i.e., lose 60%).
    Also exit if stock breaches the invalidation level below.
  • Stock invalidation level: the stock price at which the thesis is wrong.
  • Target 1: exit 50% of contracts at 50-75% gain on premium.
  • Target 2: exit remaining contracts at 100-150% gain or at resistance.
  • Greeks at entry: delta, theta (daily decay cost), vega sensitivity.
  • Total outlay: contracts × premium × 100. Confirm ≤ {CAPITAL}.
  • Max loss: total outlay (for long options/spreads = defined risk).
  • Time invalidation: if trigger not hit by {time}, cancel the order.
    For 0DTE plays, cut off no later than 2:30 PM ET.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {TICKER} — Intraday Options Swing

**{date} {time}** | Price: ${X} | Capital: ${CAPITAL} | Tape: {Supportive/Neutral/Hostile}

## Key Levels

| Level          | Price  |
|----------------|--------|
| Resistance 2   |        |
| Resistance 1   |        |
| **Now**        |        |
| Support 1      |        |
| Support 2      |        |

## Technicals

| Indicator     | Value | Signal |
|---------------|-------|--------|
| RSI 15m       |       |        |
| RSI 1hr       |       |        |
| Volume vs Avg |       |        |
| Daily Stage   |       |        |
| Pattern       |       |        |

## Options Environment

| Metric          | Value | Note              |
|-----------------|-------|-------------------|
| IV Rank         |       |                   |
| IV Percentile   |       |                   |
| IV vs HV        |       | Rich / Fair / Cheap |
| ATM Spread      |       | Liquid / Illiquid |
| Expected Move   |       |                   |
| Skew            |       | Call / Put bid    |
| Earnings Risk   |       | Yes ⚠️ / No ✅    |

## ⬆ Bullish Setup

- **Structure:**
- **Strike / Expiry:**
- **Entry Trigger (stock price):**
- **Entry Premium (target):**
- **Contracts:** {N} × ${premium} × 100 = ${total outlay}
- **Greeks:** Δ {delta} | θ {daily decay} | ν {vega}
- **Stop:** Premium at ${X} (60% loss) or stock < ${invalidation level}
- **Target 1:** 50% of contracts at ${premium target} (+{X}%)
- **Target 2:** Remaining at ${premium target} (+{X}%)
- **Max Loss:** ${total outlay}
- **Expires:** {time cutoff}

## ⬇ Bearish Setup

- **Structure:**
- **Strike / Expiry:**
- **Entry Trigger (stock price):**
- **Entry Premium (target):**
- **Contracts:** {N} × ${premium} × 100 = ${total outlay}
- **Greeks:** Δ {delta} | θ {daily decay} | ν {vega}
- **Stop:** Premium at ${X} (60% loss) or stock > ${invalidation level}
- **Target 1:** 50% of contracts at ${premium target} (+{X}%)
- **Target 2:** Remaining at ${premium target} (+{X}%)
- **Max Loss:** ${total outlay}
- **Expires:** {time cutoff}

## Capital Summary

| Item                  | Bullish  | Bearish  |
|-----------------------|----------|----------|
| Contracts             |          |          |
| Total Outlay          |          |          |
| Max Loss              |          |          |
| Target 1 Profit       |          |          |
| Target 2 Profit       |          |          |
| Capital Used / Budget | ___ / {CAPITAL} | ___ / {CAPITAL} |

## Edge Assessment

One sentence: which setup has more edge and why. State NO EDGE if
conditions don't favor either side — it is always acceptable to not trade.

⚠️ *Options can expire worthless. Max loss on each setup is the total
premium paid. Not financial advice.*

---

SAVE: Write to ~/trading-research/intraday/{TICKER}*options*{YYYY-MM-DD}.md
