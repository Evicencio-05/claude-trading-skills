# AI Trading Agent — Project Charter

> **Read this file at the start of every AI session** (Claude Code or Cursor).
> This is the lightweight router. Detailed guidance lives in `project-docs/` and is loaded only when working on that phase.

---

## What This Project Is

A private fork of `claude-trading-skills` extended into a personalized, continuously learning AI trading agent focused on:

**US equities & options — research, market analysis, portfolio management, and Robinhood Agentic execution**

Deep research, screening, and trade planning using the existing 40+ skills. Covers swing trades, earnings plays, options strategies, and long-term positions across Robinhood accounts (taxable, IRA, Agentic).

**Long-term vision:** An autonomous AI trading partner that learns from your trades, behavioral patterns, and outcomes — compounding edge over time.

**Project posture:** Extend what exists. The stock research infrastructure is largely built. The gap is production-ready pipeline → thesis → co-pilot → learning loop → Agentic execution.

---

## Operating Constraints

- **Budget:** $30–50/mo target, $100/mo ceiling
- **Time:** Limited weekly hours (college student)
- **Capital:** ~$500 Robinhood across accounts (grows over time)
- **Execution:** Robinhood Agentic MCP (Portfolio C); read all accounts, trade Agentic only
- **Hardware:** Local laptop/desktop only
- **Repo:** Private fork; no upstream contributions yet

---

## Non-Negotiables (read every session)

1. **Audit before building.** Use existing skills before extending them.
2. **Robinhood MCP gates.** Read all accounts; trade Agentic account only; flag IRA-ineligible options before actionable advice.
3. **No autonomous MCP execution before Phase 3B.** Co-pilot mode until Phase 3 sub-phase criteria met.
4. **Risk controls are immutable from the agent.** Limits live in user-editable config, not agent-writable files.
5. **Every trade is logged** to `trader-memory-core` — stocks and options.
6. **Cost discipline.** Default to free/local. Justify every paid subscription.
7. **Human-in-the-loop for skill changes.** Auto-generated PRs require review.

---

## Out of Scope

- CME futures / prop firm trading (Lucid, Tradovate) — archived 2026-05-29
- Skylit ($99/mo) until Phase 2 exit with hard ROI criteria
- Crypto, forex, mobile apps
- Upstream contributions for now

---

## Current Status

**Active phase:** Phase 1 — Research + Co-pilot. See `project-docs/STATUS.md` and `project-docs/phase-1-research-copilot.md`.

---

## How to Use This Project

### Starting a session (Claude Code or Cursor)

1. Read this file (you're doing it now).
2. Read [LOAD_GUIDE.md](LOAD_GUIDE.md) and [project-docs/STATUS.md](project-docs/STATUS.md).
3. Check the **Active Phase** below and read that phase doc only.
4. If working on a specific skill, read that skill's `SKILL.md` after the phase doc.

**Cursor:** Rules in `.cursor/rules/` apply automatically; see [AGENTS.md](AGENTS.md) for hybrid routing.

**Claude Code:** Use `commands/` slash workflows; symlink skills from `skills/` to `~/.claude/skills/`.

### Phase docs

| Phase | Doc | Focus |
|---|---|---|
| **Phase 1** | `project-docs/phase-1-research-copilot.md` | **Active** — Research pipeline + Robinhood co-pilot |
| Phase 2 | `project-docs/phase-2-learning-loop.md` | Behavioral patterns, playbook, skill improvement |
| Phase 3 | `project-docs/phase-3-agentic-execution.md` | Agentic MCP autonomous execution |

### Reference docs (load only when topic comes up)

| Topic | Doc |
|---|---|
| Cost discipline & model routing | `project-docs/reference/cost-discipline.md` |
| Tech stack decisions | `project-docs/reference/tech-stack.md` |
| Risk register | `project-docs/reference/risk-register.md` |
| Existing skills inventory + gaps | `project-docs/reference/existing-skills-map.md` |
| Robinhood MCP | `project-docs/reference/robinhood-mcp-integration.md` |

---

## Phase Progression Rule

You cannot start Phase N until Phase N-1 exit criteria are met. When advancing:

1. Verify all exit criteria of current phase (checkbox audit)
2. Update **Active Phase** in this file
3. Update **This week's focus** in STATUS.md
4. Read the new phase doc

---

## Working with Claude Code / Cursor

- Stay focused on the active phase doc — don't scope-creep into Phase 2/3 builds early.
- Cost-check before any new API integration.
- Commit format: `[Phase X] component: what changed`

### Session hygiene

- `/clear` between unrelated tasks
- `/compact` when context exceeds ~60%
- Plan mode for any task touching code
- `/context` if responses feel unfocused
- Ultrathink for high-stakes decisions (post-trade reviews on losses, risk config changes)
- Risk control config files are user-editable only — agent reads, never writes

---

## Glossary

- **Playbook:** The agent's evolving rulebook for stock/options setups
- **Co-pilot mode:** Agent surfaces alerts and recommendations; user confirms and executes
- **Autonomous mode:** Agent executes within hard limits (Phase 3B+, Agentic account only)
- **Kill switch:** User-triggered halt of all autonomous activity

---

*Last updated: 2026-05-29 | Owner: Ethan*
