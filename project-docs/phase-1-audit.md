# Phase 1 — Audit & Activate

**Duration:** 4 weeks
**Goal:** Understand what the existing fork already does for both workflows, set up infrastructure, and generate the data the system needs to learn from.

---

## Why This Phase Exists

The fork has 40+ skills covering stock research, screening, learning loops, and self-improvement infrastructure. Most of this is immediately useful for individual stock and options work. The futures gap is narrower than it might seem — market context, technical analysis, and position sizing exist and translate. What's missing is futures-specific execution plumbing, which gets built in Phase 2.

The temptation is to start building futures skills immediately. Don't. Until you've used the existing skills, you won't know what actually needs building versus what just needs configuration. Audit first.

The other reason: `trader-memory-core` needs your actual trades to produce useful patterns. Generating that data — across both stocks and futures — is the real Phase 1 deliverable.

---

## Week 1 — Setup

### Environment

- [ ] Verify `pre-commit install && pre-commit install --hook-type pre-push` runs clean
- [ ] Verify all hooks pass on a no-op commit
- [ ] Fix any hook failures before continuing
- [ ] Run `python3 -m pytest scripts/tests/ -v` — confirm baseline tests pass

### Directories the existing commands expect

These should already exists, but verify.

```bash
mkdir -p ~/trading-research/{reports,archives,intraday,options,logs}
mkdir -p state/theses
mkdir -p reports/skill-improvement-log reports/skill-generation-log
```

### API keys & budget

- [ ] FMP free tier: <https://financialmodelingprep.com/developer/docs>
- [ ] export FMP_API_KEY=... in shell profile
- [ ] Anthropic API key. Set $30/mo hard budget alert in console.

### Accounts

- [ ] Lucid Trading account — LucidFlex 50K evaluation to learn the platform
- [ ] Verify Tradovate login works (defer API access to Phase 2)
- [ ] Confirm Robinhood account accessible for manual trade logging

### Defer

Launchd auto-PR pipelines (skill-improvement, skill-generation) — disable until Phase 3.

---

## Weeks 2–3 — The Audit

For each skill: read SKILL.md, run with realistic input, rate it. Build skills_audit.md at repo root.

### Audit template

```
## <skill-name>
- [ ] Read SKILL.md
- [ ] Ran with realistic input
- Usefulness for stock/options workflow (1-5): _
- Usefulness for futures workflow (1-5): _
- Status: works as-is / needs extension / not relevant
- Notes:
- Time: _ min
```

Rate BOTH workflows separately. A skill might be 1/5 for futures and 5/5 for stocks.

### Audit priority order

**Tier 1 — Core stock & options workflow (audit first)**

These are immediately useful for your Robinhood account and options trading.

1. exposure-coach — daily market posture, first thing every morning
2. technical-analyst — chart analysis for stocks and futures
3. us-stock-analysis — fundamental + technical equity research
4. trader-memory-core — start logging trades here today
5. position-sizer — risk-based sizing (futures extension in Phase 2)
6. market-news-analyst — catalyst awareness
7. earnings-trade-analyzer — post-earnings reaction scoring
8. options-strategy-advisor — Black-Scholes, Greeks, strategy comparison
9. economic-calendar-fetcher — critical for stocks and futures
10. pead-screener — post-earnings drift setups

**Tier 2 — Screening and context (audit second)**

11. market-breadth-analyzer, uptrend-analyzer
12. vcp-screener — Minervini VCP for swing trading
13. canslim-screener — growth stock methodology
14. market-top-detector, ftd-detector
15. sector-analyst, theme-detector
16. institutional-flow-tracker
17. parabolic-short-trade-planner — study as Phase 2 template
18. portfolio-manager — study as Tradovate integration template

**Tier 3 — Learning loop infrastructure (read, don't necessarily run)**

19. edge-pipeline-orchestrator
20. signal-postmortem
21. dual-axis-skill-reviewer
22. backtest-expert
23. trader-memory-core scripts — read thesis_ingest.py in detail

**Tier 4 — Equity strategies (run if time permits)**

24. pair-trade-screener
25. value-dividend-screener, dividend-growth-pullback-screener
26. kanchi-dividend-sop and related
27. us-market-bubble-detector

---

## Week 4 — Generate Baseline Data

### Run the existing commands

- [ ] /deep-research on 3-5 stocks you're actually watching right now
- [ ] /intraday-options on a stock with a live setup
- [ ] /update-research on one of the above a week later
- [ ] /scenario-analyzer on one macro headline affecting your watchlist

### Daily market context routine

For 10+ trading days before market open:

- [ ] Run market-breadth-analyzer
- [ ] Run exposure-coach
- [ ] Save to ~/trading-research/logs/market_context_YYYY-MM-DD.md
- [ ] End of day: 2-3 sentences on whether the call matched what happened

### Trade logging — most important deliverable

For every trade (stock, option, futures, paper or real):

- [ ] Log to trader-memory-core using thesis_ingest.py
- [ ] Required: ticker, direction, entry/exit, size, thesis (why), confidence 1-5, tags, stop, target
- [ ] After close: pnl, review (what happened, what was missed)

Tag by workflow: ["stock_swing"], ["options_earnings"], ["futures_lucid_eval"] etc.
If zero real trades: log paper trades or hypothetical setups from research.

### Lucid evaluation

- [ ] Take trades on Lucid eval account
- [ ] Note platform mechanics: drawdown buffer display, qualifying days counter, auto-flatten behavior
- [ ] Log every trade to trader-memory-core with account: lucid_eval tag

---

## Exit Criteria

- [ ] skills_audit.md with dual ratings for all Tier 1-2 skills
- [ ] At least 8 Tier 1 skills audited and rated
- [ ] 10+ trades logged across at least 2 different trade types
- [ ] 10+ days of daily market context saved
- [ ] /deep-research run on at least 3 real tickers
- [ ] At least one Lucid eval account opened and one trade taken
- [ ] Total Anthropic spend < $20
- [ ] Pre-commit hooks pass cleanly

---

## Common Pitfalls

1. Only auditing futures-relevant skills — stock research skills are your PRIMARY workflow right now
2. Spending more than 15 min per skill — mark 3/5 and move on
3. Not logging trades because "still setting up" — log hypotheticals
4. Drifting into Phase 2 work — futures skill-building is Phase 2
5. Enabling the launchd jobs — Phase 3

---

## What's NOT in Phase 1

Writing new skills, Tradovate API, behavioral detection, backtesting, anything autonomous.

## When Ready to Advance

Update PROJECT.md Active Phase to Phase 2. Read project-docs/phase-2-futures-skills.md.
