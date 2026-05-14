# Personal Trading Playbook

> Canonical home for rules derived from live trading, audit,
> and system operation. Load when planning trades or reviewing
> positions. Updated at the end of each phase.
> Last updated: 2026-05-10

---

## Lucid Trading Rules (Operational)

**AutoLiq = Daily Profit Target Hit — NOT a rule violation.**
When Lucid auto-liquidates a position, check the P&L first.
If the session P&L equals or exceeds the daily profit target
($625 for current LucidFlex account), AutoLiq was triggered
by hitting the target — a qualifying day event, not a risk event.
AutoLiq as a risk event would occur at a loss — different scenario.
Source: Session D reconstruction (5/5-5/6 overnight long at
28303 -> AutoLiq at 28487.5, +$625 net).

**4:45 PM ET hard auto-flatten.**
Lucid flattens all positions daily. Agent closes earlier.
Never hold into the 4:45 window expecting a manual exit.

**Qualifying day threshold:** $625 minimum daily profit for
current $50K LucidFlex account. Required: 5 qualifying days
per payout cycle. Resets after each payout.

**Overnight holds are valid — but size accordingly.**
Session D (overnight long to profit target) was the only
significantly profitable session in the first week.
Overnight shorts in Session I (concurrent 3-way short) were
all stopped out. Lesson: overnight holds work when the macro
direction is confirmed. Three concurrent overnight shorts in
a trending market is aggressive — size down or use fewer legs.

---

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

## IRA Rules (Portfolio B)

**Portfolio B is a Robinhood IRA. All options must be IRA-eligible.**
Permitted: long calls, long puts, covered calls, cash-secured puts.
Not permitted: naked selling, undefined risk spreads, multi-leg
strategies requiring margin.

**Every options recommendation for Portfolio B must be flagged:**
- IRA-eligible: [Yes/No] — [strategy name]
Before presenting any options strategy as actionable for Portfolio B,
confirm IRA eligibility. Non-eligible suggestions are educational only.

**IRA capital is not easily replenished.**
2026 contribution limit: $7,000 ($8,000 if 50+).
Significant drawdown cannot be recovered the same way as
a taxable account. This reinforces the importance of:
- Sizing for maximum loss explicitly
- Using defined-risk structures where possible
- Not treating the IRA as a speculation account despite
  the learning-first mandate

---

## System Operational Rules

**Reports live in reports/ within the repo (git tracked).**
Structured reports (research, logs, options plans) are committed to `reports/`.
Only intermediate skill run artifacts (loose `.json` files) are gitignored.
`~/trading-research/` references in older notes are superseded — use `reports/` paths.



**Robinhood sync workflow:**
1. `python3 scripts/robinhood_sync.py` (2FA on first run only)
2. Fill ACCOUNT_MAP in script with printed account IDs
3. Run `/log-positions` in Claude Code — answer 4 questions
   per position (thesis, confidence, stop, target — everything
   else pre-filled from Robinhood)

What sync captures automatically: ticker, size, avg cost,
account, and for options: strike, expiry, type, contracts,
IRA eligibility, basic tags.
What always requires human input: thesis, confidence, stop, target.

For scheduled runs: install systemd service and timer
(see launchd/README.md for setup commands).
Enable ONLY after completing manual 2FA auth at least once.

**economic-calendar-fetcher is permanently blocked on free FMP tier.**
Returns [] silently — no error, empty output.
Use scripts/fred_calendar.py instead (built 2026-05-09).
FRED_API_KEY required (free registration at fred.stlouisfed.org).

**exposure-coach schema mismatch fixed 2026-05-10.**
P2 fix applied — extract_breadth_score(), extract_uptrend_score(),
extract_sector_score() all updated to read nested composite paths.
55/55 tests pass. Confirm STATUS.md shows fix before trusting output.

**vcp-screener is blocked on free FMP tier.**
Batch quote endpoint restricted on free tier.
FMP Starter ($29/mo) approved — upgrade before next live session.
Until upgraded: skip vcp-screener step in stock selection pipeline.
Manual VCP validation on CANSLIM candidates is the workaround.

**market-top-detector: use --static-basket flag.**
QQQ and sector ETFs blocked on free FMP tier.
--static-basket flag enables SPY-only mode.
Loses 2 of 6 components but output remains useful.

**ftd-detector: SPY-only graceful degradation.**
QQQ component blocked on free FMP tier.
Script degrades to S&P 500 only — FTD signal still meaningful.
NASDAQ component restored when FMP Starter is active.

---

## Portfolio Scale Rules

Portfolio A: ~$500 Robinhood taxable (deployment capital).
Portfolio B: ~$10K Robinhood IRA (full trading, IRA restrictions).

**Skill ratings that scale with portfolio size:**
- exposure-coach: H:3 at $500 -> H:5 at $50K
- options-strategy-advisor: H:3 at $500 -> H:5 at $5K+
  (multi-leg strategies inaccessible at $500)
- position-sizer: 1% risk = $5 at $500; $100 at $10K;
  meaningful constraint only above ~$5K

---

## Playbook Setups (seed — expand from live trading)

### Stock Setups

[To be populated after 10+ logged trades]

### Futures Setups (ES/NQ/MES/MNQ)

[To be populated after Phase 2 build]

---

## Lessons Log (most recent first)

**2026-05-09 — First live run**
The week of 5/4-5/8 was profitable overall (~+$258) despite
losing on most individual scalp sessions. The single overnight
long (Session D) generated +$625 and carried the entire week.
Scalping alone (Sessions A, B, C, G, H) was net -$370.
Pattern: overnight momentum trades > intraday scalping for MNQ.
Without Session D, the week would have been deeply negative.
