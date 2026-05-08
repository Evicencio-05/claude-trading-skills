# AI Trading Agent — Project Charter

> **Read this file at the start of every Claude Code session.**
> This is the lightweight router. Detailed guidance lives in `project-docs/` and is loaded only when working on that phase.

---

## What This Project Is

A private fork of `claude-trading-skills` extended into a personalized, continuously learning AI trading agent. Begins as a research co-pilot using the existing 40+ skills. Evolves into a futures execution system targeting **Lucid Trading** prop firm via **Tradovate**.

**Long-term goal:** Autonomous AI trading partner that learns from the user's trades, behavioral patterns, and outcomes — operating within strict risk controls and Lucid's rules.

**Project posture:** Extend what exists. Do not rebuild what already works.

---

## Operating Constraints

- **Budget:** $30–50/mo target, $100/mo ceiling
- **Time:** Limited weekly hours (college student)
- **Personal capital:** ~$500 Robinhood (kept small; growth via prop firm)
- **Live execution target:** Lucid Trading (LucidFlex initially) via Tradovate
- **Hardware:** Local laptop/desktop only
- **Repo:** Private fork; no upstream contributions yet

---

## Non-Negotiables (read every session)

1. **Audit before building.** Use existing skills before extending them. Most of what's needed is already in the repo.
2. **Lucid rules are sacred.** Hard-coded constraints. Never overridable by the agent.
3. **No HFT, no latency arbitrage.** Lucid prohibits these explicitly.
4. **4:45 PM ET hard cutoff.** Lucid auto-flattens. Agent closes earlier on its own.
5. **No autonomous execution before Phase 5.** Co-pilot mode only.
6. **Risk controls are immutable from the agent.** Position limits, kill switch, rules engine — user-only.
7. **Every trade is logged** to `trader-memory-core`. The learning loop depends on this data.
8. **Cost discipline.** Default to free/local. Justify every paid subscription.
9. **Human-in-the-loop for skill changes.** Auto-generated PRs require user review. Branch protection enforced.

---

## Out of Scope

- Skylit ($99/mo) until Phase 3+ with hard ROI criteria
- Multi-day futures holds (Lucid auto-flattens daily)
- Crypto, forex, mobile apps
- HFT, latency arbitrage
- Upstream contributions

---

## Current Status

**Active Phase:** Phase 1 — Audit & Activate
**Phase started:** [May 7 2026]
**Target phase exit:** [5/7/26 + 4 weeks]
**Current monthly spend:** $0
**Spend cap:** $30/mo

**This week's focus:**

- [ ] [Audit repo]

**Blockers:** [none / describe]

---

## How to Use This Project

### Starting a Claude Code session

1. Read this file (you're doing it now).
2. Check the **Active Phase** above.
3. Read the corresponding phase doc from `project-docs/`. **Only read the active phase doc** — don't load the others. They're long and not relevant to what you're doing today.
4. If working on a specific skill, read that skill's `SKILL.md` after the phase doc.

### Phase docs

| Phase | Doc | Status |
|---|---|---|
| Phase 1 | `project-docs/phase-1-audit.md` | Active |
| Phase 2 | `project-docs/phase-2-futures-skills.md` | Locked (read in week 5) |
| Phase 3 | `project-docs/phase-3-learning-loop.md` | Locked (read in week 11) |
| Phase 4 | `project-docs/phase-4-backtesting.md` | Locked (read in week 19) |
| Phase 5 | `project-docs/phase-5-live-execution.md` | Locked (read in week 27) |

### Always-relevant docs (read when topic comes up, not every session)

| Topic | Doc |
|---|---|
| Lucid Trading rules (LucidFlex/Pro/Direct) | `project-docs/reference/lucid-rules.md` |
| Cost discipline & model routing | `project-docs/reference/cost-discipline.md` |
| Tech stack decisions | `project-docs/reference/tech-stack.md` |
| Risk register | `project-docs/reference/risk-register.md` |
| Existing skills inventory + gaps | `project-docs/reference/existing-skills-map.md` |

---

## Phase Progression Rule

You cannot start Phase N until Phase N-1 exit criteria are met. The phase docs define exit criteria explicitly. If Claude Code suggests skipping ahead, push back.

When advancing phases:

1. Verify all exit criteria of current phase are met (checkbox audit)
2. Update the **Active Phase** in this file
3. Update the **This week's focus** section
4. Read the new phase doc to set context

---

## Working with Claude Code

- Reference the current phase explicitly in prompts: *"We're in Phase 1, week 3, auditing the screening skills."*
- Never ask Claude Code to build something a phase doc says is out of scope for the current phase.
- Cost-check before any new API integration: *"How much will this cost per month at expected usage?"*
- Commit format: `[Phase X] component: what changed`

### Session hygiene (cost & quality)

- Use `/clear` between unrelated tasks within a session
- Use `/compact` when context exceeds ~60%
- Always start with plan mode for any task touching code
- Run `/context` if responses feel unfocused — usually means context bloat
- For high-stakes work (rules engine, risk controls, post-trade reviews on losses): use ultrathink mode
- Edit permissions in Claude Code settings: rules engine and risk control files are read-only after Phase 2 build

---

## Glossary (quick reference)

- **Playbook**: The agent's evolving rulebook (`playbook/playbook.md`)
- **Co-pilot mode**: Agent surfaces alerts and recommendations; user executes
- **Autonomous mode**: Agent executes within risk limits (Phase 5+)
- **Kill switch**: User-triggered immediate halt of all autonomous activity
- **Lucid rules engine**: Hard-coded constraints module (see `reference/lucid-rules.md`)
- **Qualifying day**: Lucid's per-account minimum profit day (counts toward payout cycle eligibility)
- **EOD trailing drawdown**: Lucid's max loss limit, calculated at session close only

---

*Last updated: [date] | Owner: [user]*
