# Phase 1 — Audit & Activate

**Duration:** 4 weeks
**Goal:** Understand what the existing fork already does, set up infrastructure, generate the data the system needs to learn from.

---

## Why This Phase Exists

The temptation is to start building futures skills immediately. **Don't.** This fork has 40+ skills with mature engineering. Until you've actually used them and understood them, you don't know what's missing vs. what just needs configuration. Audit first.

The other reason: the learning loop infrastructure (`trader-memory-core`, `signal-postmortem`, `dual-axis-skill-reviewer`) is data-hungry. It needs your actual trades, your actual research reports, and your actual market context history to produce useful patterns. Generating that data is the real Phase 1 deliverable.

---

## Week 1 — Setup

### Environment

- [ ] Verify `pre-commit install && pre-commit install --hook-type pre-push` runs clean
- [ ] Verify all hooks pass on a no-op commit (`ruff`, `mypy`, `codespell`, `detect-secrets`, `no-absolute-paths`, `skill-frontmatter`, `docs-completeness`)
- [ ] If any hook fails on existing files, fix before continuing — broken hooks invite skipping them later
- [ ] Run `python3 -m pytest scripts/tests/ -v` — confirm baseline tests pass

### Directories the existing commands expect

```bash
mkdir -p ~/trading-research/{reports,archives,intraday,options,logs}
mkdir -p state/theses          # for trader-memory-core
mkdir -p reports/skill-improvement-log reports/skill-generation-log
```

### API keys & budget alerts

- [ ] Sign up for FMP free tier (250 calls/day): https://financialmodelingprep.com/developer/docs
- [ ] `export FMP_API_KEY=...` in your shell profile
- [ ] Sign up for Anthropic API. Set hard $30/mo budget alert in console.
- [ ] Soft cap: $20/mo. If you hit it mid-month, stop and review usage.

### Lucid Trading account

- [ ] Open Lucid account. Start with **LucidFlex 50K evaluation** ($175 typical, often discounted to ~$100). Most forgiving rules, lowest cost to learn the platform.
- [ ] Verify Tradovate login works
- [ ] Log into the Lucid dashboard, locate: current EOD drawdown, daily loss buffer, qualifying days counter
- [ ] **Do not buy multiple accounts yet.** Learn the platform on one account first.

### Decisions to defer

The fork includes auto-PR pipelines (skill-improvement loop and skill-generation pipeline) that run via `launchd` and open GitHub PRs automatically. **Leave these disabled in Phase 1.** You don't have enough context yet to review their PRs intelligently. Re-evaluate enabling them in Phase 3.

---

## Weeks 2–3 — The Actual Audit

This is the core work of the phase. For each skill in the catalog, do a 15-minute evaluation. Build a personal `skills_audit.md` at the repo root tracking ratings.

### Audit template

```markdown
## <skill-name>

- **Read SKILL.md:** ☐
- **Ran with realistic input:** ☐
- **Output usefulness for futures-focused workflow (1–5):** _
- **Status:** works as-is / needs extension / not relevant for me
- **Notes:** [what worked, what didn't, ideas for futures adaptation]
- **Time invested:** _ min
```

### Suggested audit order (highest leverage first)

**Tier 1 — likely highest value for your workflow**

1. `exposure-coach` — daily market posture synthesis. If this is good, it becomes the first thing you run every morning.
2. `technical-analyst` — does it work on hourly/15min charts that matter for futures?
3. `trader-memory-core` — start logging trades here today, not later
4. `position-sizer` — does it handle futures contract math? (Probably not — this becomes a Phase 2 extension target)
5. `market-news-analyst` — useful for catalyst awareness pre-market?

**Tier 2 — context-setting**

6. `market-breadth-analyzer`, `uptrend-analyzer` — how do they compare? Is one redundant?
7. `economic-calendar-fetcher` — critical for futures (FOMC, NFP, CPI move ES/NQ hard)
8. `market-top-detector`, `ftd-detector` — useful for regime context but lower frequency
9. `theme-detector` — probably less useful for futures than for equity stock-picking
10. `sector-analyst` — same caveat as theme-detector

**Tier 3 — likely lower priority for futures focus**

The screening skills (`vcp-screener`, `canslim-screener`, `value-dividend-screener`, `dividend-growth-pullback-screener`, `kanchi-dividend-sop`, etc.) are equity-focused. Audit them last and probably mark most as "not relevant for me" — but keep them around for when you want to research individual stocks.

**Tier 4 — infrastructure (audit by reading, not running)**

- `dual-axis-skill-reviewer` — read the SKILL.md to understand how it scores
- `edge-pipeline-orchestrator` — read to understand the orchestration pattern (you'll mirror this in Phase 2)
- `signal-postmortem` — read the schema; you'll feed it data in Phase 3

### What "works as-is" means

A skill works as-is if: (a) you can run it without errors, (b) the output is intelligible to you, (c) it produces something you'd actually use in your decision-making. If you read the output and shrug, that's a 2/5 regardless of whether the script ran cleanly.

### What "needs extension" means

A skill needs extension if the core logic is sound but it's missing futures-specific behavior. Example: `position-sizer` does Kelly criterion math correctly, but doesn't know that ES is $50/point. The fix is wrapping it, not rebuilding it.

---

## Week 4 — Generate Baseline Data

The learning loop needs data. Generate it.

### Run the existing pre-built commands

- [ ] Pick 5 watchlist tickers (any liquid US stocks — you're testing the pipeline, not picking trades)
- [ ] Run `/deep-research <TICKER>` on each. Save outputs to `~/trading-research/reports/`.
- [ ] Run `/update-research <TICKER>` on one a week later to test the diff workflow
- [ ] Run `/intraday-options <TICKER> 500` once on a day with an actual setup (not just to test — the output should be actionable)

### Daily market context routine

For at least 10 trading days:

- [ ] Run `market-breadth-analyzer` (morning)
- [ ] Run `exposure-coach` (morning)
- [ ] Save outputs to `~/trading-research/logs/market_context_YYYY-MM-DD.md`
- [ ] At end of day, write 2–3 sentences: did the market context call match what actually happened?

### Trade logging (the most important deliverable)

For every trade — paper or real, stocks or futures, manual or copilot-suggested:

- [ ] Use `trader-memory-core`'s `thesis_ingest.py` or write a one-line wrapper script
- [ ] Capture: ticker, direction, entry/exit, size, **thesis (free text — why)**, **confidence 1–5**, tags, stop, target
- [ ] After close: pnl, **review (free text — what happened, what was missed)**

If you take 0 trades in week 4, that's fine — log paper trades or hypothetical trades from the research reports. The point is to populate the database with text the embedding model can search later.

### Lucid evaluation

- [ ] If markets are open during week 4, take a few trades on the Lucid eval account
- [ ] Even if you fail the eval — the data on *why* you failed is the most valuable Phase 1 output
- [ ] Log every trade to `trader-memory-core` with the `account: lucid_eval` tag

---

## Exit Criteria (all must be met to advance to Phase 2)

- [ ] `skills_audit.md` exists with ratings for all skills you ran
- [ ] At least 3 Tier 1 skills audited and rated
- [ ] 10+ trades logged to `trader-memory-core` (paper or real, any market)
- [ ] 10+ days of market context outputs in `~/trading-research/logs/`
- [ ] At least one Lucid eval account purchased and at least one trade taken on it
- [ ] Total Anthropic spend < $20
- [ ] Pre-commit hooks pass cleanly on every commit you made

---

## Common Phase 1 Pitfalls

**Pitfall 1: "I'll just build the futures stuff first, audit later."**
You'll build it on assumptions about what's missing. Half of what you build will duplicate something the existing repo already does, and you won't notice until much later. Audit first.

**Pitfall 2: Spending too long on each skill audit.**
15 minutes per skill. If you can't tell if it's useful in 15 minutes, mark it 3/5 and move on. You can revisit.

**Pitfall 3: Not logging trades because you "haven't started trading yet."**
Log paper trades. Log hypothetical trades. Log the trade you would have taken if you'd been at your desk. The database needs text and structure, not P&L.

**Pitfall 4: Buying Lucid evaluations beyond the first one.**
One account in Phase 1. You need to learn the platform's quirks (4:45 PM auto-flatten behavior, dashboard refresh delays, payout cycle mechanics) before scaling.

**Pitfall 5: Enabling the launchd jobs.**
The auto-PR pipelines are powerful but assume you have time to review PRs. In Phase 1, you don't. Disable them.

---

## What's NOT in Phase 1

- Writing any new skill (Phase 2)
- Touching the Lucid rules engine (Phase 2)
- Tradovate API integration (Phase 2)
- Behavioral pattern detection (Phase 3)
- Backtesting (Phase 4)
- Anything autonomous (Phase 5)

If the conversation drifts toward any of these in Phase 1, push back: *"That's Phase X. We're still in Phase 1, focused on audit and data generation."*

---

## When You're Ready to Advance

Update the main `PROJECT.md`:
- Change "Active Phase" to Phase 2
- Reset "This week's focus"
- Read `project-docs/phase-2-futures-skills.md` to set new context
