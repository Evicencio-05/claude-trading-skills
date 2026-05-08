# Phase 3 — Learning Loop & Co-Pilot

**Duration:** 8 weeks (weeks 11–18)
**Goal:** Personalize the existing learning infrastructure. Detect behavioral patterns. Receive useful proactive alerts. Make a deliberate decision on Skylit.

---

## Prerequisites

Phase 2 exit criteria met. Specifically:
- All 6 futures skills built and tested
- `/futures-setup` used pre-market for 10+ trading days
- 5+ futures trades logged to `trader-memory-core`

The existing learning loop infrastructure is in place (`trader-memory-core`, `signal-postmortem`, `edge-pipeline-orchestrator`, `dual-axis-skill-reviewer`). Phase 3 personalizes it for your patterns.

---

## What You're Building

This phase is more design-heavy than build-heavy. The infrastructure exists; you're configuring and extending it.

### 3.1 — `behavioral-pattern-detector` (Weeks 11–12)

A new skill that reads your `trader-memory-core` history and flags patterns the agent should warn you about pre-trade.

**Patterns to detect (start with these, expand as you discover your own):**

- **Overtrading days:** >5 trades in a single session
- **Revenge trades:** new entry within 30 minutes of a stopped-out loss
- **Moved stops:** stop moved further from entry after the trade was open (vs. trailing in profit)
- **FOMO entries:** entry within 15 min of a >1% intraday move that the trader was not previously watching
- **Ignored kill rules:** trade taken when `lucid-rules-engine` had returned a warning
- **Friday flatten failures:** position held into 4:30 PM ET (within 15 min of auto-flatten)
- **Cycle-end pressure:** unusually high trade count in the last 2 days of a payout cycle when qualifying days were not yet met

**Output:**
- Daily report of any patterns triggered yesterday
- Pre-trade hook: when `/futures-setup` runs, it queries this skill for "what behaviors have I been showing this week?" and surfaces relevant warnings in the output

**Architecture:**
- Reads from `trader-memory-core` SQLite store
- No external APIs needed
- Pure pattern matching + thresholds in `config.yaml` (so you can tune without code changes)

### 3.2 — Personal playbook (Weeks 12–14)

Build `playbook/playbook.md` from scratch, then evolve it from your trade data.

**Initial structure:**

```markdown
# Personal Trading Playbook

## Setups I Trade

### Setup 1: <Name>
- **What it looks like:** [chart description]
- **Conditions required:** [structured criteria]
- **Entry trigger:** [specific price action]
- **Stop placement:** [where and why]
- **Target methodology:** [1R/2R, key level, etc.]
- **Historical performance (from my trades):** [updated by edge-pipeline-orchestrator]
- **When NOT to take it:** [counter-conditions]

### Setup 2: ...

## Risk Rules

### Per-trade
- Max risk per trade: 0.5% of account
- ...

### Per-day
- Max trades per day: 5 (warning at 3, hard stop at 5)
- ...

### Per-cycle (Lucid-specific)
- Cycle reset behavior
- Qualifying day strategy
- ...

## Lessons (most recent first)

### YYYY-MM-DD: <Lesson>
- Trade context
- What I observed
- Rule change proposed
- User decision (approve/reject/modify)
```

**Process:**
1. Week 12: Write down the 3–5 setups you actually trade (or want to trade) on Lucid
2. Week 13: Run `edge-pipeline-orchestrator` against your trade history to extract candidate rules
3. Week 14: Review proposed rules. Approve/reject/modify each. The orchestrator's output is a proposal — you decide what becomes a rule.

**The playbook is a living document.** It grows as your trade history grows. Every 2 weeks, run the orchestrator again and review proposed updates.

### 3.3 — `signal-postmortem` configuration (Week 15)

The skill exists. Configure it for your futures workflow.

- Set up automatic post-trade review trigger when a trade is closed in `trader-memory-core`
- Define your specific outcome categories beyond the defaults (TRUE_POSITIVE, FALSE_POSITIVE, MISSED_OPPORTUNITY, REGIME_MISMATCH)
- Connect outputs to the playbook update process

### 3.4 — Streamlit dashboard (Week 16)

A local web UI you check first thing every morning. Lives at `scripts/dashboard.py`.

**Sections:**
- Today's market posture (calls `exposure-coach`)
- Open Lucid positions (calls `tradovate-integration`)
- Lucid account status: EOD drawdown buffer per account, qualifying days for current payout cycle
- Recent trade reviews (last 5 closed trades from `trader-memory-core`)
- Behavioral pattern alerts (from 3.1)
- Today's calendar (calls `economic-calendar-fetcher`)
- Weekly P&L by account

**Run:** `streamlit run scripts/dashboard.py`. Bookmark `localhost:8501` in your browser.

### 3.5 — Skill auto-improvement loop (Weeks 17–18)

In Phase 1 you disabled the auto-PR pipelines. Now you have enough context to enable them carefully.

**Setup:**
1. Configure GitHub branch protection on `main`: require PR review, require passing tests, no direct pushes
2. Enable `launchd/com.trade-analysis.skill-improvement.plist` (daily 5 AM)
3. Leave `skill-generation` (the new-skill-mining one) disabled until Phase 4 — you don't need new skills yet, you need refinement of existing ones
4. Review every PR the loop creates. Most will be improvements. Some won't. Reject the bad ones — your judgment is part of the system.

**Cost note:** The improvement loop uses Claude API. Budget ~$10/mo for it.

### 3.6 — Skylit decision (end of Week 18)

By now you've used the system for 3+ months and have real trade data. Decide on Skylit.

**Subscribe only if YES to all:**
- You've identified a specific strategy that needs GEX/dark pool data (not "I'm curious," but "this exact setup needs this data")
- You've extracted what edge you can from free data sources
- You can afford 3 months ($297) to evaluate
- The strategy could realistically pay for the subscription within 2 months at your account size

**If NO to any of these, defer to Phase 4 or skip entirely.** Skylit is not a prerequisite for any subsequent phase.

---

## Exit Criteria (all must be met to advance to Phase 4)

- [ ] `behavioral-pattern-detector` built, tested, and integrated into `/futures-setup` output
- [ ] Personal playbook has 3+ setups with conditions, stops, targets
- [ ] At least 30 trades logged in `trader-memory-core` since project start
- [ ] At least 1 playbook rule has been added based on `edge-pipeline-orchestrator` output and your approval
- [ ] Streamlit dashboard is operational and you check it daily
- [ ] Skill-improvement loop is running with branch protection enforced
- [ ] Explicit YES/NO decision on Skylit (documented in `decisions.md`)
- [ ] At least one Lucid evaluation passed OR explicit lessons-learned written for any failed evaluations
- [ ] Total monthly Anthropic spend < $30

---

## Common Phase 3 Pitfalls

**Pitfall 1: Writing a fancy playbook before having trade data.**
A playbook with rules that aren't backed by your trade history is fiction. Start small (3 setups), grow with data.

**Pitfall 2: Auto-merging skill-improvement PRs.**
The loop will propose changes that look reasonable but degrade subtle skill behavior. Always read the PR diff.

**Pitfall 3: Buying Skylit "just to see."**
$99/mo is your entire monthly project budget. "Just to see" is how budgets get destroyed. Decide based on a specific strategy need.

**Pitfall 4: Treating behavioral patterns as the agent nagging you.**
They're data about you, surfaced by the system. If "revenge trade" fires three weeks in a row, the answer isn't to silence the alert — it's to address the pattern.

---

## What's NOT in Phase 3

- Backtesting against historical futures data (Phase 4)
- Autonomous execution (Phase 5)
- New skill creation (mostly — the auto-generation pipeline stays disabled)

---

## When You're Ready to Advance

Update the main `PROJECT.md`:
- Change "Active Phase" to Phase 4
- Reset "This week's focus"
- Read `project-docs/phase-4-backtesting.md`
