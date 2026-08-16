# Uptrend Analyzer Report

**Generated:** 2026-06-08 06:08:41
**Data Source:** Monty's Uptrend Ratio Dashboard (GitHub CSV)
**API Key Required:** No

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Composite Score** | **39.2/100** |
| **Zone** | 🟠 Cautious |
| **Zone Detail** | Cautious-Upper |
| **Zone Proximity** | **Near boundary: -0.8 points from 40 (below)** |
| **Exposure Guidance** | Defensive (30-60%) |
| **Warning Penalty** | -3 (raw: 42.2/100) |
| **Active Warnings** | 1: SECTOR DIVERGENCE WARNING |
| **Strongest Component** | Momentum (58/100) |
| **Weakest Component** | Market Breadth (Overall) (20/100) |
| **Data Quality** | Complete (5/5 components) |
| **Confidence** | High (moderate, Both regime coverage) |

> **Guidance:** Weak breadth environment. Prioritize capital preservation over gains.

---

## Active Warnings

### SECTOR DIVERGENCE WARNING
> Significant divergence detected within sector groups. Some sectors within the same group are moving in opposite directions, suggesting hidden risk beneath the averages.

- Verify individual sector trends before entering positions
- Avoid sectors diverging from their group majority
- Monitor for group convergence or further deterioration

---

## Current Market Snapshot

| Metric | Value |
|--------|-------|
| Uptrend Ratio | 17.8% |
| 10-Day MA | 22.9% |
| Trend | down |
| Slope | -0.0053 |
| Distance from 37% (Overbought) | -19.2pp |
| Distance from 9.7% (Oversold) | +8.1pp |
| Date | 2026-06-05 |

---

## Component Scores

| # | Component | Weight | Score | Contribution | Signal |
|---|-----------|--------|-------|--------------|--------|
| 1 | **Market Breadth (Overall)** | 30% | █░░░ 20 | 6.0 | VERY WEAK: 17.8% uptrend ratio, trend down |
| 2 | **Sector Participation** | 25% | ██░░ 52 | 13.0 | MODERATE: 3/11 sectors uptrending, spread 14.3% |
| 3 | **Sector Rotation** | 15% | ██░░ 57 | 8.5 | BALANCED: Cyclical-Defensive gap 2.0pp |
| 4 | **Momentum** | 20% | ██░░ 58 | 11.6 | NEUTRAL MOMENTUM: slope=-0.0016, strong accelerating |
| 5 | **Historical Context** | 10% | █░░░ 31 | 3.1 | BELOW AVERAGE: 17.8% at 31.4th percentile historically |

---

## Component Details

### 1. Market Breadth (Overall)

- **Uptrend Ratio:** 17.8%
- **10-Day MA:** 22.9%
- **Trend:** down
- **Slope:** -0.0053
- **Trend Adjustment:** -5

### 2. Sector Participation

- **Uptrending Sectors:** 3/11
- **Count Score:** 20/100
- **Spread:** 14.3% (score: 100/100)
- **Overbought (>37%):** 0 sectors ()
- **Oversold (<9.7%):** 2 sectors (Basic Materials, Utilities)

### 3. Sector Rotation

- **Cyclical Avg:** 18.3%
- **Defensive Avg:** 16.2%
- **Commodity Avg:** 11.9%
- **Cyclical-Defensive Gap:** 2.0pp
- **Divergence Warning:** YES (penalty: -5)
  - **Cyclical Divergence:** std=0.0333, spread=0.1009
    - Outlier: Communication Services (deviation: -0.0517)
    - Trend dissenter: Consumer Cyclical (up vs majority down)
    - Trend dissenter: Financial (up vs majority down)
  - **Defensive Divergence:** std=0.0476, spread=0.1321
    - Outlier: Utilities (deviation: -0.0736)
    - Trend dissenter: Consumer Defensive (up vs majority down)

**Cyclical Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Technology | 23.2% | Down | -0.0131 |
| Consumer Cyclical | 17.8% | Up | +0.0037 |
| Communication Services | 13.1% | Down | -0.0062 |
| Financial | 17.2% | Up | +0.0001 |
| Industrials | 20.1% | Down | -0.0051 |


**Defensive Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Utilities | 8.9% | Down | -0.0024 |
| Consumer Defensive | 16.2% | Up | +0.0024 |
| Healthcare | 17.7% | Down | -0.0043 |
| Real Estate | 22.1% | Down | -0.0010 |


**Commodity Sectors:**

| Sector | Ratio | Trend | Slope |
|--------|-------|-------|-------|
| Energy | 14.0% | Down | -0.0324 |
| Basic Materials | 9.7% | Down | -0.0066 |


### 4. Momentum

- **Raw Slope:** -0.0053
- **Smoothed Slope (EMA(3)):** -0.0016 (score: 51/100)
- **Acceleration (10v10):** 0.006067 (strong_accelerating, score: 90/100)
- **Sector Slope Breadth:** 3/11 positive (score: 27/100)

### 5. Historical Context

- **Current Ratio:** 17.8%
- **Percentile Rank:** 31.4th
- **Historical Range:** 1.1% - 44.3%
- **Historical Median:** 23.4%
- **30-Day Avg:** 24.2%
- **90-Day Avg:** 24.7%
- **Data Points:** 730 (2023-08-11 to 2026-06-05)
- **Confidence:** High (sample: moderate, regime: Both, recency: balanced)

---

## Sector Heatmap

| Rank | Sector | Ratio | Count/Total | 10MA | Trend | Slope | Status |
|------|--------|-------|-------------|------|-------|-------|--------|
| 1 | Technology | 23.2% | 95/410 | 37.5% | Down | -0.0131 | Normal |
| 2 | Real Estate | 22.1% | 32/145 | 20.5% | Down | -0.0010 | Normal |
| 3 | Industrials | 20.1% | 77/384 | 27.8% | Down | -0.0051 | Normal |
| 4 | Consumer Cyclical | 17.8% | 49/276 | 19.6% | Up | +0.0037 | Normal |
| 5 | Healthcare | 17.7% | 71/401 | 20.6% | Down | -0.0043 | Normal |
| 6 | Financial | 17.2% | 103/598 | 17.3% | Up | +0.0001 | Normal |
| 7 | Consumer Defensive | 16.2% | 19/117 | 13.0% | Up | +0.0024 | Normal |
| 8 | Energy | 14.0% | 23/164 | 19.9% | Down | -0.0324 | Normal |
| 9 | Communication Services | 13.1% | 14/107 | 21.3% | Down | -0.0062 | Normal |
| 10 | Basic Materials | 9.7% | 15/155 | 24.2% | Down | -0.0066 | Oversold |
| 11 | Utilities | 8.9% | 7/79 | 12.4% | Down | -0.0024 | Oversold |

---

## Recommended Actions

**Zone:** Cautious (Cautious-Upper)
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
