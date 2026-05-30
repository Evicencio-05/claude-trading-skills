# Phase 3 — Learning Loop & Co-Pilot

**Duration:** 8 weeks (weeks 11–18)
**Goal:** Personalize the existing learning infrastructure for both workflows. Detect behavioral patterns across stocks, options, and futures. Receive useful proactive alerts. Make a deliberate decision on Skylit.

---

## Prerequisites

Phase 2 exit criteria met. You should have:

- All 6 futures skills built and tested
- /futures-setup used pre-market for 10+ days
- 5+ futures trades logged to trader-memory-core
- 30+ total trades logged (stocks + options + futures combined)

The existing learning loop infrastructure is in place. Phase 3 personalizes it.

---

## What You're Building

### 3.1 — behavioral-pattern-detector (Weeks 11–12)

Reads your trader-memory-core history and flags patterns across ALL trade types — not just futures. The patterns that cost you money are often the same regardless of instrument.

**Patterns to detect:**

For all trade types:

- Overtrading days: >5 trades in a single session
- Revenge trades: new entry within 30 min of a stopped-out loss
- Moved stops: stop moved away from entry after trade was open
- FOMO entries: chasing a move already extended beyond your original plan
- Ignored research: trade taken without a completed research report when one was warranted
- Skipped stop: position closed manually at a larger loss than the stop defined
- Confidence mismatch: took a large position on a 2/5 confidence trade

Futures-specific additions:

- Ignored kill rules: trade taken when lucid-rules-engine returned a warning
- Friday flatten failures: position held within 15 min of auto-flatten
- Cycle-end pressure: overtrading in last 2 days of payout cycle when qualifying days not met

Stock/options-specific additions:

- Earnings gamble: entered a position within 48 hrs of earnings without an explicit earnings thesis
- IV ignorance: bought options when IV rank was above 70 (paying rich premium)
- Thesis drift: held a position past the original thesis invalidation trigger

**Output:**

- Daily report of patterns triggered yesterday
- Pre-trade hook: /futures-setup AND /deep-research both query this skill and surface relevant warnings
- Weekly summary in Streamlit dashboard

**Architecture:**

- Reads from trader-memory-core SQLite
- No external APIs
- Thresholds in config.yaml (tune without code changes)
- Separate pattern configs for futures vs stocks/options

### 3.2 — Personal playbook (Weeks 12–14)

Build playbook/playbook.md covering BOTH workflows from the start.

**Structure:**

```markdown
# Personal Trading Playbook

## Stock & Options Setups

### Setup: [Name]
- What it looks like
- Conditions required
- Entry trigger
- Stop placement
- Target methodology
- Historical performance (updated by edge-pipeline-orchestrator)
- When NOT to take it

## Futures Setups (ES/NQ)

### Setup: [Name]
- Session context (open drive, trend day, range day)
- Key level interaction required
- Entry trigger
- Stop placement (in points, not just dollars)
- Target methodology
- Lucid rule constraints that apply
- When NOT to take it

## Risk Rules

### Per-trade (stocks/options)
- Max risk per trade: 1% of account
- Max concurrent positions: [your number]

### Per-trade (futures)
- Max risk per trade: 0.5% of account
- Max concurrent positions: 1 (Phase 5 starting point)

### Per-day (all instruments)
- Max trades per day: 5 (warning at 3)
- Stop trading after 2 consecutive losses

### Lucid-specific
- Cycle qualifying day strategy
- Behavior near drawdown limits

## Lessons (most recent first)
```

**Process:**

- Week 12: Write your current setups in both categories (even if just 2-3 each)
- Week 13: Run edge-pipeline-orchestrator on your full trade history
- Week 14: Review proposed rules. Approve/reject/modify. Every rule must be YOUR decision.

### 3.3 — signal-postmortem configuration (Week 15)

Configure for both workflows:

- Stocks: track which /deep-research verdicts were correct over 6-month windows
- Options: track which options-strategy-advisor recommendations were profitable
- Futures: track which /futures-setup setups played out as expected

This is where your research quality gets measured over time. Don't skip it.

### 3.4 — Streamlit dashboard (Week 16)

One dashboard for both workflows. Run at `scripts/dashboard.py`.

**Sections:**

- Today's market posture (exposure-coach output)
- Open positions across all accounts (Robinhood manual entry + Lucid via Tradovate)
- Lucid account status: drawdown buffer, qualifying days per cycle
- Stock watchlist: tickers with open research reports and their current status
- Recent trade reviews (last 5 closed, any type)
- Behavioral pattern alerts (from 3.1)
- Today's calendar (economic events + earnings)
- Weekly P&L by account and instrument type

**Run:** `streamlit run scripts/dashboard.py`. Bookmark localhost:8501.

### 3.5 — Research quality tracking (Week 17)

This is missing from the original plan and important for the stock/options workflow.

Track every /deep-research report:

- Verdict at time of report (Strong Buy/Buy/Watch/Avoid/Short)
- Confidence score
- Actual price performance over 1 month, 3 months, 6 months
- Did the thesis invalidation triggers fire? Did you act on them?
- Were the bull/bear case probabilities well-calibrated?

After 20+ reports you'll know whether your research process has edge or just produces plausible-sounding analysis. This is how you improve the prompt and the workflow.

Store in: `~/trading-research/logs/research_outcomes.md`

### 3.6 — Skill auto-improvement loop (Week 17–18)

Enable carefully with branch protection:

1. Branch protection on main: require PR review, require tests
2. Enable skill-improvement loop (daily 5 AM)
3. Leave skill-generation pipeline disabled until Phase 4

Review every PR. Cost: ~$10/mo.

### 3.7 — Skylit decision (end of Week 18)

By now you have 3+ months of real trading data. Decide on Skylit.

Subscribe only if YES to ALL:

- You've identified a specific strategy needing GEX/dark pool data (not curiosity)
- You've extracted all edge possible from free data
- You can afford 3 months ($297)
- The strategy could realistically pay for the subscription within 2 months at your account size

Note: GEX data is most useful for options strategies on individual stocks, not for futures. If your main use case is futures, Skylit's value proposition weakens further.

---

## Exit Criteria

- [ ] behavioral-pattern-detector built for both stock/options and futures patterns
- [ ] Personal playbook has 3+ setups in each category (stocks AND futures)
- [ ] 30+ total trades logged (all instrument types)
- [ ] At least 1 playbook rule from each category approved from edge-pipeline-orchestrator output
- [ ] Research quality tracking active with 10+ reports tracked
- [ ] Streamlit dashboard operational and used daily
- [ ] Skill-improvement loop running with branch protection
- [ ] Explicit YES/NO decision on Skylit documented in decisions.md
- [ ] At least one Lucid evaluation completed (pass or fail — lessons documented)
- [ ] Monthly Anthropic spend < $30

---

## Common Pitfalls

1. Building the behavioral detector only for futures patterns — stocks and options have their own behavioral traps
2. Separate playbooks for stocks vs futures — one unified document with clearly labeled sections
3. Skipping research quality tracking — this is how you find out if /deep-research actually helps your returns
4. Auto-merging skill-improvement PRs — always read the diff
5. Buying Skylit "just to see" — $99/mo is the entire monthly project budget

---

## What's NOT in Phase 3

Backtesting, autonomous execution, new skill creation (mostly).

## When Ready to Advance

Update PROJECT.md Active Phase to Phase 4. Read project-docs/phase-4-backtesting.md.
