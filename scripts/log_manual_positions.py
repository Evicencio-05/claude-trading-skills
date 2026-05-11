#!/usr/bin/env python3
"""
One-shot script: backfill Portfolio B (Roth IRA) options positions and
Lucid futures trades into trader-memory-core.

Log date: 2026-05-09
Run once: 2026-05-10 session.

MRAM is skipped — adjustment pending (user to confirm post-adjustment state).
"""

import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "skills" / "trader-memory-core" / "scripts")
)
import thesis_store

STATE_DIR = Path(__file__).resolve().parents[1] / "state" / "theses"
LOG_DATE = "2026-05-09"

IRA_CTX = {
    "account": "ira_robinhood",
    "account_type": "ira",
    "asset_type": "options",
    "ira_eligible": True,
    "ira_strategy": "long_call",
}


def register_and_activate(data: dict, entry_price: float, entry_date: str) -> str:
    tid = thesis_store.register(STATE_DIR, data)
    t = thesis_store.get(STATE_DIR, tid)
    if t["status"] == "IDEA":
        thesis_store.transition(STATE_DIR, tid, "ENTRY_READY", "position confirmed open")
    if thesis_store.get(STATE_DIR, tid)["status"] == "ENTRY_READY":
        thesis_store.open_position(STATE_DIR, tid, actual_price=entry_price, actual_date=entry_date)
    return tid


def register_and_close(
    data: dict,
    entry_price: float,
    entry_date: str,
    exit_price: float,
    exit_date: str,
    exit_reason: str = "manual",
) -> str:
    tid = thesis_store.register(STATE_DIR, data)
    t = thesis_store.get(STATE_DIR, tid)
    if t["status"] == "IDEA":
        thesis_store.transition(STATE_DIR, tid, "ENTRY_READY", "trade executed")
    if thesis_store.get(STATE_DIR, tid)["status"] == "ENTRY_READY":
        thesis_store.open_position(STATE_DIR, tid, actual_price=entry_price, actual_date=entry_date)
    if thesis_store.get(STATE_DIR, tid)["status"] == "ACTIVE":
        thesis_store.close(
            STATE_DIR, tid, exit_reason, actual_price=exit_price, actual_date=exit_date
        )
    return tid


def log_options_positions():
    positions = [
        # ── 1. POWL ──
        {
            "data": {
                "ticker": "POWL",
                "thesis_type": "pivot_breakout",
                "thesis_statement": (
                    "Electrical grid infrastructure pure-play. DPA enacted by US govt "
                    "targets grid improvement — POWL is a direct beneficiary. "
                    "Long Call $340 exp 2026-05-15 | 1 contract @ $5.90."
                ),
                "confidence_score": 0.6,
                "setup_type": "regulatory_catalyst_breakout",
                "catalyst": "Defense Production Act — US electrical grid mandate",
                "evidence": [
                    "DPA recently enacted targeting grid improvement",
                    "POWL direct electrical grid beneficiary; near-term catalyst is law",
                ],
                "kill_criteria": [
                    "DPA reversed or implementation delayed beyond 12 months",
                    "50% premium loss",
                ],
                "exit": {"stop_loss_pct": 50},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 340,
                    "option_expiry": "2026-05-15",
                    "contracts": 1,
                    "theme": "energy_grid_dpa",
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 5.90,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 2. TSLA ──
        {
            "data": {
                "ticker": "TSLA",
                "thesis_type": "growth_momentum",
                "thesis_statement": (
                    "TSLA pulled back from highs and began new bullish run. "
                    "Playing momentum continuation. Expecting pullback to ~$410 before next leg. "
                    "Long Call $430 exp 2026-05-18 | 1 contract @ $6.95."
                ),
                "confidence_score": 0.8,
                "setup_type": "momentum_continuation",
                "evidence": [
                    "Bullish trend resumption after pullback from highs",
                    "Expecting $410 consolidation then $450 breakout",
                ],
                "kill_criteria": ["TSLA closes below $390"],
                "exit": {"take_profit": 450.0, "stop_loss": 390.0},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 430,
                    "option_expiry": "2026-05-18",
                    "contracts": 1,
                    "theme": "ev_momentum",
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 6.95,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 3. CORZ ──
        {
            "data": {
                "ticker": "CORZ",
                "thesis_type": "pivot_breakout",
                "thesis_statement": (
                    "Heavy options flow observed — tailing institutional whale activity. "
                    "Lottery-type position sized for total loss. "
                    "Long Call $24 exp 2026-05-29 | 1 contract @ $1.33."
                ),
                "confidence_score": 0.4,
                "setup_type": "flow_tail",
                "catalyst": "Heavy institutional options flow / whale activity",
                "evidence": ["Significant options flow observed in CORZ"],
                "kill_criteria": ["Whale activity exits / flow reverses"],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 24,
                    "option_expiry": "2026-05-29",
                    "contracts": 1,
                    "theme": "flow_play_lottery",
                    "sector": "crypto_mining",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 1.33,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 4. HOOD ──
        {
            "data": {
                "ticker": "HOOD",
                "thesis_type": "mean_reversion",
                "thesis_statement": (
                    "Robinhood decline driven by lower crypto trading volume. "
                    "BTC rising → crypto volume recovering → HOOD revenue recovering. "
                    "High conviction from daily user experience. Roll candidate. "
                    "Long Call $90 exp 2026-06-18 | 1 contract @ $5.80."
                ),
                "confidence_score": 0.4,
                "setup_type": "catalyst_mean_reversion",
                "catalyst": "BTC price recovery → crypto trading volume recovery → HOOD revenue",
                "evidence": [
                    "HOOD sold off on crypto volume decline",
                    "BTC in uptrend — leading indicator for HOOD revenue",
                    "Daily user experience validates platform quality",
                ],
                "kill_criteria": ["HOOD cannot break $93 after reaching it"],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 90,
                    "option_expiry": "2026-06-18",
                    "contracts": 1,
                    "theme": "fintech_crypto_recovery",
                    "roll_candidate": True,
                    "price_targets": [83, 87, 93],
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 5.80,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 5. ICHR ──
        {
            "data": {
                "ticker": "ICHR",
                "thesis_type": "pivot_breakout",
                "thesis_statement": (
                    "Breaking out with retest of $73 before continuation. "
                    "Critical semiconductor production component; sympathy play for semi uptrend. "
                    "Recent gap filled, clean break above prior high. Add candidate on $72-73 hold. "
                    "Long Call $90 exp 2026-06-18 | 1 contract @ $3.10."
                ),
                "confidence_score": 0.6,
                "setup_type": "breakout_retest",
                "evidence": [
                    "Breaking out above prior high with retest at $73",
                    "Critical semi production component — sector tailwind",
                    "Gap filled, clean breakout structure",
                ],
                "kill_criteria": ["$72-73 support fails as floor"],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 90,
                    "option_expiry": "2026-06-18",
                    "contracts": 1,
                    "theme": "semiconductor_ecosystem",
                    "add_candidate": True,
                    "add_trigger": "72-73 holds as strong floor",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 3.10,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 6a. PENG (short-dated) ──
        {
            "data": {
                "ticker": "PENG",
                "thesis_type": "growth_momentum",
                "thesis_statement": (
                    "Undervalued AI buildout play. Manages AI infrastructure, HPC systems, "
                    "and memory solutions for enterprise data centers. Significant attention on X. "
                    "SHORT-DATED LEG: Long Call $55 exp 2026-05-18 | 3 contracts @ $1.05."
                ),
                "confidence_score": 1.0,
                "setup_type": "structural_growth_momentum",
                "catalyst": "AI infrastructure buildout — enterprise HPC/memory demand",
                "evidence": [
                    "Manages AI infrastructure and HPC systems for enterprise data centers",
                    "Significant social attention on X as potential discovery",
                    "AI buildout structural tailwind",
                ],
                "kill_criteria": ["Thesis invalidated (core AI infrastructure narrative broken)"],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 55,
                    "option_expiry": "2026-05-18",
                    "contracts": 3,
                    "theme": "ai_infrastructure",
                    "leg": "short_dated",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 1.05,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 6b. PENG (long-dated) ──
        {
            "data": {
                "ticker": "PENG",
                "thesis_type": "growth_momentum",
                "thesis_statement": (
                    "Undervalued AI buildout play — same as short-dated leg. "
                    "LONG-DATED LEG provides runway for thesis development. "
                    "Long Call $40 exp 2026-09-18 | 1 contract @ $4.40."
                ),
                "confidence_score": 1.0,
                "setup_type": "structural_growth_momentum",
                "catalyst": "AI infrastructure buildout — enterprise HPC/memory demand",
                "evidence": [
                    "Same thesis as short-dated leg with longer runway",
                    "Deep ITM strike provides more theta protection",
                ],
                "kill_criteria": ["Thesis invalidated (core AI infrastructure narrative broken)"],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 40,
                    "option_expiry": "2026-09-18",
                    "contracts": 1,
                    "theme": "ai_infrastructure",
                    "leg": "long_dated",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 4.40,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 7. VECO ──
        {
            "data": {
                "ticker": "VECO",
                "thesis_type": "growth_momentum",
                "thesis_statement": (
                    "Backbone of semiconductor fabrication — makes machines that make semiconductors. "
                    "Strong, underappreciated company with near-monopoly positioning in its niche. "
                    "Long Call $75 exp 2026-07-17 | 1 contract @ $4.10."
                ),
                "confidence_score": 0.8,
                "setup_type": "moat_growth_momentum",
                "evidence": [
                    "Near-monopoly in semiconductor fabrication equipment niche",
                    "Underappreciated — market does not yet fully price the moat",
                    "Semi sector structural tailwind",
                ],
                "kill_criteria": [
                    "Monopoly position breaks",
                    "Major customer loss",
                ],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 75,
                    "option_expiry": "2026-07-17",
                    "contracts": 1,
                    "theme": "semiconductor_ecosystem",
                    "moat_type": "near_monopoly",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 4.10,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 8. GRID ──
        {
            "data": {
                "ticker": "GRID",
                "thesis_type": "pivot_breakout",
                "thesis_statement": (
                    "Same DPA/grid infrastructure thesis as POWL but broader ETF approach. "
                    "Portfolio hedge against single-stock risk in POWL position. "
                    "Long Call $205 exp 2026-09-18 | 1 contract @ $4.60."
                ),
                "confidence_score": 0.8,
                "setup_type": "regulatory_catalyst_breakout",
                "catalyst": "Defense Production Act — US electrical grid mandate (same as POWL)",
                "evidence": [
                    "DPA grid infrastructure mandate drives entire sector",
                    "ETF provides diversified exposure vs POWL single-stock risk",
                ],
                "kill_criteria": [
                    "DPA rescinded",
                    "Implementation timeline extends beyond 18 months",
                ],
                "exit": {"stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 205,
                    "option_expiry": "2026-09-18",
                    "contracts": 1,
                    "theme": "energy_grid_dpa",
                    "instrument_type": "etf",
                    "hedges": "POWL_single_stock_risk",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 4.60,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
        # ── 9. MRAM — SKIPPED ──
        # NOTE: Adjustment pending based on May 8 price action.
        # User to confirm post-adjustment state before logging.
        # Tags would be: [options_active, long_call, sector_semis, near_monopoly,
        #                 govt_contract, adjustment_pending]
        # ── 10. FLNC ──
        {
            "data": {
                "ticker": "FLNC",
                "thesis_type": "growth_momentum",
                "thesis_statement": (
                    "Global leader in utility-scale energy storage. Battery-based systems, "
                    "software, and services for grid modernization and renewable energy integration. "
                    "Similar to Bloom Energy in profile. "
                    "Long Call $45 exp 2027-01-15 | 1 contract @ $4.20."
                ),
                "confidence_score": 0.8,
                "setup_type": "structural_growth_momentum",
                "catalyst": "Grid modernization and renewable energy storage demand",
                "evidence": [
                    "Global leader in utility-scale battery energy storage",
                    "Grid modernization structural tailwind aligns with POWL/GRID DPA thesis",
                    "Long-dated option provides runway for multi-quarter thesis",
                ],
                "kill_criteria": [
                    "Break below $19-20 support",
                    "Major adverse news (contract loss, technology displacement)",
                ],
                "exit": {"stop_loss": 19.0, "stop_loss_pct": 100},
                "market_context": {
                    **IRA_CTX,
                    "option_strike": 45,
                    "option_expiry": "2027-01-15",
                    "contracts": 1,
                    "theme": "energy_storage",
                    "sector": "energy_storage_grid",
                    "sized_for_zero": True,
                },
                "origin": {"skill": "manual-options-entry", "output_file": "manual_2026-05-09"},
                "_source_date": LOG_DATE,
                "_register_reason": "Backfilled from Portfolio B Roth IRA 2026-05-09",
            },
            "entry_price": 4.20,
            "entry_date": "2026-05-09T00:00:00+00:00",
        },
    ]

    print("\n=== OPTIONS POSITIONS (Portfolio B — Roth IRA) ===")
    for pos in positions:
        tid = register_and_activate(pos["data"], pos["entry_price"], pos["entry_date"])
        ticker = pos["data"]["ticker"]
        ctx = pos["data"].get("market_context", {})
        strike = ctx.get("option_strike", "?")
        expiry = ctx.get("option_expiry", "?")
        print(f"  ✓ {ticker} ${strike} {expiry} → {tid}")

    print("\n  ⚠️  MRAM skipped — adjustment pending (log after confirming post-adjustment state)")


def log_futures_trades():
    """
    Three futures sessions — all closed (both Sessions D and I, plus the
    scalping aggregate A+B+C+G+H).

    NOTE: trader-memory-core computes P&L as (exit_price - entry_price) × shares.
    This will NOT match actual dollar P&L for futures because the MNQ multiplier
    ($2/point) is not in the schema. The real P&L is stored in market_context
    .stated_pnl_dollars for each entry.
    """

    # ── Session D — Overnight long MNQ ──
    session_d = {
        "ticker": "MNQ",
        "thesis_type": "growth_momentum",
        "thesis_statement": (
            "Missed pullback at session start, saw strong bullish momentum. "
            "No explicit bad news (Iran war). Market strong on the day. "
            "Built 2-contract position in stages during Globex. "
            "MNQ long overnight | 2 contracts | entry 28303 | exit 28487.5 | P&L +$625."
        ),
        "confidence_score": 0.8,
        "setup_type": "momentum_overnight",
        "catalyst": "Strong market momentum; absence of negative Iran/geopolitical news",
        "evidence": [
            "Strong bullish intraday momentum",
            "No adverse macro news to fight the trend",
            "Overnight Globex continuation of day session strength",
        ],
        "kill_criteria": ["Market reverses on macro news", "Daily loss limit approached"],
        "exit": {},
        "market_context": {
            "account": "lucid_eval",
            "account_type": "futures_eval",
            "asset_type": "futures",
            "ira_eligible": False,
            "contract": "MNQ",
            "contract_multiplier": 2,
            "direction": "long",
            "contracts": 2,
            "stated_pnl_dollars": 625,
            "exit_trigger": "AutoLiq daily profit target $625 hit",
            "session": "D",
            "lesson": (
                "Stick with overall market direction. Smaller contract, longer plays. "
                "Overnight momentum trade worked when day session was strong."
            ),
        },
        "origin": {"skill": "manual-futures-entry", "output_file": "lucid_eval_2026-05-05"},
        "_source_date": "2026-05-05",
        "_register_reason": "Backfilled Lucid eval trade 2026-05-05",
    }

    tid_d = register_and_close(
        session_d,
        entry_price=28303.0,
        entry_date="2026-05-05T19:04:00+00:00",
        exit_price=28487.5,
        exit_date="2026-05-06T01:55:00+00:00",
        exit_reason="target_hit",
    )
    print("\n=== FUTURES TRADES (Lucid Eval — lucid_eval) ===")
    print(f"  ✓ Session D  MNQ long  +$625  → {tid_d}")

    # ── Session I — Overnight short MNQ (stopped out) ──
    session_i = {
        "ticker": "MNQ",
        "thesis_type": "mean_reversion",
        "thesis_statement": (
            "Negative Iran news. Did not expect market to move higher before weekend. "
            "Three concurrent overnight short entries all stopped out. "
            "NQ continued higher through all stop levels. "
            "MNQ short overnight | 3 contracts | avg entry 28859 | avg exit 28883.75 | P&L -$148."
        ),
        "confidence_score": 0.4,
        "setup_type": "news_driven_short_fade",
        "catalyst": "Negative Iran geopolitical news",
        "evidence": [
            "Negative Iran news provided short catalyst",
            "Market was not expected to dip and rip overnight",
        ],
        "kill_criteria": ["Market breaks above entry level (thesis invalidated at stop)"],
        "exit": {},
        "market_context": {
            "account": "lucid_eval",
            "account_type": "futures_eval",
            "asset_type": "futures",
            "ira_eligible": False,
            "contract": "MNQ",
            "contract_multiplier": 2,
            "direction": "short",
            "contracts": 3,
            "stated_pnl_dollars": -148,
            "exit_trigger": "All three concurrent entries stopped out",
            "session": "I",
            "lesson": (
                "Same overnight strategy as Session D but opposite direction did not work. "
                "Key question: what was different from the successful overnight long? "
                "Concurrent entries amplified risk without edge confirmation."
            ),
        },
        "origin": {"skill": "manual-futures-entry", "output_file": "lucid_eval_2026-05-07"},
        "_source_date": "2026-05-07",
        "_register_reason": "Backfilled Lucid eval trade 2026-05-07",
    }

    # For shorts: system computes (exit - entry) × shares which will be positive (wrong sign).
    # stated_pnl_dollars = -148 in market_context is the authoritative figure.
    tid_i = register_and_close(
        session_i,
        entry_price=28859.0,
        entry_date="2026-05-07T21:21:00+00:00",
        exit_price=28883.75,
        exit_date="2026-05-08T02:21:00+00:00",
        exit_reason="stop_hit",
    )
    print(f"  ✓ Session I  MNQ short  -$148  → {tid_i}")

    # ── Sessions A+B+C+G+H — Intraday scalping aggregate ──
    sessions_scalp = {
        "ticker": "MNQ",
        "thesis_type": "mean_reversion",
        "thesis_statement": (
            "Intraday and Globex scalp attempts across 5 sessions (A+B+C+G+H), 2026-05-04 to 05-07. "
            "Mixed long and short bias, high trade count. Combined P&L: -$370. "
            "Week was saved by Session D overnight long and one short fade (Session E). "
            "Pattern: scalping alone was not profitable; overnight momentum trades produced the wins."
        ),
        "confidence_score": 0.4,
        "setup_type": "intraday_scalping",
        "evidence": ["Multiple intraday and Globex scalp attempts with mixed bias"],
        "kill_criteria": ["Daily drawdown limit approached"],
        "exit": {},
        "market_context": {
            "account": "lucid_eval",
            "account_type": "futures_eval",
            "asset_type": "futures",
            "ira_eligible": False,
            "contract": "MNQ",
            "contract_multiplier": 2,
            "direction": "mixed",
            "sessions": ["A", "B", "C", "G", "H"],
            "stated_pnl_dollars": -370,
            "note": (
                "Aggregate of 5 sessions. Entry/exit prices are approximate references. "
                "stated_pnl_dollars is the authoritative P&L figure."
            ),
            "lesson": (
                "Scalping alone was not profitable. Overnight momentum trades (Session D) "
                "produced the only significant win of the week. "
                "Need edge confirmation before entries — high frequency without edge = negative EV."
            ),
        },
        "origin": {"skill": "manual-futures-entry", "output_file": "lucid_eval_scalp_aggregate"},
        "_source_date": "2026-05-04",
        "_register_reason": "Backfilled Lucid eval scalping aggregate 2026-05-04 to 05-07",
    }

    # Approximate MNQ level during 5/4-5/7 for entry price reference
    tid_scalp = register_and_close(
        sessions_scalp,
        entry_price=19800.0,
        entry_date="2026-05-04T22:58:00+00:00",
        exit_price=19800.0,
        exit_date="2026-05-07T23:59:00+00:00",
        exit_reason="manual",
    )
    print(f"  ✓ Sessions A+B+C+G+H  MNQ scalp  -$370  → {tid_scalp}")
    print(
        "  ⚠️  Scalping aggregate: system P&L = $0 (mixed direction). Real P&L in market_context.stated_pnl_dollars"
    )
    print(
        "  ⚠️  Session D/I: system P&L uses raw price diff (no $2/tick multiplier). Real P&L in market_context.stated_pnl_dollars"
    )


if __name__ == "__main__":
    log_options_positions()
    log_futures_trades()
    print("\n=== Done. Verify with: ===")
    print(
        "  .venv/bin/python3 skills/trader-memory-core/scripts/thesis_store.py list --status ACTIVE"
    )
    print(
        "  .venv/bin/python3 skills/trader-memory-core/scripts/thesis_store.py list --status CLOSED"
    )
