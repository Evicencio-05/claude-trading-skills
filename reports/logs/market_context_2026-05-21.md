# Pre-Market Report — 2026-05-21
*Generated: 06:06:05*

## Market Posture

```
Date:            2026-05-21
Breadth:         32.4/100 (Bearish)
Uptrend:         20.3/100
Uptrend warning: Warning Penalty: -7 (raw score: 27.3)
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2512 rows, 2016-05-23 to 2026-05-19)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-19, 2 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 52 (NEUTRAL: 8MA=0.551 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 35 (NEGATIVE: 8MA below 200MA (gap=-0.044, 8MA falling))
  [3/6] Peak/Trough Cycle Position... Score: 15 (PEAK (53d ago): gradual decline, 8MA falling)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.551 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 23th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 26.0 (Dangerous bearish divergence: S&P +7.0%, Breadth 8MA -0.121 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  Strongest: Current Breadth Level & Trend (52)
  Weakest: Peak/Trough Cycle Position (15)


Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-21_060603.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-21_060603.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  JSON Report: reports/pre_market/market_breadth_2026-05-21_060603.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-21_060603.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (15042 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-20, ratio=21.6%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 27 (VERY WEAK: 21.6% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 7 (VERY NARROW: 1/11 sectors uptrending, spread 49.1%)
  [3/5] Sector Rotation... Score: 55 (BALANCED: Cyclical-Defensive gap 3.3pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 24 (WEAK MOMENTUM: slope=-0.0086, strong decelerating)
  [5/5] Historical Context... Score: 44 (NEAR MEDIAN: 21.6% at 43.7th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 20.3/100
  Zone: Cautious (Cautious-Lower)
  Exposure Guidance: Defensive (30-60%)
  Warning Penalty: -7 (raw score: 27.3)
  Strongest: Sector Rotation (55)
  Weakest: Sector Participation (7)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-21_060604.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-21_060604.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 20.3/100
  Zone: Cautious
  Exposure Guidance: Defensive (30-60%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-21_060604.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-21_060604.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-21

> Data as of: 2026-05-20

## Risk Regime

**BALANCED** (score: 55/100)

- Cyclical avg: 20.1%
- Defensive avg: 16.8%
- Difference: 3.3pp
- Commodity avg: 33.5%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive

## Cycle Phase Estimate

**Mid** (confidence: moderate)

- Mid: 75.0 ←
- Early: 62.9
- Late: 56.7
- Recession: 45.5

Evidence:
- Leaders in top ranks: Technology, Industrials, Energy
- Laggards in bottom ranks: Utilities, Consumer Defensive

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 57.8% | Up | Overbought |
| 2 | Technology | 29.6% | Down | Normal |
| 3 | Industrials | 22.0% | Down | Normal |
| 4 | Communication Services | 21.1% | Down | Normal |
| 5 | Real Estate | 21.0% | Down | Normal |
| 6 | Healthcare | 20.9% | Down | Normal |
| 7 | Financial | 17.8% | Down | Normal |
| 8 | Consumer Defensive | 16.4% | Down | Normal |
| 9 | Consumer Cyclical | 9.8% | Down | Normal |
| 10 | Basic Materials | 9.1% | Down | Oversold |
| 11 | Utilities | 8.8% | Down | Oversold |

## Trend Summary

- Uptrending: 1 sectors
- Downtrending: 10 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 57.8%
**Oversold** (ratio < 9.7%):
- Basic Materials: 9.1%
- Utilities: 8.8%

---
*Generated: 2026-05-21T06:06:05*
Checking data freshness...
Data is fresh (latest: 2026-05-20)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-21.md
```
