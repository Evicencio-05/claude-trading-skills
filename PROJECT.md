# AI Trading Agent — Project Charter

> **Read this file at the start of every Claude Code session.**
> This is the lightweight router. Detailed guidance lives in `project-docs/` and is loaded only when working on that phase.

---

## What This Project Is

A private fork of `claude-trading-skills` extended into a personalized, continuously learning AI trading agent with two concurrent goals:

**Goal A — Individual Stock & Options Research**
Deep research, screening, and trade planning on individual US equities and options using the existing 40+ skills. This is active from Day 1 and covers swing trades, earnings plays, options strategies, and long-term positions on the Robinhood account and beyond.

**Goal B — Futures Trading via Prop Firm**
CME futures execution (ES, NQ, MES, MNQ) targeting Lucid Trading prop firm accounts via Tradovate. This builds in parallel, with new futures-specific skills added in Phase 2. The two goals inform each other — macro context from futures work sharpens stock research; fundamentals from stock research informs index bias.

**Long-term vision:** An autonomous AI trading partner that learns from the user's trades, behavioral patterns, and outcomes across both workflows — compounding edge over time.

**Project posture:** Extend what exists. The stock research infrastructure is largely built. The futures infrastructure is the gap.

---

## Operating Constraints

- **Budget:** $30–50/mo target, $100/mo ceiling
- **Time:** Limited weekly hours (college student)
- **Stock/options capital:** ~$500 Robinhood account (grows over time)
- **Futures execution:** Lucid Trading (LucidFlex initially) via Tradovate
- **Hardware:** Local laptop/desktop only
- **Repo:** Private fork; no upstream contributions yet

---

## Non-Negotiables (read every session)

1. **Audit before building.** Use existing skills before extending them.
2. **Both goals matter equally.** Do not optimize purely for futures and neglect the stock/options research workflow, or vice versa.
3. **Lucid rules are sacred.** Hard-coded constraints. Never overridable by the agent.
4. **No HFT, no latency arbitrage.** Lucid prohibits these.
5. **4:45 PM ET hard cutoff.** Lucid auto-flattens. Agent closes earlier on its own.
6. **No autonomous execution before Phase 5.** Co-pilot mode only.
7. **Risk controls are immutable from the agent.**
8. **Every trade is logged** to `trader-memory-core` — stocks, options, and futures.
9. **Cost discipline.** Default to free/local. Justify every paid subscription.
10. **Human-in-the-loop for skill changes.** Auto-generated PRs require review.

---

## Out of Scope

- Skylit ($99/mo) until Phase 3+ with hard ROI criteria
- Multi-day futures holds (Lucid auto-flattens daily)
- Crypto, forex, mobile apps
- HFT, latency arbitrage
- Upstream contributions for now

---

## Current Status

**Current status:** See `project-docs/STATUS.md`

---

## How to Use This Project

### Starting a Claude Code session

1. Read this file (you're doing it now).
2. Check the **Active Phase** above.
3. Read the corresponding phase doc. **Only read the active phase doc.**
4. If working on a specific skill, read that skill's `SKILL.md` after the phase doc.

### Phase docs

| Phase | Doc | Status |
|---|---|---|
| Phase 1 | `project-docs/phase-1-audit.md` | Active |
| Phase 2 | `project-docs/phase-2-futures-skills.md` | Locked (week 5) |
| Phase 3 | `project-docs/phase-3-learning-loop.md` | Locked (week 11) |
| Phase 4 | `project-docs/phase-4-backtesting.md` | Locked (week 19) |
| Phase 5 | `project-docs/phase-5-live-execution.md` | Locked (week 27) |

### Reference docs (load only when topic comes up)

| Topic | Doc |
|---|---|
| Lucid Trading rules | `project-docs/reference/lucid-rules.md` |
| Cost discipline & model routing | `project-docs/reference/cost-discipline.md` |
| Tech stack decisions | `project-docs/reference/tech-stack.md` |
| Risk register | `project-docs/reference/risk-register.md` |
| Existing skills inventory + gaps | `project-docs/reference/existing-skills-map.md` |

---

## Phase Progression Rule

You cannot start Phase N until Phase N-1 exit criteria are met. When advancing:

1. Verify all exit criteria of current phase (checkbox audit)
2. Update **Active Phase** in this file
3. Update **This week's focus**
4. Read the new phase doc

---

## Working with Claude Code

- Reference both goals when relevant: *"We're in Phase 1 auditing stock research skills AND setting up the futures foundation."*
- Don't let sessions drift to purely futures or purely stocks — both get attention.
- Cost-check before any new API integration.
- Commit format: `[Phase X] component: what changed`

### Session hygiene

- `/clear` between unrelated tasks
- `/compact` when context exceeds ~60%
- Plan mode for any task touching code
- `/context` if responses feel unfocused
- Ultrathink for high-stakes decisions (rules engine, post-trade reviews on losses)
- Edit permissions: rules engine and risk control files are read-only after Phase 2

---

## Glossary

- **Playbook:** The agent's evolving rulebook — covers both stock setups and futures setups
- **Co-pilot mode:** Agent surfaces alerts and recommendations; user executes
- **Autonomous mode:** Agent executes within risk limits (Phase 5+, futures only initially)
- **Kill switch:** User-triggered halt of all autonomous activity
- **Lucid rules engine:** Hard-coded constraints module
- **Qualifying day:** Lucid's per-account minimum profit day
- **EOD trailing drawdown:** Lucid's max loss limit, calculated at session close

---

*Last updated: [date] | Owner: [user]*
