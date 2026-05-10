# Skills Audit

**Phase 1 — Audit & Activate**
**Started:** May 9, 2026
**Target completion:** May 30, 2026

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

## Tier 1 — Core Stock & Options Workflow

### exposure-coach

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 partial run: REDUCE_ONLY 50% — SCHEMA MISMATCH
- Stock/options — H: 3 | A: 2 (F: 4)
- Futures — H: 3 | A: 2 (F: 4)
- Status: PARTIALLY BROKEN — schema mismatch between input files and extraction functions
- Notes: Pure aggregator — no direct API calls. Takes JSON outputs from upstream
  skills via CLI args. Missing inputs reduce confidence but don't block execution.
  Can run with just the three free CSV skills (breadth, uptrend, sector) for a
  meaningful output without any API spend.
  SCHEMA MISMATCH (2026-05-09): calculate_exposure.py extract_breadth_score() looks
  for `breadth_score` or `composite_score` at root level. market-breadth-analyzer
  outputs `composite.composite_score` (nested). Same issue for uptrend and sector.
  Result: all inputs register as "missing" despite files being provided. Output is
  LOW confidence with all inputs showing as absent. Manual synthesis required until
  fixed. Not modifying code — logging as known issue.
  SCALE DEPENDENCY: At $500, the difference between 50% and 80% exposure is $150
  in dollar risk. The 6-7 upstream dependency chain costs more in tokens than the
  output is worth at this scale. At $10K+ it becomes meaningfully valuable.
  At $50K+ it is a 5/5. Upgrade this rating explicitly as portfolio grows.
  CURRENT USE: Run weekly. Manual synthesis from 3 breadth tools gives equivalent
  output at zero compute cost. Fix schema mismatch in quiet session (30 min effort).
- Time: 12 min

---

### technical-analyst

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 5 | A: 2 (F: 4)
- Futures — H: 5 | A: 2 (F: 4)
- Status: works as-is
- Notes: Zero dependencies — no API keys, no scripts, pure multimodal image analysis.
  User provides chart screenshots; skill outputs structured markdown with trend, S/R,
  MAs, volume, patterns, and 2-4 probability-weighted scenarios. Supports stocks,
  indices, crypto, forex — ES/NQ weekly charts work with zero adaptation.
  SPLIT RATING RATIONALE: H=5 both workflows. Analysis quality is excellent and
  directly builds TA skill over time — the system confirming, denying, or redirecting
  your own chart reads compounds human edge. A=2 because screenshot fetching requires
  manual intervention today. F=4 because screenshot automation via browser tools or
  Playwright is a Phase 2-3 solve — after which the ceiling rises significantly.
  AUTONOMOUS TRUST CONDITION: Do not trust autonomously until outcome tracking shows
  >60% scenario accuracy across 30+ logged calls. Log every primary scenario predicted
  from Day 1. This data earns autonomous trust — without it, automation adds noise.
  CURRENT USE: Use heavily as human-assisted tool. Log every prediction in
  trader-memory-core with tag ["ta_prediction"]. Check outcome 5-10 sessions later.
  Build the accuracy dataset now so autonomous trust is earned, not assumed.
- Time: 8 min

---

### us-stock-analysis

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 live run: NVDA comprehensive, bearish timing
- Stock/options — H: 4 | A: 1 (F: 2)
- Futures — H: 1 | A: 1 | F: 1
- Status: works as-is
- Notes: No API keys, no scripts — WebSearch/WebFetch for live data. Four modes:
  basic info, fundamental, technical, comprehensive. Strong equity research tool.
  LEARNING CHAIN LIMITATION: Produces reports a human reads and acts on. Does not
  automatically feed trader-memory-core, cannot run on a schedule. Research tool,
  not a learning tool — this distinction governs token prioritization.
  INDIRECT FUTURES USE: Researching a high-weight index stock (NVDA at ~9% of QQQ)
  before a major catalyst is valid. Not worth more than H:2 for futures given this
  is niche and situational.
  LIVE RUN (2026-05-09): NVDA comprehensive. $215 price, $216.82 52W high, $4.77T mcap.
  FY2026 rev $215.94B (+65%), 55% margin, 101% ROE. Q1 beat EPS 8%. Strong Buy consensus
  avg $270.73. Earnings May 20. Conclusion: fundamentals 5/5, timing 1/5 (at 52W high,
  CPI tomorrow, earnings in 11 days). Thesis registered to trader-memory-core as WATCH.
  TOKEN COST: ~6 WebSearch + WebFetch calls. Moderate. Use intentionally, not daily.
  CURRENT USE: Pre-trade due diligence on individual stocks. Token cost is variable
  (WebSearch volume unpredictable). Use intentionally before entering a position,
  not as a daily routine.
- Time: 9 min

---

### trader-memory-core

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 live run: NVDA thesis logged, th_nvda_grw_20260509_ae9b
- Stock/options — H: 5 | A: 5 | F: 5
- Futures — H: 5 | A: 5 | F: 5
- Status: works as-is (stocks/options); minor gap for futures
- Notes: THE central nervous system. Every other skill either feeds into it or is
  served by it. Non-negotiable from Day 1. No API required for core.
  Scripts: thesis_ingest.py (register), thesis_store.py (query/transition),
  thesis_review.py (postmortem, summary). State is YAML in state/theses/,
  atomic writes, git-tracked.
  REQUIRES VENV: `source .venv/bin/activate` before running — jsonschema not
  available in system Python. Add this to daily workflow notes.
  LIVE RUN (2026-05-09): NVDA growth_momentum thesis registered via canslim-screener
  adapter (closest fit for manual research). ID: th_nvda_grw_20260509_ae9b. Status:
  IDEA. Confidence=4, entry $200, stop $188, target $250, next_review=2026-06-08.
  INGEST LIMITATION: No "manual research" or "us-stock-analysis" source adapter.
  Must use closest screener format (canslim for growth_momentum type). Thesis
  statement is auto-generated from adapter — not the full thesis text. Consider
  adding a "manual" adapter in Phase 2 (5-line change).
  LEARNING CHAIN: This IS the learning chain. Without structured trade data flowing
  through here, every other skill produces research that evaporates. With it,
  patterns compound over months and feed Phase 3 behavioral detection.
  FUTURES GAP: No futures thesis types in current enum. Approximate with
  pivot_breakout or mean_reversion for now. Add futures_momentum,
  futures_mean_reversion, futures_open_drive in Phase 2 as a one-line fix.
  TAGGING CONVENTION: Tag every entry by workflow — stock_swing, options_earnings,
  futures_lucid_eval — enables workflow-specific pattern extraction in Phase 3.
  Also tag macro context: pre_FOMC, CPI_week, earnings_nearby.
  CURRENT USE: Start immediately. Log paper and hypothetical trades if no real ones.
  The system needs text and structure now.
- Time: 13 min

---

### position-sizer

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 5 | A: 4 (F: 5)
- Futures — H: 2 | A: 1 (F: 4)
- Status: works as-is (stocks/options); needs extension for futures
- Notes: No API, standard library only — fully offline. Three modes: Fixed
  Fractional, ATR-based, Kelly Criterion. Outputs shares, dollar risk, constraints.
  LEARNING CHAIN: Can be called programmatically before any position — one of the
  few skills that improves system behavior without requiring human review of output.
  FUTURES GAP: No contract multiplier (ES $50/pt, MES $5/pt, NQ $20/pt, MNQ $2/pt),
  no margin, no Lucid daily loss limit. This is the primary template for
  futures-position-sizer in Phase 2 — methodology is identical, only output unit
  changes from shares to contracts.
  CURRENT USE: Use as-is for all stock trades. Do futures math manually until Phase 2.
  Do not skip position sizing — the discipline habit matters more than the tool now.
- Time: 10 min

---

### market-news-analyst

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 3 | A: 2 | F: 3
- Futures — H: 5 | A: 4 (F: 5)
- Status: works as-is
- Notes: No API — WebSearch/WebFetch only. 10-day macro sweep: FOMC, CPI, NFP,
  GDP, geopolitical events, mega-cap earnings. Four reference files.
  FUTURES RATING: FOMC, CPI, NFP are PRIMARY ES/NQ movers. This skill is more
  critical for futures than stocks. Run before every futures session. A=4 not 5
  because web search reliability varies and output warrants spot-checking.
  STOCK RATING: At $500 with 1-2 positions, daily token cost of WebSearch + article
  fetching + long output is expensive relative to actionable signal. Run before major
  decisions and near economic events — not as a daily stock routine. 3/5 is honest.
  CURRENT USE: Daily for futures pre-session (Phase 2+). Pre-decision for stocks.
- Time: 11 min

---

### earnings-trade-analyzer

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 5 | A: 4 (F: 5)
- Futures — H: 2 | A: 1 | F: 2
- Status: works as-is (requires FMP API key)
- Notes: FMP required. Free tier sufficient for defaults (2-day lookback, top 20).
  5-factor scoring: Gap Size, Pre-Earnings Trend, Volume Trend, MA200, MA50.
  Grades A/B/C/D. Feeds directly into pead-screener pipeline.
  LEARNING CHAIN: Structured, automatable, scoreable. A/B/C/D grade is a learning
  signal — over time, system learns whether A-grade setups outperform. A=4 not 5
  because FMP dependency and API call budget constraints.
  CURRENT USE: Post-earnings windows, 2-day lookback. Blocked until FMP key set.
- Time: 9 min

---

### options-strategy-advisor

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 3 | A: 1 (F: 4)
- Futures — H: 1 | A: 1 | F: 1
- Status: works as-is
- Notes: FMP optional — Black-Scholes works fully offline. Covers 17 strategies,
  full Greeks, P/L simulation.
  CAPITAL CONSTRAINT: At $500, multi-leg strategies (iron condors, straddles,
  ratio spreads) require margin or capital that doesn't exist. Realistically limited
  to single-leg calls/puts or simple verticals. H=3 is honest. Revisit at $5K+.
  LEARNING CHAIN: Requires human judgment on strategy selection, expiry, Greeks
  interpretation. Cannot be meaningfully automated. A=1.
  CURRENT USE: Education and single-leg option planning on Robinhood positions only.
- Time: 9 min

---

### economic-calendar-fetcher

- Read SKILL.md: [x]
- Ran with realistic input: [x] — CONFIRMED BROKEN on FMP free tier (2026-05-09)
- Stock/options — H: 5 | A: 5 | F: 5
- Futures — H: 5 | A: 5 | F: 5
- Status: broken — FMP economics-calendar endpoint blocked on free tier
- Notes: FMP required — single API call, deterministic output, no human review
  needed before logging. Fetches FOMC, CPI, NFP, GDP, PPI, retail sales. 7-day
  default, 90-day max range.
  FMP ENDPOINT ISSUE (confirmed 2026-05-09): The script uses
  `/stable/economics-calendar`. On free tier (post-Aug 2025 accounts), this endpoint
  silently returns `[]` — no error, no data. FMP changed all v3 endpoints to
  "Legacy Endpoint" (pre-Aug 2025 subscribers only) and restricted the stable
  economics-calendar endpoint to paid plans. The skill is effectively blocked without
  a paid FMP subscription or an alternative data source (e.g., Investing.com scraping,
  FRED API for macro data).
  LEARNING CHAIN SUPERPOWER (when unblocked): Attaching economic event proximity
  to trade outcomes in trader-memory-core enables catalyst correlation over time.
  Tag trades with pre_FOMC, CPI_week, NFP_day. The system learns which catalysts
  move your instruments and by how much. This compounds.
  WORKAROUND: FRED API (free, no key required for basic endpoints) covers FOMC,
  CPI, NFP release dates. Consider a FRED-based replacement script in Phase 2.
  CURRENT USE: Blocked until either (a) FMP paid tier, or (b) FRED-based replacement.
  Ratings remain at 5/5 to reflect the skill's value when the endpoint works —
  revisit if FMP paid tier is not pursued.
- Time: 15 min (including API debugging)

---

### pead-screener

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 4 | A: 3 (F: 4)
- Futures — H: 1 | A: 1 | F: 1
- Status: works as-is (requires FMP API key)
- Notes: FMP required. Free tier sufficient. Two modes: Mode A standalone (earnings
  calendar), Mode B pipeline from earnings-trade-analyzer. State machine:
  MONITORING → SIGNAL_READY → BREAKOUT → EXPIRED.
  LEARNING CHAIN: State transitions are trackable — log every SIGNAL_READY and
  check outcome at 5 weeks. System learns whether PEAD setups have edge in your
  specific conditions. A=3 not 4 because pipeline-dependent on earnings-trade-analyzer,
  only active in post-earnings windows, not continuously schedulable.
  CURRENT USE: Pipeline with earnings-trade-analyzer during post-earnings windows.
  Blocked until FMP key set.
- Time: 9 min

---

### earnings-calendar

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 live run: 3 results (CPRX, CSCO, BABA)
- Stock/options — H: 4 | A: 5 (F: 5)
- Futures — H: 4 | A: 5 (F: 5)
- Status: works as-is (requires FMP API key)
- Notes: FMP required. Free tier sufficient (single calendar call). Two-script
  design: fetch + report. Filters by market cap >$2B, groups by BMO/AMC.
  DISTINCT FROM economic-calendar-fetcher: This is company earnings dates;
  that is macro events (FOMC, CPI, NFP). Both are needed daily — complementary,
  not redundant.
  LEARNING CHAIN: Deterministic, single API call, structured output. Tag futures
  trades with upcoming earnings context (NVDA_earnings_AMC) for NQ gap risk
  correlation. A=5 because it requires no human review before logging.
  FUTURES VALUE: NVDA (~9% QQQ), AAPL, MSFT, AMZN reporting after hours creates
  NQ gap risk next session. H=4 not 5 because human must decide which earnings
  to act on — the calendar is input, not a signal.
  CROSS-REFERENCE RULE: When both a major earnings and a macro event (FOMC, CPI)
  fall in the same week, treat that week as high-risk. Reduce position sizing.
  CURRENT USE: Run Monday AM each week. Blocked until FMP key set.
- Time: 11 min

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

## Tier 2 — Screening and Context

### market-breadth-analyzer

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 live run: 33.1/100 Weakening, 40-60% exposure
- Stock/options — H: 4 | A: 5 | F: 5
- Futures — H: 4 | A: 5 | F: 5
- Status: works as-is
- Notes: No API — fetches free public CSVs from GitHub Pages (tradermonty's
  market breadth data, 2016-present). 6-component score (0-100): Breadth Level
  & Trend (25%), MA Crossover (20%), Peak/Trough Cycle (20%), Bearish Signal (15%),
  Historical Percentile (10%), S&P Divergence (10%). Score history persisted to
  market_breadth_history.json across runs (max 20 entries).
  MOST AUTOMATABLE SKILL IN REPO: Deterministic, no auth, free data, structured
  JSON output, runs in seconds, tracks history. A=5 highest confidence here.
  EQUAL RATING BOTH WORKFLOWS: S&P 500 breadth IS the underlying of ES/NQ futures.
  Narrow breadth = rising reversal risk for index longs. Broad breadth = risk-on
  confirmed. This is a direct futures signal, not indirect.
  LIVE RUN (2026-05-09): 33.1/100 Weakening. 8MA in downtrend. S&P +6% vs breadth
  -0.118 over 60 days = dangerous divergence. Output exactly as predicted. Under 10s.
  DAILY WORKFLOW: First of the three free daily skills. Pipe output to
  ~/trading-research/logs/market_context_YYYY-MM-DD.md.
- Time: 10 min

---

### uptrend-analyzer

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 live run: 31.6/100 Cautious, 1/11 sectors uptrending
- Stock/options — H: 4 | A: 5 | F: 5
- Futures — H: 4 | A: 5 | F: 5
- Status: works as-is
- Notes: No API — free GitHub CSV data (~2,800 US stocks, 11 sectors, Monty's
  Uptrend Ratio Dashboard). 5-component scoring: Market Breadth (30%), Sector
  Participation (25%), Momentum (20%), Sector Rotation (15%), Historical Context (10%).
  Warning overlays: Late Cycle, High Spread, Divergence — each penalizes score.
  RELATIONSHIP TO market-breadth-analyzer: These are the two halves of the daily
  breadth check. breadth-analyzer scores the S&P breadth index (advance/decline).
  This scores individual stock uptrend participation across sectors. Run both.
  SECTOR HEATMAP: Cyclicals leading = risk-on for ES/NQ longs. Defensives leading
  = risk-off. Same signal applies to stock sector rotation plays.
  LEARNING CHAIN: Log composite score and zone daily. Score vs index outcome over
  time is data for the learning loop.
  LIVE RUN (2026-05-09): 31.6/100, Cautious. Only 1/11 sectors uptrending (Comm Services).
  Late Cycle + Divergence warnings active. -7pt penalty applied. Momentum=26 weakest.
  DAILY WORKFLOW: Second of the three free daily skills.
- Time: 9 min

---

### vcp-screener

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09: CONFIRMED BROKEN — batch quote blocked on free tier
- Stock/options — H: 4 | A: 3 (F: 5)
- Futures — H: 1 | A: 1 | F: 1
- Status: BROKEN on free tier — batch quote endpoint blocked
- Notes: FMP required. Free tier sufficient for default top-100 screen. Paid tier
  needed for --full-sp500. Screens for Stage 2 stocks with contracting volatility
  near breakout pivot. Tunable parameters. Strict mode = valid_vcp=True AND
  Pre-breakout/Breakout state only — directly actionable.
  BATCH QUOTE BLOCKED (2026-05-09): stable/quote?symbol=A,B,C returns "Special Endpoint"
  on FMP free tier. Single-symbol quote works. fmp_client.py tries stable batch
  first, falls back to v3 batch (also blocked). 0 quotes returned for 18-stock
  custom universe — screener produces no output. FMP Starter ($29/mo) likely fixes.
  WORKAROUND ANALYSIS: Looping single-symbol calls would need 50-100 calls for a
  meaningful screen — exceeds the 250/day free limit if any other skills run.
  Not viable as a workaround. Need paid tier for this pipeline to function.
  RATING ADJUSTMENT FROM PRIOR VERSION: H:5 → H:4. At $500, a VCP breakout on a
  $150 stock is 3 shares. The setup quality is real but direct trading utility is
  constrained by capital. 4/5 is honest.
  A:4 → A:3. Requires FMP AND human chart validation before any entry. The chart
  read step is structural — it doesn't go away until technical-analyst screenshot
  automation closes the loop in Phase 2-3. After that, F=5 is achievable.
  CAPITAL NOTE: The durable value at $500 is logging structured setups in
  trader-memory-core — building the dataset regardless of position size.
  PIPELINE POSITION: CANSLIM → VCP → technical-analyst → position-sizer
  CURRENT USE: BLOCKED. Unlock condition: FMP Starter tier.
- Time: 10 min

---

### canslim-screener

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 4 | A: 3 (F: 4)
- Futures — H: 1 | A: 1 | F: 1
- Status: works as-is (requires FMP; free tier limits to ~35 candidates)
- Notes: FMP required. Full 7-component CANSLIM: C/A/N/S/L/I/M. Multi-period RS
  (3m/6m/12m weighted). Free tier caps at 35 candidates (--max-candidates 35).
  Paid FMP or FINVIZ Elite needed for full universe.
  DISTINCT FROM vcp-screener: VCP is purely technical. CANSLIM adds fundamental
  dimensions — Earnings (C/A), New Product/High (N), Institutional Sponsorship (I).
  Complementary: CANSLIM filters by fundamentals first, VCP validates technical
  structure on survivors.
  RATING ADJUSTMENT: A:4 → A:3. Weekly cadence, 35-candidate cap on free tier,
  feeds a human review step. Not a 4.
  CEILING NOTE: F=4 not 5 because full-universe screening requires paid FMP or
  FINVIZ Elite. Free tier gives useful but limited sample.
  PIPELINE POSITION: Leads the stock selection pipeline. CANSLIM first, then VCP.
  CURRENT USE: Weekly scan. --max-candidates 35 on free tier. Blocked until FMP.
- Time: 10 min

---

### market-top-detector

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 retest: 47.3/100 Orange (Elevated Risk), --static-basket
- Stock/options — H: 3 | A: 2 (F: 3)
- Futures — H: 3 | A: 2 | F: 3
- Status: PARTIALLY WORKING — degrades gracefully with --static-basket flag; QQQ still blocked
- Notes: FMP required (~33 API calls/execution, free tier sufficient). Also
  requires WebSearch to collect S&P 500 50DMA breadth % and CBOE Put/Call ratio
  as manual CLI inputs — hybrid workflow, not purely automatable.
  6-component composite: O'Neil distribution days, Minervini leading stock
  deterioration, Monty defensive rotation. Higher score = more risk (inverted
  from breadth skills). 2-8 week tactical horizon, targeting 10-20% corrections.
  RETEST RESULT (2026-05-09): --static-basket flag lets it skip ETF batch fetch.
  QQQ still blocked (legacy endpoint). Components that work: Distribution Day Count
  (75=WARNING), Breadth Divergence (64=WARNING), Index Technical (0=healthy), Sentiment (24).
  Components degraded (INSUFFICIENT DATA): Leading Stock Health, Defensive Sector Rotation.
  Composite 47.3 still meaningful — the two working components are the most important.
  Historical closest match: 2018 Q4 Correction. FTD detected 2026-04-08.
  DOWNGRADED from H:4 to H:3: Loses leading stock health and ETF rotation data.
  Still actionable but with reduced confidence. Flag partial function in daily use.
  REGIME BRACKET: Run alongside ftd-detector with `--static-basket` flag.
  FUTURES: Distribution and leading stock breakdown are valid indirect ES/NQ signals.
  CURRENT USE: `python3 ... --static-basket --breadth-200dma X --breadth-50dma Y
  --put-call Z --vix-term contango`. Manual breadth inputs required.
- Time: 12 min

---

### ftd-detector

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 retest: FTD_CONFIRMED S&P 500, quality 95/100
- Stock/options — H: 4 | A: 4 (F: 5)
- Futures — H: 3 | A: 3 | F: 3
- Status: PARTIALLY WORKING — degrades gracefully to S&P 500 only when QQQ blocked
- Notes: FMP only — no WebSearch dependency (cleaner than market-top-detector).
  State machine tracks rally attempts → FTD qualification → post-FTD health
  across runs. Dual-index: S&P 500 + NASDAQ. FTD = Day 4+ of rally attempt with
  volume surge. Scores 0-100 quality with exposure guidance.
  RETEST RESULT (2026-05-09): Degrades gracefully. QQQ WARN printed, NASDAQ state
  NO_SIGNAL. S&P 500 only mode produces: FTD_CONFIRMED, swing low 2026-03-30 ($6343.73),
  quality 95/100, Power Trend YES (3/3), post-FTD dist days=0. Real and actionable.
  Guidance says 75-100% exposure — conflicts with breadth tools (30-60%). Conflict
  is the signal: narrow advance (mega-caps recovered, breadth hasn't). Resolution:
  treat as CAUTIOUS not aggressive. FTD is real but breadth confirmation is absent.
  STILL RATES A=4: Fully automatable even on SPY-only. Run it. The partial output
  is far better than skipping the skill entirely.
  REGIME BRACKET PARTNER: market-top-detector + ftd-detector bracket corrections.
  FUTURES: FTD = new market advance beginning = ES/NQ risk-on mode. Valid indirect
  signal but futures re-entry happens faster than equity FTD confirmation. H=3.
  CURRENT USE: Run no-flag defaults. Watch for FTD state transitions. Log conflicts
  with breadth tools — the gap IS the analysis.
- Time: 11 min

---

### sector-analyst

- Read SKILL.md: [x]
- Ran with realistic input: [x] — 2026-05-09 live run: BALANCED 65/100, Tech overbought, late-cycle
- Stock/options — H: 4 | A: 5 | F: 5
- Futures — H: 4 | A: 5 | F: 5
- Status: works as-is
- Notes: No API — stdlib only, fetches sector_summary.csv + uptrend_ratio_timeseries.csv
  from public GitHub (same data family as market-breadth-analyzer, uptrend-analyzer).
  Ranks 11 sectors by uptrend ratio, cyclical/defensive risk score, overbought/
  oversold flags, market cycle phase estimate. Optional chart image input for
  supplementary visual analysis.
  THIRD PILLAR OF DAILY FREE CHECKS: market-breadth-analyzer + uptrend-analyzer +
  sector-analyst form a complete free breadth picture in under 60 seconds. Together
  they give you S&P breadth health, per-stock participation, and sector rotation —
  everything needed for a credible daily posture without spending a token.
  EQUAL RATING BOTH WORKFLOWS: Cyclical vs defensive balance is the same index-level
  signal for stocks and ES/NQ futures. When defensives lead, risk-off applies to both.
  FEEDS exposure-coach: This is the --sector CLI input. Running all three free skills
  gives exposure-coach a credible input set.
  LIVE RUN (2026-05-09): BALANCED 65/100 risk regime. Only Comm Services uptrending.
  Tech #1 by ratio (37.1%) but in downtrend and overbought. Late-cycle flag: Energy
  - Materials lead both cyclical and defensive. Cycle phase: Mid (low confidence).
  DAILY WORKFLOW: Third of the three free daily skills. No setup required.
- Time: 9 min

---

### theme-detector

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 3 | A: 2 (F: 4)
- Futures — H: 2 | A: 1 | F: 2
- Status: works as-is (limited without FINVIZ Elite)
- Notes: FINVIZ Elite optional (~$40/mo); FMP optional. Public FINVIZ mode works
  without keys but is rate-limited and fragile. 3D scoring: Theme Heat (0-100),
  Lifecycle Maturity (Emerging/Accelerating/Trending/Mature/Exhausting),
  Confidence (Low/Medium/High).
  A=2: Public FINVIZ scraping is not safely schedulable due to rate limits and
  structural changes. If/when FINVIZ Elite is added, upgrade A to 4 and F to 5.
  FUTURES: Themes like "AI capex boom" affect NQ component weights indirectly.
  Too indirect for a primary futures signal. H=2 is honest.
  CURRENT USE: Monthly strategic context or when macro narrative shifts. Not daily.
  Skip until FINVIZ Elite is justified by portfolio size and strategy needs.
- Time: 10 min

---

### institutional-flow-tracker

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 3 | A: 3 | F: 3
- Futures — H: 1 | A: 1 | F: 1
- Status: works as-is (requires FMP; free tier sufficient)
- Notes: FMP required — free tier sufficient. Tracks 13F SEC filings: quarterly
  institutional ownership changes, smart money accumulation/distribution.
  PERMANENT STRUCTURAL CONSTRAINT: 13F data has a hardcoded 45-day SEC reporting
  lag. Newest signal is always at least 45 days stale. This is not a bug or API
  limitation — it is SEC regulation. No upgrade path overcomes this.
  F=3 ceiling reflects this permanent constraint. This skill cannot become a
  reliable real-time signal at any budget level.
  CORRECT USE: Thesis validation (is smart money in the same stocks I'm watching?),
  not trade timing. Run quarterly when new 13F filings drop.
  FUTURES: 13F filings do not report futures positions (equity only). Zero relevance.
  CURRENT USE: Quarterly context check. Not daily or weekly. Low urgency.
- Time: 10 min

---

### parabolic-short-trade-planner

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 3 | A: 4 (F: 5)
- Futures — H: 2 | A: 1 (F: 3)
- Status: works as-is (requires FMP; Alpaca optional — ManualBrokerAdapter fallback)
- Notes: Most production-mature skill in the repo. 3-phase FSM:
  Phase 1 (screen_parabolic.py): 5-factor parabolic scorer, A/B/C/D grades.
  Phase 2 (generate_pre_market_plan.py): pre-market short plans, SSR Rule 201,
  borrow check, blocking vs advisory confirmation gating.
  Phase 3 (monitor_intraday_trigger.py): one-shot 5-min FSM evaluator,
  replay-deterministic. ManualBrokerAdapter makes Phase 2-3 work without Alpaca.
  RATING ADJUSTMENT: H:4 → H:3. Short-selling at $500 on Robinhood requires margin
  approval. The Qullamaggie short setup has specific broker requirements the current
  account may not meet. The FSM study value is real; the direct trading utility is
  constrained.
  PRIMARY AUDIT GOAL: Understand the FSM architecture — this 3-phase pattern
  (daily scan → pre-market plan → intraday monitor) is the template for
  futures-session-monitor in Phase 2. Read scripts/ carefully before Phase 2.
  A=4 reflects that the pipeline itself is automatable even if you're not currently
  executing the trades — it still runs and logs candidates for observation.
  FUTURES: FSM architecture is the value, not the output. H=2, F=3 because the
  patterns learned directly inform Phase 2 build quality.
  CURRENT USE: Read scripts/ directory now. Run it in observation mode (watch_only
  via ManualBrokerAdapter) to understand the workflow without needing short access.
- Time: 13 min

---

### portfolio-manager

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 3 | A: 3 (F: 5)
- Futures — H: 1 | A: 1 (F: 4)
- Status: not currently usable (requires Alpaca MCP Server; Robinhood not supported)
- Notes: Requires Alpaca MCP — not FMP. Uses MCP tools for real-time holdings.
  Robinhood has no API access and is not supported.
  BLOCKED FOR NOW: The skill works — the blocker is account setup. Rating assumes
  the skill is functional because it is; the constraint is external.
  QUICK WIN POTENTIAL: Alpaca paper trading is free. Setup documented in
  references/alpaca-mcp-setup.md. Activating an Alpaca paper account for stock
  tracking could unlock this in Phase 1 without any additional cost.
  F=5 stock: Once Alpaca paper is configured, this activates cleanly.
  INTEGRATION TEMPLATE: The Alpaca MCP pattern here is the direct template for
  tradovate-integration in Phase 2. Read references/alpaca-mcp-setup.md carefully
  before Phase 2 build begins. F=4 futures because the pattern transfers directly.
  PRIMARY AUDIT GOAL: Read alpaca-mcp-setup.md before Phase 2.
  CURRENT USE: Not usable. Set up Alpaca paper account to activate.
- Time: 11 min

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

## Tier 3 — Learning Loop Infrastructure

### edge-pipeline-orchestrator

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 2 | A: 3 (F: 4)
- Futures — H: 1 | A: 1 (F: 2)
- Status: Phase 3 dependency — do not run now
- Notes: Top-level coordinator for the edge research pipeline. Runs 6 stages in
  sequence: auto_detect → hints → concepts → drafts → review-revision loop → export.
  Takes tickets/OHLCV as input, emits validated strategy YAML files as output.
  Supports --dry-run, --review-only, --resume-from, --llm-ideas-file modes.
  PHASE 3 PREREQUISITE: Requires edge-candidate-agent output (market_summary.json +
  anomalies.json) before the pipeline can run. Neither of these exists yet. Running
  this without populated inputs produces empty pipeline output — no value.
  H=2: Human can use the orchestrator to run the pipeline manually. But the equity
  research value comes from what the pipeline produces, not from running the tool.
  At current scale, manually driven skills (canslim, vcp, technical-analyst) cover
  the same ground with more control and less infrastructure overhead.
  A=3 (F=4): Architecture is designed for automation. Once upstream inputs are
  populated (Phase 3+), this becomes the daily automated pipeline runner. High ceiling,
  zero immediate value.
  TRADER-MEMORY-CORE LINK: Indirect and deferred. The pipeline exports strategies
  in its own format (strategy.yaml), not trader-memory-core thesis format. In Phase 3,
  a bridge script that ingests exported strategies into trader-memory-core as IDEA
  theses would close this loop. This bridge does not exist yet.
  FUTURES: Nothing in the pipeline is futures-native. Could extend in Phase 3+ by
  adding futures-specific edge candidates as ticket input. H=1 now.
  CURRENT USE: Read `references/pipeline_flow.md` before Phase 3 to understand data
  contracts. Do not run. Do not enable automated scheduling.
- Time: 12 min

---

### signal-postmortem

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 2 | A: 2 (F: 4)
- Futures — H: 1 | A: 1 (F: 2)
- Status: Phase 3 dependency — do not run now
- Notes: Records outcomes for signals generated by edge-signal-aggregator (not audited yet).
  Classifies each signal as TRUE_POSITIVE, FALSE_POSITIVE, MISSED_OPPORTUNITY, or
  REGIME_MISMATCH. Generates weight-adjustment feedback for edge-signal-aggregator
  and skill improvement backlog entries.
  DISTINCT FROM trader-memory-core: These are PARALLEL systems, not the same thing.
  trader-memory-core: tracks HUMAN-executed trade thesis lifecycle (IDEA → ACTIVE → CLOSED).
  signal-postmortem: tracks AUTOMATED edge-pipeline signal outcomes at 5d and 20d.
  Do not conflate them. In Phase 3, a bridge could link them (edge signal → trade →
  postmortem feeds back). But they serve different masters.
  DEPENDENCY CHAIN: Requires edge-signal-aggregator signals in JSON format as input.
  edge-signal-aggregator is not yet audited. Running this without populated signal
  records produces nothing useful.
  H=2: Human can manually record outcomes for hand-reviewed signals (provide --exit-price
  and --exit-date manually). But without edge-signal-aggregator generating signal IDs
  and structured records, there's nothing to record postmortems against. No meaningful
  standalone use yet.
  A=2 (F=4): Automatable once the upstream signal pipeline is live. Currently has
  nothing to consume. Phase 3 ceiling is high — this is the feedback loop closure
  that makes the whole system self-improving.
  FUTURES: 13F and equity signals are the current inputs. Zero futures coverage.
  CURRENT USE: None. Read `references/outcome-classification.md` and
  `references/feedback-integration.md` in Phase 3 when building the signal pipeline.
- Time: 11 min

---

### dual-axis-skill-reviewer

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 2 | A: 4 (F: 5)
- Futures — H: 1 | A: 1 (F: 2)
- Status: works as-is; automated runs deferred to Phase 3
- Notes: Quality gate for the skill improvement loop. Two axes:
  Auto-axis: deterministic checks — structure (SKILL.md frontmatter), scripts,
  tests, execution safety. Runs without human intervention.
  LLM-axis: qualitative content review — correctness, risk, missing logic,
  maintainability. Human (or Claude) reads generated prompt and returns JSON review.
  Weighted final score (0-100). Below 90 → improvement items required.
  STANDALONE VALUE: Can be run ad-hoc on any single skill for a quality audit.
  `uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py --skill <name> --project-root .`
  This is genuinely useful before Phase 3 — run it on any skill you're about to use
  heavily to catch documentation gaps or script issues.
  PHASE 3 AUTOMATION: This is the scoring engine inside run_skill_improvement_loop.py.
  When Phase 3 is live, it runs daily on a round-robin skill schedule. Do not enable
  automated runs (launchd) until Phase 3.
  H=2: You get a quality score and improvement list. This tells you which skills to
  avoid or extend — useful signal, but indirect trading value.
  A=4 (F=5): Deterministic auto-axis runs without human involvement. In Phase 3,
  daily runs are the quality control backbone for all skills. Highest ceiling of the
  Tier 3 group.
  FUTURES: Scores any skill including futures skills added in Phase 2. But the
  automation value is for the improvement loop, not futures trading directly. H=1.
  CURRENT USE: Run ad-hoc on Tier 1-2 skills before heavy use. Use `--skip-tests`
  for a faster check. Do not schedule automated runs yet.
  QUICK AD-HOC COMMAND:
  `uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py --project-root . --skill technical-analyst --skip-tests --output-dir reports/`
- Time: 10 min

---

### backtest-expert

- Read SKILL.md: [x]
- Ran with realistic input: [ ]
- Stock/options — H: 4 | A: 1 (F: 2)
- Futures — H: 4 | A: 1 (F: 2)
- Status: works as-is — pure knowledge + evaluation script, no dependencies
- Notes: Systematic backtesting methodology reference. Core philosophy: find strategies
  that "break the least", not strategies that "profit the most" on paper. 80% of
  testing time on stress tests (parameter sensitivity, slippage, time robustness,
  sample size). Walk-forward out-of-sample validation required.
  NO API, NO DEPENDENCIES: Entirely offline. The evaluate_backtest.py script takes
  user-provided stats (win rate, avg win/loss, max drawdown, years tested, num
  parameters) and outputs a Deploy/Refine/Abandon verdict with per-dimension scores.
  H=4 BOTH WORKFLOWS: Before any Phase 2 futures skill is deployed live, or before
  any stock strategy is traded systematically, run this methodology to validate it.
  The evaluate_backtest.py script is the first sanity check. Phase 5 before live
  execution — this is the required gate.
  A=1 (F=2): Backtesting methodology is inherently human judgment. The script
  automates the verdict calculation, but the inputs (win rate, drawdown, years) come
  from a human running and interpreting a backtest, not from an automated pipeline.
  The ceiling stays permanently low — strategy deployment decisions require human sign-off.
  FUTURES SPECIFIC: When futures-session-monitor (Phase 2) is candidate for live
  deployment, run it through this methodology before Phase 5. Minimum 100+ trades,
  multiple regime periods, 1.5-2x slippage pessimism. Do not deploy any futures
  strategy to Lucid eval without this step.
  KEY REFERENCE TO READ BEFORE PHASE 5: `references/methodology.md` — stress testing
  methods, sample size requirements, common biases. `references/failed_tests.md` —
  failure patterns to recognize early.
  CURRENT USE: Use whenever validating a strategy before live implementation. Read
  methodology.md now as background for understanding what "edge" means before logging
  trades. The evaluate_backtest.py script is usable today.
- Time: 10 min

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

## Tier 4 — Equity Strategies

### pair-trade-screener

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred, not applicable
- Stock/options — H: 1 | A: 1
- Futures — H: 1 | A: 1
- Status: not relevant at current setup
- Notes: Market-neutral two-leg strategy requires shorting capability (unavailable on
  Robinhood) and sufficient capital for hedged positions ($500 account makes this
  impractical). Solid statistical methodology (correlation, ADF cointegration,
  z-score), but wrong tool for the current execution environment. Revisit when
  account is significantly larger and broker supports shorting. FMP + statsmodels
  required. Not applicable to futures as designed.
- Time: 5 min

---

### value-dividend-screener

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred, wrong priority
- Stock/options — H: 2 | A: 2 (F: 3)
- Futures — H: 1 | A: 1
- Status: works as-is — low operational priority at $500 account
- Notes: Two-stage screening (FINVIZ Elite optional + FMP free tier). Produces
  structured JSON that feeds kanchi-dividend-sop and thesis pipeline. Dividend
  investing (3% yield on $500 = $15/year) is economically irrelevant at current
  capital. Use to build a watchlist for when capital grows. FMP-only mode works on
  free tier (slower). FINVIZ Elite ($40/mo) not in budget — skip --use-finviz flag.
  F rises when capital is large enough to make dividend income meaningful and
  automated scheduling is set up in Phase 3.
- Time: 8 min

---

### dividend-growth-pullback-screener

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred, wrong priority
- Stock/options — H: 2 | A: 2 (F: 3)
- Futures — H: 1 | A: 1
- Status: works as-is — low operational priority at $500 account
- Notes: Targets a different dividend profile than value-dividend-screener — high
  dividend CAGR (12%+) with RSI ≤40 pullback entries. Growth-investor framing
  rather than yield-seeker. Complementary to value-dividend-screener; designed to
  be used as an upstream input to kanchi-dividend-sop. Same FMP free tier
  constraints. Defer alongside value-dividend-screener until capital grows.
- Time: 5 min

---

### kanchi-dividend-sop

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred, upstream screener required first
- Stock/options — H: 2 | A: 2 (F: 3)
- Futures — H: 1 | A: 1
- Status: works as-is — downstream of dividend screeners, same capital constraint
- Notes: Kanchi Japanese dividend methodology adapted for US equities. Takes upstream
  output from value-dividend-screener or dividend-growth-pullback-screener and
  builds a one-page SOP memo with pullback entry signals (build_entry_signals.py)
  and position monitoring cadence. Well-structured 5-step workflow. No independent
  value without running upstream screeners first. Interesting long-term, but deferred
  with the rest of the dividend stack until capital grows. FMP required.
- Time: 5 min

---

### us-market-bubble-detector

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred, run quarterly
- Stock/options — H: 3 | A: 1
- Futures — H: 3 | A: 1
- Status: works as-is — run quarterly or when market feels extended
- Notes: Minsky/Kindleberger bubble framework v2.1 with quantitative scoring.
  WebSearch-based data collection (Put/Call ratio, VIX, margin debt, breadth, IPO
  count) — no API key required. Two-phase workflow: mandatory data collection, then
  qualitative adjustment (max +3 pts, confirmation bias checklist built in). Output
  is a bubble risk score with phase classification (Normal/Elevated/Bubble). Relevant
  to both workflows: stock exposure reduction decisions AND ES/NQ directional bias
  for futures. H=3 because it's a portfolio-level risk signal when run with real
  data. A=1 because qualitative adjustment requires human judgment. Run monthly
  during extended bull markets, quarterly otherwise.
- Time: 8 min

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

## Questionable Skills — Full 15-Minute Audit Required

### macro-regime-detector

- Read SKILL.md: [x]
- Ran with realistic input: [x] — CONFIRMED BROKEN on FMP free tier (2026-05-09)
- Stock/options — H: 4 | A: 3
- Futures — H: 4 | A: 3
- Status: broken — FMP free tier blocks 8 of 9 required ETFs
- Notes: FMP ENDPOINT ISSUE (confirmed via actual run 2026-05-09). The script
  fetches 9 ETFs: RSP, SPY, IWM, HYG, LQD, TLT, SHY, XLY, XLP. Only SPY works
  on free tier. All others return "Premium Query Parameter: Special Endpoint"
  (not a legacy error — these are explicitly gated behind a paid plan, even on the
  stable endpoint). Output: all 6 components score 0, regime = "Concentration
  (confidence: very_low)". Useless output, not a partial degradation.
  Treasury rates endpoint (/stable/treasury-rates) works fine on free tier.
  Ratings reflect genuine skill value when unblocked — cross-asset regime detection
  (1-2 year horizon) is directly relevant to futures index bias (ES/NQ directional
  positioning). A=3 because monthly cadence and structured JSON output make it
  automatable. UNLOCK CONDITION: FMP paid plan (Starter $29/mo or higher).
- Time: 15 min

---

### scenario-analyzer

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — cannot run, Japanese output not usable
- Stock/options — H: 1 | A: 1
- Futures — H: 1 | A: 1
- Status: not usable as-is — Japanese output hardcoded throughout
- Notes: Japanese output is NOT configurable. It is hardcoded in:
  (1) frontmatter description, (2) "When to Use" section, (3) agent prompts
  ("全て日本語で出力"), (4) Important Notes ("全ての分析・出力は日本語で行う").
  There is no language config flag. To use this skill, the SKILL.md would need
  a full rewrite — replace all Japanese instructions with English equivalents.
  The underlying workflow is good: dual-agent analysis (scenario-analyst +
  strategy-reviewer critic pass), 18-month Base/Bull/Bear scenarios, 1st/2nd/3rd
  order sector impacts. No API keys required (WebSearch/WebFetch only). If
  rewritten to English this would rate H:3/A:1 for stocks. Deferred until rewrite.
- Time: 10 min

---

### breakout-trade-planner

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred, requires vcp-screener JSON output first
- Stock/options — H: 4 | A: 2 (F: 3)
- Futures — H: 2 | A: 1
- Status: works as-is — genuinely distinct from vcp-screener, fills a real gap
- Notes: NOT redundant with vcp-screener. These are sequential pipeline stages:
  vcp-screener → breakout-trade-planner → trader-memory-core. The screener
  identifies VCP candidates; this skill converts them into sized, gated,
  ready-to-execute trade plans with:
  - Minervini Gate filtering (valid_vcp, rating_band good/strong/textbook,
    risk_pct_worst ≤8%, breakout volume confirmation)
  - Portfolio heat management (max 6% total open risk, sector concentration limits)
  - Two execution modes: pre_place (stop-limit, pre-breakout) and post_confirm
    (limit, 5-min confirmation after breakout)
  - Alpaca API-compatible order templates
  No API keys required — works entirely on local VCP JSON output.
  H=4 because it converts a screener list into executable plans with position
  sizing — a task that would otherwise require manual calculation per trade.
  Futures H=2 because order templates are equity-specific (stop-limit, limit),
  not futures contracts. The position sizing logic could be adapted.
  Run immediately after any vcp-screener session.
- Time: 10 min

---

### ibd-distribution-day-monitor

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred; QQQ blocked, SPY-only degrades primary use
- Stock/options — H: 2 | A: 2
- Futures — H: 2 | A: 1
- Status: partially broken — QQQ blocked on FMP free tier
- Notes: FMP ENDPOINT ISSUE (confirmed 2026-05-09): QQQ returns "Special Endpoint"
  on free tier. SPY works. The skill defaults to QQQ + SPY, and the TQQQ exposure
  policy is QQQ-weighted. Without QQQ, you only get the S&P 500 side of the signal.
  Compounding factor: current strategy does not include TQQQ or leveraged ETFs, so
  the primary output (TQQQ exposure recommendations) is irrelevant regardless.
  H=2 because SPY-only distribution day counting still signals market deterioration,
  but market-top-detector covers similar ground (NOTE: market-top-detector ALSO
  fetches QQQ + XLK/XLC/XLY sector ETFs — all likely blocked — recheck it).
  Futures H=2 because distribution day count informs ES/NQ short bias during
  distribution phases, but this is already covered by market-breadth-analyzer.
  UNLOCK CONDITION: FMP paid plan (same as macro-regime-detector) OR use SPY-only
  mode and accept partial signal.
- Time: 10 min

---

### strategy-pivot-designer

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — Phase 4 dependency, no inputs exist
- Stock/options — H: 1 | A: 1 (F: 3)
- Futures — H: 1 | A: 1 (F: 2)
- Status: Phase 4 dependency — revisit when backtest iteration history exists
- Notes: Detects stagnation in backtest iteration loops and proposes structurally
  different strategy architectures. Deep in the edge pipeline: requires accumulated
  backtest evaluation history (multiple backtest-expert runs on the same strategy).
  No standalone value without this history. The three pivot techniques (assumption
  inversion, archetype switch, objective reframe) are interesting conceptually.
  F=3 once backtesting is established in Phase 4. Note and move on.
- Time: 5 min

---

### edge-candidate-agent

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — auto-detection deferred (no OHLCV parquet file)
- Stock/options — H: 2 | A: 2 (F: 4)
- Futures — H: 1 | A: 1 (F: 2)
- Status: partially standalone — manual ticket creation usable now, auto-detection Phase 3
- Notes: Has BOTH standalone and pipeline modes. The split depends on what you use:
  AUTO-DETECTION (Phase 3+): auto_detect_candidates.py requires --ohlcv
  /path/to/ohlcv.parquet — this file doesn't exist yet. This generates
  market_summary.json + anomalies.json + tickets/ that feed edge-pipeline-orchestrator.
  MANUAL TICKET CREATION (Day 1): The research_ticket_schema.md can be used to
  manually create structured hypothesis tickets without the parquet file. This is a
  lightweight way to formalize trade hypotheses more rigorously than trader-memory-core
  entries (includes experiment design, invalidation criteria, signal family tagging).
  EXPORT/VALIDATE (Phase 3+): export_candidate.py and validate_candidate.py are
  pipeline integration tools, not standalone.
  H=2 today reflects manual ticket creation value. F=4 once auto-detection is wired
  up in Phase 3 (daily EOD run → anomaly detection → structured tickets → pipeline).
- Time: 10 min

---

### trade-hypothesis-ideator

- Read SKILL.md: [x]
- Ran with realistic input: [ ] — deferred; no trade log data to feed it yet
- Stock/options — H: 2 | A: 2 (F: 4)
- Futures — H: 2 | A: 1 (F: 3)
- Status: works as-is — schema incompatible with trader-memory-core but complementary
- Notes: Schema compatibility answer: NOT directly compatible with trader-memory-core
  thesis schema, but complementary at a higher abstraction level. trader-memory-core
  is trade-level (individual thesis: ticker, direction, entry/exit, stop, target).
  trade-hypothesis-ideator is strategy-level (hypothesis card: mechanism, experiment
  design, kill criteria, entry_family). The workflow connection:
    trader-memory-core (30+ trades) → export trade_log_summary + performance_summary
    → feed to ideator input bundle → ideator generates hypothesis cards → cards
    become strategy drafts → more trades → back to trader-memory-core
  They bridge via aggregated data, not direct record exchange.
  Input bundle requires: trade_log_summary, performance_summary, strategy_context,
  journal_snippets. These don't exist until you have real trade history. Today H=2
  because you can run it with synthetic/hypothetical data to test the output format.
  F=4 once 30+ trader-memory-core entries exist and can be aggregated as input.
  Two-pass workflow (normalization + evidence extraction → critique → ranking) is
  well-designed. Outputs strategy.yaml compatible with edge pipeline.
- Time: 10 min

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
