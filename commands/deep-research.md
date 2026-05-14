---
description: "Comprehensive deep research report on a stock ticker. Covers market context, competitive intelligence, ecosystem analysis, financials, earnings, technicals, ownership, and trade planning. Produces a Quick Glance summary for fast review."
argument-hint: "<TICKER>"
---

# Deep Research — {TICKER}

> **Two-pass architecture:**
> **Pass 1 — Collect:** Run all applicable skills and scripts. Save all outputs.
> **Pass 2 — Synthesize:** Read collected outputs and write the report.
>
> Complete ALL data collection before writing a single line of the report.
> If a skill or script fails, note the gap in one sentence and continue.
> Do not stop for failures — partial data is better than no report.

---

## PASS 1 — DATA COLLECTION

Run every applicable item below. Do not analyze yet.

**Market context (always run):**

- `market-breadth-analyzer` → composite score + 6-component breakdown
- `uptrend-analyzer` → composite score + warning overlays
- `exposure-coach` → exposure ceiling + posture recommendation
- `market-top-detector` → distribution day count + topping probability
- `python3 scripts/fred_calendar.py` → upcoming FOMC, CPI, NFP dates
- `earnings-calendar` → next earnings date for {TICKER} + consensus

**Company intelligence (always run via WebSearch/WebFetch):**

- Search: "{TICKER} competitors market share {current year}"
- Search: "{TICKER} key customers revenue concentration"
- Search: "{TICKER} strategic partners suppliers"
- Search: "{TICKER} CEO CFO management track record"
- Search: "{TICKER} government contracts regulatory relationships" (if applicable)
- Search: "{TICKER} analyst price targets consensus rating"
- Search: "{TICKER} news last 14 days"

**Fundamental data (always run):**

- `us-stock-analysis` via FMP API → financials, valuation, fundamentals
- `technical-analyst` → trend, key levels, momentum, stage (requires chart screenshot)
- `institutional-flow-tracker` → ownership %, QoQ change, smart money

**Conditional — run only if applicable:**

- `earnings-trade-analyzer` → only if {TICKER} reported earnings in last 21 days
- `pead-screener` → only if earnings-trade-analyzer score is B or higher
- `vcp-screener` + `breakout-trade-planner` → only if stock appears Stage 2
- `canslim-screener` → only if revenue growth > 15% YoY
- `theme-detector` → always run; include in report only if confidence is Medium+
- `options-strategy-advisor` → only if Phase 11 produces an actionable trade plan
- `us-market-bubble-detector` → only if market-top-detector shows elevated risk

---

## PASS 2 — SYNTHESIS

Work through each phase in order. Hard length limits are enforced.
Use tables where numbers are the point. Use prose where interpretation is the point.
Never use prose to restate what a table already shows.
If data is unavailable for any item, say so in one sentence and continue.

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK GLANCE — write this LAST, place it FIRST in output
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Written after all phases are complete. Hard limit: 10 lines.
Plain language. No jargon. Specific — vague statements are useless here.
If an answer is "nothing notable" — say that rather than padding.

**What they do:** [One sentence — if it takes two, cut it]
**Why interesting now:** [Specific setup, catalyst, or signal — not generic praise]
**Competitive edge:** [What makes them hard to displace in one sentence]
**Biggest risk:** [The specific thing most likely to break the thesis]
**Key relationship:** [Most important customer, partner, or contract — one line]
**Next catalyst:** [Event + approximate date]
**Verdict:** [Strong Buy / Buy / Watch / Avoid / Short] — [one-sentence reason]
**Chart:** [Stage + one-line technical setup summary]
**Keep in mind:** [1-2 things that would change the verdict — be specific]
**Confidence:** [High / Medium / Low] — [one-line reason for the level]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1 — MARKET CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Synthesize breadth, uptrend, exposure-coach, and market-top outputs.
One table, then 2-3 sentences of interpretation. 150 words maximum.

| Signal                  | Reading | Implication |
|-------------------------|---------|-------------|
| Breadth composite       |         |             |
| Uptrend ratio           |         |             |
| Exposure ceiling        |         |             |
| Distribution days       |         |             |
| Market posture          |         |             |

Key question answered in 2-3 sentences: Does the macro environment support
or undermine the individual thesis for {TICKER} right now?

Upcoming macro events affecting {TICKER} or its sector (within 2 weeks):
[From fred_calendar.py and earnings-calendar — one bullet per relevant event.
Skip events that don't apply to this name or sector.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2 — BUSINESS & PRODUCTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**2a. Business model** (100 words max)
What {TICKER} does and how it makes money. Be specific — name the actual
product lines, pricing model (subscription/license/usage/hardware), and
end markets served. One sentence on why customers buy from them.

**2b. Products & technology** (150 words max)
Key products by name and approximate revenue contribution.
What makes the product technically hard to replicate?
R&D spend as % of revenue and trend.
Product roadmap: what is launching in the next 12-24 months?
Patent or regulatory moat if applicable.
Is the company early, mid, or late in its product cycle?

**2c. TAM & growth runway**
Total addressable market estimate with source and date.
Current penetration %. Is the TAM growing, stable, or contracting?
How many years of meaningful growth are plausible at current trajectory?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 — COMPETITIVE INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This section answers: Where does {TICKER} stand in its market?
How defensible is that position? Who is trying to take it away?

**3a. Market position**
{TICKER}'s estimated market share (source and date if available).
Is it the market leader, a strong #2, a niche specialist, or a challenger?
Has share been growing, stable, or declining over the last 3 years?

**3b. Competitor comparison**
List the 3-5 most relevant direct competitors by name.

| Company     | Ticker | Market Share | Revenue | Gross Margin | Key Advantage vs {TICKER} |
|-------------|--------|-------------|---------|-------------|--------------------------|
| {TICKER}    |        |             |         |             | (this is the baseline)   |
| Competitor1 |        |             |         |             |                          |
| Competitor2 |        |             |         |             |                          |
| Competitor3 |        |             |         |             |                          |

Below the table (one paragraph max):
Where does {TICKER} win deals? Where does it lose? What would cause a
customer to switch to a competitor? Is the competitive gap widening or narrowing?

**3c. Moat assessment**
Classify the moat type: switching costs / network effects / cost advantage /
intangible assets (patents, brand, licenses) / efficient scale / none.
Is the moat strengthening, stable, or eroding? Specific evidence required —
not a generic claim. Name what actually protects this company.

**3d. Primary competitive threat**
The single most credible threat to {TICKER}'s position in the next 3 years.
Could be: a well-funded competitor, technology disruption, commoditization,
regulatory change, or customer vertical integration. Name it specifically.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 4 — ECOSYSTEM: CUSTOMERS, PARTNERS & SUPPLIERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This section answers: Who does {TICKER} depend on, and who depends on {TICKER}?
These relationships are where thesis risk and thesis confirmation often live.

**4a. Key customers**
Name top customers if disclosed. Estimate revenue concentration.

| Customer  | Est. % Revenue | Relationship Type      | Risk if Lost |
|-----------|---------------|------------------------|-------------|
|           |               |                        |             |

Customer concentration risk: If the top customer left, what % of revenue
disappears? Is there a >10% customer disclosed in SEC filings (10-K)?
Is the customer base diversifying or concentrating over time?

**4b. Strategic partners**
List partners that materially affect {TICKER}'s business — technology,
distribution, co-development, certification, or licensing agreements.

| Partner   | Partnership Type    | What It Provides     | Risk if Ended |
|-----------|---------------------|----------------------|--------------|
|           |                     |                      |              |

**4c. Key suppliers & dependencies**
Who supplies critical inputs? Are there single-source dependencies?
What is the supply chain disruption scenario for {TICKER}?
Any supply chain changes noted in recent earnings calls or SEC filings?

**4d. Government & regulatory relationships** (if applicable — skip if not)
Active government contracts: name, size, and renewal timeline if known.
Policy tailwinds: DPA, IRA, CHIPS Act, grid modernization programs, etc.
Policy risks: pending rule changes or enforcement that could hurt.
If government is a key customer or funder, what is the dependency level?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 5 — MANAGEMENT & GOVERNANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

150 words maximum. Direct assessment — not a bio summary.

**5a. Leadership**
CEO and CFO names and tenure. Prior track record — what did they build or fix?
Founder-led or professional managers? Insider ownership %: skin in the game?

**5b. Capital allocation track record**
Buybacks: buying at good prices or just offsetting dilution?
M&A: has acquisition history created or destroyed value?
Debt: leverage increasing, decreasing, or stable?
Dividend history if applicable.

**5c. One-sentence verdict on management:**
Management earns trust / warrants skepticism / is unproven — and the
specific reason. Compensation structure aligned with shareholders or not?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 6 — FINANCIAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**6a. Financial health**

| Metric             | TTM/Latest | 1yr Ago | 2yr Ago | Trend | vs Sector |
|--------------------|-----------|---------|---------|-------|-----------|
| Revenue growth YoY |           |         |         |       |           |
| Gross margin       |           |         |         |       |           |
| Operating margin   |           |         |         |       |           |
| FCF margin         |           |         |         |       |           |
| D/E ratio          |           |         |         |       |           |
| Current ratio      |           |         |         |       |           |
| ROE / ROIC         |           |         |         |       |           |

**6b. Earnings quality**
Operating cash flow vs net income divergence.
Revenue recognition concerns, restatements, or audit flags?
One sentence: are the reported earnings real?

**6c. Valuation**

| Metric     | Current | 5yr Low | 5yr High | Sector Median | Cheap/Fair/Rich |
|------------|---------|---------|----------|---------------|-----------------|
| P/E        |         |         |          |               |                 |
| Fwd P/E    |         |         |          |               |                 |
| PEG        |         |         |          |               |                 |
| P/S        |         |         |          |               |                 |
| EV/EBITDA  |         |         |          |               |                 |

DCF sanity check (skip if FCF negative or pre-revenue):
At the current price, what growth rate is the market pricing in?
Is that achievable? One paragraph only.

**6d. One red flag / one green flag**
Specific evidence only. Vague flags are unacceptable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 7 — EARNINGS & CATALYSTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**7a. Earnings track record**

| Quarter | EPS Est | EPS Act | Surprise % | Rev Surprise % | Day-After Move |
|---------|---------|---------|-----------|----------------|----------------|
Last 6 quarters. One sentence trend: consistent beater, inconsistent, or misser?

**7b. Analyst consensus**
Number of analysts. Rating split (Buy/Hold/Sell count).
Average price target + range (low to high target spread).
Any recent upgrades or downgrades? Wide target dispersion signals uncertainty.

**7c. Next earnings**
Date, consensus EPS, implied options move if available.
Does this fall within a potential trade window? Yes/No + implication.

**7d. Catalyst timeline**
Events that could move {TICKER} more than 3% — specific and dated.
| Date (approx) | Catalyst                     | Bull Impact | Bear Impact |
Include: product launches, contract announcements, regulatory decisions,
government funding, conference presentations, partner announcements,
index events, macro events from fred_calendar.py relevant to this sector.

**7e. Recent news** (14-day window, from market-news-analyst or WebSearch)
Most important single development and whether it changes the thesis.
"No material news" if nothing significant — do not pad with generic commentary.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 8 — TECHNICAL SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**8a. Stage and trend**
Minervini stage (1/2/3/4) and one-sentence implication for trade eligibility.
Primary trend: direction, duration, MA relationship (price vs 50/150/200).

**8b. Key levels**

| Level Type    | Price | Notes                |
|---------------|-------|----------------------|
| Resistance 3  |       |                      |
| Resistance 2  |       |                      |
| Resistance 1  |       |                      |
| Current price |       |                      |
| Support 1     |       |                      |
| Support 2     |       |                      |
| Support 3     |       |                      |

**8c. Pattern**
Active or forming chart pattern — name it, one sentence, pivot level.
If no pattern: say so.

**8d. Momentum**

| Indicator    | Value | Signal       |
|--------------|-------|--------------|
| RSI (14)     |       |              |
| MACD         |       |              |
| Volume trend |       | vs 50d avg   |
| RS vs SPX    |       | 1m / 3m / 6m |

One sentence: momentum confirming or diverging from price?

**8e. Screener results**
VCP-screener: [score, state, pivot] if run.
Breakout-trade-planner: [plan summary] if run.
CANSLIM: [composite score, key components] if run.
Skip sections where screeners were not run.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 9 — OWNERSHIP & FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**9a. Institutional snapshot**

| Metric                        | Value | QoQ Change |
|-------------------------------|-------|------------|
| Total institutional ownership |       |            |
| Number of holders             |       |            |
| Net accumulation/distribution |       |            |

**9b. Smart money**
Superinvestor moves last 2 quarters. "None notable" if none.

**9c. Insider activity**
Net sentiment (buying/selling/neutral) last 6 months.
Flag cluster buys. Flag large sales and whether they follow a 10b5-1 plan.

**9d. Short interest**
% of float + days to cover + trend.
One sentence: tailwind (squeeze potential), headwind, or neutral?

**9e. Options market structure** (skip if options are illiquid)
Put/call ratio: fear or complacency?
Unusual activity in last 5 sessions (large flows, sweeps, unusual strikes)?
IV rank: rich or cheap for options strategies?
Note flows that confirm or contradict the fundamental thesis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 10 — RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Top 5 risks ranked by severity × probability:**

| Risk                   | Severity | Probability | Specific Evidence            |
|------------------------|----------|-------------|------------------------------|
|                        | H/M/L    | H/M/L       |                              |

Vague risks not permitted. "Competition" is not a risk.
"Customer X reducing orders 20% would cut revenue by Y%" is a risk.

**Downside scenarios:**

- Re-rates to sector median multiples: implied downside ___%
- Growth decelerates 50%: implied fair value $___
- Maximum drawdown in last 12 months: ___%
- Customer concentration: if top customer leaves, revenue impact: ___%

**What the market might be wrong about (bull):**
One specific mispricing or overlooked factor — not a generic statement.

**What the bull case might be wrong about:**
The most common bull assumption most likely to prove incorrect.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 11 — TRADE PLAN (only if actionable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If verdict is Avoid or chart stage is 3 or 4, write:
"No trade plan — verdict is [X]. Revisit if [specific condition changes]."
and stop here.

Run position-sizer with the levels below. Default: 1% portfolio risk.
Specify which account (Portfolio A taxable / Portfolio B IRA).
For IRA positions: confirm the structure is IRA-eligible before including.

**Structure:**

| Parameter        | Stock | Options (if applicable)          |
|------------------|-------|----------------------------------|
| Entry level      |       |                                  |
| Stop loss        |       |                                  |
| Target 1 (1R)    |       |                                  |
| Target 2 (2R)    |       |                                  |
| Target 3 (3R)    |       |                                  |
| Position size    |       |                                  |
| Max loss $       |       |                                  |
| IRA-eligible?    | N/A   | Yes / No — [structure name]      |

Stop rationale: one sentence on why this level was chosen.

Options: if options-strategy-advisor was run — IV rank, recommended structure,
key Greeks at entry, and IRA eligibility. Otherwise skip.

**Thesis invalidation (specific, measurable, not "if stock falls"):**
1.
2.
3.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCORECARD — complete after all phases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Dimension             | Score (1-10) | Key Signal (one phrase)        |
|-----------------------|-------------|-------------------------------|
| Market context        |             |                               |
| Business quality      |             |                               |
| Competitive position  |             |                               |
| Ecosystem health      |             |                               |
| Management quality    |             |                               |
| Valuation             |             |                               |
| Earnings momentum     |             |                               |
| Technical setup       |             |                               |
| Ownership & flow      |             |                               |
| Risk profile          |             |                               |
| **Composite**         |             |                               |

Scoring: 9-10 Exceptional | 7-8 Good | 5-6 Mixed | 3-4 Weak | 1-2 Avoid

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASES & CONVICTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Bull case (probability: __%):**
Three specific claims — name actual catalysts, contracts, or market dynamics.
Not "strong brand." Falsifiable claims only.

**Bear case (probability: __%):**
Three specific reasons this fails.

**Base case (probability: __%):**
Most likely outcome and expected return range over 6-12 months.

Probabilities must sum to 100%.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA SOURCES & GAPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

List every skill, script, and web search used.
Note failures, rate limits, unavailable data, and skipped sections.

---
*Research and educational purposes only. Not financial advice.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAVE & VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Check if reports/research/{TICKER}.md already exists.
   - If yes: archive to reports/archives/{TICKER}_{old-date}.md
     using the date from the OLD report's "Generated" line, not today.
   - Write new report to reports/research/{TICKER}.md.
   - If no: write directly.

2. Append one line to reports/logs/research_log.md:
   `{date} | {TICKER} | Verdict: {verdict} | Composite: {score}/10 | Earnings: {date}`

3. Confirm: "Report saved to reports/research/{TICKER}.md"
