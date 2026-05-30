# Phase 3 — Agentic Execution

**Duration:** Ongoing
**Goal:** Execute real trades on Robinhood Agentic via MCP, starting in co-pilot mode, scaling to autonomous only after proven performance.

---

## Prerequisites

Phase 2 exit criteria met. Specifically:

- 2+ playbook strategies passed equity backtest quality gates
- Behavioral pattern detector operational
- 30+ trades logged with full thesis discipline
- Skill-improvement loop enabled with branch protection

If any of these are not true, **do not start Phase 3.** Go back and finish Phase 2.

---

## Sync infrastructure

Auto-execution builds on sync established in Phase 1:

- `robinhood_sync.py` → `state/pending_ingest.json` → `/log-positions` (Portfolio A)
- Robinhood Agentic MCP → read + trade Portfolio C
- `state/synced_positions.json` becomes source of truth for what the agent owns

The executor in Phase 3B reads this file before placing any order to verify position state matches expectations.

---

## Core discipline

Progress through three sub-phases. **You cannot skip a sub-phase.** Each runs for a defined minimum period. The goal is evidence the system is reliable — not maximum returns.

---

## Sub-Phase 3A — Co-Pilot Live (minimum 8 weeks)

Agent surfaces alerts and recommendations. **You confirm every MCP order.** Live capital on Agentic account.

### Setup

- [ ] Robinhood Agentic MCP configured in Cursor (`.cursor/mcp.json`)
- [ ] Production logging — every recommendation and execution logged with full context
- [ ] Risk limits documented in `config/agentic_risk.yaml` (user-editable only)

### Operating mode

- Run `pre_market.py` + exposure-coach pre-market every trading day
- Take trades aligned with playbook setups and research
- Present plan → wait for user **confirm** → MCP order on Agentic only
- Log every trade to `trader-memory-core` immediately on close
- Daily review: did the agent's reasoning hold up?

### What to track

- Recommendation acceptance rate
- Override outcomes (trades skipped vs would-have-been)
- Reverse override outcomes (trades taken against recommendation)
- Slippage vs recommended entry/stop levels

### Exit criteria for 3A

- 8+ weeks completed
- Net profitable after commissions (or documented learning if not)
- Zero unintended MCP orders
- At least 80% of agent recommendations taken (if overriding most, agent isn't ready)
- Documented decision: continue co-pilot indefinitely OR proceed to 3B

**Default: continue in co-pilot.** Autonomous execution is only worth the risk if the agent will outperform your manual execution.

---

## Sub-Phase 3B — Autonomous Test (weeks after 3A exit)

If and only if you proceed: run autonomous on a **small, capped Agentic allocation** while you continue manual co-pilot on the remainder.

### Setup

- [ ] Build executor module (project scripts or skill wrapper) with `place_order()`, `cancel_order()`
- [ ] Hard limits in `config/agentic_risk.yaml` (agent reads, never writes):
  - Max position size (% of Agentic equity)
  - Max concurrent positions
  - Daily loss circuit breaker
  - Mandatory cooldown after 2 consecutive losses
  - News blackout windows (FOMC, NFP, CPI ±5 min)
- [ ] Pre-flight checklist before every autonomous order:
  - Risk config check returns PASS
  - Position size matches recommendation
  - Account state matches `synced_positions.json`
  - Playbook setup criteria met

### Operating mode

- Agent executes autonomously within limits on test allocation
- You execute manually on remaining Agentic capital (or full account if test allocation is separate tracking only)
- Compare daily: autonomous vs manual outcomes
- Kill switch tested weekly

### Exit criteria for 3B

- 12+ weeks parallel operation
- Autonomous allocation net profitable
- Zero unintended order placements
- Autonomous performance within 20% of manual co-pilot (no surprise drift)
- No risk limit violations

If autonomous underperforms manual: **manual is your edge.** Stay in co-pilot.

---

## Sub-Phase 3C — Scaled Autonomous (only if 3B succeeds)

Gradual expansion after 3B evidence:

- Increase max concurrent positions (your decision, quarterly review)
- Add second playbook strategy to autonomous executor
- Quarterly review: is system still in expected behavior?

**Never let the agent modify its own constraints.** Every capability increase is your manual decision after evidence.

---

## Risk controls (always-on, all sub-phases)

Encoded in `config/agentic_risk.yaml` — user-editable only, agent read-only:

- Hard daily loss limit
- Hard position size limit
- News blackout windows
- Mandatory cooldowns after losses
- Kill switch (tested weekly)
- Daily reconciliation (agent logs vs MCP vs sync)
- Weekly review of all autonomous decisions

Test each control by intentionally triggering it before relying on it.

---

## Common pitfalls

1. **Skipping co-pilot, going straight to autonomous** — cost of a bug is real capital
2. **Increasing size after a winning week** — sizing changes are quarterly, not weekly
3. **Letting the agent modify constraints** — constraints are immutable from the agent
4. **Stopping journaling** — data flywheel must continue

---

## When to pause Phase 3

- Three consecutive losing weeks: pause autonomous, review
- Any unintended order: pause immediately, root-cause before resuming
- Major life change reducing review time: pause until daily review possible
- Major regime change: pause and re-evaluate strategies

---

## What's NOT in Phase 3

- New strategy invention without Phase 2 backtest gates
- MCP trades on IRA or taxable accounts
- Agent operating without daily human review (even in 3B/3C)

---

## Phase 3 has no exit

Steady-state: operate, monitor, refine. Learning loop continues. Playbook evolves. Skill auto-improvement maintains quality.

The goal was never autonomous trading for its own sake — it was a personalized, continuously learning system that augments your edge.
