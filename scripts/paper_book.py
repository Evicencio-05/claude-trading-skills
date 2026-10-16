#!/usr/bin/env python3
"""Record a paper options book from TA confluence. Never places brokerage orders.

Robinhood Agentic ``create_alert`` is the alert destination once a book is fresh.
Live ``place_*`` tools stay unused: Agentic orders are real money, and this
project does not autonomously execute before Phase 3B.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

CHASE_ABS_CHANGE_PCT = 4.0
DISCOUNT_FRACTION = 0.4
MAX_WEEKDAY_LAG = 1
ALERT_DESTINATION = "robinhood_create_alert"

_ZONE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[\u2012\u2013\u2014-]\s*(\d+(?:\.\d+)?)")


def weekday_lag(as_of: date, session: date) -> int:
    """Trading sessions strictly after ``as_of`` through ``session``."""
    if as_of >= session:
        return 0
    lag = 0
    day = as_of
    while day < session:
        day += timedelta(days=1)
        if day.weekday() < 5:
            lag += 1
    return lag


def _num(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def parse_zone(text):
    if not text:
        return None
    match = _ZONE_RE.search(str(text).replace("*", ""))
    if not match:
        return None
    low = float(match.group(1))
    high = float(match.group(2))
    if low > high:
        low, high = high, low
    return (low, high)


def _primary_target(targets):
    parsed = []
    for item in targets or []:
        if not isinstance(item, dict):
            continue
        level = _num(item.get("level"))
        if level is None:
            continue
        parsed.append((level, str(item.get("note") or "")))
    for needle in ("king", "magnet"):
        for level, note in parsed:
            lowered = note.lower()
            if needle in lowered and "not a profit" not in lowered:
                return level, note
    if parsed:
        return parsed[0]
    return None, None


def _sketch(payload):
    judgment = payload.get("judgment") or {}
    sketch = judgment.get("rr_sketch") or {}
    zone = parse_zone(sketch.get("entry_zone"))
    stop = _num(sketch.get("stop"))
    target, target_note = _primary_target(sketch.get("targets"))
    return zone, stop, target, target_note


def _alert(symbol, role, price, trigger, note):
    return {
        "symbol": symbol,
        "kind": "price",
        "role": role,
        "price": price,
        "trigger": trigger,
        "destination": ALERT_DESTINATION,
        "pushed": False,
        "note": note,
    }


def _contract(bias):
    return {
        "instrument": "option",
        "right": "call" if bias == "long" else "put",
        "tenor": "weekly_or_shorter",
        "moneyness": "atm_to_slightly_itm",
        "size_for_zero": True,
        "management": (
            "Add or roll on a claim through the zone. Trim if the claim fails. "
            "Flat if invalidation breaks. Do not reach far OTM."
        ),
    }


def _entry_plan(bias, low, high, spot, change, allow_open):
    """Where a fresh long/short is allowed to open, or which test to alert."""
    band = DISCOUNT_FRACTION * (high - low)
    chase = change is not None and abs(change) > CHASE_ABS_CHANGE_PCT
    if bias == "long":
        if spot < low:
            return "wait", low, "cross_above", "wait_for_test"
        if spot > high:
            return "wait", high, "cross_below", "wait_for_retest"
        if allow_open and spot <= low + band and not chase:
            return "open", spot, None, "paper_open"
        return "wait", low, "cross_below", "wait_for_test"
    if bias == "short":
        if spot > high:
            return "wait", high, "cross_below", "wait_for_test"
        if spot < low:
            return "wait", low, "cross_above", "wait_for_retest"
        if allow_open and spot >= high - band and not chase:
            return "open", spot, None, "paper_open"
        return "wait", high, "cross_above", "wait_for_test"
    return "incomplete", None, None, "missing_bias"


def _entry_note(verdict, reason, trigger):
    if verdict == "WATCH" and reason == "wait_for_test" and trigger == "cross_above":
        return "WATCH reclaim test. Not a paper fill."
    if verdict == "WATCH":
        return "WATCH test only. Not a paper fill."
    if reason == "wait_for_retest":
        return "Extended. Alert the retest. Do not chase."
    return "Wait for the test. Do not buy the expansion bar."


def _invalidation_trigger(bias):
    return "cross_below" if bias == "long" else "cross_above"


def _target_trigger(bias):
    return "cross_above" if bias == "long" else "cross_below"


def _base_row(payload, zone, stop, target, target_note):
    judgment = payload.get("judgment") or {}
    return {
        "ticker": payload.get("ticker"),
        "as_of": payload.get("as_of"),
        "source": payload.get("_source"),
        "verdict": payload.get("verdict"),
        "bias": payload.get("bias"),
        "spot": _num(payload.get("spot")),
        "change_pct": _num(payload.get("change_pct")),
        "entry_zone": list(zone) if zone else None,
        "paper_entry": None,
        "invalidation": stop,
        "target": target,
        "target_note": target_note,
        "operator_thesis": payload.get("operator_thesis") or "",
        "one_thing_to_verify": judgment.get("one_thing_to_verify") or "",
        "contract": None,
        "alerts": [],
        "shadow": None,
    }


def _decide_fresh(payload):
    zone, stop, target, target_note = _sketch(payload)
    row = _base_row(payload, zone, stop, target, target_note)
    verdict = payload.get("verdict")
    bias = payload.get("bias")
    hard_stops = payload.get("hard_stops") or []

    if verdict == "NO_TRADE":
        row["status"] = "flat"
        row["action"] = "flat"
        row["reason"] = "no_trade"
        return row

    # A hard stop on a PLAY caps it at WATCH. WATCH already is the cap.
    if verdict == "PLAY" and hard_stops:
        verdict = "WATCH"
        row["verdict"] = "PLAY"
        row["_hard_stop"] = True

    if verdict not in {"PLAY", "WATCH"}:
        row["status"] = "flat"
        row["action"] = "flat"
        row["reason"] = "unsupported_verdict"
        row.pop("_hard_stop", None)
        return row

    if zone is None or row["spot"] is None or bias not in {"long", "short"}:
        row["status"] = "watch"
        row["action"] = "flat"
        row["reason"] = "missing_entry_zone" if zone is None else "missing_bias"
        if row["spot"] is None and zone is not None:
            row["reason"] = "missing_spot"
        row.pop("_hard_stop", None)
        return row

    allow_open = verdict == "PLAY" and stop is not None and target is not None
    kind, price, trigger, reason = _entry_plan(
        bias, zone[0], zone[1], row["spot"], row["change_pct"], allow_open
    )

    if verdict == "PLAY" and stop is None:
        row["status"] = "watch"
        row["action"] = "alert_only" if trigger else "flat"
        row["reason"] = "missing_invalidation"
        if trigger:
            row["alerts"] = [
                _alert(
                    row["ticker"],
                    "entry_test",
                    price,
                    trigger,
                    "PLAY has no invalidation. Alert the test only.",
                )
            ]
        return row

    if kind == "open":
        row["status"] = "paper_open"
        row["action"] = "paper_open"
        row["reason"] = "paper_open"
        row["paper_entry"] = price
        row["contract"] = _contract(bias)
        row["alerts"] = [
            _alert(
                row["ticker"],
                "invalidation",
                stop,
                _invalidation_trigger(bias),
                "Paper invalidation. Flat the option if this breaks.",
            ),
            _alert(
                row["ticker"],
                "target",
                target,
                _target_trigger(bias),
                target_note or "First target.",
            ),
        ]
        return row

    row["status"] = "armed_wait" if verdict == "PLAY" else "watch"
    row["action"] = "alert_only"
    row["reason"] = reason
    if verdict == "WATCH":
        row["contract"] = None
    else:
        row["contract"] = _contract(bias)
    note = _entry_note(verdict, reason, trigger)
    alerts = [_alert(row["ticker"], "entry_test", price, trigger, note)]
    if verdict == "PLAY" and stop is not None:
        alerts.append(
            _alert(
                row["ticker"],
                "invalidation",
                stop,
                _invalidation_trigger(bias),
                "Idea dies here before the paper fill.",
            )
        )
    row["alerts"] = alerts
    if row.get("_hard_stop"):
        row["status"] = "watch"
        row["reason"] = "hard_stop"
        row["contract"] = None
        row["paper_entry"] = None
        row["alerts"] = [alert for alert in alerts if alert["role"] == "entry_test"]
    row.pop("_hard_stop", None)
    return row


def decide_play(payload, session, include_shadow=True):
    as_of = date.fromisoformat(payload["as_of"])
    lag = weekday_lag(as_of, session)
    row = _decide_fresh(payload)
    row["weekday_lag"] = lag
    row["session_date"] = session.isoformat()
    if lag > MAX_WEEKDAY_LAG:
        row["status"] = "stale"
        row["action"] = "flat"
        row["reason"] = "stale_ta"
        row["alerts"] = []
        row["paper_entry"] = None
        row["contract"] = None
        row["shadow"] = _decide_fresh(payload) if include_shadow else None
        return row
    row["shadow"] = None
    return row


def load_latest_confluence(confluence_dir: Path):
    chosen = {}
    for path in sorted(confluence_dir.glob("*_confluence_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        ticker = payload.get("ticker")
        as_of = payload.get("as_of")
        if not ticker or not as_of:
            continue
        payload = dict(payload)
        payload["_source"] = path.name
        prev = chosen.get(ticker)
        if prev is None or (as_of, path.name) >= (prev["as_of"], prev["_source"]):
            chosen[ticker] = payload
    return [chosen[ticker] for ticker in sorted(chosen)]


def pattern_notes(rows):
    rug_names = []
    rsi = 0
    kings = 0
    for row in rows:
        texts = [row.get("operator_thesis") or "", row.get("one_thing_to_verify") or ""]
        shadow = row.get("shadow") or {}
        texts.append(shadow.get("operator_thesis") or "")
        texts.append(shadow.get("target_note") or "")
        blob = " ".join(texts)
        if re.search(r"\brug\b", blob, re.IGNORECASE):
            rug_names.append(row["ticker"])
        if re.search(r"\bRSI\b", blob):
            rsi += 1
        if (
            "king" in (row.get("target_note") or "").lower()
            or "king" in (shadow.get("target_note") or "").lower()
        ):
            kings += 1
    return {
        "ticker_count": len(rows),
        "named_rug_setups": rug_names,
        "rsi_mentions": rsi,
        "king_targets": kings,
    }


def build_book(confluence_dir: Path, session: date):
    rows = [decide_play(payload, session) for payload in load_latest_confluence(confluence_dir)]
    alerts = [alert for row in rows for alert in row["alerts"]]
    return {
        "session_date": session.isoformat(),
        "mode": "paper",
        "broker_orders": "none",
        "alert_destination": ALERT_DESTINATION,
        "phase_gate": "No live MCP orders before Phase 3B. Paper is this book only.",
        "open_count": sum(1 for row in rows if row["status"] == "paper_open"),
        "armed_count": sum(1 for row in rows if row["status"] == "armed_wait"),
        "rules": {
            "max_weekday_lag": MAX_WEEKDAY_LAG,
            "chase_abs_change_pct": CHASE_ABS_CHANGE_PCT,
            "discount_fraction": DISCOUNT_FRACTION,
            "contract": "weekly or shorter, ATM to slightly ITM, size for 0",
        },
        "alerts": alerts,
        "rows": rows,
        "pattern_notes": pattern_notes(rows),
    }


def _fmt(value):
    if value is None:
        return "-"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _zone_text(zone):
    if not zone:
        return "-"
    return f"{_fmt(zone[0])}-{_fmt(zone[1])}"


def render_markdown(book):
    lines = [
        f"# Paper book — {book['session_date']}",
        "",
        "No brokerage order was sent. Robinhood Agentic places live orders on Portfolio C,",
        "and this book only records paper options. Alerts below are unpushed",
        f"`{book['alert_destination']}` payloads.",
        "",
        f"**Open:** {book['open_count']} · **Armed:** {book['armed_count']} · "
        f"**Live alerts:** {len(book['alerts'])}",
        "",
        "## Rules encoded from the operator read",
        "",
        "- Daily direction comes from the confluence verdict. A fresh `NO_TRADE` stays flat.",
        "- Enter at the test (discount 40% of the zone for longs, premium 40% for shorts).",
        f"- A bar moving more than {CHASE_ABS_CHANGE_PCT:g}% does not get a paper fill.",
        "- Add/roll is a later claim through the zone, not the first fill at the high.",
        "- Target prefers a king node over the first fib when both are on the sketch.",
        "- Contract is weekly or shorter, ATM to slightly ITM, sized for 0 (premium is the risk).",
        "- TA older than one trading session is stale. Stale levels do not arm and do not alert.",
        "",
        "## This session",
        "",
        "| Ticker | As of | Verdict | Status | Why |",
        "|--------|-------|---------|--------|-----|",
    ]
    for row in book["rows"]:
        lines.append(
            f"| {row['ticker']} | {row['as_of']} | {row['verdict']} | {row['status']} | {row['reason']} |"
        )
    lines.extend(["", "## If that tape had been fresh", ""])
    lines.append("| Ticker | Shadow | Entry zone | Test / fill | Invalidation | Target |")
    lines.append("|--------|--------|------------|-------------|--------------|--------|")
    for row in book["rows"]:
        shown = row["shadow"] or row
        fill = shown.get("paper_entry")
        test = next(
            (
                alert["price"]
                for alert in shown.get("alerts") or []
                if alert["role"] == "entry_test"
            ),
            None,
        )
        lines.append(
            "| {ticker} | {status} | {zone} | {touch} | {stop} | {target} |".format(
                ticker=row["ticker"],
                status=shown.get("status"),
                zone=_zone_text(shown.get("entry_zone")),
                touch=_fmt(fill if fill is not None else test),
                stop=_fmt(shown.get("invalidation")),
                target=_fmt(shown.get("target")),
            )
        )
    notes = book["pattern_notes"]
    waited = []
    opened = []
    flat_names = []
    watches = []
    for row in book["rows"]:
        shown = row["shadow"] or row
        if shown.get("status") == "armed_wait":
            waited.append(row["ticker"])
        elif shown.get("status") == "paper_open":
            opened.append(f"{row['ticker']} @ {_fmt(shown.get('paper_entry'))}")
        elif shown.get("status") == "flat":
            flat_names.append(row["ticker"])
        elif shown.get("status") == "watch":
            test = next(
                (
                    alert["price"]
                    for alert in shown.get("alerts") or []
                    if alert["role"] == "entry_test"
                ),
                None,
            )
            watches.append(f"{row['ticker']} {_fmt(test)}")
    lines.extend(
        [
            "",
            "## Patterns in this tape",
            "",
            f"- Names on the latest confluence tape: {notes['ticker_count']}.",
            f"- King-node targets on the sketch: {notes['king_targets']}.",
            f"- RSI called out in the thesis or the one-thing-to-verify: {notes['rsi_mentions']}.",
            "- Named rug / reverse-rug setups: "
            + (", ".join(notes["named_rug_setups"]) if notes["named_rug_setups"] else "none."),
            "- Fresh shadow would paper-open: " + (", ".join(opened) if opened else "none."),
            "- Fresh shadow would wait for the test: " + (", ".join(waited) if waited else "none."),
            "- Fresh shadow stays flat: " + (", ".join(flat_names) if flat_names else "none."),
            "- Fresh shadow watches: " + (", ".join(watches) if watches else "none."),
            "",
            "## Questions",
            "",
            "1. Newest confluence `as_of` in this book is "
            + (max((row["as_of"] for row in book["rows"]), default="none"))
            + ". If that is not last night or this pre-market, where is the later TA paste?",
            "2. A paper fill requires the discount/premium 40% of the zone and a bar inside",
            f"   {CHASE_ABS_CHANGE_PCT:g}% absolute. Should a claim through the far side open",
            "   an add the same day, or only after you say the claim held?",
            "3. Invalidation in these artifacts is a daily-close level. For weeklies, do you",
            "   want the paper book to flatten on an intraday break instead?",
            "4. 4H agreement is not in the operator JSON. Should a missing 4H note block a",
            "   paper open, or only the scalp add?",
            "5. Robinhood `create_alert` can notify the Agentic account without an order.",
            "   MCP trade approvals default off, which lets a connected agent place live",
            "   orders. Confirm approvals stay on, and confirm the next fresh book may push",
            "   price alerts only.",
            "6. Earnings: sell immediately on the open. Should any name with earnings inside",
            "   the contract life be an automatic pass?",
            "7. Rug and reverse-rug need a target node larger than the opposing -GEX node.",
            "   Mark that node on the next map paste so the book can require it.",
            "",
        ]
    )
    return "\n".join(lines)


def write_book(book, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / f"paper_book_{book['session_date']}"
    stem.with_suffix(".json").write_text(json.dumps(book, indent=2) + "\n", encoding="utf-8")
    stem.with_suffix(".md").write_text(render_markdown(book), encoding="utf-8")
    return stem.with_suffix(".md")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Record a paper options book from confluence")
    parser.add_argument("--session-date", required=True, help="YYYY-MM-DD paper session")
    parser.add_argument("--confluence-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    if not args.confluence_dir.is_dir():
        print(f"ERROR: confluence dir not found: {args.confluence_dir}", file=sys.stderr)
        return 1
    session = date.fromisoformat(args.session_date)
    book = build_book(args.confluence_dir, session)
    path = write_book(book, args.output_dir)
    print(
        f"paper book {book['session_date']}: open={book['open_count']} "
        f"armed={book['armed_count']} alerts={len(book['alerts'])} -> {path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
