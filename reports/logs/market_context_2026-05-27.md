# Pre-Market Report — 2026-05-27
*Generated: 06:01:34*

## Market Posture

```
Date:            2026-05-27
Breadth:         41.6/100 (Neutral)
Uptrend:         55.1/100
Uptrend warning: Warning Penalty: -3 (raw score: 58.1)
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2510 rows, 2016-05-31 to 2026-05-22)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-22, 5 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 57 (NEUTRAL: 8MA=0.567 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 45 (NEUTRAL: Near crossover (gap=-0.027, 8MA rising) (recovery signal))
  [3/6] Peak/Trough Cycle Position... Score: 45 (PEAK (56d ago): recovery attempt, 8MA rising)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.567 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 25th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 26.0 (Dangerous bearish divergence: S&P +9.0%, Breadth 8MA -0.105 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 41.6/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  Strongest: Current Breadth Level & Trend (57)
  Weakest: Bearish Signal Status (25)

  Score Trend: improving (delta +9.2 over 5 observations)

Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-27_060133.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-27_060133.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 41.6/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  JSON Report: reports/pre_market/market_breadth_2026-05-27_060133.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-27_060133.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (15674 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-26, ratio=26.3%, trend=up

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 48 (NEUTRAL: 26.3% uptrend ratio, trend up)
  [2/5] Sector Participation... Score: 66 (HEALTHY: 7/11 sectors uptrending, spread 27.7%)
  [3/5] Sector Rotation... Score: 71 (RISK-ON: Cyclical leads by 8.2pp)
  [4/5] Momentum... Score: 54 (NEUTRAL MOMENTUM: slope=-0.0004, steady)
  [5/5] Historical Context... Score: 58 (NEAR MEDIAN: 26.3% at 57.7th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 55.1/100
  Zone: Neutral (Neutral)
  Exposure Guidance: Reduced Exposure (60-80%)
  Warning Penalty: -3 (raw score: 58.1)
  Strongest: Sector Rotation (71)
  Weakest: Market Breadth (Overall) (48)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-27_060134.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-27_060134.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 55.1/100
  Zone: Neutral
  Exposure Guidance: Reduced Exposure (60-80%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-27_060134.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-27_060134.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-27

> Data as of: 2026-05-26

## Risk Regime

**RISK-ON** (score: 71/100)

- Cyclical avg: 27.3%
- Defensive avg: 19.1%
- Difference: 8.2pp
- Commodity avg: 27.2%
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Mid** (confidence: low)

- Mid: 80.0 ←
- Early: 75.7
- Late: 50.0
- Recession: 32.6

Evidence:
- Leaders in top ranks: Technology, Industrials, Energy
- Laggards in bottom ranks: Utilities, Consumer Defensive

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Technology | 39.9% | Up | Overbought |
| 2 | Industrials | 30.2% | Up | Normal |
| 3 | Energy | 27.3% | Down | Normal |
| 4 | Basic Materials | 27.1% | Down | Normal |
| 5 | Real Estate | 25.2% | Up | Normal |
| 6 | Healthcare | 24.3% | Down | Normal |
| 7 | Financial | 23.7% | Up | Normal |
| 8 | Communication Services | 23.4% | Up | Normal |
| 9 | Consumer Cyclical | 19.1% | Up | Normal |
| 10 | Utilities | 14.8% | Up | Normal |
| 11 | Consumer Defensive | 12.2% | Down | Normal |

## Trend Summary

- Uptrending: 7 sectors
- Downtrending: 4 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Technology: 39.9%

---
*Generated: 2026-05-27T06:01:34*
Checking data freshness...
Data is fresh (latest: 2026-05-26)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-27.md
```
