# LuxAlgo — Volume Profile with Node Detection

Source: [TradingView — Volume Profile with Node Detection (LuxAlgo)](https://www.tradingview.com/v/zVCsx5DL/) (open-source; updated May 15, 2024).

Operator displays this on the **right** of price (sometimes extended left). Orange/blue/gray bars are the profile histogram; shelves = significant volume nodes/clusters.

## What it shows

Volume of trades across price levels (“buckets”). Height of each bar = volume at that price. Used here as **VP shelves** — zones of acceptance or rejection.

## Node types

| Concept | Definition | Trading relevance (from LuxAlgo) |
|---------|------------|----------------------------------|
| **Peak volume node** | Volume at level N higher than N neighbors before/after | Intensified activity; often **consolidation** / indecision zones; clusters show the range |
| **Trough volume node** | Volume at level N lower than neighbors | Thin interest between denser areas |
| **Highest volume nodes** | Strongest volume areas | **Strong price acceptance** |
| **Lowest volume nodes** | Weakest volume areas | **Rejection** or low interest |
| **Point of Control (POC)** | Highest-volume level in profile | Key acceptance magnet (if shown) |
| **Value Area (VAH/VAL)** | Band covering configured % of volume | Core traded range (if shown) |

## Settings the operator may use (do not assume values)

- Volume Peaks / Troughs / Clusters toggles + detection %
- Volume Node Threshold %
- Highest / Lowest Volume Nodes count
- Profile lookback length, value area %, rows, width, placement (right)

## Agent extract rules

1. Prefer labeled prices on the profile (high/low/node labels).
2. Describe major **shelves** as price bands when discrete nodes are hard to read.
3. Orange/blue coloring is LuxAlgo value-area / up-down customization — not TradeWhisperer candle colors.
4. Gray/dark bars usually lower-volume rows relative to bright shelves.
5. Never invent POC/VAH/VAL if not labeled on the screenshot.
