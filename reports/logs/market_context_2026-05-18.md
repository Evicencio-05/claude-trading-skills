# Pre-Market Report — 2026-05-18
*Generated: 06:10:33*

## Market Posture

```
Date:            2026-05-18
Breadth:         32.4/100 (Bearish)
Uptrend:         15.9/100
Uptrend warning: Warning Penalty: -10 (raw score: 25.9)
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2513 rows, 2016-05-17 to 2026-05-14)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-14, 4 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 52 (NEUTRAL: 8MA=0.557 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 35 (NEGATIVE: 8MA below 200MA (gap=-0.039, 8MA falling))
  [3/6] Peak/Trough Cycle Position... Score: 15 (PEAK (50d ago): gradual decline, 8MA falling)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.557 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 24th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 26.0 (Dangerous bearish divergence: S&P +9.6%, Breadth 8MA -0.119 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  Strongest: Current Breadth Level & Trend (52)
  Weakest: Peak/Trough Cycle Position (15)


Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-18_061032.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-18_061032.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  JSON Report: reports/pre_market/market_breadth_2026-05-18_061032.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-18_061032.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (14568 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-15, ratio=20.8%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 26 (VERY WEAK: 20.8% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 1 (VERY NARROW: 0/11 sectors uptrending, spread 54.1%)
  [3/5] Sector Rotation... Score: 59 (BALANCED: Cyclical-Defensive gap 6.9pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 24 (WEAK MOMENTUM: slope=-0.0061, strong decelerating)
  [5/5] Historical Context... Score: 42 (NEAR MEDIAN: 20.8% at 41.9th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 15.9/100
  Zone: Bear (Bear)
  Exposure Guidance: Capital Preservation (0-30%)
  Warning Penalty: -10 (raw score: 25.9)
  Strongest: Sector Rotation (59)
  Weakest: Sector Participation (1)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-18_061032.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-18_061032.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 15.9/100
  Zone: Bear
  Exposure Guidance: Capital Preservation (0-30%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-18_061032.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-18_061032.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-18

> Data as of: 2026-05-15

## Risk Regime

**BALANCED** (score: 59/100)

- Cyclical avg: 20.0%
- Defensive avg: 13.0%
- Difference: 6.9pp
- Commodity avg: 39.9%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Mid** (confidence: low)

- Mid: 70.0 ←
- Late: 65.0
- Early: 52.9
- Recession: 45.5

Evidence:
- Leaders in top ranks: Technology, Industrials, Energy
- Laggards in bottom ranks: Utilities, Consumer Defensive

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 60.2% | Down | Overbought |
| 2 | Technology | 32.4% | Down | Normal |
| 3 | Industrials | 25.5% | Down | Normal |
| 4 | Communication Services | 21.1% | Down | Normal |
| 5 | Healthcare | 19.8% | Down | Normal |
| 6 | Basic Materials | 19.5% | Down | Normal |
| 7 | Consumer Defensive | 14.9% | Down | Normal |
| 8 | Real Estate | 11.3% | Down | Normal |
| 9 | Consumer Cyclical | 10.5% | Down | Normal |
| 10 | Financial | 10.4% | Down | Normal |
| 11 | Utilities | 6.2% | Down | Oversold |

## Trend Summary

- Uptrending: 0 sectors
- Downtrending: 11 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 60.2%
**Oversold** (ratio < 9.7%):
- Utilities: 6.2%

---
*Generated: 2026-05-18T06:10:33*
Checking data freshness...
Data is fresh (latest: 2026-05-15)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-18.md
```
