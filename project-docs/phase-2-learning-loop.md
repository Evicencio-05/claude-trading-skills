# Phase 2 — Learning Loop

**Duration:** 8 weeks
**Goal:** Personalize the learning infrastructure for stock/options workflows. Detect behavioral patterns, validate playbook setups, improve research quality, and enable the skill auto-improvement loop.

---

## Prerequisites

Phase 1 exit criteria met. You should have:

- 10+ trades logged across ≥2 types in `trader-memory-core`
- 3+ co-pilot Agentic trades with full thesis logging
- Daily pre-market stack running reliably
- Personal playbook seed started in [playbook.md](playbook.md)

---

## What you're building

### 2.1 — behavioral-pattern-detector (Weeks 1–2)

Reads `trader-memory-core` history and flags stock/options behavioral patterns:

- Overtrading days: &gt;5 trades in a single session
- Revenge trades: new entry within 30 min of a stopped-out loss
- Moved stops: stop moved away from entry after trade was open
- FOMO entries: chasing a move beyond the original plan
- Ignored research: trade without a completed research report when warranted
- Skipped stop: manual close at larger loss than defined stop
- Confidence mismatch: large position on low-confidence thesis
- Earnings gamble: entry within 48 hrs of earnings without explicit earnings thesis
- IV ignorance: bought options when IV rank &gt;70
- Thesis drift: held past original invalidation trigger

**Output:**

- Daily report of patterns triggered yesterday
- Pre-trade hook: `/deep-research` and co-pilot checklist query this skill for warnings
- Weekly summary in Streamlit dashboard

**Architecture:** Reads from trader-memory-core SQLite; thresholds in `config.yaml`; no external APIs.

### 2.2 — Personal playbook (Weeks 2–4)

Expand [playbook.md](playbook.md) with stock/options setups only:

```markdown
## Stock & Options Setups

### Setup: [Name]
- What it looks like
- Conditions required
- Entry trigger
- Stop placement
- Target methodology
- Historical performance (updated by edge-pipeline-orchestrator)
- When NOT to take it

## Risk Rules

### Per-trade
- Max risk per trade: 1% of account
- Max concurrent positions: [your number]

### Per-day
- Max trades per day: 5 (warning at 3)
- Stop trading after 2 consecutive losses

## Lessons (most recent first)
```

**Process:**

- Week 2: Document current setups (even if just 2–3)
- Week 3: Run `edge-pipeline-orchestrator` on full trade history
- Week 4: Review proposed rules; approve/reject/modify — every rule is your decision

### 2.3 — Equity backtesting (Weeks 4–5)

Use `backtest-expert` skill to validate playbook setups on historical equity data:

- Define entry/stop/target as code per setup
- Model slippage and commissions honestly
- Walk-forward analysis (rolling 6-month train, 3-month test)
- Regime-segmented analysis (high VIX vs low VIX)

**Quality gates** (must pass before a setup graduates to live co-pilot):

- Sharpe ratio &gt; 1.0 on out-of-sample windows
- Profit factor &gt; 1.5
- Max drawdown &lt; 15% at strategy level
- Win rate &gt; 40% (or compensating R:R)
- At least 100 trades in test period
- Performance consistent across regimes (not single-regime overfit)

Strategies that fail: revise playbook entry or retire the rule.

### 2.4 — signal-postmortem configuration (Week 5)

- Stocks: track which `/deep-research` verdicts were correct over 6-month windows
- Options: track which `options-strategy-advisor` recommendations were profitable

### 2.5 — Streamlit dashboard (Week 6)

Run at `scripts/dashboard.py` (or `tools/thesis-manager/` for research UI):

- Today's market posture (exposure-coach output)
- Open positions across Robinhood accounts
- Stock watchlist with research report status
- Recent trade reviews (last 5 closed)
- Behavioral pattern alerts
- Today's calendar (economic events + earnings)
- Weekly P&L by account and instrument type

### 2.6 — Research quality tracking (Week 7)

Track every `/deep-research` report:

- Verdict, confidence score
- Price performance at 1/3/6 months
- Thesis invalidation triggers — did they fire? Did you act?
- Bull/bear probability calibration

Store in: `reports/logs/research_outcomes.md` (or repo-relative equivalent).

### 2.7 — Skill auto-improvement loop (Weeks 7–8)

Enable with branch protection:

1. Branch protection on main: require PR review, require tests
2. Enable skill-improvement loop (daily)
3. Leave skill-generation pipeline disabled until Phase 3

Review every PR. Cost: ~$10/mo.

### 2.8 — Skylit decision (end of Week 8)

Subscribe only if YES to ALL:

- Specific strategy needs GEX/dark pool data
- Free data alternatives exhausted
- Can afford 3 months ($297)
- Strategy could pay for subscription within 2 months at account size

Document YES/NO in [decisions.md](../decisions.md).

---

## Exit criteria

- [ ] `behavioral-pattern-detector` built for stock/options patterns
- [ ] Personal playbook has 3+ stock/options setups
- [ ] At least 2 playbook setups passed equity backtest quality gates
- [ ] 30+ total trades logged
- [ ] At least 1 playbook rule approved from edge-pipeline-orchestrator output
- [ ] Research quality tracking active with 10+ reports tracked
- [ ] Streamlit dashboard operational and used daily
- [ ] Skill-improvement loop running with branch protection
- [ ] Explicit YES/NO on Skylit in decisions.md
- [ ] Monthly Anthropic spend &lt; $30

---

## Common pitfalls

1. Skipping research quality tracking — this measures whether `/deep-research` actually helps returns
2. Cherry-picking backtest parameters — walk-forward prevents this
3. Auto-merging skill-improvement PRs — always read the diff
4. Buying Skylit "just to see" — $99/mo is the entire project budget

---

## What's NOT in Phase 2

Autonomous MCP execution (Phase 3). New upstream skill creation beyond wrappers and project-specific tools.

---

## When ready to advance

Update `PROJECT.md` Active Phase to Phase 3. Read [phase-3-agentic-execution.md](phase-3-agentic-execution.md).
