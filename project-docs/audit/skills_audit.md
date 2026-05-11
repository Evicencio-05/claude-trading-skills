<!-- Load for operational reference.
     Load skills_audit_detail.md only when investigating a specific skill. -->

# Skills Audit

**Phase 1 — Audit & Activate**
**Started:** May 9, 2026
**Target completion:** May 30, 2026

**Portfolio scale (updated 2026-05-09):**

| Portfolio | Account | Capital | Access | Constraint |
|---|---|---|---|---|
| A | Robinhood taxable | ~$500 | Stocks + options | Deployment capital |
| B | Robinhood Roth IRA | ~$10K | Stocks + IRA-eligible options only | Capital preservation secondary; IRA options rules apply |

IRA-eligible options: long calls, long puts, covered calls, cash-secured puts.
NOT eligible: naked selling, undefined-risk spreads, margin strategies.
**IRA rule for all sessions:** any skill recommendation for Portfolio B must be
flagged IRA-eligible or NOT EXECUTABLE before it is presented as actionable.

---

## Rating System

**Human-assisted (H):** Value when a human reviews and acts on the output.
**Autonomous learning chain (A):** Value as an automated, schedulable component
that feeds the learning loop without human intervention at every step.
**Future autonomous potential (F):** Ceiling once screenshot automation, outcome
tracking, reliability validation, and capital growth are in place.

Format per skill: Stock H/A(F) | Futures H/A(F)
F is only shown when it differs meaningfully from A.

**A skill earns its tokens if it either:**

1. Feeds structured, measurable outputs into trader-memory-core or the learning
   pipeline, OR
2. Materially improves a human trading decision traceable to an outcome

Skills that do neither are decoration.

---

## Open Fixes

Known issues with workaround status. Fix before relying on the affected skill.

| ID | Issue | Status | Effort | File |
|---|---|---|---|---|
| P1 | API keys unavailable in non-interactive shells (Claude Code bash tool) | [x] FIXED 2026-05-10 | 30 min | All `fmp_client.py` + `fred_calendar.py` |
| P2 | exposure-coach schema mismatch — extraction functions couldn't parse actual JSON outputs | [x] FIXED 2026-05-10 | 30 min | `skills/exposure-coach/scripts/calculate_exposure.py` |

**P1 fix details:** Added `python-dotenv` to `pyproject.toml`. Created `.env` at repo root
(gitignored). Added `load_dotenv()` to all 9 `fmp_client.py` files and `scripts/fred_calendar.py`.
Keys now load automatically without `bash -i` workaround. Confirmed: FMP_API_KEY loaded in
non-interactive shell. Installed via `uv pip install python-dotenv`.

**P2 fix details:** Three extraction functions updated in `calculate_exposure.py`:

- `extract_breadth_score()`: now reads `data["composite"]["composite_score"]` first
- `extract_uptrend_score()`: now reads `data["composite"]["composite_score"]` first
- `extract_sector_score()`: now reads `data["groups"]["score"]` first
All three inputs now parse correctly (breadth=33, uptrend=31, sector=65 on 2026-05-09 data).
Remaining LOW confidence is accurate — `regime` and `top_risk` (both in CRITICAL_INPUTS)
are legitimately missing (require FMP paid tier). 55/55 exposure-coach tests still pass.

---

## Daily Workflow Stack (established from Tier 1–2 audit)

These three run together every morning. Zero API cost. Zero setup required.
Total time: under 60 seconds. They replace exposure-coach at current portfolio scale.

```
market-breadth-analyzer   →  S&P breadth health score (0-100)
uptrend-analyzer          →  Per-stock uptrend participation + sector heatmap
sector-analyst            →  Sector rotation + cyclical/defensive balance
```

Together these produce a credible exposure-coach output at zero cost.
Run exposure-coach itself only weekly, when all upstream JSON outputs are saved.
Log all three scores to ~/trading-research/logs/market_context_YYYY-MM-DD.md daily.

**When FMP key is configured, add:**

```
earnings-calendar         →  This week's earnings (run once per week Monday AM)
```

**economic-calendar-fetcher is blocked on FMP free tier. Use the FRED replacement instead:**

```bash
# FOMC dates work immediately (hard-coded, no key needed)
python3 scripts/fred_calendar.py --from $(date +%Y-%m-%d) --to 2026-12-31 --format text

# Full CPI/NFP/PPI coverage requires free FRED API key:
# Get key at fred.stlouisfed.org/docs/api/api_key.html → export FRED_API_KEY=...
python3 scripts/fred_calendar.py --format text
```

---

## FMP Key Priority

**Confirmed 2026-05-09: FMP free tier unlocks 8 of 9 skills. One exception.**

economic-calendar-fetcher, earnings-calendar, earnings-trade-analyzer,
pead-screener, vcp-screener, canslim-screener, market-top-detector,
ftd-detector, institutional-flow-tracker

FMP key is set in ~/.bashrc. Source it before running scripts:

```bash
source ~/.bashrc  # or: FMP_KEY=$(grep 'FMP_API_KEY=' ~/.bashrc | tail -1 | sed 's/.*FMP_API_KEY=//')
```

**Exception: economic-calendar-fetcher is blocked on free tier.**
The `/stable/economics-calendar` endpoint silently returns `[]` on free tier.
All other FMP stable endpoints (historical-price, quote, earnings-calendar,
profile) work on free tier. 250 calls/day is sufficient for default settings.
**Replacement built (2026-05-09):** `scripts/fred_calendar.py` — FOMC dates work
immediately (hard-coded from federalreserve.gov). CPI/NFP/PPI require a free FRED
API key (fred.stlouisfed.org/docs/api/api_key.html). No monthly cost.

**Additional FMP free tier restriction discovered (2026-05-09):**
All ETFs except SPY are blocked on free tier — returns "Premium Query Parameter:
Special Endpoint." Confirmed blocked: RSP, IWM, HYG, LQD, TLT, SHY, QQQ, and all
sector ETFs (XLE, XLK, XLC, XLY, XLP, etc.). This affects skills beyond
economic-calendar-fetcher. See RETEST REQUIRED flags on market-top-detector and
ftd-detector in Tier 2.

**FMP paid tier upgrade decision gate:**
FMP Starter ($29/mo) unlocks a meaningful skill cluster simultaneously:

- macro-regime-detector — H:4/A:3, cross-asset regime detection for futures bias
- ibd-distribution-day-monitor — QQQ unblocked, partial fix
- market-top-detector — likely fixes sector ETF fetches (retest required)
- ftd-detector — likely fixes QQQ component (retest required)
- economic-calendar-fetcher — native skill restored, FRED workaround retired
Upgrade condition: when Lucid prop firm account is live and generating consistent
P&L. At that point regime context directly improves futures positioning decisions
and $29/mo has a clear ROI case. Do not upgrade before Phase 5 unless conditions
create urgent need. Document decision in decisions.md when made.

**scenario-analyzer rewrite — open action item:**
Japanese output is hardcoded throughout — not a config change, a ~30 min SKILL.md
edit. The underlying methodology (dual-agent, 18-month scenarios, critic pass) is
worth having. Not urgent. Add to a quiet session when current priorities are clear.

---

## Key Skill Pipelines (established from Tier 1–2 audit)

**Daily market check (free, automatable):**
market-breadth-analyzer + uptrend-analyzer + sector-analyst
→ exposure-coach (weekly synthesis)

**Stock selection pipeline:**
canslim-screener (fundamental filter, weekly)
→ vcp-screener (technical structure filter, weekly)
→ breakout-trade-planner (Minervini gate + portfolio heat + sized order plans)
→ technical-analyst (chart validation, human-assisted)
→ position-sizer (risk sizing confirmation, pre-trade)
→ trader-memory-core (log thesis and outcome)

**Earnings momentum pipeline:**
earnings-calendar (weekly, Monday AM)
→ earnings-trade-analyzer (post-earnings window, 2-day lookback)
→ pead-screener (tracks SIGNAL_READY → BREAKOUT states, up to 5 weeks)
→ trader-memory-core (log each state transition as outcome data)

**Market regime bracket:**
market-top-detector (defensive — when to reduce exposure)
↔ ftd-detector (offensive — when to re-enter after correction)
These two are only meaningful as a pair. Neither is useful in isolation.

**Futures pre-session stack (Phase 2+):**
market-news-analyst + economic-calendar-fetcher + earnings-calendar
→ futures-pre-market-scan (Phase 2 build)
→ lucid-rules-engine check
→ futures-position-sizer

---

## Tier 1 — Action Items

**Immediate (do today):**

- [x] Set FMP_API_KEY — in ~/.bashrc (needs sourcing each session: `source ~/.bashrc`)
- [x] Run economic-calendar-fetcher as first FMP key validation test
      → RESULT: economics-calendar endpoint blocked on FMP free tier (silently returns []).
        FMP historical-price, quote, and earnings-calendar endpoints work on free tier.
        See workaround note in economic-calendar-fetcher entry above.
- [ ] Log first entry to trader-memory-core (paper trade or hypothetical)

**FMP endpoint summary (post-Aug 2025 accounts):**

| Endpoint | Status | Skills using it |
|----------|--------|-----------------|
| `/stable/historical-price-eod/full` (individual stocks) | ✅ Works | earnings-trade-analyzer, pead-screener |
| `/stable/historical-price-eod/full` (most ETFs) | ❌ "Special Endpoint" | macro-regime-detector, ibd-distribution-day-monitor, market-top-detector |
| `/stable/quote` (individual stocks) | ✅ Works | vcp-screener, canslim-screener |
| `/stable/earnings-calendar` | ✅ Works | earnings-calendar |
| `/stable/profile` | ✅ Works | earnings-calendar (market cap filter) |
| `/stable/treasury-rates` | ✅ Works | macro-regime-detector (treasury component only) |
| `/stable/economics-calendar` | ❌ Returns [] silently | economic-calendar-fetcher |
| `/api/v3/*` all endpoints | ❌ Legacy error | Any skills using old API |

**ETF access on free tier (tested 2026-05-09):**
SPY ✅ | QQQ ❌ | RSP ❌ | IWM ❌ | HYG ❌ | LQD ❌ | TLT ❌ | SHY ❌ | XLY ❌ | XLP ❌ | XLE ❌
Implication: skills requiring non-SPY ETFs need a paid FMP plan. Affects:
macro-regime-detector (broken — 0/6 components), ibd-distribution-day-monitor
(QQQ blocked — partial), market-top-detector + ftd-detector (recheck — likely broken).

**Shell note:** FMP_API_KEY is in ~/.bashrc but Bash tool sessions don't auto-source it.
Pass it explicitly: `FMP_KEY=$(grep 'FMP_API_KEY=' ~/.bashrc | tail -1 | sed 's/.*FMP_API_KEY=//')`

**Before Tier 2 audit:**

- [ ] Run each Tier 1 skill once with realistic input (mark "Ran" checkboxes)
- [ ] Start logging technical-analyst predictions for outcome tracking

---

## Tier 2 — Key Observations

**The three free daily skills** (market-breadth-analyzer, uptrend-analyzer,
sector-analyst) are the most immediately deployable output of the entire audit.
Zero setup, zero cost, meaningful signal. Start running them tomorrow morning.

**FMP unlocks 9 skills.** One action, maximum leverage. Do this today.

**The stock selection pipeline is now clear:**
CANSLIM → VCP → technical-analyst → position-sizer → trader-memory-core
Each stage has a defined output that feeds the next. This pipeline can be
partially automated once FMP is configured.

**institutional-flow-tracker has a permanent ceiling.** 45-day SEC lag is not
fixable at any budget. Use it quarterly for thesis validation only.

**market-top-detector and ftd-detector need retesting.**
FMP free tier ETF restriction (discovered Questionable Skills session, 2026-05-09)
blocks QQQ and all sector ETFs. Both skills fetch these — do not rely on them until
retested. Add to next FMP debugging session. See RETEST REQUIRED flags on each entry.

**parabolic-short-trade-planner should be read, not necessarily run.**
The FSM architecture is Phase 2 study material. The Qullamaggie short setup
requires broker capabilities the current account may not have.

**portfolio-manager is a quick win.** Alpaca paper account setup costs nothing
and activates this skill plus provides the integration template for Phase 2.

---

## Tier 3 — Key Observations

**Two separate learning loops exist in this repo — don't confuse them.**

Loop A (trader-memory-core): Tracks your actual trades. Thesis lifecycle: IDEA → ENTRY_READY → ACTIVE → CLOSED. Postmortem with MAE/MFE. This is running from Day 1.

Loop B (edge pipeline): Automated signal generation → signal-postmortem → weight adjustments → skill improvement. Skills: edge-candidate-agent → edge-pipeline-orchestrator → signal-postmortem → dual-axis-skill-reviewer → skill improvement loop. This is Phase 3+.

Both loops need to run eventually. Loop A starts now with every trade you log. Loop B starts in Phase 3 when the pipeline infrastructure is connected.

**dual-axis-skill-reviewer is immediately usable for ad-hoc quality checks.** The automation deferred to Phase 3, but running it manually on any Tier 1-2 skill takes 2 minutes and surfaces documentation gaps or broken scripts before you depend on them.

**backtest-expert is immediately usable for any strategy validation.** No dependencies. Run evaluate_backtest.py on any paper trade strategy before scaling it. Read methodology.md now — the thinking applies to how you log and tag trades in trader-memory-core from Day 1.

**edge-pipeline-orchestrator and signal-postmortem have zero Day 1 value.** Their inputs don't exist yet. Reading SKILL.md was worth the time to understand the Phase 3 architecture; running them now would be wasted effort.

**economic-calendar workaround needed.** FRED API (federal reserve, free, no API key) provides FOMC, CPI, NFP dates. Consider a FRED-based alternative to economic-calendar-fetcher before Phase 2 futures pre-session stack is built.

---

## Tier 4 — Key Observations

**The dividend stack is a package, not three independent skills.**
value-dividend-screener → dividend-growth-pullback-screener → kanchi-dividend-sop
form a pipeline where each skill feeds the next. Evaluating them separately
understates their combined value but overstates their individual usefulness. At
$500 account size, dividend income is economically trivial; these skills earn their
keep only once capital exceeds ~$5K.

**pair-trade-screener is wrong for the current setup.**
Market-neutral two-leg strategies require shorting. Robinhood doesn't support
shorting. The methodology is sound, but execution is impossible until broker and
capital constraints change.

**us-market-bubble-detector is the sleeper.**
No API required. Quarterly cadence. Directly relevant to futures index bias. The
confirmation bias checklist in the workflow is unusually rigorous for a stock market
skill. Run this before every major position sizing decision.

---

## Questionable Skills — Key Observations

**The FMP free tier ETF restriction is bigger than expected.**
Testing during this section revealed that only SPY (and major index tickers like
individual equities) are accessible on the stable endpoint. All ETFs except SPY
return "Premium Query Parameter: Special Endpoint" on free tier:

- Blocked: RSP, IWM, HYG, LQD, TLT, SHY, XLY, XLP, QQQ, XLE, XLC, XLK
- Works: SPY, individual US equities (AAPL, MSFT, etc.)

**Affected skills beyond this section:**
This discovery likely affects Tier 2 skills that were previously rated assuming
the endpoint worked. market-top-detector fetches QQQ + sector ETFs (XLK, XLC,
XLY) — all now known to be blocked. ftd-detector may have the same issue.
These should be retested before relying on them in the daily workflow stack.

**macro-regime-detector: highest ceiling, highest unlock cost.**
H=4/A=3 for both workflows when working. The six-component cross-asset regime
framework (concentration, yield curve, credit, size, equity-bond, sector rotation)
is exactly the kind of structural context that improves futures index positioning.
One FMP paid plan ($29/mo Starter) unlocks this AND fixes ibd-distribution-day-monitor
AND probably fixes market-top-detector. Budget decision: not now, but the ROI case
is clear once the prop firm account is live.

**scenario-analyzer is a rewrite, not a config change.**
Japanese is architectural, not a flag. The agent prompts, Important Notes section,
and "When to Use" section all hardcode Japanese. Rewriting it to English is a ~30
minute SKILL.md edit — worth doing if 18-month scenario analysis with a critic
pass is a workflow you want. The methodology is sound.

**breakout-trade-planner is the most immediate find.**
It was in "Questionable" because of suspected vcp-screener overlap, but it's not
overlap — it's the next pipeline stage. Run vcp-screener → save JSON → run
breakout-trade-planner. The output includes Minervini gate filtering, portfolio
heat, and Alpaca order templates. This should be in the active workflow today.

**ibd-distribution-day-monitor is redundant at current setup.**
No TQQQ, QQQ blocked on free tier, market-top-detector (if fixed) covers similar
ground. Low priority until FMP paid plan OR TQQQ becomes part of the strategy.

**edge-candidate-agent and trade-hypothesis-ideator are Phase 3 tools in disguise.**
Both have nominal Day-1 value (manual ticket creation, synthetic test runs), but
their real function activates when trade data exists. Log trades to trader-memory-core
for 60+ days, then come back to these.

**strategy-pivot-designer is correctly Phase 4.**
No ambiguity. Skip until backtest iteration history exists.

---

## Not Relevant Now — Skip

- stanley-druckenmiller-investment: macro philosophy, not operational
- downtrend-duration-analyzer: visualization tool, very low frequency
- kanchi-dividend-review-monitor: dividend workflow, not current focus
- kanchi-dividend-us-tax-accounting: dividend workflow, not current focus
- skill-idea-miner: Phase 3+ only
- skill-designer: Phase 3+ only
- skill-creator: Phase 3+ only

---

## Audit Progress

| Tier | Total | Read | Ran | Read+Ran (complete) |
|------|-------|------|-----|---------------------|
| Tier 1 (inc. earnings-calendar) | 11 | 11 | 8 | 7 |
| Tier 2 | 11 | 11 | 3 | 2 |
| Tier 3 | 4 | 4 | 0 | 0 |
| Tier 4 | 5 | 5 | 0 | 0 |
| Questionable | 7 | 7 | 2 | 0 |
| **Total** | **38** | **38** | **13** | **9** |

Notes:

- Tier 1 Ran (2026-05-09 live session): market-breadth-analyzer ✅, uptrend-analyzer ✅,
  sector-analyst ✅, exposure-coach ✅ (partial — schema mismatch), earnings-calendar ✅,
  us-stock-analysis ✅, trader-memory-core ✅, economic-calendar-fetcher ❌ (free tier blocked).
  Not yet run: technical-analyst (requires chart image), position-sizer (no active trade),
  market-news-analyst (not needed today), earnings-trade-analyzer, pead-screener, options-strategy-advisor.
- Tier 1 complete (Read+Ran): market-breadth-analyzer, uptrend-analyzer, sector-analyst,
  earnings-calendar, us-stock-analysis, trader-memory-core, vcp-screener (confirmed broken counts).
  Exposure-coach partial (schema mismatch — not truly "complete").
- Tier 2 Ran (2026-05-09 live session): market-top-detector ✅ (partial, --static-basket),
  ftd-detector ✅ (partial, SPX-only), vcp-screener ❌ (confirmed broken).
- economic-calendar-fetcher: Ran = [x] because the run confirmed it is broken on free tier.
  Running it was the diagnostic, not a success case.
- Tier 3 skills are "Phase 3 dependency" — they are read-only; Ran checkbox deferred.
  Exception: dual-axis-skill-reviewer and backtest-expert can be run ad-hoc today.
- Tier 4 skills: pair-trade-screener not runnable (Robinhood can't short). Dividend
  stack (value-dividend, dividend-growth, kanchi) deferred — capital constraint.
  us-market-bubble-detector deferred to quarterly cadence. All 5 read, none run.
- Questionable Ran (2026-05-09): macro-regime-detector ❌ (confirmed broken, all-zero output,
  prior session). scenario-analyzer not run (Japanese output). breakout-trade-planner not run
  (requires vcp-screener JSON first, and vcp-screener is now confirmed broken). Others deferred.

A skill is complete only when both Read AND Ran are checked.
Reading alone is research. Running confirms it works in your environment.

---

## First Live Run — 2026-05-09

**Session type:** Full morning workflow simulation
**Skills invoked:** 10 (8 new runs + 2 retests)
**Trades logged:** 1 (NVDA WATCH, th_nvda_grw_20260509_ae9b)
**Market context log:** ~/trading-research/logs/market_context_2026-05-09.md

---

### Skills That Produced Immediately Useful Output

**market-breadth-analyzer** — Best skill of the session. Zero friction. Under 10 seconds.
Score 33.1/100 is a real, actionable number. The S&P vs breadth divergence (+6% vs -0.118
over 60 days) alone is worth the daily run. Exactly as predicted in audit. No surprises.

**uptrend-analyzer** — Runs identically fast. 31.6/100 with two active warning overlays
(Late Cycle, Divergence) added context the breadth score alone couldn't give. 1/11 sectors
uptrending is a concrete, memorable number for the daily posture decision.

**sector-analyst** — Third pillar confirmed. Together, the three free tools gave a more
complete picture than a typical pre-market briefing. Tech overbought + late-cycle flag from
commodity leadership is genuinely useful context for both stock selection and index futures bias.

**ftd-detector** — Surprise find. SPY-only degradation is graceful and meaningful. FTD_CONFIRMED
with quality 95/100 and Power Trend YES is a real signal even without QQQ. The conflict between
FTD guidance (75-100%) and breadth tools (30-60%) is itself analytically valuable — it precisely
characterizes the current market: narrow advance into mega-cap strength, breadth hasn't confirmed.

**earnings-calendar** — Three tickers in two seconds. CSCO and BABA on Wednesday is exactly
the kind of positioning constraint you need to know before Monday open.

**trader-memory-core** — Worked cleanly once venv was activated. Thesis schema saved as expected.
The canslim-screener adapter workaround for manual research inputs is functional but not elegant.

---

### Surprises (Better or Worse Than Rated)

**BETTER: ftd-detector SPY-only mode** — Rated "RETEST REQUIRED" with pessimism. Actually runs
well with meaningful partial output. Upgrade status from RETEST REQUIRED to PARTIALLY WORKING.

**BETTER: market-top-detector --static-basket** — Same story. Distribution Day Count=75 and
Breadth Divergence=64 are the two most important components anyway. Not crippled, just partial.

**WORSE: vcp-screener** — Rated "works as-is (requires FMP API key)" in audit. Actually broken
on free tier. The batch quote endpoint restriction is more severe than anticipated. The entire
core pipeline (VCP → breakout-trade-planner) is blocked until FMP Starter ($29/mo). This is
the most consequential free-tier limitation discovered to date.

**WORSE: exposure-coach schema mismatch** — Expected to work with three inputs. Silently
ignored all three due to schema mismatch (looks for root-level `composite_score` but
market-breadth-analyzer nests it under `composite.composite_score`). Output is LOW confidence
with all inputs "missing" — misleading unless you know this. Filed as known issue.

**NEUTRAL: fred_calendar.py interactive shell requirement** — Keys loaded in ~/.bashrc but
only available in interactive bash (`-i` flag). Scripts invoked without `bash -i` don't see
FMP_API_KEY or FRED_API_KEY. Workaround: always use `bash -i -c '...'` in Claude Code sessions
or source ~/.bashrc inline in the same command.

---

### Friction Points Before Daily Use

1. **venv activation** — Must `source .venv/bin/activate` for trader-memory-core. No
   auto-venv. Add to daily session checklist.

2. **API keys in non-interactive shell** — `bash -i -c '...'` pattern needed for any script
   using FMP_API_KEY or FRED_API_KEY in Claude Code bash tool calls. Or export keys permanently
   to /etc/environment or ~/.bashrc with login-shell mode.

3. **vcp-screener + breakout-trade-planner blocked** — The core swing trading pipeline is
   dead on free FMP tier. Either upgrade or find a workaround (FINVIZ screener → manual
   VCP validation is a possible free alternative).

4. **exposure-coach schema fix** — 30-min edit to align extraction functions to actual JSON
   output schema. Currently produces misleading "all inputs missing" output.

5. **technical-analyst requires chart image** — Cannot invoke via CLI. Must upload chart
   screenshot in Claude Code session. Not an issue for normal use but blocks automation.
   Live sessions work fine.

6. **No manual thesis adapter** — trader-memory-core has no "us-stock-analysis" or "manual"
   source adapter. Had to use canslim-screener as a workaround. Thesis statement is
   auto-generated and doesn't capture the real thesis. Low-priority fix but adds friction.

---

### FTD vs Breadth Conflict — Key Finding

The FTD_CONFIRMED signal (95/100, Power Trend YES) directly contradicts the breadth signals
(33.1 + 31.6, both Weakening/Cautious). This conflict is not a system error — it's a precise
characterization of the current market structure:

- S&P 500 has recovered from the March 30 low primarily via mega-cap tech (NVDA near 52W high)
- Breadth has NOT confirmed — only 1/11 sectors uptrending, 8MA in downtrend
- Distribution days are accumulating (score=75)

Resolution rule going forward: **when ftd-detector and breadth tools conflict, the lower
exposure ceiling governs.** FTD is a necessary but insufficient condition for aggressive
exposure — breadth confirmation is required. Mark this as a recurring calibration question.

---

### market-top-detector + ftd-detector — Confirmed Retest Results

| Skill | Status | Notes |
|---|---|---|
| market-top-detector | PARTIALLY WORKING | Works with `--static-basket`; QQQ blocked; loses 2/6 components |
| ftd-detector | PARTIALLY WORKING | Degrades to SPY-only; NASDAQ NO_SIGNAL; quality score still meaningful |

Both can be used in daily workflow with appropriate caveats. Not crippled. Remove "RETEST
REQUIRED" flag from both — replace with "PARTIALLY WORKING — see notes."

---

### Phase 1 Exit Criteria Progress After This Session

| Criterion | Status |
|---|---|
| skills_audit.md with dual ratings, all Tier 1-2 | ✅ Complete |
| At least 8 Tier 1 skills audited and rated | ✅ Complete (11/11) |
| 10+ trades logged across 2+ trade types | ❌ 1/10 (NVDA WATCH today) |
| 10+ days of daily market context saved | ❌ 1/10 (today) |
| /deep-research on 3+ real tickers | ❌ 0/3 |
| Lucid eval account + 1 trade | ❌ Not started |
| Total Anthropic spend < $20 | ✅ (monitoring) |
| Pre-commit hooks pass | ✅ |

---

> Full per-skill detail: [skills_audit_detail.md](skills_audit_detail.md)
