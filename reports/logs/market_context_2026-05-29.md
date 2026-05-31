# Pre-Market Report — 2026-05-29
*Generated: 14:10:51*

## Market Posture

```
Date:            2026-05-29
Breadth:         42.4/100 (Neutral)
Uptrend:         46.9/100
Uptrend warning: Warning Penalty: -3 (raw score: 49.9)
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2513 rows, 2016-05-31 to 2026-05-28)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-28, 1 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 57 (NEUTRAL: 8MA=0.582 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 45 (NEUTRAL: Near crossover (gap=-0.013, 8MA rising) (recovery signal))
  [3/6] Peak/Trough Cycle Position... Score: 45 (PEAK (59d ago): recovery attempt, 8MA rising)
  [4/6] Bearish Signal Status... Score: 25 (WARNING (muted): Bearish signal active in downtrend, but 8MA=0.582 still relatively strong [PINK ZONE])
  [5/6] Historical Percentile... Score: 30 (LOW: 27th percentile - below average breadth)
  [6/6] S&P 500 vs Breadth Divergence... Score: 34.0 (Dangerous bearish divergence: S&P +10.4%, Breadth 8MA -0.076 over 60d)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 42.4/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  Strongest: Current Breadth Level & Trend (57)
  Weakest: Bearish Signal Status (25)


Step 4: Generating Reports
----------------------------------------------------------------------
  JSON report saved to: reports/pre_market/market_breadth_2026-05-29_141049.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-29_141049.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 42.4/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  JSON Report: reports/pre_market/market_breadth_2026-05-29_141049.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-29_141049.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (15990 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-28, ratio=23.8%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 32 (WEAK: 23.8% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 54 (MODERATE: 4/11 sectors uptrending, spread 27.4%)
  [3/5] Sector Rotation... Score: 70 (RISK-ON: Cyclical leads by 7.5pp)
  [4/5] Momentum... Score: 56 (NEUTRAL MOMENTUM: slope=-0.0004, accelerating)
  [5/5] Historical Context... Score: 51 (NEAR MEDIAN: 23.8% at 51.3th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 46.9/100
  Zone: Neutral (Neutral)
  Exposure Guidance: Reduced Exposure (60-80%)
  Warning Penalty: -3 (raw score: 49.9)
  Strongest: Sector Rotation (70)
  Weakest: Market Breadth (Overall) (32)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-29_141050.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-29_141050.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 46.9/100
  Zone: Neutral
  Exposure Guidance: Reduced Exposure (60-80%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-29_141050.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-29_141050.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-29

> Data as of: 2026-05-28

## Risk Regime

**RISK-ON** (score: 70/100)

- Cyclical avg: 25.8%
- Defensive avg: 18.3%
- Difference: 7.5pp
- Commodity avg: 20.1%
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Mid** (confidence: low)

- Mid: 80.0 ←
- Early: 75.7
- Late: 41.7
- Recession: 32.6

Evidence:
- Leaders in top ranks: Technology, Industrials, Consumer Cyclical
- Laggards in bottom ranks: Utilities, Consumer Defensive

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Technology | 39.7% | Up | Overbought |
| 2 | Industrials | 29.5% | Down | Normal |
| 3 | Basic Materials | 27.6% | Down | Normal |
| 4 | Healthcare | 24.2% | Down | Normal |
| 5 | Real Estate | 22.9% | Up | Normal |
| 6 | Consumer Cyclical | 22.5% | Up | Normal |
| 7 | Communication Services | 21.6% | Down | Normal |
| 8 | Financial | 15.5% | Up | Normal |
| 9 | Consumer Defensive | 13.7% | Down | Normal |
| 10 | Energy | 12.7% | Down | Normal |
| 11 | Utilities | 12.3% | Down | Normal |

## Trend Summary

- Uptrending: 4 sectors
- Downtrending: 7 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Technology: 39.7%

---
*Generated: 2026-05-29T14:10:51*
Checking data freshness...
Data is fresh (latest: 2026-05-28)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-29.md
```
