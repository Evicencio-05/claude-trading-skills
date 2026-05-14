#!/usr/bin/env python3
"""
robinhood_sync.py — Pull current Robinhood positions into state/pending_ingest.json

Runs headlessly after first auth (robin_stocks stores token at ~/.tokens/).
Only outputs positions not already tracked in state/synced_positions.json.

Usage:
    python3 scripts/robinhood_sync.py              # sync all accounts
    python3 scripts/robinhood_sync.py --dry-run    # show what would be added
    python3 scripts/robinhood_sync.py --force      # re-add all positions (ignores sync history)

First run requires interactive login (2FA on phone). Subsequent runs are headless.

Outputs:
    state/pending_ingest.json   — positions awaiting thesis input (/log-positions reads this)
    state/synced_positions.json — tracks what has already been ingested (prevents duplicates)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# ── Account Configuration ─────────────────────────────────────────────────────
#
# Portfolio structure:
#
#   Portfolio A — Robinhood individual (taxable)
#     Login:    New Robinhood login (not the IRA login)
#     Size:     ~$250 currently
#     Access:   Full stock + options (standard margin account)
#     API:      Reachable via robin_stocks — this is what gets synced
#
#   Portfolio B — Robinhood IRA (Roth or Traditional)
#     Login:    Separate Robinhood login
#     Size:     ~$10K
#     Access:   IRA-eligible options only (long calls/puts, covered calls,
#               cash-secured puts — no naked selling, no undefined risk)
#     API:      NOT reachable via unofficial API — IRA accounts sit on a
#               separate Robinhood internal path. Log positions manually
#               via /log-positions command.
#
#   Lucid Trading — Futures prop firm account
#     Platform: Tradovate (CME futures only)
#     API:      Deferred to Phase 2 — tradovate_sync.py follows this pattern
#
# ── Account ID Map ────────────────────────────────────────────────────────────
# Fill in the account URL printed on first sync run.
# Run: python3 scripts/robinhood_sync.py --dry-run
# Look for the "Found these account IDs" line in the output.

ACCOUNT_MAP = {
    "https://api.robinhood.com/accounts/487509309/": "robinhood_taxable",  # Portfolio A (~$500)
}

# NOTE: Only Portfolio A (taxable individual account) is synced here.
# Portfolio B (IRA) positions are logged manually via /log-positions.
# This is by design — Robinhood IRA accounts are not accessible via
# the unofficial API regardless of authentication method.

# If ACCOUNT_MAP is empty, all positions are labeled by their Robinhood account_id.
# Fill in the map after first run — script will print account IDs it finds.

STATE_DIR = Path("state")
PENDING_FILE = STATE_DIR / "pending_ingest.json"
SYNCED_FILE = STATE_DIR / "synced_positions.json"

# ── Helpers ───────────────────────────────────────────────────────────────────


def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return default
    return default


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str))


def position_key(ticker: str, asset_type: str, strike=None, expiry=None, option_type=None) -> str:
    """Unique key for deduplication. Options include strike+expiry+type."""
    if asset_type == "options" and strike and expiry:
        return f"{ticker}|{asset_type}|{strike}|{expiry}|{option_type}"
    return f"{ticker}|{asset_type}"


def resolve_account(account_id: str) -> str:
    """Map account_id to portfolio label, or return raw id if unmapped."""
    return ACCOUNT_MAP.get(account_id, account_id)


def format_stock_position(pos: dict) -> dict:
    """Convert robin_stocks stock position to pending_ingest format."""
    ticker = pos.get("symbol", "UNKNOWN").upper()
    avg_cost = float(pos.get("average_buy_price", 0))
    qty = float(pos.get("quantity", 0))
    account_id = pos.get("account", "")

    return {
        "key": position_key(ticker, "stock"),
        "ticker": ticker,
        "asset_type": "stock",
        "direction": "long",
        "account": resolve_account(account_id),
        "size": qty,
        "avg_cost": round(avg_cost, 4),
        "total_cost": round(avg_cost * qty, 2),
        "synced_at": datetime.now().isoformat(),
        # Fields requiring human input — left empty for /log-positions
        "confidence": None,
        "thesis": None,
        "stop": None,
        "target": None,
        "tags": [],
        "status": "PENDING_THESIS",
    }


def format_option_position(pos: dict) -> dict:
    """Convert robin_stocks option position to pending_ingest format."""
    ticker = pos.get("chain_symbol", "UNKNOWN").upper()
    strike = pos.get("strike_price", "")
    expiry = pos.get("expiration_date", "")
    option_type = pos.get("option_type", "").lower()  # "call" or "put"
    qty = float(pos.get("quantity", 0))
    avg_cost = float(pos.get("average_buy_price", 0))
    account_id = pos.get("account", "")
    account = resolve_account(account_id)

    # Determine IRA eligibility
    is_ira = "ira" in account.lower()
    ira_eligible = option_type in ("call", "put")  # long calls/puts always IRA-eligible
    strategy = f"long_{option_type}" if option_type in ("call", "put") else option_type

    return {
        "key": position_key(ticker, "options", strike, expiry, option_type),
        "ticker": ticker,
        "asset_type": "options",
        "direction": "long",
        "strategy": strategy,
        "account": account,
        "contracts": int(qty),
        "strike": strike,
        "expiry": expiry,
        "option_type": option_type,
        "avg_cost": round(avg_cost, 4),
        "total_cost": round(avg_cost * int(qty) * 100, 2),  # options are per 100 shares
        "ira_eligible": ira_eligible if is_ira else None,
        "synced_at": datetime.now().isoformat(),
        # Fields requiring human input
        "confidence": None,
        "thesis": None,
        "stop": None,
        "target": None,
        "tags": [strategy, f"expiry_{expiry[:7].replace('-', '_')}" if expiry else ""],
        "status": "PENDING_THESIS",
    }


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Sync Robinhood positions to pending_ingest.json")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would be added, no writes"
    )
    parser.add_argument(
        "--force", action="store_true", help="Re-add all positions, ignore sync history"
    )
    parser.add_argument("--stocks-only", action="store_true", help="Sync stock positions only")
    parser.add_argument("--options-only", action="store_true", help="Sync options positions only")
    args = parser.parse_args()

    # ── Import robin_stocks (fail clearly if not installed) ───────────────────
    try:
        import robin_stocks.robinhood as rh
    except ImportError:
        print("ERROR: robin_stocks not installed.")
        print("Install: pip install robin_stocks --break-system-packages")
        print("Or: uv add robin_stocks")
        sys.exit(1)

    # ── Login ─────────────────────────────────────────────────────────────────
    print("Authenticating with Robinhood...")
    print("First run: check your phone for 2FA. Subsequent runs are headless.")
    try:
        login = rh.login()
        if not login:
            print("ERROR: Login failed. Check credentials.")
            sys.exit(1)
        print("✓ Authenticated")
    except Exception as e:
        print(f"ERROR: Login failed — {e}")
        sys.exit(1)

    # ── Load existing sync state ───────────────────────────────────────────────
    synced = load_json(SYNCED_FILE, {"ingested_keys": [], "pending_keys": []})
    pending = load_json(PENDING_FILE, {"positions": [], "last_sync": None})

    already_tracked = set(synced.get("ingested_keys", []))
    if not args.force:
        already_tracked.update(synced.get("pending_keys", []))

    new_positions = []
    found_accounts = set()

    # ── Pull stock positions ───────────────────────────────────────────────────
    if not args.options_only:
        print("Fetching stock positions...")
        try:
            stocks = rh.account.get_open_stock_positions() or []
            for pos in stocks:
                if float(pos.get("quantity", 0)) <= 0:
                    continue
                formatted = format_stock_position(pos)
                found_accounts.add(pos.get("account", ""))
                if formatted["key"] not in already_tracked:
                    new_positions.append(formatted)
            print(
                f"  {len(stocks)} stock position(s) found, "
                f"{sum(1 for p in new_positions if p['asset_type'] == 'stock')} new"
            )
        except Exception as e:
            print(f"WARNING: Could not fetch stock positions — {e}")

    # ── Pull options positions ────────────────────────────────────────────────
    if not args.stocks_only:
        print("Fetching options positions...")
        try:
            options = rh.options.get_open_option_positions() or []
            for pos in options:
                if float(pos.get("quantity", 0)) <= 0:
                    continue
                formatted = format_option_position(pos)
                found_accounts.add(pos.get("account", ""))
                if formatted["key"] not in already_tracked:
                    new_positions.append(formatted)
            print(
                f"  {len(options)} option position(s) found, "
                f"{sum(1 for p in new_positions if p['asset_type'] == 'options')} new"
            )
        except Exception as e:
            print(f"WARNING: Could not fetch options positions — {e}")

    # ── Print account IDs if map is empty ────────────────────────────────────
    if not ACCOUNT_MAP and found_accounts:
        print("\n⚠️  ACCOUNT_MAP is empty in robinhood_sync.py.")
        print("   Found these account IDs — add them to ACCOUNT_MAP:")
        for acct in found_accounts:
            print(f'   "{acct}": "robinhood_taxable_or_ira_robinhood"')
        print("   Then re-run to get correct account labels on positions.")

    # ── Dry run output ─────────────────────────────────────────────────────────
    if args.dry_run:
        print(f"\nDRY RUN — {len(new_positions)} position(s) would be added:")
        for p in new_positions:
            if p["asset_type"] == "options":
                print(
                    f"  {p['ticker']} ${p['strike']} {p['option_type'].upper()} "
                    f"{p['expiry']} x{p['contracts']} @ ${p['avg_cost']} "
                    f"[{p['account']}]"
                )
            else:
                print(f"  {p['ticker']} x{p['size']} @ ${p['avg_cost']} [{p['account']}]")
        print("\nRun without --dry-run to write to state/pending_ingest.json")
        return

    # ── Write output ──────────────────────────────────────────────────────────
    if not new_positions:
        print("\n✓ No new positions to sync. All positions already tracked.")
        return

    # Merge new positions into pending file
    existing_positions = pending.get("positions", [])
    existing_keys = {p["key"] for p in existing_positions}
    merged = existing_positions + [p for p in new_positions if p["key"] not in existing_keys]

    save_json(
        PENDING_FILE,
        {
            "positions": merged,
            "last_sync": datetime.now().isoformat(),
            "note": "Run '/log-positions' in Claude Code to add thesis to each pending position.",
        },
    )

    # Update synced state to include new pending keys
    all_pending_keys = list({p["key"] for p in merged if p["status"] == "PENDING_THESIS"})
    synced["pending_keys"] = all_pending_keys
    save_json(SYNCED_FILE, synced)

    print(f"\n✓ {len(new_positions)} new position(s) written to state/pending_ingest.json")
    print(f"  Pending thesis input: {len(all_pending_keys)} position(s)")
    print("\nNext step: run '/log-positions' in Claude Code to add thesis context.")


if __name__ == "__main__":
    main()
