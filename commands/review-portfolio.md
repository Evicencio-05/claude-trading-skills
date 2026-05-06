---
description: "Run a batch update across all tracked tickers in ~/trading-research/reports/, showing staleness and offering to refresh selected or all reports with a portfolio summary table."
---

Run a batch update across all tracked tickers.

1. List all .md files in ~/trading-research/reports/ to identify active tickers.

2. For each ticker found, print:
   - Ticker, last report date, days since last update.

3. Sort by staleness (oldest update first).

4. Ask which tickers to update, or offer to update all.

5. For each selected ticker, run the equivalent of /update-research {TICKER}.

6. After all updates complete, generate a portfolio summary table:

   # Portfolio Research Summary — {today's date}

   | Ticker | Last Updated | Composite | Trend  | Action       | Key Change       |
   |--------|-------------|-----------|--------|--------------|------------------|
   |        |             |           | ↑/→/↓  |              |                  |

   ## Alerts
   {List any tickers where invalidation triggers were hit or nearly hit}

   ## Stalest Reports
   {List any tickers not updated in >14 days}

   Save this summary to ~/trading-research/logs/portfolio_summary_{YYYY-MM-DD}.md
