# Lucid Trading Rules Reference

> **Read this when:** building or modifying the `lucid-rules-engine` skill, or any time a Lucid-specific decision needs to be encoded.
>
> **Source verification:** Always cross-check against `support.lucidtrading.com` and `lucidtrading.com/general-faq/` before encoding. Rules can change.

---

## Product Lines (verified as of project start)

Lucid offers three product lines, each with different rule sets:

| Product | Phase | Best for |
|---|---|---|
| **LucidFlex** | Eval → Funded | Most forgiving rules, news traders, traders who want one big day |
| **LucidPro** | Eval → Funded | Structured evaluation, ~40% consistency rule, fastest payouts |
| **LucidDirect** | Instant funded | Skip evaluation, 20% consistency from day one, higher upfront cost |

---

## Rules Common to All Product Lines

### Trading hours
- Sun 6:00 PM ET → Fri 4:45 PM ET
- Daily break: 4:45 PM ET to 6:00 PM ET (closed for maintenance window)
- Reduced hours on market holidays (CME holiday calendar)

### Auto-flatten
- **All open positions force-closed at 4:45 PM ET daily** by Lucid's risk system
- Triggered server-side, not platform-side
- NinjaTrader, Tradovate, etc. do not enforce this independently — Lucid does
- Liquidations at the cutoff can result in poor fills due to thin liquidity
- **Implication for agent:** force-close at 4:35 PM ET to avoid slippage at the auto-flatten

### Profit split
- **First $10,000 in payouts: 100% to trader**
- After that: **90% trader / 10% Lucid**
- Applies to LucidPro, LucidFlex, LucidDirect

### Account limits
- Up to 10 active evaluation accounts per household
- Up to 5 active funded accounts per household
- Total combined cap: 10 (e.g., 5 eval + 5 funded)

### Permitted markets
- CME futures only (ES, NQ, YM, RTY, NQ, MES, MNQ, MYM, M2K, CL, GC, etc.)
- No equities, no options, no forex, no crypto

### Permitted automation
- **Algorithmic trading explicitly allowed**
- API access supported for Python, Java, C++
- Trade copiers permitted
- TradersPost integration supported via Tradovate
- **Prohibited:** HFT, latency arbitrage, "similar strategies" (per Lucid's docs)
- Lucid uses automated detection for HFT — repeated offenses can result in profit removal and account closure

### Account management
- **One-time fees** (no monthly subscriptions for trading accounts)
- Activation: typically 5–30 minutes after purchase
- Resets available for evaluation accounts (not funded)
- Accounts not traded for 30 calendar days may be deleted (irreversible)

---

## LucidFlex Rules (most relevant for project start)

### Evaluation phase
- Profit target: account-size dependent (~6-8%)
- 50% consistency rule: biggest day cannot exceed 50% of total profit
- EOD trailing max loss
- No daily loss limit (but EOD trail effectively constrains)

### Funded phase
- **No 50% consistency rule** (key differentiator vs. eval phase and other firms)
- **No daily loss limit**
- **EOD trailing max loss continues**
- One large winning day is permitted, BUT...

### Minimum qualifying days for payout (CORRECTED)

**You must hit the minimum daily profit on 5 separate trading days during each payout cycle.** Counter resets after every approved payout.

| Account Size | Minimum Daily Profit (Net) |
|---|---|
| $25,000 | $100 |
| $50,000 | $150 |
| $100,000 | $200 |
| $150,000 | $250 |

**Critical clarifications:**
- "Net" means after commissions
- The 5 days don't have to be consecutive
- A day with $50 profit doesn't count even though it was profitable — must hit the full minimum
- One day with $5,000 profit counts as exactly one qualifying day, not five
- Counter resets to 0 after every approved payout

### EOD trailing max loss (Flex)
- Calculated at session close only — intraday equity does not affect the floor
- Trails the highest closing balance
- Once balance exceeds Initial Trail Balance, the MLL locks at starting balance + $100
- "One of the best drawdown systems in the futures prop firm space" per multiple reviews — but still strict

### Profit cap per cycle (Flex)
- Yes — Flex caps payouts per cycle (varies by account; check current dashboard)
- LucidPro and LucidDirect have different cap structures

---

## LucidPro Rules

- Two-step evaluation
- ~40% consistency rule (biggest day cannot exceed 40% of total profit) — applies in funded phase too
- EOD trailing max loss
- Frequent payout cadence
- Better for structured, consistent traders

---

## LucidDirect Rules

- No evaluation — instant funded
- 20% consistency rule from day one (most demanding ruleset)
- LucidScale DLL (daily loss limit) at 60% of peak EOD above the initial trail
- Maximum 5 accounts per household
- Free activation
- Higher upfront cost than evaluation route

---

## Rules That Apply at Payout Time

- Minimum 5 qualifying days per cycle (Flex)
- Consistency rule check (Pro: 40%, Direct: 20%, Flex funded: not applied)
- Profit must come from compliant trading (no HFT, no latency arb)
- Payout request submitted via dashboard
- Payouts: bank transfer, PayPal, or wire
- Minimum payout: $500

---

## Implications for `lucid-rules-engine` Implementation

### State to persist per account
- Account type (flex/pro/direct)
- Account size (25k/50k/100k/150k)
- Current cycle start date
- Current cycle qualifying days count
- Highest closing balance ever (for EOD trail calc)
- Initial trail balance
- Current MLL (max loss limit)
- Last payout date and amount

### Functions the engine must expose

```python
# Pre-trade checks
can_open_position(account_id, contract, size, est_max_loss) -> RuleCheckResult
estimate_remaining_buffer(account_id) -> Decimal  # how much can I afford to lose today
time_until_auto_flatten(now_et) -> timedelta  # always available
is_within_trading_hours(now_et) -> bool

# Cycle eligibility
qualifying_days_status(account_id) -> dict  # {met: 3, required: 5, current_day_qualified: bool}
days_until_next_payout_eligible(account_id) -> int

# Payout-time checks
can_request_payout(account_id) -> RuleCheckResult
estimate_payout_amount(account_id) -> Decimal  # net of profit split

# Hard constraints (always callable)
get_max_position_size(account_id, contract) -> int
is_in_blackout_window(now_et) -> bool  # news, market close approach, etc.
```

### Test coverage requirements

For every rule, test:
- Pass case
- Block case
- Boundary (1 dollar from breach, 1 minute from cutoff)
- Cycle reset behavior
- Multiple accounts (state isolation)
- Daylight saving time transitions (4:45 PM ET shifts wall-clock by an hour twice a year)
- Holiday-shortened sessions
- Newly opened account (no prior history)

### What the agent must NEVER do

- Modify the rules file
- Modify account state to manipulate buffer calculations
- Override a BLOCK result
- Place an order without first calling `can_open_position()`
- Hold a position past 4:35 PM ET (defensive — Lucid's auto-flatten is at 4:45)

---

## Update Cadence

Lucid is a young firm (launched early 2025) and rules can change. **Verify rules against the source quarterly** at minimum. When verifying:

1. Pull current `general-faq` page text
2. Diff against `references/lucid-rules-flex.md` (and pro, direct)
3. Update references file if changed
4. Update `rules.py` only after references are updated
5. Re-run full test suite
6. Commit with message: `[lucid-rules] Updated per <date> verification: <what changed>`
