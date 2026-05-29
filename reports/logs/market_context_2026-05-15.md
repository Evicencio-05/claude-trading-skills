# Pre-Market Report — 2026-05-15
*Generated: 06:00:49*

## Market Posture

```
Date:            2026-05-15
Breadth:         32.4/100 (Bearish)
Uptrend:         26.7/100
Uptrend warning: Warning Penalty: -10 (raw score: 36.7)
Leading sector:  Energy
Cycle phase:     Late
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
  Data freshness: OK (latest: 2026-05-14, 1 days old)

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
  JSON report saved to: reports/pre_market/market_breadth_2026-05-15_060048.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-15_060048.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  JSON Report: reports/pre_market/market_breadth_2026-05-15_060048.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-15_060048.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (14410 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-14, ratio=24.6%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 33 (WEAK: 24.6% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 29 (NARROW: 2/11 sectors uptrending, spread 40.9%)
  [3/5] Sector Rotation... Score: 55 (BALANCED: Cyclical-Defensive gap 5.1pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 30 (WEAK MOMENTUM: slope=-0.0041, strong decelerating)
  [5/5] Historical Context... Score: 53 (NEAR MEDIAN: 24.6% at 52.9th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 26.7/100
  Zone: Cautious (Cautious-Lower)
  Exposure Guidance: Defensive (30-60%)
  Warning Penalty: -10 (raw score: 36.7)
  Strongest: Sector Rotation (55)
  Weakest: Sector Participation (29)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-15_060048.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-15_060048.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 26.7/100
  Zone: Cautious
  Exposure Guidance: Defensive (30-60%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-15_060048.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-15_060048.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-15

> Data as of: 2026-05-14

## Risk Regime

**BALANCED** (score: 55/100)

- Cyclical avg: 23.0%
- Defensive avg: 17.9%
- Difference: 5.1pp
- Commodity avg: 43.9%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Late** (confidence: low)

- Late: 75.0 ←
- Mid: 70.0
- Recession: 49.8
- Early: 48.6

Evidence:
- Leaders in top ranks: Energy, Basic Materials, Healthcare
- Laggards in bottom ranks: Consumer Cyclical

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 52.4% | Down | Overbought |
| 2 | Technology | 36.8% | Down | Normal |
| 3 | Basic Materials | 35.4% | Up | Normal |
| 4 | Industrials | 30.8% | Down | Normal |
| 5 | Healthcare | 25.7% | Up | Normal |
| 6 | Communication Services | 23.4% | Down | Normal |
| 7 | Real Estate | 18.9% | Down | Normal |
| 8 | Consumer Defensive | 14.8% | Down | Normal |
| 9 | Financial | 12.5% | Down | Normal |
| 10 | Utilities | 12.3% | Down | Normal |
| 11 | Consumer Cyclical | 11.5% | Down | Normal |

## Trend Summary

- Uptrending: 2 sectors
- Downtrending: 9 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 52.4%

---
*Generated: 2026-05-15T06:00:49*
Checking data freshness...
Data is fresh (latest: 2026-05-14)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-15.md
```
