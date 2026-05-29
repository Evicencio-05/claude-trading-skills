# Pre-Market Report — 2026-05-26
*Generated: 06:00:58*

## Market Posture

```
Date:            2026-05-26
Breadth:         41.6/100 (Neutral)
Uptrend:         37.5/100
Uptrend warning: Warning Penalty: -7 (raw score: 44.5)
Leading sector:  Energy
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
  Fetching detail CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv... OK (2511 rows, 2016-05-27 to 2026-05-22)
  Fetching summary CSV from https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv... OK (12 metrics)
  Data freshness: OK (latest: 2026-05-22, 4 days old)

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/6] Current Breadth Level & Trend... Score: 57 (NEUTRAL: 8MA=0.567 in downtrend - mixed signals)
  [2/6] 8MA vs 200MA Crossover... Score: 45 (NEUTRAL: Near crossover (gap=-0.028, 8MA rising) (recovery signal))
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
  JSON report saved to: reports/pre_market/market_breadth_2026-05-26_060056.json
  Markdown report saved to: reports/pre_market/market_breadth_2026-05-26_060056.md

======================================================================
Market Breadth Analysis Complete
======================================================================
  Composite Score: 41.6/100
  Health Zone: Neutral
  Equity Exposure: 60-75%
  JSON Report: reports/pre_market/market_breadth_2026-05-26_060056.json
  Markdown Report: reports/pre_market/market_breadth_2026-05-26_060056.md
```

## Uptrend Detail

```
======================================================================
Uptrend Analyzer
Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard
======================================================================

Step 1: Fetching CSV Data
----------------------------------------------------------------------
  Fetching timeseries data... OK (15516 rows)
  Fetching sector summary... OK (11 sectors)
  Latest data: 2026-05-25, ratio=23.1%, trend=down

Step 2: Calculating Components
----------------------------------------------------------------------
  [1/5] Market Breadth (Overall)... Score: 30 (WEAK: 23.1% uptrend ratio, trend down)
  [2/5] Sector Participation... Score: 48 (MODERATE: 5/11 sectors uptrending, spread 35.4%)
  [3/5] Sector Rotation... Score: 59 (BALANCED: Cyclical-Defensive gap 4.8pp [LATE CYCLE WARNING])
  [4/5] Momentum... Score: 48 (NEUTRAL MOMENTUM: slope=-0.0030, steady)
  [5/5] Historical Context... Score: 50 (NEAR MEDIAN: 23.1% at 49.6th percentile historically)

Step 3: Calculating Composite Score
----------------------------------------------------------------------
  Composite Score: 37.5/100
  Zone: Cautious (Cautious-Upper)
  Exposure Guidance: Defensive (30-60%)
  Warning Penalty: -7 (raw score: 44.5)
  Strongest: Sector Rotation (59)
  Weakest: Market Breadth (Overall) (30)

Step 4: Generating Reports
----------------------------------------------------------------------
JSON report saved to: reports/pre_market/uptrend_analysis_2026-05-26_060057.json
Markdown report saved to: reports/pre_market/uptrend_analysis_2026-05-26_060057.md

======================================================================
Uptrend Analysis Complete
======================================================================
  Composite Score: 37.5/100
  Zone: Cautious
  Exposure Guidance: Defensive (30-60%)
  JSON Report: reports/pre_market/uptrend_analysis_2026-05-26_060057.json
  Markdown Report: reports/pre_market/uptrend_analysis_2026-05-26_060057.md
```

## Sector Detail

```
# Sector Rotation Analysis — 2026-05-26

> Data as of: 2026-05-25

## Risk Regime

**BALANCED** (score: 59/100)

- Cyclical avg: 22.4%
- Defensive avg: 17.5%
- Difference: 4.8pp
- Commodity avg: 31.5%
- **Late Cycle Flag**: Commodity sectors leading both cyclical and defensive
- **Divergence Flag**: High intra-group spread detected

## Cycle Phase Estimate

**Mid** (confidence: moderate)

- Mid: 75.0 ←
- Early: 57.1
- Late: 51.7
- Recession: 41.2

Evidence:
- Leaders in top ranks: Technology, Industrials, Energy
- Laggards in bottom ranks: Utilities, Consumer Defensive

## Sector Ranking (by uptrend ratio)

| Rank | Sector | Ratio | Trend | Status |
|------|--------|-------|-------|--------|
| 1 | Energy | 46.7% | Up | Overbought |
| 2 | Technology | 36.2% | Down | Normal |
| 3 | Industrials | 25.2% | Down | Normal |
| 4 | Real Estate | 23.1% | Up | Normal |
| 5 | Healthcare | 22.1% | Down | Normal |
| 6 | Communication Services | 19.3% | Down | Normal |
| 7 | Financial | 17.1% | Up | Normal |
| 8 | Basic Materials | 16.2% | Down | Normal |
| 9 | Consumer Cyclical | 14.1% | Up | Normal |
| 10 | Consumer Defensive | 13.8% | Down | Normal |
| 11 | Utilities | 11.2% | Up | Normal |

## Trend Summary

- Uptrending: 5 sectors
- Downtrending: 6 sectors

## Overbought / Oversold

**Overbought** (ratio > 37%):
- Energy: 46.7%

---
*Generated: 2026-05-26T06:00:58*
Checking data freshness...
Data is fresh (latest: 2026-05-25)
Fetching sector summary...
Parsed 11 sectors
Saved to reports/pre_market/sector_rotation_2026-05-26.md
```
