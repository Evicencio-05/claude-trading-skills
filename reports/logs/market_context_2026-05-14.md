# Pre-Market Report — 2026-05-14
*Generated: 06:27:52*

## Market Posture

```
Date:            2026-05-14
Breadth:         33.1/100 (Bearish)
Uptrend:         33.5/100
Uptrend warning: Warning Penalty: -10 (raw score: 43.5)
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2513 rows, 2016-05-16 to 2026-05-13)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-13, 1 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 52 (NEUTRAL: 8MA=0.559 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 35 (NEGATIVE: 8MA below 200MA (gap=-0.038, 8MA falling))
  [3/6] Peak/Trough Cycle Position... Score: 15 (PEAK (49d ago): gradual decline, 8MA falling)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.559 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 24th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 34.0 (Dangerous bearish divergence: S&P +8.5%, Breadth 8MA -0.120 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 33.1/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  Strongest: Current Breadth Level & Trend (52)
  Weakest: Peak/Trough Cycle Position (15)


Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-14_062751.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-14_062751.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 33.1/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  JSON Report: reports/pre_market/market_breadth_2026-05-14_062751.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-14_062751.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (14252 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-13, ratio=24.0%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 32 (WEAK: 24.0% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 54 (MODERATE: 7/11 sectors uptrending, spread 40.1%)
  [3/5] Sector Rotation... Score: 48 (BALANCED: Cyclical-Defensive gap 2.4pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 40 (NEUTRAL MOMENTUM: slope=-0.0027, strong decelerating)
  [5/5] Historical Context... Score: 52 (NEAR MEDIAN: 24.0% at 51.7th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 33.5/100
  Zone: Cautious (Cautious-Upper)
  Exposure Guidance: Defensive (30-60%)
  Warning Penalty: -10 (raw score: 43.5)
  Strongest: Sector Participation (54)
  Weakest: Market Breadth (Overall) (32)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-14_062752.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-14_062752.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 33.5/100
  Zone: Cautious
  Exposure Guidance: Defensive (30-60%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-14_062752.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-14_062752.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-14

> Data as of: 2026-05-13

## Risk Regime

**BALANCED** (score: 48/100)

- Cyclical avg: 20.9%
- Defensive avg: 18.5%
- Difference: 2.4pp
- Commodity avg: 46.8%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Late** (confidence: low)

- Late: 75.0 ←
- Mid: 70.0
- Recession: 54.0
- Early: 44.3

Evidence:
- Leaders in top ranks: Energy, Basic Materials, Healthcare
- Laggards in bottom ranks: Consumer Cyclical

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 50.9% | Up | Overbought |
| 2 | Basic Materials | 42.8% | Up | Overbought |
| 3 | Technology | 36.2% | Up | Normal |
| 4 | Industrials | 26.9% | Down | Normal |
| 5 | Healthcare | 26.6% | Up | Normal |
| 6 | Communication Services | 18.9% | Up | Normal |
| 7 | Consumer Defensive | 18.3% | Up | Normal |
| 8 | Real Estate | 16.8% | Down | Normal |
| 9 | Utilities | 12.5% | Up | Normal |
| 10 | Consumer Cyclical | 11.7% | Down | Normal |
| 11 | Financial | 10.9% | Down | Normal |

## Trend Summary

- Uptrending: 7 sectors
- Downtrending: 4 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 50.9%
- Basic Materials: 42.8%

---
*Generated: 2026-05-14T06:27:52*
Checking data freshness...
Data is fresh (latest: 2026-05-13)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-14.md
```
