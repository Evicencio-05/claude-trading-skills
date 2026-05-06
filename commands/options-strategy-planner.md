---
description: "Build a comprehensive options strategy plan for a ticker: condensed stock context, IV environment analysis, strategy generation with P/L modeling, side-by-side comparison, recommendation, and trade management plan."
argument-hint: "<TICKER>"
---

Build a comprehensive options strategy plan for {TICKER}. This prompt has two
stages: a condensed stock assessment to establish directional conviction and
context, followed by a deep options-specific analysis with concrete trade
structures. Use all available skills, scripts, and live data. Where a skill
or API call fails, note the gap and continue.

Format the final output as a single, clean Markdown report using the structure
defined at the end of this prompt.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 1 — CONTEXT ASSESSMENT (condensed deep dive)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The goal here is NOT a full research report — it's gathering the specific
context that matters for options decision-making.

1a. Market Posture — Run exposure-coach, market-breadth-analyzer, and
    market-top-detector. We need to know: Is the broad market environment
    favorable or hostile? What is the exposure ceiling? This directly
    affects whether we lean toward defined-risk or aggressive strategies.

1b. Sector & Theme — Run sector-analyst and theme-detector for {TICKER}'s
    sector. Is the sector in rotation? Is {TICKER} aligned with a
    trending theme? Sector momentum affects strategy selection (e.g.,
    strong sector = more aggressive strikes).

1c. Fundamental Snapshot — Using us-stock-analysis and FMP API, pull:
    • Current price, market cap, P/E, forward P/E, PEG ratio.
    • Last 4 quarters EPS surprise history (beat/miss % and magnitude).
    • Revenue growth rate (YoY), earnings growth rate (YoY).
    • Free cash flow yield.
    • Dividend yield and ex-date if applicable (dividend risk for options).
    We need this for strike selection and to gauge whether the stock is
    cheap/fair/expensive relative to its earnings power.

1d. Technical Snapshot — Using technical-analyst, identify:
    • Minervini Stage (1-4) and primary trend direction.
    • 3 key support levels and 3 key resistance levels.
    • Distance from 21EMA, 50MA, 200MA (as %).
    • RSI (14), current chart pattern if any, and pivot/breakout level.
    • 30-day and 90-day historical volatility (annualized).
    Support/resistance directly maps to strike selection and stop levels.

1e. Upcoming Events — Using earnings-calendar and economic-calendar-fetcher:
    • Next earnings date and whether it falls within the options expiration.
    • Any other known catalysts (FDA dates, product launches, conferences,
      ex-dividend dates, index rebalances).
    THIS IS CRITICAL: never sell premium through an earnings event without
    explicitly acknowledging the risk.

1f. Directional Conviction — Based on 1a-1e, state:
    • Directional bias: Bullish / Bearish / Neutral / No edge.
    • Conviction level: High / Medium / Low.
    • Time horizon: Days / Weeks / Months.
    • Volatility outlook: Expecting expansion or contraction?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 2 — OPTIONS ENVIRONMENT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2a. Implied Volatility Assessment — Using options-strategy-advisor and
    available data:
    • Current IV rank (where IV sits relative to its 52-week range, 0-100).
    • Current IV percentile (% of days in the past year IV was lower).
    • IV vs historical volatility: Is IV overstating or understating
      expected movement? (IV premium/discount).
    • If IV rank > 50: premium selling strategies are favored.
    • If IV rank < 30: premium buying strategies or debit spreads favored.
    • Skew analysis: Is put skew elevated (fear) or call skew elevated
      (speculation)?

2b. Expected Move Calculation —
    • Calculate the implied expected move for the nearest monthly expiration
      using ATM straddle pricing (or Black-Scholes from options-strategy-advisor).
    • Calculate expected move for the expiration closest to 45 DTE.
    • Compare to the stock's actual average move over the same period.
    • Does the market seem to be overpricing or underpricing movement?

2c. Options Liquidity Check —
    • Average daily options volume for {TICKER}.
    • Bid-ask spread on ATM options (tight = liquid, wide = illiquid).
    • Open interest at key strikes near support/resistance levels.
    • Flag if liquidity is poor — this changes strategy selection
      significantly (avoid multi-leg strategies in illiquid names).

2d. Greeks Baseline — Run options-strategy-advisor to calculate for ATM
    options at 30 and 45 DTE:
    • Delta, Gamma, Theta, Vega for both calls and puts.
    • Note the theta decay curve — when does decay accelerate?

2e. Earnings Volatility Analysis — If earnings are within 60 days:
    • Historical average post-earnings move (last 8 quarters).
    • Current straddle-implied earnings move vs historical average.
    • Is the market over/underpricing the earnings event?
    • Pre-earnings IV crush magnitude (typical IV drop after earnings).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 3 — STRATEGY GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on the directional conviction, IV environment, and time horizon from
Stages 1-2, generate 3-4 candidate strategies. For EACH strategy, use
options-strategy-advisor to model the full trade.

Selection logic (use as a guide, not rigid rules):

    BULLISH + HIGH IV     → Bull put spread, short put, covered call
    BULLISH + LOW IV      → Long call, bull call spread, LEAPS
    BEARISH + HIGH IV     → Bear call spread, short call spread
    BEARISH + LOW IV      → Long put, bear put spread
    NEUTRAL + HIGH IV     → Iron condor, short strangle, short straddle
    NEUTRAL + LOW IV      → Long straddle, long strangle, calendar spread
    EARNINGS PLAY         → Straddle/strangle (long if IV cheap, short if rich)
    INCOME/HEDGE          → Covered call, protective put, collar

For each candidate strategy, provide:

3a. Strategy Structure —
    • Strategy name and type (credit/debit, defined/undefined risk).
    • Exact legs: strike prices, expiration, buy/sell, call/put.
    • Why these specific strikes were chosen (anchored to support/resistance
      from Phase 1d, or delta targets, or expected move boundaries).
    • Why this expiration was chosen (DTE rationale, event avoidance or
      inclusion, theta decay sweet spot).

3b. Greeks Profile —
    • Net delta, gamma, theta, vega for the position.
    • What is the position most sensitive to?
    • How will Greeks shift if the stock moves ±5%, ±10%?

3c. P/L Scenarios — Run options-strategy-advisor to model:
    • Max profit (dollar amount and % of capital at risk).
    • Max loss (dollar amount and % of capital at risk).
    • Breakeven price(s).
    • P/L at key levels: support 1, support 2, current price, resistance 1,
      resistance 2.
    • P/L at expiration vs P/L at 50% of max profit (early exit).

3d. Probability Metrics —
    • Probability of profit (PoP).
    • Probability of max profit.
    • Probability of max loss.
    • Expected value (probability-weighted return).

3e. Risk/Reward Ratio — Express as R-multiple. Compare to simply buying
    or shorting the stock outright.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 4 — STRATEGY COMPARISON & RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4a. Side-by-Side Comparison Table — For all candidate strategies, compare:
    • Max profit, max loss, breakeven(s).
    • Risk/reward ratio, probability of profit.
    • Capital required, capital efficiency (return on capital at risk).
    • Greeks exposure (which is most/least sensitive to adverse moves).
    • Complexity (number of legs, management difficulty).

4b. Recommended Strategy — Select the best strategy and explain why:
    • How does it align with the directional conviction and IV environment?
    • What edge does it exploit (mispriced IV, directional momentum,
      time decay, mean reversion)?
    • Why was it chosen over the alternatives?

4c. Position Sizing — Using position-sizer logic:
    • Calculate position size based on max loss = 1-2% of portfolio.
    • Number of contracts.
    • Total capital deployed and max capital at risk.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 5 — TRADE MANAGEMENT PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5a. Entry Rules —
    • Exact entry trigger (e.g., "enter on breakout above $XXX with
      volume confirmation" or "enter immediately at current prices").
    • Limit order or market order? Target fill price.
    • Scale-in plan if applicable (e.g., 50% now, 50% on pullback to support).

5b. Profit Taking Rules —
    • Close at what % of max profit? (Common: 50% for credit spreads,
      100%+ for debit spreads).
    • Partial profit targets (e.g., close half at 50% max profit, trail rest).
    • Time-based exit: close if X DTE remain regardless of P/L?

5c. Stop Loss / Defense Rules —
    • Close at what multiple of credit received for losses? (Common: 2x).
    • Stock price level that invalidates the thesis → exit.
    • Rolling rules: When and how to roll (down/out for puts, up/out for calls).
    • Adjustment triggers: At what delta or P/L level do you adjust?

5d. Adjustment Playbook — For the recommended strategy, define specific
    adjustments for these scenarios:
    • Stock moves sharply against you (>1 expected move).
    • Stock moves sharply in your favor quickly (>1 expected move).
    • IV spikes (e.g., pre-earnings run-up).
    • IV crushes (e.g., post-earnings, event resolution).
    • Time decay accelerates with position still open.
    • Stock pins near a short strike at expiration.

5e. Earnings Handling — If an earnings date falls within the trade window:
    • Plan to hold through, close before, or adjust before earnings?
    • What is the risk of holding through? (IV crush, gap risk).
    • Quantify worst-case scenario with the earnings gap.

5f. Exit Checklist — A numbered, yes/no checklist the trader should run
    through before closing the position for any reason.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {TICKER} — Options Strategy Plan

**Generated:** {date}
**Current Price:** ${price}
**Directional Bias:** {Bullish/Bearish/Neutral} | **Conviction:** {H/M/L}
**IV Environment:** {Rich/Fair/Cheap} (IV Rank: _**, IV Percentile:**_)
**Market Posture:** {exposure-coach recommendation}
**Next Earnings:** {date} ({X} DTE from target expiration)

## Executive Summary

3-5 sentences: What's the play, why now, and what's the expected outcome.

## 1. Stock Context Snapshot

### Market & Sector

{Phase 1a-1b findings, condensed}

### Fundamental Snapshot

| Metric          | Value    | vs Sector  |
|-----------------|----------|------------|
| P/E             |          |            |
| Forward P/E     |          |            |
| EPS Growth (YoY)|          |            |
| Rev Growth (YoY)|          |            |
| FCF Yield       |          |            |

### Technical Snapshot

| Level            | Price    | Distance   |
|------------------|----------|------------|
| Resistance 3     |          |            |
| Resistance 2     |          |            |
| Resistance 1     |          |            |
| **Current Price** |         |            |
| Support 1        |          |            |
| Support 2        |          |            |
| Support 3        |          |            |

| Indicator | Value  | Signal     |
|-----------|--------|------------|
| RSI (14)  |        |            |
| Stage     |        |            |
| 30d HV    |        |            |
| 90d HV    |        |            |
| Trend     |        |            |

### Catalyst Timeline

| Date       | Event                | Impact  | Within Trade Window? |
|------------|----------------------|---------|----------------------|
|            |                      |         |                      |

## 2. Options Environment

### Volatility Profile

| Metric              | Value    | Interpretation       |
|---------------------|----------|----------------------|
| Current IV          |          |                      |
| IV Rank (52w)       |          |                      |
| IV Percentile       |          |                      |
| 30d HV              |          |                      |
| IV vs HV            |          | Premium / Discount   |
| Put Skew             |          |                      |
| Expected Move (monthly)|       |                      |

### Earnings Vol Analysis (if applicable)

| Quarter  | Implied Move | Actual Move | Over/Under |
|----------|-------------|-------------|------------|
|          |             |             |            |

## 3. Strategy Candidates

### Strategy A: {Name}

{Full 3a-3e analysis}

**P/L Diagram Reference Points:**

| Stock Price | P/L ($) | P/L (%) | Notes       |
|-------------|---------|---------|-------------|
| Support 2   |         |         |             |
| Support 1   |         |         |             |
| Breakeven   |         |         |             |
| Current     |         |         |             |
| Resistance 1|         |         |             |
| Resistance 2|         |         |             |

### Strategy B: {Name}

{Repeat}

### Strategy C: {Name}

{Repeat}

## 4. Strategy Comparison

| Metric              | Strategy A | Strategy B | Strategy C |
|---------------------|-----------|-----------|-----------|
| Type                |           |           |           |
| Max Profit          |           |           |           |
| Max Loss            |           |           |           |
| Breakeven           |           |           |           |
| Risk/Reward         |           |           |           |
| Prob of Profit      |           |           |           |
| Capital Required    |           |           |           |
| Capital Efficiency  |           |           |           |
| Complexity          |           |           |           |

## 5. Recommended Strategy

### The Trade

{Exact structure with strikes, expiration, and contract count}

### Position Sizing

| Item                 | Value    |
|----------------------|----------|
| Contracts            |          |
| Capital at Risk      |          |
| Max Profit           |          |
| Risk as % of Portfolio|         |

### Why This Strategy

{Explanation from 4b}

## 6. Trade Management Plan

### Entry

{5a rules}

### Profit Taking

{5b rules}

### Stop Loss & Defense

{5c rules}

### Adjustment Playbook

| Scenario                    | Action                              |
|-----------------------------|-------------------------------------|
| Stock drops > 1 exp. move   |                                     |
| Stock rallies > 1 exp. move |                                     |
| IV spikes                   |                                     |
| IV crushes                  |                                     |
| Theta accelerating          |                                     |
| Pinning near short strike   |                                     |

### Earnings Handling

{5e plan}

### Pre-Close Exit Checklist

{5f numbered checklist}

## Risk Warnings

- Options involve substantial risk and are not suitable for all investors.
- Theoretical pricing from Black-Scholes is an approximation. Actual market
  prices may differ due to supply/demand, skew, and liquidity.
- Always verify Greeks and pricing with your broker's platform before executing.
- This analysis is for educational and research purposes only.

## Data Sources & Gaps

{List of every data source, API, and skill used. Note any failures or
unavailable data.}

---
_This plan is for research and educational purposes only. It is not financial
advice. Options trading carries significant risk including the potential for
total loss of invested capital. All trading decisions should be based on your
own analysis and risk tolerance._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAVE & VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After generating the plan:

1. Check if ~/trading-research/options/{TICKER}.md already exists.
   - If it does, copy the existing file to:
     ~/trading-research/archives/{TICKER}_options_{YYYY-MM-DD}.md
     (using the date from the OLD plan's "Generated" line, not today).
   - Then overwrite ~/trading-research/options/{TICKER}.md with the new plan.
   - If it doesn't exist, simply write the new plan there.

2. Confirm save with: "Options plan saved to ~/trading-research/options/{TICKER}.md"
   and if an archive was created, note that too.
