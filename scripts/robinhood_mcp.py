#!/usr/bin/env python3
"""
Robinhood MCP CLI — reliable broker reads without Cursor in-editor MCP.

Uses local mcp-remote + structuredContent proxy (not Cursor spawn).

Examples:
  uv run python3 scripts/robinhood_mcp.py accounts
  uv run python3 scripts/robinhood_mcp.py positions --all
  uv run python3 scripts/robinhood_mcp.py portfolio --account 487509309
  uv run python3 scripts/robinhood_mcp.py ingest-pending --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from robinhood_accounts import thesis_store_for_account
from robinhood_mcp_client import (
    RobinhoodMcpClient,
    RobinhoodMcpError,
    extract_accounts,
    extract_positions,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = _REPO_ROOT / "state"
PENDING_FILE = STATE_DIR / "pending_ingest.json"


def _mask_account(num: str) -> str:
    s = str(num)
    return f"••••{s[-4:]}" if len(s) >= 4 else s


def _position_key(ticker: str, asset_type: str) -> str:
    return f"{ticker}|{asset_type}"


def _format_mcp_equity_position(pos: dict, account_number: str) -> dict:
    ticker = str(pos.get("symbol", "UNKNOWN")).upper()
    qty = float(pos.get("quantity", 0) or 0)
    avg = float(pos.get("average_buy_price", 0) or 0)
    account = thesis_store_for_account(account_number)
    return {
        "key": _position_key(ticker, "stock"),
        "ticker": ticker,
        "asset_type": "stock",
        "direction": "long" if qty >= 0 else "short",
        "account": account,
        "size": abs(qty),
        "avg_cost": round(avg, 4),
        "total_cost": round(avg * abs(qty), 2),
        "synced_at": datetime.now().isoformat(),
        "confidence": None,
        "thesis": None,
        "stop": None,
        "target": None,
        "tags": [],
        "status": "PENDING_THESIS",
        "source": "robinhood_mcp",
    }


def cmd_accounts(client: RobinhoodMcpClient, args: argparse.Namespace) -> int:
    payload = client.tool_data("get_accounts")
    accounts = extract_accounts(payload)
    accounts.sort(
        key=lambda a: (
            not a.get("is_default", False),
            not a.get("agentic_allowed", False),
            a.get("brokerage_account_type", ""),
        )
    )
    if args.format == "json":
        out = []
        for a in accounts:
            num = str(a.get("account_number", ""))
            out.append(
                {
                    **a,
                    "account_display": _mask_account(num),
                    "thesis_store": thesis_store_for_account(num),
                }
            )
        print(json.dumps(out, indent=2))
        return 0

    print("# Robinhood accounts\n")
    for a in accounts:
        num = str(a.get("account_number", ""))
        nick = a.get("nickname") or ""
        btype = a.get("brokerage_account_type", "")
        default = " (default)" if a.get("is_default") else ""
        agentic = " | Agentic trading" if a.get("agentic_allowed") else ""
        print(
            f"- **{_mask_account(num)}** — {btype} {nick}{default} → "
            f"`{thesis_store_for_account(num)}`{agentic}"
        )
    return 0


def cmd_positions(client: RobinhoodMcpClient, args: argparse.Namespace) -> int:
    if args.all:
        accts = extract_accounts(client.tool_data("get_accounts"))
        account_numbers = [str(a["account_number"]) for a in accts if a.get("account_number")]
    elif args.account:
        account_numbers = [args.account]
    else:
        print("Specify --account NUMBER or --all", file=sys.stderr)
        return 1

    all_positions: list[dict] = []
    for num in account_numbers:
        payload = client.tool_data("get_equity_positions", {"account_number": num})
        for pos in extract_positions(payload):
            pos["_account_number"] = num
            pos["_thesis_store"] = thesis_store_for_account(num)
            all_positions.append(pos)

    if args.format == "json":
        print(json.dumps(all_positions, indent=2, default=str))
        return 0

    print("# Equity positions\n")
    for pos in all_positions:
        sym = pos.get("symbol", "?")
        qty = pos.get("quantity", "?")
        acct = _mask_account(str(pos.get("_account_number", "")))
        store = pos.get("_thesis_store", "")
        print(f"- **{sym}** qty={qty} — {acct} (`{store}`)")
    return 0


def cmd_portfolio(client: RobinhoodMcpClient, args: argparse.Namespace) -> int:
    payload = client.tool_data("get_portfolio", {"account_number": args.account})
    data = payload.get("data", payload)
    if args.format == "json":
        print(json.dumps(data, indent=2, default=str))
        return 0
    print(f"# Portfolio — {_mask_account(args.account)}\n")
    print(json.dumps(data, indent=2, default=str))
    return 0


def cmd_ingest_pending(client: RobinhoodMcpClient, args: argparse.Namespace) -> int:
    accts = extract_accounts(client.tool_data("get_accounts"))
    new_rows: list[dict] = []
    for a in accts:
        num = str(a.get("account_number", ""))
        if not num:
            continue
        payload = client.tool_data("get_equity_positions", {"account_number": num})
        for pos in extract_positions(payload):
            qty = float(pos.get("quantity", 0) or 0)
            if qty == 0:
                continue
            new_rows.append(_format_mcp_equity_position(pos, num))

    if args.dry_run:
        print(json.dumps({"positions": new_rows}, indent=2, default=str))
        print(f"\n{len(new_rows)} position(s) would be merged into {PENDING_FILE}")
        return 0

    existing = {"positions": [], "last_sync": None}
    if PENDING_FILE.exists():
        try:
            existing = json.loads(PENDING_FILE.read_text())
        except json.JSONDecodeError:
            pass
    merged = list(existing.get("positions") or [])
    keys = {p.get("key") for p in merged}
    added = 0
    for row in new_rows:
        if row["key"] not in keys:
            merged.append(row)
            keys.add(row["key"])
            added += 1
    out = {
        "positions": merged,
        "last_sync": datetime.now().isoformat(),
        "last_mcp_ingest": datetime.now().isoformat(),
    }
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps(out, indent=2, default=str))
    print(f"✓ Merged {added} new position(s) into {PENDING_FILE} ({len(merged)} total)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Robinhood MCP CLI")
    parser.add_argument("--timeout", type=float, default=30.0, help="MCP RPC timeout seconds")
    sub = parser.add_subparsers(dest="command", required=True)

    def _fmt_args(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--format",
            choices=("text", "json"),
            default="text",
            help="Output format",
        )

    _fmt_args(sub.add_parser("accounts", help="List brokerage accounts"))

    p_pos = sub.add_parser("positions", help="List equity positions")
    _fmt_args(p_pos)
    p_pos.add_argument("--account", help="account_number from get_accounts")
    p_pos.add_argument("--all", action="store_true", help="All accounts")

    p_pf = sub.add_parser("portfolio", help="Portfolio / buying power for one account")
    _fmt_args(p_pf)
    p_pf.add_argument("--account", required=True, help="account_number")

    p_ing = sub.add_parser("ingest-pending", help="Merge equity positions into pending_ingest.json")
    p_ing.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)

    try:
        with RobinhoodMcpClient(timeout=args.timeout) as client:
            if args.command == "accounts":
                return cmd_accounts(client, args)
            if args.command == "positions":
                return cmd_positions(client, args)
            if args.command == "portfolio":
                return cmd_portfolio(client, args)
            if args.command == "ingest-pending":
                return cmd_ingest_pending(client, args)
    except (RobinhoodMcpError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print(
            "Run: bash scripts/setup_robinhood_mcp.sh",
            file=sys.stderr,
        )
        return 1
    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
