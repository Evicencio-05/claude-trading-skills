# Pre-Market Report — 2026-05-19
*Generated: 06:19:51*

## Market Posture

```
Date:            2026-05-19
Breadth:         32.4/100 (Bearish)
Uptrend:         18.0/100
Uptrend warning: Warning Penalty: -10 (raw score: 28.0)
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2511 rows, 2016-05-20 to 2026-05-15)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-15, 4 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 52 (NEUTRAL: 8MA=0.550 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 35 (NEGATIVE: 8MA below 200MA (gap=-0.046, 8MA falling))
  [3/6] Peak/Trough Cycle Position... Score: 15 (PEAK (51d ago): gradual decline, 8MA falling)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.550 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 23th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 26.0 (Dangerous bearish divergence: S&P +7.5%, Breadth 8MA -0.126 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  Strongest: Current Breadth Level & Trend (52)
  Weakest: Peak/Trough Cycle Position (15)


Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-19_061947.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-19_061947.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 32.4/100
  Health Zone: Weakening
  Equity Exposure: 40-60%
  JSON Report: reports/pre_market/market_breadth_2026-05-19_061947.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-19_061947.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (14726 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-18, ratio=19.5%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 24 (VERY WEAK: 19.5% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 12 (VERY NARROW: 3/11 sectors uptrending, spread 62.0%)
  [3/5] Sector Rotation... Score: 54 (BALANCED: Cyclical-Defensive gap 4.9pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 30 (WEAK MOMENTUM: slope=-0.0053, strong decelerating)
  [5/5] Historical Context... Score: 37 (BELOW AVERAGE: 19.5% at 37.2th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 18.0/100
  Zone: Bear (Bear)
  Exposure Guidance: Capital Preservation (0-30%)
  Warning Penalty: -10 (raw score: 28.0)
  Strongest: Sector Rotation (54)
  Weakest: Sector Participation (12)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-19_061948.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-19_061948.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 18.0/100
  Zone: Bear
  Exposure Guidance: Capital Preservation (0-30%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-19_061948.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-19_061948.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-19

> Data as of: 2026-05-18

## Risk Regime

**BALANCED** (score: 54/100)

- Cyclical avg: 18.2%
- Defensive avg: 13.2%
- Difference: 4.9pp
- Commodity avg: 41.9%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Recession** (confidence: low)

- Recession: 63.1 ←
- Late: 56.7
- Mid: 55.0
- Early: 48.6

Evidence:
- Leaders in top ranks: Consumer Defensive, Healthcare
- Laggards in bottom ranks: Consumer Cyclical, Financial

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 69.5% | Up | Overbought |
| 2 | Technology | 27.8% | Down | Normal |
| 3 | Communication Services | 22.0% | Up | Normal |
| 4 | Industrials | 21.5% | Down | Normal |
| 5 | Consumer Defensive | 15.5% | Up | Normal |
| 6 | Healthcare | 15.1% | Down | Normal |
| 7 | Real Estate | 14.8% | Down | Normal |
| 8 | Basic Materials | 14.3% | Down | Normal |
| 9 | Financial | 10.9% | Down | Normal |
| 10 | Consumer Cyclical | 8.7% | Down | Oversold |
| 11 | Utilities | 7.5% | Down | Oversold |

## Trend Summary

- Uptrending: 3 sectors
- Downtrending: 8 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 69.5%
**Oversold** (ratio < 9.7%):
- Consumer Cyclical: 8.7%
- Utilities: 7.5%

---
*Generated: 2026-05-19T06:19:51*
Checking data freshness...
Data is fresh (latest: 2026-05-18)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-19.md
```
