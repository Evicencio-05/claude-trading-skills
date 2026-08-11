---
description: "Rank options flow screener rows for tailing: extract screenshot, score whale prints, enrich with market context and research, lite structure for primary pick."
argument-hint: "[bias: long|short|either]"
---

# /options-flow-tail

Paste an options flow screener screenshot or row text. The agent acts as a veteran flow analyst: extract rows, score whale prints, enrich with same-day project artifacts, and recommend **one primary tail** with a lite executable structure.

**Co-pilot only:** rank and recommend — no MCP orders. Aligns with [cost-discipline.md](../project-docs/reference/cost-discipline.md) (no new data subscriptions).

**Artifact paths:** [scripts/report_paths.py](../scripts/report_paths.py) — output under `reports/flow/`.

---

## Invoke

```
/options-flow-tail
/options-flow-tail bias: long
```

Or: "options flow tail", "which flow would you tail", paste screener screenshot.

Paste screenshot(s) or pasted row text in the same message.

---

## PHASE 0 — INPUT AND OVERRIDES

Parse optional chat overrides (defaults in parentheses):

| Override | Default | Effect |
|----------|---------|--------|
| `bias: long` / `short` / `either` | `long` if all rows are calls; `either` if mixed | Filter wrong-side prints |
| `account: ira` / `agentic` / `taxable` | `agentic` | IRA flags ineligible option structures |
| `min_premium: N` | $250000 | Ignore rows below premium floor |
| `skip posture` | off | Ignore market_context gate |
| `single-name only` | off | Penalize ETF/index flow (USO, SPY, QQQ) |

Load scoring rubric before Phase 3:

`.cursor/skills/options-flow-tail/references/tail_rubric.md`

---

## PHASE 1 — MARKET GATE (reuse-first)

Load same-day market context **without** auto-running `pre_market.py`:

1. Glob `reports/logs/market_context_YYYY-MM-DD.json` (today ET preferred).
2. If found, read: `recommendation`, `exposure_ceiling_pct`, `bias`, `participation`, `confidence`.
3. If missing, note **posture unknown** and continue.

**Gate rules** (unless user said `skip posture`):

| Condition | Default action |
|-----------|----------------|
| `recommendation` = `CASH_PRIORITY` | Skew verdict to **NO TAIL** unless user overrides |
| `exposure_ceiling_pct` < 40 | Require High confidence for primary tail |
| `recommendation` = `NEW_ENTRY_ALLOWED` | Normal scoring |

Record `market_context_path` for the JSON sidecar (or `null`).

---

## PHASE 2 — EXTRACT (vision)

For each screener row, normalize fields. Mark unreadable values `unknown`.

| Field | Notes |
|-------|--------|
| `timestamp` | Date/time of print |
| `ticker` | Underlying symbol |
| `contract` | e.g. `392.5 C 06/18/2026` |
| `option_type` | `call` or `put` |
| `strike` | Numeric |
| `expiry` | YYYY-MM-DD |
| `dte` | Days to expiration |
| `spot` | Stock price at trade |
| `pct_otm` | % OTM (+ = OTM for calls) |
| `premium` | Total $ premium |
| `volume` | Session volume |
| `open_interest` | OI |
| `delta_oi` | Change in OI |
| `delta_oi_pct` | % change OI |
| `contract_bull_pct` | Contract Bull/Bear bar |
| `chain_sentiment` | Chain Bull/Bear (e.g. BULL 59%, MID) |
| `ask_ratio_pct` | Contract ratio ASK % |
| `iv` | Implied volatility if shown |
| `chg_pct` / `day_pct` | Option price change |
| `earnings_days` | Days to earnings if shown |
| `pct_tot` | % of total flow |

Show extracted table to user before scoring. If a row is ambiguous, note it — do not invent strike/expiry.

---

## PHASE 3 — SCORE

Apply [tail_rubric.md](../.cursor/skills/options-flow-tail/references/tail_rubric.md):

1. **Hard disqualifiers** — mark `DISQUALIFIED` with reason (still list in pass section).
2. **Weighted score** 0–100 for survivors.
3. Sort descending. Tie-break: higher premium, then higher ask_ratio_pct, then higher opening evidence.

Respect `min_premium` override from Phase 0.

---

## PHASE 4 — ENRICH TOP 2

For the top two scored survivors only (reuse-first):

### 4a. Research cross-check

Glob latest `reports/research/{TICKER}_*.md`. Note:

- Exists / missing
- Report date and staleness (>14 days = stale)
- Actionable verdict if stated in report

Apply rubric boosts/penalties.

### 4b. Entry watchlist

Glob latest `reports/logs/entry_watchlist_YYYY-MM-DD.json` (today preferred). If ticker in tiers:

| Tier | Score adjustment |
|------|------------------|
| A | +10 |
| B | +5 |
| C | 0 |
| D | −5 |

If missing, note gap — do not auto-run `build_entry_watchlist.py`.

### 4c. Sector alignment

From `market_context` sector summary or latest `reports/market/sector/sector_rotation_YYYY-MM-DD.json`:

- If ticker sector is in top-3 rotation and bias aligns → +5
- If sector defensive / lagging while tailing aggressive OTM call → −5

### 4d. Earnings (primary pick only)

Run `earnings-calendar` for primary ticker if `FMP_API_KEY` available:

```bash
python3 earnings-calendar/scripts/fetch_earnings_fmp.py --from YYYY-MM-DD --to YYYY-MM-DD
```

If no key or failure: note gap, use screener `earnings_days` if visible.

**Flag prominently** if earnings falls inside contract DTE.

Recompute primary score after boosts/penalties.

---

## PHASE 5 — LITE STRUCTURE (primary pick only)

Condensed tail plan — **not** a full [options-strategy-planner.md](options-strategy-planner.md) run.

Provide:

1. **Thesis (one sentence)** — what institutional flow implies (sector/theme/direction).
2. **Why not copy exact contract** — DTE lottery, OTM %, IV chase, spread risk.
3. **Suggested structure** — apply [intraday-options.md](intraday-options.md) selection logic:
   - IV rank > 50 (or premium rich): favor **debit spread** over naked long.
   - IV rank < 30: favor **long call/put**.
   - Earnings inside DTE: avoid buying premium unless explicit event play — say **skip or spread only**.
   - Prefer 2–6 week DTE and 0.40–0.55 delta for directional tail (not whale's 6 DTE OTM).
4. **Strike / expiry guidance** — anchor to spot, not whale strike; state approximate delta target.
5. **Invalidation** — stock price level or thesis break.
6. **Confidence** — High / Medium / Low (factor in market gate, research, earnings).
7. **IRA note** — if `account: ira`, flag strategies that fail IRA eligibility (naked short options, etc.).

Use `options-strategy-advisor` / Black-Scholes for Greeks guidance when FMP or user inputs allow; otherwise qualitative.

---

## PHASE 6 — VERDICT

Deliver exactly:

| Slot | Rule |
|------|------|
| **Primary tail** | Highest adjusted score; must pass market gate or user override |
| **Runner-up** | Second highest eligible row |
| **Pass list** | All others + disqualified rows with one-line reason each |

**NO TAIL** is always valid — use when gate blocks, nothing passes disqualifiers, or all scores < 60.

State clearly: *Tail the thesis, not the contract.*

---

## PHASE 7 — SAVE

Write both artifacts to `reports/flow/` (create dir if needed):

| File | Path |
|------|------|
| Markdown report | `reports/flow/flow_tail_{YYYY-MM-DD}.md` |
| JSON sidecar | `reports/flow/flow_tail_{YYYY-MM-DD}.json` |

Use today's date ET unless screener timestamp indicates a prior session (then use screener date in filename suffix note in report header).

### JSON schema

```json
{
  "schema_version": 1,
  "generated_at": "ISO8601",
  "market_context_path": "reports/logs/market_context_YYYY-MM-DD.json",
  "bias": "long",
  "account": "agentic",
  "min_premium": 500000,
  "posture_gate": "NEW_ENTRY_ALLOWED",
  "rows": [
    {
      "ticker": "ALAB",
      "contract": "392.5C 2026-06-18",
      "premium": 2000000,
      "tail_score": 82,
      "adjusted_score": 87,
      "verdict": "primary"
    }
  ],
  "primary": {
    "ticker": "ALAB",
    "confidence": "medium",
    "structure": "bull_call_spread",
    "invalidation": "Close below $X"
  },
  "runner_up": { "ticker": "LRCX", "tail_score": 76 },
  "pass": [{ "ticker": "USO", "reason": "ETF macro flow" }],
  "handoffs": ["options-strategy-planner", "intraday-options"]
}
```

---

## PHASE 8 — HANDOFFS (document only)

List optional follow-on commands — **do not auto-run**:

| Next step | When |
|-----------|------|
| `/options-strategy-planner {TICKER}` | Full structure comparison for primary pick |
| `/intraday-options {TICKER} {CAPITAL}` | Same-day / next-day execution plan |
| `/deep-research {TICKER}` | No research report or stale >14d |
| `/agentic-copilot-trade {TICKER}` | Stock tail on Portfolio C (not options MCP) |

---

## OUTPUT FORMAT (markdown report)

```markdown
# Options Flow Tail Review — {YYYY-MM-DD}

**Bias:** {long|short|either} | **Account:** {account} | **Posture:** {gate summary}
**Rows reviewed:** {N} | **Market context:** {path or not available}

## Ranking

| Rank | Ticker | Contract | Prem | Score | Verdict |
|------|--------|----------|------|-------|---------|
| 1 | ... | ... | ... | ... | **Primary tail** |
| 2 | ... | ... | ... | ... | Runner-up |

## Primary Pick — {TICKER}

### Why tail
...

### Why not copy exact contract
...

### Lite structure
- **Structure:** ...
- **Strike / Expiry guidance:** ...
- **Invalidation:** ...
- **Confidence:** High / Medium / Low
- **IRA:** eligible / flagged

## Runner-up — {TICKER}
One paragraph.

## Pass list
- **{TICKER}** — reason

## Cross-checks

| Ticker | Research | Watchlist tier | Sector | Earnings risk |
|--------|----------|----------------|--------|---------------|
| ... | ... | ... | ... | ... |

## Handoffs
- `/options-strategy-planner {TICKER}` — ...
- ...

⚠️ *Flow tailing is speculative. Tail thesis, not contract. Not financial advice.*
```

---

## Rules

- Do **not** subscribe to or fetch Unusual Whales / QuantData APIs — user supplies screener data.
- Do **not** auto-run `pre_market.py` or `build_entry_watchlist.py` — reuse artifacts only.
- Do **not** place MCP orders.
- FMP calls limited to earnings check on primary pick only.
- It is always acceptable to recommend **NO TAIL**.
