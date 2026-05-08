# Phase 2 — Futures Skills

**Duration:** 6 weeks (weeks 5–10)
**Goal:** Build the missing futures-specific skills. Use existing skill patterns as templates.

---

## Prerequisites

You should have completed Phase 1's exit criteria. Specifically:
- You know which existing skills work for you (from `skills_audit.md`)
- You have at least 10 trades in `trader-memory-core`
- You have at least one Lucid evaluation account (active or breached — both are useful)
- You have hands-on familiarity with the Tradovate platform

If any of these are not true, **go back and finish Phase 1**. Building futures skills without this context produces solutions to imagined problems.

---

## What You're Building

Six new skills, in this order. Each follows the SKILL.md pattern of the existing repo. Each is built using existing skills as templates.

| # | Skill | Week | Template to study |
|---|---|---|---|
| 1 | `lucid-rules-engine` | 5 | `position-sizer` (offline calculation pattern) |
| 2 | `futures-position-sizer` | 5 | `position-sizer` (extend with futures math) |
| 3 | `tradovate-integration` | 6–7 | `portfolio-manager` (Alpaca MCP pattern) |
| 4 | `futures-pre-market-scan` | 8 | `parabolic-short-trade-planner` Phase 1 + `technical-analyst` |
| 5 | `futures-session-monitor` | 9 | `parabolic-short-trade-planner` Phase 3 (intraday FSM) |
| 6 | `/futures-setup` command | 10 | `/intraday-options` command pattern |

**Build order matters.** The rules engine comes first because everything downstream depends on respecting it. The integration comes before the scanners because the scanners need real data.

---

## Skill 1: `lucid-rules-engine` (Week 5)

The most important skill in this phase. It encodes Lucid's constraints as hard-coded Python functions that the rest of the system queries before any execution decision.

### Core principle

Rules live in `skills/lucid-rules-engine/scripts/rules.py`. The agent **reads** this module. The agent **never writes** to it. User-only modifications. Encode this with a file permission check at runtime — if the file's mtime changed since startup, raise a hard error.

### Functions to implement

```python
# Account state
def get_account_state(account_id: str) -> LucidAccountState
def get_qualifying_days(account_id: str, cycle_start: date) -> int
def get_eod_drawdown_buffer(account_id: str) -> Decimal
def get_daily_loss_buffer(account_id: str, account_type: Literal["pro", "flex", "direct"]) -> Decimal | None  # None for Flex funded

# Pre-trade checks (return PASS/BLOCK with reason)
def can_open_position(account_id: str, contract: str, size: int, est_max_loss: Decimal) -> RuleCheckResult
def time_until_auto_flatten(now_et: datetime) -> timedelta
def is_within_trading_hours(now_et: datetime) -> bool  # Sun 6PM ET to Fri 4:45PM ET, excluding daily 4:45PM-6PM break

# Cycle eligibility
def qualifying_days_remaining_for_payout(account_id: str) -> int
def days_until_cycle_reset(account_id: str) -> int

# LucidFlex-specific minimum daily profit thresholds
MIN_QUALIFYING_PROFIT = {
    25_000: Decimal("100"),
    50_000: Decimal("150"),
    100_000: Decimal("200"),
    150_000: Decimal("250"),
}
```

### What goes in this skill

- `SKILL.md` describing when to use it (every pre-trade decision, every status check)
- `references/lucid-rules-flex.md`, `references/lucid-rules-pro.md`, `references/lucid-rules-direct.md` — the full rule text for each product
- `scripts/rules.py` — the implementation
- `scripts/account_state.py` — state persistence (SQLite)
- `tests/test_rules.py` — unit tests covering every rule and every edge case (test-first mandatory per repo conventions)

### Test coverage requirements

For every rule, test:
- The pass case
- The block case
- The boundary (1 dollar from breach, 1 minute from auto-flatten, etc.)
- Cycle reset behavior
- Multiple accounts (per-account state isolation)

### Critical edge cases

- **EOD drawdown trail:** Updates only at session close, never intraday. Make this explicit. Don't mistakenly use intraday equity for the trail calculation.
- **Auto-flatten time:** 4:45 PM ET. Account for daylight saving — Lucid is on US Eastern, agent must respect the same.
- **Holiday hours:** CME has reduced sessions on holidays. Hard-code the calendar or pull from CME API.
- **Lucid Flex qualifying days:** Min profit must be **net** (after commissions), not gross.

---

## Skill 2: `futures-position-sizer` (Week 5)

A wrapper around the existing `position-sizer` that adds futures contract math and Lucid account constraints.

### What it adds

```python
CONTRACT_VALUES = {
    "ES":  {"point_value": 50,  "tick_size": 0.25, "tick_value": 12.50},  # E-mini S&P
    "MES": {"point_value": 5,   "tick_size": 0.25, "tick_value": 1.25},   # Micro E-mini S&P
    "NQ":  {"point_value": 20,  "tick_size": 0.25, "tick_value": 5.00},   # E-mini Nasdaq
    "MNQ": {"point_value": 2,   "tick_size": 0.25, "tick_value": 0.50},   # Micro E-mini Nasdaq
    "YM":  {"point_value": 5,   "tick_size": 1.00, "tick_value": 5.00},   # E-mini Dow
    "MYM": {"point_value": 0.5, "tick_size": 1.00, "tick_value": 0.50},   # Micro E-mini Dow
    "RTY": {"point_value": 50,  "tick_size": 0.10, "tick_value": 5.00},   # E-mini Russell 2000
    "M2K": {"point_value": 5,   "tick_size": 0.10, "tick_value": 0.50},   # Micro E-mini Russell 2000
    # Add CL (Crude), GC (Gold), etc. as you start trading them
}

def size_futures_position(
    contract: str,
    entry: Decimal,
    stop: Decimal,
    account_id: str,
    risk_pct: float = 0.5,  # Lower default than equity (futures are levered)
) -> PositionSizeResult
```

### Key behavior

- Calls `lucid-rules-engine.can_open_position()` first. If BLOCK, return zero contracts with the block reason.
- Calculates risk per contract = `abs(entry - stop) * point_value`
- Caps position at the largest size that keeps `total_risk <= account_size * risk_pct / 100`
- For micro contracts, allow fractional risk percentages (you can risk 0.25% on MES)
- For full-size contracts on a small account, the answer is often "0 contracts — too risky." Return 0 honestly, don't round up.

### Default risk per trade for futures

**0.5% per trade** (vs. 1% for equity). Futures leverage means the same dollar risk concentrates in fewer contracts, and a single 1% loss on a Lucid account meaningfully erodes the EOD drawdown buffer. Make this configurable but default conservative.

---

## Skill 3: `tradovate-integration` (Weeks 6–7)

Mirror the `portfolio-manager` Alpaca MCP pattern. Tradovate has a REST API and a WebSocket API.

### Phase 2 scope: read-only

In Phase 2, **only implement read operations.** No order placement until Phase 4 (sim) and Phase 5 (live). This is a discipline boundary — even if order placement is technically easy, building it before you need it invites accidents.

### Functions to implement (read-only)

```python
async def get_account_balance(account_id: str) -> AccountBalance
async def get_open_positions(account_id: str) -> list[Position]
async def get_orders(account_id: str, status: Literal["working", "filled", "cancelled"]) -> list[Order]
async def get_fills(account_id: str, since: datetime) -> list[Fill]
async def stream_quotes(symbols: list[str]) -> AsyncIterator[Quote]  # WebSocket
async def stream_bars(symbol: str, timeframe: Literal["1m", "5m", "15m"]) -> AsyncIterator[Bar]
```

### Auth pattern

- Tradovate uses OAuth2. Store refresh token in `.env` (never commit).
- Implement automatic token refresh on 401 responses.
- Store the `cid` (client ID) and `sec` (secret) as env vars: `TRADOVATE_CID`, `TRADOVATE_SECRET`, `TRADOVATE_USERNAME`, `TRADOVATE_PASSWORD`.

### Demo vs. live endpoint

Tradovate has separate API hosts for demo and live. Make this configurable:
```bash
export TRADOVATE_ENV=demo  # or "live"
```
The wrapper resolves this to the correct base URL. **Default to demo.** Live is an explicit opt-in via env var change.

### Skill structure

```
skills/tradovate-integration/
├── SKILL.md
├── references/
│   ├── tradovate-api-overview.md
│   ├── tradovate-auth-flow.md
│   └── tradovate-rate-limits.md
├── scripts/
│   ├── client.py            # Auth, request signing, retries
│   ├── account.py           # Balance, positions, orders
│   ├── market_data.py       # Quotes, bars (WebSocket)
│   └── check_connection.py  # Smoke test (mirror check_alpaca_connection.py)
└── tests/
    ├── test_client.py
    └── fixtures/            # Recorded API responses for offline testing
```

### Verification step

Before declaring this skill done: run `check_connection.py` against your demo account. Expected output: account balance, current positions (likely empty), 5 most recent quotes for ES.

---

## Skill 4: `futures-pre-market-scan` (Week 8)

Daily ES/NQ pre-market briefing. Run this every morning before 9:30 AM ET.

### What it produces

A markdown report saved to `~/trading-research/intraday/futures_premarket_YYYY-MM-DD.md` with:

- Overnight session summary (Globex high/low, range, volume)
- Gap analysis vs. previous RTH close
- Key levels: yesterday's H/L/C, 5-day H/L, prior week H/L, current week opening range
- Economic calendar events for today (uses existing `economic-calendar-fetcher`)
- Earnings movers that could ripple into ES (uses existing `earnings-calendar`)
- Overnight news catalysts (uses existing `market-news-analyst`)
- Volatility context: yesterday's ATR vs. 20-day average ATR
- Session bias: is the overnight action consistent with the broader trend (uses existing `technical-analyst`)?
- Three potential setups with conditional entry/stop/target plans (mirrors the parabolic-short Phase 2 trigger pattern)

### Why this is a wrapper, not a rebuild

Most of the data and reasoning already exists in other skills. This skill's job is **orchestration and futures-specific framing**, not net-new analysis. Internally it should call:
- `economic-calendar-fetcher` for today's events
- `market-news-analyst` for overnight news
- `technical-analyst` (with futures inputs) for trend context
- `tradovate-integration` for overnight bars
- `lucid-rules-engine` for current account constraints (don't suggest setups that would breach)

### Output format

Use the same template structure as `/intraday-options` so your eye learns one format. Add sections for:
- Lucid account status (current EOD drawdown buffer per active account)
- Time until auto-flatten window opens
- Qualifying days status for current payout cycle

---

## Skill 5: `futures-session-monitor` (Week 9)

Real-time intraday monitoring. Equivalent to `parabolic-short-trade-planner`'s Phase 3 monitor but for futures session structure.

### Scope (Phase 2: monitoring only, no execution)

Watches the live Tradovate stream and emits alerts on:
- Opening range breakout/breakdown (first 30 min H/L)
- Approach to key levels from pre-market scan
- VWAP reclaim/loss
- Volume divergence at extremes
- Time-based events: 11 AM ET (lunchtime fade window starts), 2 PM ET (power hour begins), 4:30 PM ET (15-min auto-flatten warning), 4:40 PM ET (5-min warning)
- Lucid rule warnings: approaching daily loss buffer, approaching EOD drawdown buffer, position open within 5 min of auto-flatten

### Architecture

One-shot evaluator wrapped in `watch -n 60` or a 1-minute cron — same pattern as `monitor_intraday_trigger.py` in `parabolic-short-trade-planner`. State persists in JSON between runs.

### Output

Write alerts to `~/trading-research/logs/session_YYYY-MM-DD.jsonl` (one JSON object per line). Optional: pipe to a desktop notification using `terminal-notifier` (macOS) or `notify-send` (Linux).

---

## Skill 6: `/futures-setup` Command (Week 10)

Mirrors `/intraday-options` but for futures. One-shot pre-market briefing producing concrete trade plans.

### Argument signature

```bash
/futures-setup <CONTRACT> [<ACCOUNT_ID>]
# Examples:
/futures-setup ES
/futures-setup MNQ lucid_flex_50k_001
```

### What it does

1. Calls `futures-pre-market-scan` for the contract's index (ES → SPX, NQ → NDX)
2. Calls `lucid-rules-engine.get_account_state()` for the specified account (default: first active account)
3. Calls `futures-position-sizer` to size each candidate setup
4. Produces a markdown report with 1–3 conditional trade plans

### Output template

Reuse `/intraday-options` structure with futures-specific fields:
- Contract spec (point value, tick size)
- Lucid account context (buffer, qualifying days)
- Per-setup: trigger, entry, stop, target, sized contracts, max loss as % of buffer
- Time invalidation (default: cancel all setups by 11:30 AM ET unless still actionable)
- Exit checklist that includes "close before 4:30 PM ET"

---

## Exit Criteria (all must be met to advance to Phase 3)

- [ ] All 6 skills built with `SKILL.md`, references, scripts, and tests
- [ ] `lucid-rules-engine` has unit tests covering every rule and every boundary case
- [ ] `tradovate-integration` verified against demo account with `check_connection.py`
- [ ] `/futures-setup` used pre-market for at least 10 trading days
- [ ] At least 5 trades taken using `/futures-setup` recommendations (paper or live), all logged to `trader-memory-core`
- [ ] No skill in this phase has any path to autonomous execution. (Verify by code review: no skill calls `place_order` because that function should not exist yet.)
- [ ] Total Anthropic spend for Phase 2 < $40

---

## Common Phase 2 Pitfalls

**Pitfall 1: Building order placement "just in case."**
Don't. Phase 5 is when this happens. Building it earlier means it exists when you don't yet have the discipline to leave it alone.

**Pitfall 2: Encoding Lucid rules from memory or single search results.**
Re-verify every rule against `support.lucidtrading.com` before encoding. Pull the raw text into the references directory. Then encode against the references, not against your interpretation.

**Pitfall 3: Skipping tests on the rules engine.**
The rules engine is the foundation of everything that follows. Skipping its tests is how you end up with a position-sizer that allows a 200% risk trade because you forgot a sign flip in the daily loss check.

**Pitfall 4: Trying to be clever with the orchestration.**
Skill 4 (pre-market scan) is the most tempting place to over-engineer. Resist. It's a wrapper that calls existing skills in sequence and formats their output. The intelligence is already in the existing skills.

**Pitfall 5: Touching live Tradovate.**
Demo only in Phase 2. The env var must default to demo. Make it require an explicit `--i-know-what-im-doing` flag to ever hit the live endpoint, and only do that in Phase 5.

---

## What's NOT in Phase 2

- Backtesting (Phase 4)
- Behavioral pattern detection (Phase 3)
- The personal playbook (Phase 3)
- Any autonomous decision-making (Phase 5)
- Live Tradovate (Phase 5)

---

## When You're Ready to Advance

Update the main `PROJECT.md`:
- Change "Active Phase" to Phase 3
- Reset "This week's focus"
- Read `project-docs/phase-3-learning-loop.md`
