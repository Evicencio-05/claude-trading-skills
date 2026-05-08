# Phase 4 — Backtesting & Lucid Sim Validation

**Duration:** 8 weeks (weeks 19–26)
**Goal:** Validate playbook strategies against historical futures data and Lucid sim accounts. Catch overfitting before it costs real money.

---

## Prerequisites

Phase 3 exit criteria met. Specifically:
- Personal playbook has 3+ setups with documented conditions
- 30+ trades logged in `trader-memory-core`
- Behavioral pattern detector is operational
- At least one Lucid evaluation completed (passed or failed, both useful)

---

## Why This Phase Matters

Until now, every strategy decision has been validated against your live trade history (small sample, recent regime only). Phase 4 stress-tests your playbook against years of historical data across multiple market regimes. **This is the phase where overfitted strategies die.** Better to die in a backtest than in a Lucid evaluation.

---

## What You're Building

### 4.1 — Historical futures data acquisition (Week 19)

- [ ] Buy historical 1-minute data for ES and NQ from Firstrate Data
  - Cost: ~$25/symbol one-time
  - Coverage: minimum 5 years (covers 2020 vol, 2022 bear, 2023-2024 grind, 2025 conditions)
- [ ] Optional: MES and MNQ historical for micro contract backtests (often cheaper or included)
- [ ] Store in `data/raw/futures/` as Parquet
- [ ] Build a data validation script that catches gaps, holiday-adjusted sessions, and contract roll discontinuities

### 4.2 — Futures backtesting harness (Weeks 20–22)

Use the existing `backtest-expert` skill as the methodology framework. Build the futures-specific harness using `vectorbt` or `backtrader`.

**Critical realism requirements (the existing `backtest-expert` documents these — follow them):**
- Slippage modeling: 1 tick on entry, 1 tick on exit minimum
- Commission modeling: ~$2.50 round-turn for ES through prop firm
- Realistic fills: assume mid-price + slippage, not best-case
- Survivorship bias: not applicable for futures (single contract per period), but honor contract rolls correctly
- No look-ahead: stops and targets must be evaluated against bar-by-bar action, not bar high/low simultaneously

**Per playbook rule:**
- Define entry condition as code
- Define stop and target methodology
- Run backtest across full historical window
- Run walk-forward analysis (rolling 6-month train, 3-month test)
- Run regime-segmented analysis (high VIX vs. low VIX, trending vs. ranging)

### 4.3 — Strategy quality gates (Week 23)

Before a strategy graduates from backtest to Lucid sim, it must pass:

- **Sharpe ratio > 1.0** on out-of-sample windows
- **Profit factor > 1.5** (gross profit / gross loss)
- **Max drawdown < 15%** at the strategy level (lower for Lucid since drawdown rules are tighter)
- **Win rate > 40%** (lower is acceptable if R:R compensates; flag for review if <40%)
- **At least 100 trades** in the test period (statistical relevance)
- **Performance consistency across regimes** (not solely a 2022 bear strategy or solely a 2024 grind strategy)
- **Lucid rule compliance** when run through `lucid-rules-engine` against simulated account state — does the strategy ever trigger a daily loss breach, EOD drawdown breach, or auto-flatten violation?

Strategies that fail gates: revise the playbook entry or retire the rule.

### 4.4 — Lucid sim account integration (Weeks 24–25)

- [ ] Run paper trades through Tradovate sim against an active Lucid evaluation account
- [ ] Use `tradovate-integration` to fetch fills, calculate true P&L including commissions
- [ ] Daily reconciliation script: compare what `/futures-setup` recommended vs. what got executed (manual or sim) vs. what the backtest would have done
- [ ] Track drift: is live sim performance matching backtest expectations? If not, why? (Slippage worse than modeled? Setups firing differently in real-time?)

### 4.5 — Pre-execution risk infrastructure (Week 26)

Before Phase 5 ever executes a real trade, the following must exist and be tested:

- [ ] **Kill switch:** Web-accessible (or mobile shortcut) endpoint that halts all autonomous activity. Test it three different ways: from your phone, from another machine, from the dashboard.
- [ ] **Hard position limits:** Encoded in `lucid-rules-engine`, not in the executor. Even if the executor is asked to place a 10-contract trade, the rules engine refuses if your max is 3.
- [ ] **News blackout windows:** No new positions in the 5 minutes before/after FOMC, NFP, CPI releases. Hard-coded.
- [ ] **Mandatory cooldown:** After 2 consecutive losses, no new positions for 30 minutes (configurable; this matches Lucid's psychology of grinding).
- [ ] **Max concurrent positions:** Default 1 for futures (you're starting small).
- [ ] **Daily auto-flatten check:** If any position is open after 4:35 PM ET, force-close. Don't wait for Lucid's 4:45 PM auto-flatten.
- [ ] **Daily loss circuit breaker:** If daily loss reaches 80% of Lucid's daily loss limit, no new positions for the rest of the session.

Test each by intentionally triggering it. A risk control you haven't tested doesn't exist.

---

## Exit Criteria (all must be met to advance to Phase 5)

- [ ] At least 5 years of ES/NQ historical 1-min data validated and stored
- [ ] Backtesting harness runs new strategy in <10 minutes
- [ ] Walk-forward and regime-segmented analysis implemented
- [ ] At least 2 playbook strategies have passed all quality gates
- [ ] 8+ weeks of Lucid sim trading with positive risk-adjusted returns
- [ ] Sim trading performance matches backtest expectations within 30% (worse is suspicious — investigate)
- [ ] All 7 risk controls in 4.5 implemented and intentionally tested
- [ ] Kill switch verified accessible from phone
- [ ] Total monthly Anthropic spend < $40

---

## Common Phase 4 Pitfalls

**Pitfall 1: Strategy that backtests beautifully but only on the last 2 years.**
This is overfitting. Force test on multiple regimes. If a strategy only works in low-vol grind markets, it's a regime bet, not an edge.

**Pitfall 2: Cherry-picking parameters until backtest looks good.**
Walk-forward analysis prevents this. Set parameters on training windows, test on out-of-sample only. Don't peek.

**Pitfall 3: Skipping the slippage and commission modeling because "it's only $2.50."**
Over hundreds of trades, $2.50 commissions and 1-tick slippage routinely turn a "profitable" strategy into a loser. Model them honestly.

**Pitfall 4: Assuming Lucid sim P&L matches what you'd get on a live account.**
Sim usually fills better than live (no real spread, no real liquidity constraints). Discount sim performance by 10-20% mentally.

**Pitfall 5: Building autonomous execution "in preparation" for Phase 5.**
Phase 5 starts the moment you have one strategy through quality gates AND 8 weeks of sim performance AND tested risk controls. Not before.

---

## What's NOT in Phase 4

- Live trading on real capital (Phase 5)
- New strategy invention beyond what's already in the playbook
- Anything outside Lucid's product set

---

## When You're Ready to Advance

Update the main `PROJECT.md`:
- Change "Active Phase" to Phase 5
- Reset "This week's focus"
- Read `project-docs/phase-5-live-execution.md`
