# Personal Trading Playbook

> Canonical home for rules derived from live trading, audit,
> and system operation. Load when planning trades or reviewing
> positions. Updated at the end of each phase.
> Last updated: 2026-08-16

---

## Session core (TA-first)

Daily product: TradeWhisperer **lists** + GEX/VEX + operator charts →
`/ta-confluence` → PLAY/WATCH/NO_TRADE → optional `/agentic-copilot-trade` on
Portfolio C. Deep research and FMP screeners are gated optional backup only.

**Account scope:** Log and size for Portfolio **A** (taxable) and **C** (Agentic).
**Do not log IRA (Portfolio B)** — operator discontinued four-questions cadence.

---

## TA routing (charter)

**Default path:** TradeWhisperer lists → Skylit GEX/VEX (pasted) → operator charts → `ta-confluence` → thesis / Agentic co-pilot.

**Deep-research / fundamentals:** optional backup only — PLAY verdict, verge of confluence (operator OK), or explicit ask.

**Artifact rule:** Ask for missing sources before forcing a score. Lists beat chart-inferred TW color. Operator chart required before PLAY. NO_TRADE is success.

**Playbook edits:** Agent proposes; operator approves. Never silent overwrite of this file or risk config.

## Market Context Rules

**FTD vs Breadth conflict resolution:**
When ftd-detector and market-breadth-analyzer/uptrend-analyzer
conflict, the LOWER exposure ceiling governs.
FTD_CONFIRMED is necessary but insufficient for aggressive
exposure — breadth confirmation is required to act on the signal.
Example: FTD_CONFIRMED 95/100 + breadth 33/100 = CAUTIOUS
posture, not aggressive. Narrow advance = selective exposure only.
Source: First live run 2026-05-09.

**Free daily breadth stack replaces exposure-coach at current scale:**
market-breadth-analyzer + uptrend-analyzer + sector-analyst
run together = credible daily posture at zero token cost.
Run exposure-coach weekly (not daily) when all three CSV outputs
are available. exposure-coach value scales with portfolio size —
at $500 the token cost exceeds the signal value.

---

## IRA (Portfolio B) — out of operator scope

Portfolio B (Roth IRA) may appear in MCP account discovery. **Do not:**
- Run `/log-positions` four-questions for IRA holdings
- Treat IRA logging as a Phase 1 exit criterion
- Spend session time on IRA thesis intake

MCP trades on IRA remain forbidden. If the operator later resumes IRA
logging, restore rules from git history / decisions.md — until then skip B.

---

## System Operational Rules

**Reports live in reports/ within the repo (git tracked).**
Structured reports (research, logs, options plans) are committed to `reports/`.
Only intermediate skill run artifacts (loose `.json` files) are gitignored.
`~/trading-research/` references in older notes are superseded — use `reports/` paths.



**Portfolios (2026-05-28):**

| Label | Account | Size | Sync / log path |
|-------|---------|------|-----------------|
| A | Robinhood taxable | ~$250 | `robinhood_sync.py` → `pending_ingest.json` → `/log-positions` |
| B | Robinhood Roth IRA | ~$10K | **Do not log** (discover-only) |
| C | Robinhood Agentic | ~$50 | Official Robinhood Agentic MCP → `/log-positions` after fills |

**Robinhood sync workflow (Portfolio A):**
1. `uv run python3 scripts/robinhood_sync.py` (2FA on first run only)
2. Fill ACCOUNT_MAP in script with printed account IDs (refresh if login changed)
3. Run `/log-positions` for **taxable (A) only** — answer 4 questions per new A position

**Robinhood Agentic MCP (Portfolio C):**
Trade Agentic only. Co-pilot workflow:
[commands/agentic-copilot-trade.md](../commands/agentic-copilot-trade.md)
(confirm → review → confirm → place). Log C fills to `robinhood_agentic`.
Skip IRA (B) logging — see [decisions.md](../decisions.md) / PROJECT.md.

What sync/MCP captures automatically: ticker, size, avg cost, account, options fields.
What always requires human input: thesis, confidence, stop, target.

**Scheduled sync:** `robinhood-sync.timer` at 4:30 PM ET weekdays — see [launchd/README.md](../launchd/README.md).
Enable only after manual 2FA succeeds once.

**economic-calendar-fetcher is permanently blocked on free FMP tier.**
Returns [] silently — no error, empty output.
Use scripts/fred_calendar.py instead (built 2026-05-09).
FRED_API_KEY required (free registration at fred.stlouisfed.org).

**exposure-coach schema mismatch fixed 2026-05-10 (verified 2026-05-28).**
Nested `composite.composite_score` paths parse correctly (breadth/uptrend).
LOW confidence when only breadth+uptrend provided is **expected** — missing
`regime` and `top_risk` are in CRITICAL_INPUTS. Run weekly with full inputs when FMP allows.

**vcp-screener (optional / demoted):** FMP Starter active — use `--universe`
from watchlist. Full S&P 500 needs Premium (not approved). TA-first path
does not require daily vcp runs.

**market-top-detector:** works on Starter stable API for posture context;
`--static-basket` only if ETF endpoints fail.

**ftd-detector: SPY-only graceful degradation.**
QQQ component blocked on free FMP tier.
Script degrades to S&P 500 only — FTD signal still meaningful.
NASDAQ component restored when FMP Starter is active.

---

## Portfolio Scale Rules

Portfolio A: ~$250 Robinhood taxable (deployment capital) — sync + log.
Portfolio B: ~$10K Robinhood IRA — out of logging scope.
Portfolio C: ~$50 Robinhood Agentic (equities; options later) — trade + log.

**Skill ratings that scale with portfolio size:**
- exposure-coach: H:3 at $500 -> H:5 at $50K
- options-strategy-advisor: H:3 at $500 -> H:5 at $5K+
  (multi-leg strategies inaccessible at $500)
- position-sizer: 1% risk = $5 at $500; $100 at $10K;
  meaningful constraint only above ~$5K

---

## Playbook Setups (seed — expand from confluence sessions)

Setups should cite all three sources. Expand via weekly distill ([phase-2-learning-loop.md](phase-2-learning-loop.md)).

### TA Setup template

```markdown
### Setup: [Name]
- TW: period list color + HTF stack / fight rules
- Maps: GEX/VEX magnets, kings, traps
- Operator: S/R, fib, VP shelf, SMA stack
- Entry trigger
- Invalidation (TW + maps + operator)
- Targets
- When NOT to take it
- Linked confluence / thesis IDs
```

### Stock / options setups

[To be populated from live `ta-confluence` sessions — target 3+ before Phase 2 exit]

---

## Charting Coach (active learning)

Operator-approved notes on markup hygiene. Newest first.

| Date | Keep / Fix | Next session try |
|------|------------|------------------|
| _(empty)_ | | |

---

## Lessons Log (most recent first)

**2026-08-16 — Charter pivot to TA-first**
Center of gravity is three-source confluence and playbook learning.
Fundamentals/deep-research demoted to gated backup. Phase 2 rewritten
around pattern journal → charting coach → playbook → postmortem.

**2026-05-09 — First live run**
The week of 5/4-5/8 established that overnight momentum setups can carry
a week when intraday scalps are net negative. Pattern worth tracking in
stock/options swing workflow as playbook matures.
