# Uptrend Analyzer Report

**Generated:** 2026-07-24 06:05:21
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **21.0/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Lower |
| **Zone Proximity** | **Near boundary: +1.0 points from 20 (above)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -10 (raw: 31.0/100) |
| **Active Warnings** | 3: LATE CYCLE WARNING, HIGH SELECTIVITY WARNING, SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Historical Context (36/100) |
| **Weakest Component** | Market Breadth (Overall) (24/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

---

## Active Warnings

### LATE CYCLE WARNING
> Commodity sectors leading both cyclical and defensive groups. Historically associated with late-cycle inflation or sector rotation preceding broader market weakness.

- Favor lower end of exposure range (e.g. 80% if guidance is 80-100%)
- New entries limited to A-grade setups only
- Tighten stops on commodity/cyclical positions
- Monitor for commodity rollover as potential broad market lead indicator

### HIGH SELECTIVITY WARNING
> Wide spread between strongest and weakest sectors indicates highly selective market. Breadth may be masking narrowing leadership.

- Concentrate on sectors with ratio above 10MA
- Avoid lagging sectors even if trend is nominally 'up'
- Reduce position count to highest-conviction ideas

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 19.9% |
| 10-Day MA | 24.3% |
| Trend | down |
| Slope | -0.0064 |
| Distance from 37% (Overbought) | -17.1pp |
| Distance from 9.7% (Oversold) | +10.2pp |
| Date | 2026-07-23 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 24 | 7.2 | VERY WEAK: 19.9% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | █░░░ 33 | 8.2 | NARROW: 5/11 sectors uptrending, spread 47.3% |
| 3 | **Sector Rotation** | 15% | █░░░ 33 | 5.0 | DEFENSIVE TILT: Defensive leads by 4.0pp [LATE CYCLE WARNING] |
| 4 | **Momentum** | 20% | █░░░ 35 | 7.0 | WEAK MOMENTUM: slope=-0.0045, strong decelerating |
| 5 | **Historical Context** | 10% | █░░░ 36 | 3.6 | BELOW AVERAGE: 19.9% at 36.2th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 19.9%
- **10-Day MA:** 24.3%
- **Trend:** down
- **Slope:** -0.0064
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 5/11
- **Count Score:** 40/100
- **Spread:** 47.3% (score: 23/100)
- **Overbought (>37%):** 1 sectors (Energy)
- **Oversold (<9.7%):** 3 sectors (Communication Services, Technology, Consumer Defensive)

### 3. Sector Rotation

- **Cyclical Avg:** 14.7%
- **Defensive Avg:** 18.6%
- **Commodity Avg:** 37.6%
- **Cyclical-Defensive Gap:** -4.0pp
- **Late Cycle Warning:** YES (commodity penalty: -10)
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0524, spread=0.1346
    - Trend dissenter: Industrials (up vs majority down)
  - **Defensive Divergence:** std=0.0744, spread=0.1791
    - Trend dissenter: Consumer Defensive (down vs majority up)
    - Trend dissenter: Healthcare (down vs majority up)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 9.0% | Down | -0.0122 |
| Consumer Cyclical | 14.1% | Down | -0.0013 |
| Communication Services | 9.3% | Down | -0.0148 |
| Financial | 18.5% | Down | -0.0130 |
| Industrials | 22.5% | Up | +0.0033 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 14.8% | Up | +0.0049 |
| Consumer Defensive | 8.3% | Down | -0.0090 |
| Healthcare | 25.2% | Down | -0.0254 |
| Real Estate | 26.2% | Up | +0.0021 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 55.6% | Up | +0.0319 |
| Basic Materials | 19.6% | Up | +0.0087 |


### 4. Momentum

- **Raw Slope:** -0.0064
- **Smoothed Slope (EMA(3)):** -0.0045 (score: 46/100)
- **Acceleration (10v10):** -0.006011 (strong_decelerating, score: 10/100)
- **Sector Slope Breadth:** 5/11 positive (score: 45/100)

### 5. Historical Context

- **Current Ratio:** 19.9%
- **Percentile Rank:** 36.2th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.8%
- **30-Day Avg:** 26.9%
- **90-Day Avg:** 24.0%
- **Data Points:** 764 (2023-08-11 to 2026-07-23)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Energy | 55.6% | 89/160 | 39.4% | Up | +0.0319 | Overbought |
| 2 | Real Estate | 26.2% | 37/141 | 32.5% | Up | +0.0021 | Normal |
| 3 | Healthcare | 25.2% | 106/421 | 35.6% | Down | -0.0254 | Normal |
| 4 | Industrials | 22.5% | 88/391 | 18.6% | Up | +0.0033 | Normal |
| 5 | Basic Materials | 19.6% | 29/148 | 12.8% | Up | +0.0087 | Normal |
| 6 | Financial | 18.5% | 112/606 | 29.7% | Down | -0.0130 | Normal |
| 7 | Utilities | 14.8% | 12/81 | 14.8% | Up | +0.0049 | Normal |
| 8 | Consumer Cyclical | 14.1% | 39/276 | 18.3% | Down | -0.0013 | Normal |
| 9 | Communication Services | 9.3% | 10/108 | 20.6% | Down | -0.0148 | Oversold |
| 10 | Technology | 9.0% | 37/409 | 14.5% | Down | -0.0122 | Oversold |
| 11 | Consumer Defensive | 8.3% | 10/120 | 17.0% | Down | -0.0090 | Oversold |

---

## Recommended Actions

**Zone:** Cautious (Cautious-Lower)
**Exposure Guidance:** Defensive (30-60%)

- Significant cash allocation (40-70%)
- Only hold strongest leaders in uptrending sectors
- Tight stops on all positions
- Consider defensive sector allocation
- No new aggressive entries

---

## Methodology

This analysis uses Monty's Uptrend Ratio Dashboard data to assess market breadth health.
The dashboard tracks ~2,800 US stocks across 11 sectors, measuring the percentage in uptrends.

**5-Component Scoring System (0-100, higher = healthier):**

1. **Market Breadth (30%):** Overall uptrend ratio level and trend direction
2. **Sector Participation (25%):** Number of uptrending sectors and spread uniformity
3. **Sector Rotation (15%):** Cyclical vs Defensive vs Commodity balance
4. **Momentum (20%):** Slope direction, acceleration, and sector slope breadth
5. **Historical Context (10%):** Percentile rank in historical distribution

**Key Thresholds (Monty's Dashboard):** Overbought = 37%, Oversold = 9.7%

For detailed methodology, see `references/uptrend_methodology.md`.

---

**Disclaimer:** This analysis is for educational and informational purposes only. Not investment advice. Past patterns may not predict future outcomes. Conduct your own research and consult a financial advisor before making investment decisions.
