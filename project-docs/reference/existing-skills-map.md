# Existing Skills Map

> **Read this when:** considering whether to build something new (check if it exists first), or during Phase 1 audit.

---

## Immediately Useful — Stock & Options Workflow

Use these from Day 1. They work as-is for equity research and options planning.

**Daily workflow:**

- exposure-coach — market posture synthesis, run every morning
- market-breadth-analyzer — 6-component breadth score (free CSV)
- uptrend-analyzer — 5-component uptrend ratio (free CSV)
- economic-calendar-fetcher — earnings dates, FOMC, NFP, CPI (FMP)
- market-news-analyst — last 10 days of market-moving news (web search)

**Stock research:**

- us-stock-analysis — comprehensive fundamental + technical research
- technical-analyst — chart analysis (stocks, indices, FX)
- institutional-flow-tracker — 13F filings, smart money positioning (FMP)
- earnings-calendar — upcoming earnings by date (FMP)

**Trade planning:**

- position-sizer — risk-based sizing for equities
- options-strategy-advisor — Black-Scholes, 17 strategies, Greeks
- breakout-trade-planner — breakout setup planning

**Screening:**

- vcp-screener — Minervini VCP pattern, Stage 2 stocks (FMP)
- canslim-screener — O'Neil CANSLIM, 7 components including RS (FMP)
- earnings-trade-analyzer — 5-factor post-earnings scoring (FMP)
- pead-screener — post-earnings drift detection, weekly candle analysis (FMP)
- theme-detector — trending themes with heat/lifecycle scoring (free + FMP optional)
- finviz-screener — natural language to FinViz filters (free public)
- sector-analyst — sector rotation patterns (free CSV)
- market-top-detector — distribution day detection
- ftd-detector — follow-through day for market bottom confirmation (FMP)
- macro-regime-detector — structural regime detection (FMP)
- us-market-bubble-detector — speculative excess assessment

**Pre-built commands (use as-is):**

- /deep-research TICKER — 8-phase comprehensive report
- /update-research TICKER — diff-based update of prior report
- /intraday-options TICKER CAPITAL — same-day options swing analysis
- /options-strategy-planner TICKER — comprehensive options strategy plan
- /review-portfolio — batch update across watchlist
- /scenario-analyzer headline — 18-month scenario projection (Japanese output)

**Income/dividend strategies (lower priority unless this is your focus):**

- value-dividend-screener — high-yield dividend stocks (FMP + FINVIZ optional)
- dividend-growth-pullback-screener — dividend growth at pullbacks (FMP)
- kanchi-dividend-sop — 5-step dividend SOP
- kanchi-dividend-review-monitor — anomaly detection for dividend positions
- kanchi-dividend-us-tax-accounting — qualified vs ordinary dividend classification
- pair-trade-screener — statistical arbitrage (FMP)

---

## Learning Loop Infrastructure

Use throughout all phases once populated with data.

- trader-memory-core — thesis lifecycle from IDEA to CLOSED, postmortem
- signal-postmortem — post-trade outcome classification and feedback
- edge-pipeline-orchestrator — full edge research pipeline, orchestrates other skills
- edge-strategy-reviewer — deterministic quality gate for strategy drafts
- edge-signal-aggregator — aggregates signals from multiple skills
- edge-candidate-agent — converts research tickets to strategy specs
- trade-hypothesis-ideator — falsifiable hypothesis generation
- strategy-pivot-designer — detects backtest stagnation, proposes pivots
- backtest-expert — methodology framework for equity strategy validation

---

## Quality & Self-Improvement Infrastructure

Enable in Phase 2 with branch protection.

- dual-axis-skill-reviewer — deterministic + optional LLM scoring (0-100)
- skill-idea-miner — mines session logs for new skill ideas
- skill-designer — builds Claude CLI prompts for new skill design
- data-quality-checker — validates markdown reports before use
- skill-improvement-loop — daily auto-review and improvement PRs
- skill-generation-pipeline — weekly idea mining + daily skill creation PRs

---

## Study These As Templates

- parabolic-short-trade-planner — most production-mature skill, 3-phase FSM pattern
- position-sizer — clean offline calculation pattern
- portfolio-manager — broker integration pattern (Alpaca; Robinhood MCP is primary here)
- edge-pipeline-orchestrator — orchestration pattern
- trader-memory-core — state management pattern
- ibd-distribution-day-monitor — daily monitoring pattern

---

## Gaps You Will Build (Phase 2+)

| Phase | Skill / component | Why Needed |
|---|---|---|
| 2 | behavioral-pattern-detector | Personal behavioral detection for stocks/options |
| 3 | agentic-executor (or scripts wrapper) | Autonomous Robinhood Agentic MCP execution |

---

## Authoritative Source

This map is a quick reference. Full detail lives in:

- README.md — full skill descriptions
- CLAUDE.md — operational details, API requirements
- docs/en/skill-catalog.md — categorized catalog

Keep this file updated when you build or retire a skill.
