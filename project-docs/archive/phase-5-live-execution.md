# Phase 5 — Live Execution

**Duration:** Ongoing (starts week 27+)
**Goal:** Execute real trades on Lucid via Tradovate, starting in co-pilot mode, scaling to autonomous only after proven performance.

---

## Prerequisites

Phase 4 exit criteria met. Specifically:
- 8+ weeks of positive sim performance
- 2+ strategies through quality gates
- All 7 risk controls implemented and tested
- Kill switch verified

If any of these are not true, **do not start Phase 5.** The cost of skipping ahead is real money. Go back and finish Phase 4.

---

## Sync Infrastructure

Auto-execution in Phase 5 builds on the sync infrastructure established in earlier phases:
- Phase 1: `robinhood_sync.py` → `state/pending_ingest.json` → `/log-positions`
- Phase 2: `tradovate_sync.py` → same pipeline, futures account tags

`state/synced_positions.json` becomes the source of truth for what the agent owns.
The executor in Phase 5B reads this file before placing any order to verify
current position state matches expectations.

## The Core Discipline of Phase 5

You will progress through three sub-phases. **You cannot skip a sub-phase.** Each one runs for a defined minimum time period, regardless of how well it's going. The goal is not maximum returns — it's compounding evidence that the system is reliable enough to trust with more.

---

## Sub-Phase 5A — Co-Pilot Live (Weeks 27–34, minimum 8 weeks)

The agent surfaces alerts and recommendations. **You manually execute every trade.** Live capital, real Lucid account.

### Setup

- [ ] Pass a Lucid evaluation (paid for from project budget if needed)
- [ ] Get to LucidLive (real funded account)
- [ ] Configure `tradovate-integration` in production mode (LIVE env var explicitly set, with a startup banner that confirms which mode is active)
- [ ] Enable production logging — every quote, every recommendation, every execution gets logged with full context

### Operating mode

- Run `/futures-setup` pre-market every day
- Take only the trades the agent recommends
- Manually execute via Tradovate
- Log every trade to `trader-memory-core` immediately on close
- Daily review at end of session: did the agent's reasoning hold up?

### What to track

- Agent recommendation acceptance rate (did you take the trade or override?)
- Override outcomes (when you didn't take the trade, what would have happened?)
- Reverse override outcomes (when you took a trade the agent didn't recommend, how did it go?)
- Slippage vs. recommended entry/stop levels
- Lucid rule compliance (any close calls on buffers?)

### Exit criteria for 5A

- 8+ weeks completed
- Net profitable after commissions
- Drawdown stayed within 50% of Lucid's max
- Zero rule violations
- At least 80% of agent recommendations taken (if you're overriding most, the agent isn't ready)
- Documented decision: continue in co-pilot indefinitely OR proceed to 5B

**The default is "continue in co-pilot."** Autonomous execution is only worth the operational risk if you're confident the agent will outperform your manual execution. Many experienced traders never leave co-pilot, and that's fine.

---

## Sub-Phase 5B — Autonomous Test (parallel account, weeks 35+)

If and only if you choose to proceed to autonomous: run it on a **second account in parallel** to your manual co-pilot account. This lets you compare directly.

### Setup

- [ ] Take a SECOND Lucid evaluation account (not your funded primary)
- [ ] Build the executor module: `skills/futures-executor/` with `place_order()`, `modify_order()`, `cancel_order()`
- [ ] Hard-coded constraints in the executor:
  - Max 1 concurrent position
  - Max 1 contract per trade (start absurdly small)
  - Hard daily loss circuit breaker at 50% of Lucid daily limit
  - Mandatory 30-min cooldown after 2 consecutive losses
  - News blackout windows enforced
  - Force-close at 4:35 PM ET
- [ ] Pre-flight checklist that must pass before every order:
  - `lucid-rules-engine` returns PASS
  - Position size matches recommendation
  - Stop loss is set as a server-side bracket order (not a mental stop)
  - Account is in expected state

### Operating mode

- Agent executes autonomously on the test account
- You execute manually on the funded co-pilot account
- Compare daily: which had better outcomes? Why?
- Kill switch must be tested weekly (intentionally trigger it, verify it works)

### Exit criteria for 5B

- 12+ weeks of parallel operation
- Autonomous account net profitable
- No autonomous trade has violated any Lucid rule
- Zero unintended order placements (every order matches an explicit recommendation)
- Autonomous performance is within 20% of manual co-pilot performance (better or worse — what matters is no surprise drift)

If autonomous underperforms manual: **the manual one is your edge, not the agent.** Keep co-pilot mode.

---

## Sub-Phase 5C — Scaled Autonomous (only if 5B succeeds)

After 5B success, gradually expand:

- Increase max concurrent positions from 1 to 2
- Allow micro contracts → mini contracts (carefully)
- Add second strategy to the autonomous executor
- Review every quarter: is the system still in expected behavior?

**Never let the agent modify its own constraints.** Every increase in capability is your decision, made manually, after evidence.

---

## Risk Controls (always-on, all sub-phases)

- Hard daily loss limit (encoded, not configurable by agent)
- Hard position size limit (encoded, not configurable by agent)
- News blackout windows
- Mandatory cooldowns after losses
- Force-flatten before Lucid auto-flatten
- Kill switch (tested weekly)
- Daily reconciliation (agent logs vs. broker logs vs. account state)
- Weekly review of all autonomous decisions

---

## Common Phase 5 Pitfalls

**Pitfall 1: Skipping co-pilot, going straight to autonomous.**
The cost of an autonomous bug in a fresh deployment is your funded account. Co-pilot first.

**Pitfall 2: Letting the agent execute on your funded account in 5B.**
5B uses a SEPARATE evaluation account. The funded account stays in your manual hands until 5C.

**Pitfall 3: Increasing position size after a winning week.**
Position sizing changes are quarterly decisions, not weekly. A single winning week is statistical noise.

**Pitfall 4: Letting the agent "learn" to violate constraints.**
The constraints are immutable. The agent's job is to operate within them, not to test them.

**Pitfall 5: Stopping the journaling discipline.**
Every trade still gets logged with thesis and review. The data flywheel doesn't stop just because you have a profitable system — it's how the system stays profitable.

---

## When (Maybe) to Pause Phase 5

- Three consecutive losing weeks: pause autonomous, review
- Any rule violation: pause autonomous immediately, root-cause before resuming
- Major personal life change reducing review time: pause until you can review daily
- Major market regime change (vol expansion event): pause and re-evaluate strategies against the new regime

---

## What's NOT in Phase 5

- New strategy development (that goes through Phases 3-4 again before reaching live)
- Adding new asset classes
- Letting the agent operate without daily human review

---

## Phase 5 Has No Exit

This is the steady-state of the project. The work shifts from "build" to "operate, monitor, refine."

The learning loop continues feeding data. The playbook continues evolving. The skill auto-improvement loop keeps maintaining quality. You become the senior operator of a system you understand deeply.

The goal was never autonomous trading for its own sake. The goal was a personalized, continuously learning system that augments your edge. Mission accomplished if Phase 5C is stable for 6+ months.
