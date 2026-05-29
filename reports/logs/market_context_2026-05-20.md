# Pre-Market Report — 2026-05-20
*Generated: 06:00:23*

## Market Posture

```
Date:            2026-05-20
Breadth:         32.4/100 (Bearish)
Uptrend:         14.4/100
Uptrend warning: Warning Penalty: -7 (raw score: 21.4)
Leading sector:  Energy
Cycle phase:     N/A
Macro events:    none
Flags:           none
Posture:         REDUCE_ONLY
Ceiling:         30%
```

## Position Flags

No urgent or watch flags.

## Breadth Detail

```
======================================================================
Market Breadth Analyzer
6-Component Health Scoring (No API Key Required)
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2511 rows, 2016-05-23 to 2026-05-18)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-18, 2 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 52 (NEUTRAL: 8MA=0.553 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 35 (NEGATIVE: 8MA below 200MA (gap=-0.042, 8MA falling))
  [3/6] Peak/Trough Cycle Position... Score: 15 (PEAK (52d ago): gradual decline, 8MA falling)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.553 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 23th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 26.0 (Dangerous bearish divergence: S&P +8.5%, Breadth 8MA -0.120 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  Strongest: Current Breadth Level & Trend (52)
  Weakest: Peak/Trough Cycle Position (15)


Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-20_060022.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-20_060022.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  JSON Report: reports/pre_market/market_breadth_2026-05-20_060022.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-20_060022.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (14884 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-19, ratio=16.9%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 19 (VERY WEAK: 16.9% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 0 (VERY NARROW: 1/11 sectors uptrending, spread 60.6%)
  [3/5] Sector Rotation... Score: 54 (BALANCED: Cyclical-Defensive gap 2.8pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 24 (WEAK MOMENTUM: slope=-0.0080, strong decelerating)
  [5/5] Historical Context... Score: 28 (BELOW AVERAGE: 16.9% at 28.4th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 14.4/100
  Zone: Bear (Bear)
  Exposure Guidance: Capital Preservation (0-30%)
  Warning Penalty: -7 (raw score: 21.4)
  Strongest: Sector Rotation (54)
  Weakest: Sector Participation (0)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-20_060022.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-20_060022.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 14.4/100
  Zone: Bear
  Exposure Guidance: Capital Preservation (0-30%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-20_060022.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-20_060022.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-20

> Data as of: 2026-05-19

## Risk Regime

**BALANCED** (score: 54/100)

- Cyclical avg: 15.3%
- Defensive avg: 12.6%
- Difference: 2.8pp
- Commodity avg: 36.2%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive

## Cycle Phase Estimate

**Mid** (confidence: low)

- Mid: 60.0 ←
- Recession: 58.8
- Late: 56.7
- Early: 52.9

Evidence:
- Leaders in top ranks: Technology, Industrials, Energy
- Laggards in bottom ranks: Utilities

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 66.5% | Up | Overbought |
| 2 | Technology | 24.9% | Down | Normal |
| 3 | Communication Services | 19.4% | Down | Normal |
| 4 | Industrials | 16.1% | Down | Normal |
| 5 | Consumer Defensive | 15.5% | Down | Normal |
| 6 | Healthcare | 14.5% | Down | Normal |
| 7 | Real Estate | 14.1% | Down | Normal |
| 8 | Financial | 8.7% | Down | Oversold |
| 9 | Consumer Cyclical | 7.6% | Down | Oversold |
| 10 | Utilities | 6.2% | Down | Oversold |
| 11 | Basic Materials | 5.9% | Down | Oversold |

## Trend Summary

- Uptrending: 1 sectors
- Downtrending: 10 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 66.5%
**Oversold** (ratio < 9.7%):
- Financial: 8.7%
- Consumer Cyclical: 7.6%
- Utilities: 6.2%
- Basic Materials: 5.9%

---
*Generated: 2026-05-20T06:00:23*
Checking data freshness...
Data is fresh (latest: 2026-05-19)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-20.md
```
