# Pre-Market Report — 2026-05-28
*Generated: 06:00:55*

## Market Posture

```
Date:            2026-05-28
Breadth:         42.4/100 (Neutral)
Uptrend:         54.7/100
Uptrend warning: Warning Penalty: -3 (raw score: 57.7)
Leading sector:  Technology
Cycle phase:     N/A
Macro events:    none
Flags:           none
Posture:         CAUTIOUS
Ceiling:         50%
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2511 rows, 2016-05-31 to 2026-05-26)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-26, 2 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 57 (NEUTRAL: 8MA=0.574 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 45 (NEUTRAL: Near crossover (gap=-0.021, 8MA rising) (recovery signal))
  [3/6] Peak/Trough Cycle Position... Score: 45 (PEAK (57d ago): recovery attempt, 8MA rising)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.574 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 26th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 34.0 (Dangerous bearish divergence: S&P +9.7%, Breadth 8MA -0.100 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 42.4/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  Strongest: Current Breadth Level & Trend (57)
  Weakest: Bearish Signal Status (25)

  Score Trend: improving (delta +10.0 over 5 observations)

Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-28_060054.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-28_060054.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 42.4/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  JSON Report: reports/pre_market/market_breadth_2026-05-28_060054.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-28_060054.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (15832 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-27, ratio=24.4%, trend=up

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 43 (WEAK: 24.4% uptrend ratio, trend up)
  [2/5] Sector Participation... Score: 67 (HEALTHY: 7/11 sectors uptrending, spread 26.2%)
  [3/5] Sector Rotation... Score: 69 (BALANCED: Cyclical-Defensive gap 7.1pp)
  [4/5] Momentum... Score: 62 (POSITIVE MOMENTUM: slope=-0.0000, accelerating)
  [5/5] Historical Context... Score: 53 (NEAR MEDIAN: 24.4% at 52.8th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 54.7/100
  Zone: Neutral (Neutral)
  Exposure Guidance: Reduced Exposure (60-80%)
  Warning Penalty: -3 (raw score: 57.7)
  Strongest: Sector Rotation (69)
  Weakest: Market Breadth (Overall) (43)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-28_060054.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-28_060054.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 54.7/100
  Zone: Neutral
  Exposure Guidance: Reduced Exposure (60-80%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-28_060054.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-28_060054.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-28

> Data as of: 2026-05-27

## Risk Regime

**BALANCED** (score: 69/100)

- Cyclical avg: 26.5%
- Defensive avg: 19.5%
- Difference: 7.1pp
- Commodity avg: 19.2%
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Early** (confidence: low)

- Early: 75.7 ←
- Mid: 70.0
- Late: 36.7
- Recession: 32.6

Evidence:
- Leaders in top ranks: Technology, Industrials
- Laggards in bottom ranks: Utilities, Consumer Defensive, Healthcare

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Technology | 39.6% | Up | Overbought |
| 2 | Industrials | 30.7% | Up | Normal |
| 3 | Basic Materials | 25.2% | Down | Normal |
| 4 | Real Estate | 24.5% | Up | Normal |
| 5 | Communication Services | 23.6% | Up | Normal |
| 6 | Healthcare | 23.5% | Down | Normal |
| 7 | Consumer Cyclical | 20.6% | Up | Normal |
| 8 | Financial | 18.1% | Up | Normal |
| 9 | Consumer Defensive | 16.2% | Down | Normal |
| 10 | Utilities | 13.6% | Up | Normal |
| 11 | Energy | 13.3% | Down | Normal |

## Trend Summary

- Uptrending: 7 sectors
- Downtrending: 4 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Technology: 39.6%

---
*Generated: 2026-05-28T06:00:55*
Checking data freshness...
Data is fresh (latest: 2026-05-27)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-28.md
```
