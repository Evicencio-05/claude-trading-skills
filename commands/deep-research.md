---
description: "Conduct a comprehensive 8-phase deep research report on a stock ticker covering market context, fundamentals, earnings, technicals, ownership, screening, risk, and trade planning."
argument-hint: "<TICKER>"
---

# Deep Stock Research Prompt

> **Usage:** Replace `{TICKER}` with your target stock symbol (e.g., NVDA, AAPL, TSLA).

---

## The Prompt

```
Conduct a comprehensive, multi-dimensional research report on {TICKER}. Work through
every phase below sequentially. Use all available skills, scripts, and data sources.
Fetch live data wherever possible — do not rely on stale training knowledge for prices,
financials, or market conditions. Where a skill or API call fails, note the gap and
continue with the remaining analysis.

Format the final output as a single, clean Markdown report with the structure defined
at the end of this prompt.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1 — MARKET CONTEXT (Run first: sets the macro backdrop)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1a. Market Breadth — Run the market-breadth-analyzer to get the composite
    health score (0-100). Report the 6-component breakdown.

1b. Sector Analysis — Run the sector-analyst to identify the current market
    cycle phase and whether {TICKER}'s sector is in a favorable rotation.

1c. Uptrend Ratio — Run the uptrend-analyzer for composite breadth scoring
    and any warning overlays (Late Cycle, High Selectivity).

1d. Macro Regime — If macro-regime-detector is available, identify the current
    structural regime (Concentration, Broadening, Contraction, etc.).

1e. Market Top/Bottom — Run market-top-detector for distribution day count and
    topping probability. Run ftd-detector if the market is in correction to
    check for follow-through day signals.

1f. Exposure Coach — Run exposure-coach to synthesize the above into an
    exposure ceiling and posture recommendation.

Summarize: Is this a market environment where new long positions are appropriate?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2 — FUNDAMENTAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2a. Company Overview — Business model, revenue segments, competitive moat,
    TAM, and key products/services. Identify the 2-3 most important growth
    drivers and the 2-3 biggest risks.

2b. Financial Deep Dive (use us-stock-analysis skill and FMP API) —
    • Income Statement: Revenue, gross margin, operating margin, net margin
      trends over 3-5 years. YoY and QoQ growth rates.
    • Balance Sheet: Total debt, cash position, D/E ratio, current ratio,
      quick ratio. Any red flags in goodwill, intangibles, or off-balance
      sheet items.
    • Cash Flow: Operating cash flow, free cash flow, FCF margin, capex
      intensity. FCF trend vs net income (quality of earnings check).
    • Per-Share Metrics: EPS growth (diluted), book value per share, FCF
      per share.

2c. Valuation —
    • Current P/E, forward P/E, PEG ratio, P/S, P/B, EV/EBITDA.
    • Compare each metric to: (a) the stock's own 5-year range,
      (b) sector/industry median, (c) closest 3-5 peers.
    • DCF estimate: Provide a simple 2-stage DCF with explicit assumptions
      for growth rate, terminal multiple, and discount rate. Show bull/base/bear
      case fair values.

2d. Profitability & Efficiency — ROE, ROIC, ROA, asset turnover, inventory
    turnover (if applicable). Compare to peers.

2e. Earnings Quality — Accrual ratio, operating cash flow vs net income
    divergence, revenue recognition notes, any restatements or audit flags.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 — EARNINGS & CATALYSTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3a. Earnings History — Last 4-8 quarters of EPS surprise (beat/miss %),
    revenue surprise, and post-earnings price reaction (gap % and direction).

3b. Upcoming Earnings — Next earnings date (use earnings-calendar), consensus
    EPS and revenue estimates, whisper numbers if available.

3c. Earnings Momentum — Run earnings-trade-analyzer if the stock recently
    reported. Score the post-earnings reaction. If applicable, run pead-screener
    for drift setup detection.

3d. Catalyst Pipeline — Identify upcoming catalysts: product launches, FDA
    decisions, conference appearances, analyst days, dividend ex-dates,
    share buyback authorizations, index inclusion/exclusion, insider
    transaction windows, regulatory decisions, macro events from
    economic-calendar-fetcher that could impact this stock.

3e. Recent News — Run market-news-analyst or web search for the last 10-14
    days of material news. Rank events by market impact.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 4 — TECHNICAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4a. Trend Structure (use technical-analyst skill) —
    • Primary trend (weekly): Direction, duration, key MAs (10w, 30w, 40w).
    • Intermediate trend (daily): Direction, key MAs (21d, 50d, 200d).
    • Minervini Stage Analysis: Which stage is the stock in (1-4)?
      Is it in a Stage 2 uptrend with price > 200MA > 150MA > 50MA?

4b. Support & Resistance — Identify 3 key support levels and 3 key resistance
    levels. Note any confluence zones where multiple levels align.

4c. Chart Patterns — Identify any active or forming patterns: VCP, cup with
    handle, double bottom, ascending base, flat base, head & shoulders,
    wedges, channels, triangles. Reference pivot/breakout points.

4d. Volume Analysis — Average daily volume, recent volume trend vs 50-day
    average, accumulation/distribution patterns. Up-volume vs down-volume
    ratio over last 20 sessions.

4e. Momentum Indicators — RSI (14), MACD (12,26,9), stochastic, ADX/DMI.
    Note any divergences between price and momentum.

4f. Relative Strength — Price performance vs S&P 500 over 1m, 3m, 6m, 12m.
    RS rating or rank if available. Is relative strength line at new highs?

4g. VCP Screening — Run vcp-screener to check if this stock qualifies as
    a Volatility Contraction Pattern setup. Report score and state.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 5 — OWNERSHIP & FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5a. Institutional Ownership — Run institutional-flow-tracker. Report total
    institutional ownership %, QoQ change, number of holders trend.

5b. Smart Money — Identify any superinvestor positions (Berkshire, Baupost,
    Appaloosa, Pershing Square, Tiger Global, etc.). New positions, increases,
    decreases, and exits over the last 2-4 quarters.

5c. Insider Activity — Recent insider buys and sells (last 6 months).
    Cluster buys are especially notable. Calculate net insider sentiment.

5d. Short Interest — Current short interest as % of float, days to cover,
    and trend over last 3-6 months.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 6 — SCREENING CROSS-CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6a. CANSLIM Score — Run canslim-screener on {TICKER} if it fits the growth
    profile. Report composite score and component breakdown (C, A, N, S, I, M).

6b. Theme Detection — Run theme-detector. Does {TICKER} align with any
    trending market themes? Report theme heat, lifecycle maturity, and
    confidence level.

6c. Pair Trade Context — If {TICKER} has an obvious peer/rival, run
    pair-trade-screener to check cointegration and relative value.

6d. Dividend Analysis — If {TICKER} pays a dividend, run value-dividend-screener
    or kanchi-dividend-sop. Report yield, payout ratio, dividend growth rate,
    sustainability score.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 7 — RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7a. Company-Specific Risks — Regulatory, competitive, concentration (revenue,
    customer, geographic), litigation, key-person dependency, technological
    disruption risk.

7b. Macro Risks — Interest rate sensitivity, currency exposure, commodity
    input costs, trade/tariff exposure, geopolitical risk.

7c. Valuation Risk — How much downside if the stock re-rates to sector
    median multiples? What if growth decelerates by 50%?

7d. Technical Risk — Distance from key support levels. Maximum drawdown
    in last 12 months. Beta and historical volatility (30d, 90d, 1yr).

7e. Bubble Check — Run us-market-bubble-detector. Is the broader market
    in a risk phase that warrants caution?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 8 — TRADE PLANNING (if actionable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

8a. Position Sizing — Run position-sizer with the identified entry and stop
    levels. Use 1% portfolio risk as default. Report recommended share count
    and dollar amount.

8b. Entry Strategy — Define primary and secondary entry triggers (e.g.,
    breakout above pivot, pullback to support, earnings gap-and-go).

8c. Stop Loss — Define initial stop and rationale (e.g., below base low,
    below 21EMA, below gap-fill level). Calculate R-multiple.

8d. Profit Targets — Define 1R, 2R, 3R targets. Identify logical resistance
    zones that could cap upside.

8e. Options Strategy — If appropriate, run options-strategy-advisor to
    evaluate alternatives (e.g., risk-defined spread vs outright stock,
    covered calls for income, protective puts for hedging).

8f. Thesis Invalidation — State the specific, falsifiable conditions under
    which the thesis is wrong and the position should be exited, regardless
    of stop loss.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT — Structure the final report exactly as follows:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {TICKER} — Deep Research Report
**Generated:** {date}
**Market Posture:** {exposure-coach recommendation}

## Executive Summary
3-5 sentence overview: what this company does, why it's interesting right
now, and the bottom-line verdict (Strong Buy / Buy / Hold / Avoid / Short).

## Scorecard
| Dimension         | Rating (1-10) | Key Signal                         |
|-------------------|---------------|-------------------------------------|
| Market Context    |               |                                     |
| Fundamentals      |               |                                     |
| Valuation         |               |                                     |
| Earnings Momentum |               |                                     |
| Technical Setup   |               |                                     |
| Ownership & Flow  |               |                                     |
| Risk Profile      |               |                                     |
| **Composite**     |               |                                     |

## 1. Market Context
{Phase 1 findings}

## 2. Fundamental Analysis
{Phase 2 findings with key tables for financials, valuation comps, DCF}

## 3. Earnings & Catalysts
{Phase 3 findings with earnings surprise table and catalyst timeline}

## 4. Technical Analysis
{Phase 4 findings with key levels table}

## 5. Ownership & Flow
{Phase 5 findings with institutional holder changes table}

## 6. Screening Cross-Check
{Phase 6 findings — CANSLIM score, theme alignment, etc.}

## 7. Risk Assessment
{Phase 7 findings with risk matrix}

## 8. Trade Plan
{Phase 8 findings — entry, stop, targets, position size, R-multiples}

## Bull Case (probability: __%)
Top 3 reasons this stock outperforms over the next 6-12 months.

## Bear Case (probability: __%)
Top 3 reasons this stock underperforms or declines.

## Base Case (probability: __%)
Most likely scenario and expected return range.

## Thesis Invalidation Triggers
Numbered list of specific, measurable conditions that would kill the thesis.

## Data Sources & Gaps
List every data source used, any API calls that failed, and any analysis
that was skipped due to missing data or unavailable skills.

---
*This report is for research and educational purposes only. It is not
financial advice. All investment decisions carry risk and should be made
based on your own due diligence.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAVE & VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After generating the report:

1. Check if ~/trading-research/reports/{TICKER}.md already exists.
   - If it does, copy the existing file to:
     ~/trading-research/archives/{TICKER}_{YYYY-MM-DD}.md
     (using the date from the OLD report's "Generated" line, not today).
   - Then overwrite ~/trading-research/reports/{TICKER}.md with the new report.
   - If it doesn't exist, simply write the new report there.

2. Confirm save with: "Report saved to ~/trading-research/reports/{TICKER}.md"
   and if an archive was created, note that too.
```
