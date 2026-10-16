#!/usr/bin/env python3
"""Record a paper options book from TA confluence. Never places brokerage orders.

Robinhood Agentic ``create_alert`` is the alert destination once a book is fresh.
Live ``place_*`` tools stay unused: Agentic orders are real money, and this
project does not autonomously execute before Phase 3B.
"""

from __future__ import annotations

import argparse
import copy
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
_EARNINGS_RE = re.compile(r"20\d{2}-\d{2}-\d{2}")


def weekly_expiry(anchor: date) -> date:
    """Friday with enough life left for a weekly.

    Monday through Wednesday use this Friday. Thursday, Friday, and the
    weekend use the following Friday.
    """
    weekday = anchor.weekday()
    if weekday <= 2:
        return anchor + timedelta(days=4 - weekday)
    if weekday == 3:
        return anchor + timedelta(days=8)
    if weekday == 4:
        return anchor + timedelta(days=7)
    if weekday == 5:
        return anchor + timedelta(days=6)
    return anchor + timedelta(days=5)


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


def tradingview_condition(trigger):
    if trigger == "cross_below":
        return "Crossing down"
    if trigger == "cross_above":
        return "Crossing up"
    return "Crossing"


def _alert(symbol, role, price, trigger, note):
    condition = tradingview_condition(trigger)
    return {
        "symbol": symbol,
        "kind": "price",
        "role": role,
        "price": price,
        "trigger": trigger,
        "destination": ALERT_DESTINATION,
        "pushed": False,
        "note": note,
        "tradingview": {
            "condition": condition,
            "price": price,
            "message": f"{symbol} {role} {condition} {price}. Paper book. No brokerage order.",
        },
    }


_FAMILY_RANK = {"fib": 0, "shelf": 1, "sma": 2, "trend": 3, "sr": 4}
_SMA_RANK = {"200": 0, "100": 1, "50": 2, "20": 3}
_TF_RANK = {
    "1W": 1,
    "W": 1,
    "WEEKLY": 1,
    "1WK": 1,
    "1D": 2,
    "D": 2,
    "DAILY": 2,
    "1DAY": 2,
    "4H": 3,
    "240": 3,
    "1H": 4,
    "60": 4,
}


def _tf_rank(timeframe):
    token = re.sub(r"[^A-Z0-9]", "", (timeframe or "").upper())
    return _TF_RANK.get(token, 5)


def operator_levels(extracted):
    """Fib, shelf, SMA, trend, and S/R prices from an operator chart."""
    if not isinstance(extracted, dict):
        return []
    levels = []

    chart_rank = _tf_rank(extracted.get("timeframe"))

    def add(price, family, period_rank=0, tf_rank=5):
        number = _num(price)
        if number is None:
            return
        levels.append(
            {
                "price": number,
                "family": family,
                "period_rank": period_rank,
                "tf_rank": tf_rank,
            }
        )

    def add_fib(fib, fallback):
        if not isinstance(fib, dict):
            return
        rank = _tf_rank(fib.get("timeframe")) if fib.get("timeframe") else fallback
        add(fib.get("price"), "fib", tf_rank=rank)

    for fib in extracted.get("fib_levels") or []:
        add_fib(fib, chart_rank)
    for fib_set in extracted.get("fib_sets") or []:
        if not isinstance(fib_set, dict):
            continue
        fallback = _tf_rank(fib_set.get("timeframe")) if fib_set.get("timeframe") else chart_rank
        for fib in fib_set.get("levels") or []:
            add_fib(fib, fallback)
    for key, price in (extracted.get("sma") or {}).items():
        add(price, "sma", _SMA_RANK.get(str(key), 5))
    vp = extracted.get("vp") or {}
    for price in vp.get("peak_nodes") or []:
        add(price, "shelf")
    for price in extracted.get("sr_levels") or []:
        add(price, "sr")
    channel = extracted.get("channel") or {}
    if isinstance(channel, dict):
        labeled = False
        for key in ("upper", "lower", "high", "low"):
            if _num(channel.get(key)) is not None:
                labeled = True
            add(channel.get(key), "trend")
        if not labeled:
            for price in _channel_note_prices(channel.get("notes")):
                add(price, "trend")
    return levels


def _channel_note_prices(notes):
    """Bound prices written as '~16.0' in a channel note. A fib ratio is not a bound."""
    prices = []
    pattern = re.compile(
        r"\b(?:lower|upper|midline|rail|trendline|TL|bound)\b"
        r"[^~]{0,80}~\$?(\d+(?:\.\d+)?)"
        r"(?:\s*(?:\u2013|-)\s*(\d+(?:\.\d+)?))?",
        re.IGNORECASE,
    )
    for match in pattern.finditer(notes or ""):
        for group in match.groups():
            if group is None:
                continue
            number = float(group)
            if number not in prices:
                prices.append(number)
    return prices


def _price_band(spot):
    """Levels farther apart than this are not the same entry area."""
    return max(float(spot) * 0.03, 0.05)


def _price_gap(spot):
    """Cushion that still counts as sitting on a level."""
    return max(float(spot) * 0.01, 0.02)


def opposing_cluster(levels, bias, spot, zone=None):
    """Nearest band with at least two indicator families beyond the entry, against the trade."""
    if spot is None or bias not in {"long", "short"} or not levels:
        return None
    band = _price_band(spot)
    gap = _price_gap(spot)
    if zone and len(zone) == 2:
        edge_low, edge_high = zone
    else:
        edge_low = edge_high = spot
    opposing = []
    for item in levels:
        price = item["price"]
        if bias == "long" and price < edge_low - gap:
            opposing.append(item)
        elif bias == "short" and price > edge_high + gap:
            opposing.append(item)
    opposing.sort(key=lambda item: abs(item["price"] - spot))
    if not opposing:
        return None
    clusters = []
    current = [opposing[0]]
    for item in opposing[1:]:
        if abs(item["price"] - current[0]["price"]) <= band:
            current.append(item)
        else:
            clusters.append(current)
            current = [item]
    clusters.append(current)
    nearest_price = clusters[0][0]["price"]

    def packed(cluster):
        families = sorted(
            {item["family"] for item in cluster},
            key=lambda name: (_FAMILY_RANK.get(name, 9), name),
        )
        by_price = {}
        for item in cluster:
            by_price.setdefault(round(item["price"], 4), []).append(item)

        def price_key(items):
            best_family = min(_FAMILY_RANK.get(item["family"], 9) for item in items)
            same_family = [
                item for item in items if _FAMILY_RANK.get(item["family"], 9) == best_family
            ]
            best_tf = min(item.get("tf_rank", 5) for item in same_family)
            best_period = min(item.get("period_rank", 0) for item in same_family)
            return (
                best_family,
                best_tf,
                -len({item["family"] for item in items}),
                best_period,
                abs(items[0]["price"] - spot),
            )

        best = min(by_price.values(), key=price_key)
        prices = [item["price"] for item in cluster]
        return {"price": best[0]["price"], "families": families, "levels": prices}

    for cluster in clusters:
        if len({item["family"] for item in cluster}) < 2:
            continue
        if abs(cluster[0]["price"] - nearest_price) <= band:
            return packed(cluster)
    return packed(clusters[0])


def rsi_against(rsi, bias):
    """Daily RSI through 50 is the strength filter. Missing RSI does not block.

    A long also stays a watch when the operator marked buyers as not in control,
    or when the white line is under the yellow signal and that flag is absent.
    """
    if bias not in {"long", "short"}:
        return False
    buyer_strength = None
    yellow = None
    if isinstance(rsi, dict):
        white = _num(rsi.get("white"))
        yellow = _num(rsi.get("yellow"))
        if rsi.get("buyer_strength") is True:
            buyer_strength = True
        elif rsi.get("buyer_strength") is False:
            buyer_strength = False
    else:
        white = _num(rsi)
    if bias == "long" and buyer_strength is False:
        return True
    if white is None:
        return False
    if bias == "long":
        if buyer_strength is not True and yellow is not None and white < yellow:
            return True
        return white < 50
    return white > 50


def target_smaller_than_opposing(nodes, bias, spot, target):
    """True when the target node is not larger than a negative node in the path."""
    if not nodes or spot is None or target is None or target == 0 or bias not in {"long", "short"}:
        return False
    if bias == "long" and target <= spot:
        return False
    if bias == "short" and target >= spot:
        return False
    at_target = []
    opposing = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        strike = _num(node.get("strike"))
        value = _num(node.get("value_k"))
        if strike is None or value is None:
            continue
        if abs(strike - target) / abs(target) <= 0.02:
            at_target.append(abs(value))
        between = (bias == "long" and spot < strike < target) or (
            bias == "short" and target < strike < spot
        )
        sign = str(node.get("sign") or "")
        if between and (sign == "neg" or value < 0):
            opposing.append(abs(value))
    if not at_target or not opposing:
        return False
    return max(at_target) <= max(opposing)


def _expiry_anchor(anchor):
    if isinstance(anchor, date):
        return anchor
    if isinstance(anchor, str):
        try:
            return date.fromisoformat(anchor)
        except ValueError:
            return None
    return None


def _contract(bias, anchor=None, four_hour=None):
    scalp = "A scalp add uses the 20 SMA and the 50 SMA on the 1-minute options chart. "
    if four_hour == "fight":
        scalp += "Skip that scalp add while the 4H fights. "
    contract = {
        "instrument": "option",
        "right": "call" if bias == "long" else "put",
        "tenor": "weekly_or_shorter",
        "moneyness": "atm_to_slightly_itm",
        "size_for_zero": True,
        "management": (
            "Add or roll on a claim through the zone. "
            + scalp
            + "Trim if the claim fails. Flat if invalidation breaks. Do not reach far OTM."
        ),
    }
    expiry_day = _expiry_anchor(anchor)
    if expiry_day is not None:
        contract["expiry"] = weekly_expiry(expiry_day).isoformat()
    return contract


def _zone_edges(row):
    zone = row.get("entry_zone")
    if not isinstance(zone, (list, tuple)) or len(zone) != 2:
        return None
    low = _num(zone[0])
    high = _num(zone[1])
    if low is None or high is None:
        return None
    return low, high


def _ensure_claim_alert(row):
    if _alert_by_role(row, "claim"):
        return
    edges = _zone_edges(row)
    bias = row.get("bias")
    if edges is None or bias not in {"long", "short"}:
        return
    low, high = edges
    if high == low:
        return
    if bias == "long":
        price, trigger = high, "cross_above"
    else:
        price, trigger = low, "cross_below"
    row.setdefault("alerts", []).append(
        _alert(
            row.get("ticker"),
            "claim",
            price,
            trigger,
            "Claim through the zone. Paper add at this edge.",
        )
    )


def _entry_plan(bias, low, high, spot, change, allow_open):
    """Where a fresh long/short is allowed to open, or which test to alert."""
    band = DISCOUNT_FRACTION * (high - low)
    chase = change is not None and abs(change) > CHASE_ABS_CHANGE_PCT
    if high == low:
        cushion = _price_gap(spot)
        if bias == "long":
            if spot < low - cushion:
                return "wait", low, "cross_above", "wait_for_test"
            if spot > high + cushion:
                return "wait", high, "cross_below", "wait_for_retest"
            if allow_open and not chase:
                return "open", spot, None, "paper_open"
            return "wait", low, "cross_below", "wait_for_test"
        if bias == "short":
            if spot > high + cushion:
                return "wait", high, "cross_below", "wait_for_test"
            if spot < low - cushion:
                return "wait", low, "cross_above", "wait_for_retest"
            if allow_open and not chase:
                return "open", spot, None, "paper_open"
            return "wait", high, "cross_above", "wait_for_test"
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
        "four_hour": payload.get("four_hour") or "absent",
        "sketch_stop": stop,
        "invalidation_cluster": None,
        "contract": None,
        "alerts": [],
        "shadow": None,
    }


def _apply_cluster(row, extracted, bias, stop):
    spot = row.get("spot")
    cluster = opposing_cluster(operator_levels(extracted), bias, spot, row.get("entry_zone"))
    if not cluster:
        return stop
    row["sketch_stop"] = stop
    row["invalidation"] = cluster["price"]
    row["invalidation_cluster"] = {
        "price": cluster["price"],
        "families": cluster["families"],
    }
    return cluster["price"]


def _long_below_green_50(extracted, spot):
    """Green 50 SMA. A blank price still counts when the chart says price is below it.

    The labeled 50 price wins over price_vs_sma. Blue 20 and orange 200 do not
    use this gate: a long can sit under those and still hold the green 50.
    """
    if not isinstance(extracted, dict):
        return False
    sma_50 = _num((extracted.get("sma") or {}).get("50"))
    if sma_50 is not None and spot is not None:
        return spot < sma_50
    relation = (extracted.get("price_vs_sma") or {}).get("50")
    return isinstance(relation, str) and relation.strip().lower() == "below"


def _directional_king(nodes, bias, spot, zone):
    """Starred king in the trade direction. Longs use a positive node above; shorts a negative node below."""
    if not nodes or spot is None or bias not in {"long", "short"}:
        return None
    if zone and len(zone) == 2:
        edge = zone[1] if bias == "long" else zone[0]
    else:
        edge = spot
    best_strike = None
    best_abs = -1.0
    for node in nodes:
        if not isinstance(node, dict) or not node.get("starred"):
            continue
        strike = _num(node.get("strike"))
        value = _num(node.get("value_k"))
        if strike is None or value is None:
            continue
        sign = str(node.get("sign") or "")
        if bias == "long":
            agrees = strike > edge and (sign == "pos" or value > 0)
        else:
            agrees = strike < edge and (sign == "neg" or value < 0)
        if agrees and abs(value) > best_abs:
            best_strike = strike
            best_abs = abs(value)
    return best_strike


def _target_with_king(nodes, bias, spot, target, zone):
    """Use the king when it is larger than the negative nodes in its path."""
    king = _directional_king(nodes, bias, spot, zone)
    if king is None or target_smaller_than_opposing(nodes, bias, spot, king):
        return target
    return king


def _play_cap(verdict, hard_stops, extracted, payload, bias, spot, target):
    if verdict != "PLAY":
        return None
    if hard_stops:
        return "hard_stop"
    if rsi_against((extracted or {}).get("rsi"), bias):
        return "rsi_against"
    if bias == "long" and _long_below_green_50(extracted, spot):
        return "below_50_sma"
    if payload.get("chop"):
        return "chop"
    if target_smaller_than_opposing(payload.get("map_nodes"), bias, spot, target):
        return "target_smaller_than_opposing"
    if payload.get("daily_against"):
        return "daily_against"
    return None


def _decide_fresh(payload, anchor=None):
    zone, stop, target, target_note = _sketch(payload)
    if target_note == "next operator level":
        upgraded = _target_with_king(
            payload.get("map_nodes"), payload.get("bias"), payload.get("spot"), target, zone
        )
        if upgraded != target and upgraded is not None:
            target = upgraded
            target_note = "directional king"
    row = _base_row(payload, zone, stop, target, target_note)
    verdict = payload.get("verdict")
    bias = payload.get("bias")
    hard_stops = payload.get("hard_stops") or []

    if verdict == "NO_TRADE":
        row["status"] = "flat"
        row["action"] = "flat"
        row["reason"] = "no_trade"
        return row

    extracted = (
        payload.get("operator_extracted")
        if isinstance(payload.get("operator_extracted"), dict)
        else {}
    )
    stop = _apply_cluster(row, extracted, bias, stop)
    cap = _play_cap(verdict, hard_stops, extracted, payload, bias, row["spot"], target)
    if cap:
        verdict = "WATCH"
        row["verdict"] = payload.get("verdict")
        row["_cap"] = cap

    if verdict not in {"PLAY", "WATCH"}:
        row["status"] = "flat"
        row["action"] = "flat"
        row["reason"] = "unsupported_verdict"
        row.pop("_cap", None)
        return row

    if zone is None or row["spot"] is None or bias not in {"long", "short"}:
        row["status"] = "watch"
        row["action"] = "flat"
        row["reason"] = "missing_entry_zone" if zone is None else "missing_bias"
        if row["spot"] is None and zone is not None:
            row["reason"] = "missing_spot"
        cap = row.pop("_cap", None)
        if cap:
            row["reason"] = cap
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
        row["contract"] = _contract(bias, anchor, row.get("four_hour"))
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
        _ensure_claim_alert(row)
        return row

    row["status"] = "armed_wait" if verdict == "PLAY" else "watch"
    row["action"] = "alert_only"
    row["reason"] = reason
    if verdict == "WATCH":
        row["contract"] = None
    else:
        row["contract"] = _contract(bias, anchor, row.get("four_hour"))
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
    cap = row.pop("_cap", None)
    if cap:
        row["status"] = "watch"
        row["reason"] = cap
        row["contract"] = None
        row["paper_entry"] = None
        row["alerts"] = [alert for alert in row["alerts"] if alert["role"] == "entry_test"]
    return row


def earnings_dates(payload):
    """ISO dates only. A month name such as 'early September' is not a session."""
    texts = []
    direct = payload.get("earnings_on")
    if isinstance(direct, str):
        texts.append(direct)
    extracted = payload.get("operator_extracted")
    if isinstance(extracted, dict):
        marker = extracted.get("earnings_markers")
        if isinstance(marker, str):
            texts.append(marker)
        elif isinstance(marker, list):
            texts.extend(str(item) for item in marker)
    found = set()
    for text in texts:
        for match in _EARNINGS_RE.findall(text):
            try:
                found.add(date.fromisoformat(match))
            except ValueError:
                continue
    return sorted(found)


def _flatten_earnings(row):
    row["status"] = "flat"
    row["action"] = "flat"
    row["reason"] = "earnings_open"
    row["alerts"] = []
    row["paper_entry"] = None
    row["contract"] = None
    return row


def decide_play(payload, session, include_shadow=True):
    as_of = date.fromisoformat(payload["as_of"])
    lag = weekday_lag(as_of, session)
    row = _decide_fresh(payload, session)
    row["weekday_lag"] = lag
    row["session_date"] = session.isoformat()
    if lag > MAX_WEEKDAY_LAG:
        row["status"] = "stale"
        row["action"] = "flat"
        row["reason"] = "stale_ta"
        row["alerts"] = []
        row["paper_entry"] = None
        row["contract"] = None
        row["shadow"] = _decide_fresh(payload, as_of) if include_shadow else None
        return row
    row["shadow"] = None
    upcoming = [day for day in earnings_dates(payload) if day >= session]
    if upcoming:
        row["earnings_on"] = upcoming[0].isoformat()
    if row.get("earnings_on") == session.isoformat() and row["status"] in {
        "paper_open",
        "armed_wait",
    }:
        return _flatten_earnings(row)
    return row


def _position_done(row, session):
    """Expiry and the earnings open end a carried paper position."""
    if row.get("earnings_on") == session.isoformat():
        row["carried"] = True
        row["session_date"] = session.isoformat()
        return _flatten_earnings(row)
    expiry = (row.get("contract") or {}).get("expiry")
    if isinstance(expiry, str):
        try:
            expiry_day = date.fromisoformat(expiry)
        except ValueError:
            expiry_day = None
        if expiry_day is not None and session > expiry_day:
            row["status"] = "expired"
            row["action"] = "flat"
            row["reason"] = "expired"
            row["alerts"] = []
    row["carried"] = True
    row["session_date"] = session.isoformat()
    return row


def merge_carried(rows, prior, session):
    """Keep a recorded paper_open until it ends or a newer tape replaces it."""
    if not isinstance(prior, dict):
        return rows
    prior_open = {}
    for row in prior.get("rows") or []:
        ticker = row.get("ticker")
        if ticker and row.get("status") == "paper_open":
            prior_open[ticker] = row
    if not prior_open:
        return rows
    merged = []
    for row in rows:
        previous = prior_open.pop(row.get("ticker"), None)
        if previous is None:
            merged.append(row)
            continue
        newer = (row.get("as_of") or "") > (previous.get("as_of") or "")
        if newer and row.get("status") != "stale":
            merged.append(row)
            continue
        merged.append(_position_done(copy.deepcopy(previous), session))
    for ticker in sorted(prior_open):
        merged.append(_position_done(copy.deepcopy(prior_open[ticker]), session))
    merged.sort(key=lambda row: row.get("ticker") or "")
    return merged


def _repo_root(confluence_dir: Path):
    if (
        confluence_dir.name == "confluence"
        and confluence_dir.parent.name == "charts"
        and confluence_dir.parent.parent.name == "reports"
    ):
        return confluence_dir.parent.parent.parent
    return confluence_dir


def _read_artifact(root: Path, rel):
    if not isinstance(rel, str) or not rel or rel.startswith("/") or ".." in Path(rel).parts:
        return None
    path = (root / rel).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _extracted(doc):
    if not isinstance(doc, dict):
        return None
    extracted = doc.get("extracted")
    return extracted if isinstance(extracted, dict) else doc


def attach_tape(payload, root: Path):
    artifacts = payload.get("artifacts") or {}
    operator = _extracted(_read_artifact(root, artifacts.get("operator")))
    if operator:
        payload["operator_extracted"] = operator
    nodes = []
    for key in ("gex", "vex"):
        doc = _extracted(_read_artifact(root, artifacts.get(key)))
        if not doc:
            continue
        king = doc.get("king_node")
        if isinstance(king, dict):
            nodes.append(king)
        for node in doc.get("top_nodes") or []:
            if isinstance(node, dict):
                nodes.append(node)
    if nodes:
        payload["map_nodes"] = nodes
    return payload


_THESIS_LEVEL_RE = re.compile(
    r"\b(?:below|above|under|over|test|retest|target|targets|shelf|at)\s+"
    r"(?:the\s+)?(?:mid-band\s+)?(?:near\s+)?\$?(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def _bias_from_thesis(text):
    lowered = text or ""
    long_at = re.search(r"\blong\b", lowered, re.IGNORECASE)
    short_at = re.search(r"\bshort\b", lowered, re.IGNORECASE)
    if long_at and short_at:
        return "long" if long_at.start() < short_at.start() else "short"
    if long_at:
        return "long"
    if short_at:
        return "short"
    if re.search(r"\bbreak below\b", lowered, re.IGNORECASE):
        return "short"
    if re.search(r"\bbreak above\b", lowered, re.IGNORECASE):
        return "long"
    return None


_CHOP_RE = re.compile(
    r"\b(?:in|into|still)\s+chop\b|\bmid-?chop\b|\bchoppy\b|\bno trend\b|\brange-bound\b",
    re.IGNORECASE,
)
_FOUR_HOUR_WORD = r"(?:4\s*h|4-hour|4 hour)"


def _chart_is_daily(timeframe):
    """A daily operator chart is the directional read. 4H and weekly are not."""
    token = re.sub(r"[^A-Z0-9]", "", (timeframe or "").upper())
    return token in {"1D", "D", "DAILY", "1DAY"}


_DAILY_DOWN_RE = re.compile(
    r"\bdaily\b(?:\s+\w+){0,4}\s+(?:is\s+|remains\s+|stays\s+)?(?:down|weak|bearish)\b"
    r"|\bdaily\b(?:\s+\w+){0,4}\s+holding\s+below\b"
    r"|\bdaily\b(?:\s+\w+){0,3}\s+(?:below|under)\b",
    re.IGNORECASE,
)
_DAILY_UP_RE = re.compile(
    r"\bdaily\b(?:\s+\w+){0,4}\s+(?:is\s+|remains\s+|stays\s+)?(?:up|strong|bullish)\b"
    r"|\bdaily\b(?:\s+\w+){0,4}\s+holding\s+above\b"
    r"|\bdaily\b(?:\s+\w+){0,3}\s+(?:above|over)\b",
    re.IGNORECASE,
)


def _daily_against(thesis, bias):
    """The daily is the direction. A 4-hour idea against that daily does not open.

    "Daily is up" and "daily holding above" are up. "Daily is down" and
    "daily holding below" are down. Both sides in one thesis do not block.
    """
    if bias not in {"long", "short"}:
        return False
    text = thesis or ""
    down = _DAILY_DOWN_RE.search(text)
    up = _DAILY_UP_RE.search(text)
    if bias == "long":
        return down is not None and up is None
    return up is not None and down is None


def _four_hour_state(thesis, bias):
    """4H agreement is extra confluence for the scalp. It is not the daily direction."""
    text = thesis or ""
    window = rf"\b{_FOUR_HOUR_WORD}\b.{{0,48}}"
    if re.search(
        window + r"\b(?:does not agree|doesn't agree|disagrees|fighting|fights|against)\b",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        return "fight"
    if re.search(window + r"\bagrees?\b", text, re.IGNORECASE | re.DOTALL):
        return "agree"
    down = re.search(
        window + r"\b(?:is\s+|remains\s+|stays\s+)?(?:down|weak|bearish)\b",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    up = re.search(
        window + r"\b(?:is\s+|remains\s+|stays\s+)?(?:up|strong|bullish)\b",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if bias == "long" and down is not None and up is None:
        return "fight"
    if bias == "short" and up is not None and down is None:
        return "fight"
    return "absent"


def _thesis_levels(text):
    prices = []
    source = text or ""
    for match in _THESIS_LEVEL_RE.finditer(source):
        if re.match(r"\s*(?:SMA|EMA)\b", source[match.end() :], re.IGNORECASE):
            continue
        prefix = source[max(0, match.start() - 24) : match.start()]
        if re.search(
            r"\b(?:gaps?|volume|a/d|accumulation|distribution)(?:\s+fill)?\s+$",
            prefix,
            re.IGNORECASE,
        ):
            continue
        price = float(match.group(1))
        if price not in prices:
            prices.append(price)
    return prices


def _level_prices(extracted, thesis=""):
    prices = []
    for item in operator_levels(extracted):
        price = item["price"]
        if price not in prices:
            prices.append(price)
    for price in _thesis_levels(thesis):
        if price not in prices:
            prices.append(price)
    return prices


def _plan_zone(bias, spot, prices):
    if bias not in {"long", "short"} or spot is None or not prices:
        return None
    if bias == "long":
        under = [price for price in prices if price <= spot]
        if not under:
            return None
        low = max(under)
        above = [price for price in prices if price > low]
        high = min(above) if above else low
        return _tighten_zone("long", spot, low, high)
    over = [price for price in prices if price >= spot]
    if over:
        high = min(over)
    else:
        under = [price for price in prices if price < spot]
        if not under:
            return None
        high = max(under)
    below = [price for price in prices if price < high]
    low = max(below) if below else high
    return _tighten_zone("short", spot, low, high)


def _tighten_zone(bias, spot, low, high):
    """A far next level is the target. It does not extend the entry away from the test."""
    if high - low <= _price_band(spot):
        return (low, high)
    if bias == "long":
        return (low, low)
    return (high, high)


def _plan_target(bias, prices, zone):
    if not zone or bias not in {"long", "short"}:
        return None
    if bias == "long":
        above = [price for price in prices if price > zone[1] + 1e-9]
        if above:
            return min(above)
        if zone[1] > zone[0]:
            return zone[1]
        return None
    below = [price for price in prices if price < zone[0] - 1e-9]
    if below:
        return max(below)
    if zone[0] < zone[1]:
        return zone[0]
    return None


def plan_from_operator(doc):
    """Paper payload from an operator chart. No confluence verdict required.

    A daily chart is the direction. A 4-hour or weekly chart becomes a PLAY only
    when the thesis also states that daily direction. Otherwise it stays a watch.
    """
    extracted = doc.get("extracted") if isinstance(doc.get("extracted"), dict) else {}
    thesis = extracted.get("operator_thesis") or ""
    bias = _bias_from_thesis(thesis)
    spot = _num(extracted.get("last"))
    prices = _level_prices(extracted, thesis)
    zone = _plan_zone(bias, spot, prices)
    target = _plan_target(bias, prices, zone)
    timeframe = str(extracted.get("timeframe") or "")
    daily_stated = re.search(r"\bdaily\b", thesis, re.IGNORECASE) is not None
    daily = daily_stated or _chart_is_daily(timeframe)
    four_hour = _four_hour_state(thesis, bias)
    daily_against = _daily_against(thesis, bias)
    chop = _CHOP_RE.search(thesis) is not None
    verdict = "PLAY" if bias and daily else "WATCH"
    if timeframe.upper() in {"4H", "240"} and not daily_stated:
        verdict = "WATCH"
    targets = [{"level": target, "note": "next operator level"}] if target is not None else []
    return {
        "ticker": doc.get("ticker"),
        "as_of": doc.get("as_of"),
        "verdict": verdict,
        "bias": bias,
        "spot": spot,
        "change_pct": _num(extracted.get("change_pct")),
        "hard_stops": [],
        "operator_thesis": thesis,
        "operator_extracted": extracted,
        "four_hour": four_hour,
        "daily_against": daily_against,
        "chop": chop,
        "judgment": {
            "one_thing_to_verify": "" if daily else "Daily direction is in the thesis.",
            "rr_sketch": {
                "entry_zone": f"{zone[0]}-{zone[1]}" if zone else None,
                "stop": None,
                "targets": targets,
            },
        },
        "_source": doc.get("_source"),
    }


def load_operator_docs(operator_dir: Path):
    docs = []
    if not operator_dir.is_dir():
        return docs
    for path in sorted(operator_dir.glob("*_operator_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        ticker = payload.get("ticker")
        as_of = payload.get("as_of")
        if not ticker or not as_of:
            continue
        payload = dict(payload)
        payload["_source"] = path.name
        docs.append(payload)
    return docs


def load_latest_operator(operator_dir: Path):
    chosen = {}
    for payload in load_operator_docs(operator_dir):
        ticker = payload.get("ticker")
        prev = chosen.get(ticker)
        stamp = (payload.get("as_of") or "", payload.get("_source") or "")
        if prev is None or stamp >= (prev.get("as_of") or "", prev.get("_source") or ""):
            chosen[ticker] = payload
    return [chosen[ticker] for ticker in sorted(chosen)]


def _carry_fresh_nodes(plan, prev):
    """A newer chart keeps yesterday's GEX/VEX. Older maps do not follow it."""
    nodes = prev.get("map_nodes") if isinstance(prev, dict) else None
    prev_as_of = prev.get("as_of") if isinstance(prev, dict) else None
    if not nodes or not prev_as_of or not plan.get("as_of"):
        return
    try:
        lag = weekday_lag(date.fromisoformat(prev_as_of), date.fromisoformat(plan["as_of"]))
    except ValueError:
        return
    if lag <= MAX_WEEKDAY_LAG:
        plan["map_nodes"] = list(nodes)


def _with_longer_tf_fibs(latest, docs):
    """A newer 4H chart keeps daily or weekly fibs from the prior session."""
    extracted = dict(latest.get("extracted") or {})
    chart_tf = extracted.get("timeframe") or ""
    try:
        latest_day = date.fromisoformat(latest.get("as_of") or "")
    except ValueError:
        return latest
    fibs = []
    for fib in extracted.get("fib_levels") or []:
        if isinstance(fib, dict):
            item = dict(fib)
            item.setdefault("timeframe", chart_tf)
            fibs.append(item)
    for doc in docs:
        if doc.get("_source") == latest.get("_source") and doc.get("as_of") == latest.get("as_of"):
            continue
        other = doc.get("extracted") if isinstance(doc.get("extracted"), dict) else {}
        other_tf = other.get("timeframe") or ""
        if _tf_rank(other_tf) >= _tf_rank(chart_tf):
            continue
        try:
            lag = weekday_lag(date.fromisoformat(doc.get("as_of") or ""), latest_day)
        except ValueError:
            continue
        if lag > MAX_WEEKDAY_LAG:
            continue
        for fib in other.get("fib_levels") or []:
            if isinstance(fib, dict) and _num(fib.get("price")) is not None:
                item = dict(fib)
                item["timeframe"] = other_tf
                fibs.append(item)
        for fib_set in other.get("fib_sets") or []:
            if not isinstance(fib_set, dict):
                continue
            set_tf = fib_set.get("timeframe") or other_tf
            for fib in fib_set.get("levels") or []:
                if isinstance(fib, dict) and _num(fib.get("price")) is not None:
                    item = dict(fib)
                    item["timeframe"] = fib.get("timeframe") or set_tf
                    fibs.append(item)
    extracted["fib_levels"] = fibs
    merged = dict(latest)
    merged["extracted"] = extracted
    return merged


def merge_operator_plans(payloads, operator_docs, session):
    """Use an operator plan when it is fresh, or newer than that ticker's confluence."""
    by_ticker = {}
    for payload in payloads:
        ticker = payload.get("ticker")
        if ticker:
            by_ticker[ticker] = payload
    grouped = {}
    for doc in operator_docs or []:
        ticker = doc.get("ticker")
        if ticker:
            grouped.setdefault(ticker, []).append(doc)
    for ticker in sorted(grouped):
        docs = grouped[ticker]
        latest = max(docs, key=lambda doc: (doc.get("as_of") or "", doc.get("_source") or ""))
        doc = _with_longer_tf_fibs(latest, docs)
        plan = plan_from_operator(doc)
        ticker = plan.get("ticker")
        as_of = plan.get("as_of")
        if not ticker or not as_of:
            continue
        prev = by_ticker.get(ticker)
        fresh = weekday_lag(date.fromisoformat(as_of), session) <= MAX_WEEKDAY_LAG
        if prev is None:
            if fresh:
                by_ticker[ticker] = plan
            continue
        if as_of > prev.get("as_of", ""):
            _carry_fresh_nodes(plan, prev)
            by_ticker[ticker] = plan
    return [by_ticker[ticker] for ticker in sorted(by_ticker)]


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


def build_book(confluence_dir: Path, session: date, prior=None):
    root = _repo_root(confluence_dir)
    payloads = [attach_tape(payload, root) for payload in load_latest_confluence(confluence_dir)]
    operator_docs = load_operator_docs(confluence_dir.parent / "operator")
    payloads = merge_operator_plans(payloads, operator_docs, session)
    rows = merge_carried(
        [decide_play(payload, session) for payload in payloads],
        prior,
        session,
    )
    alerts = [alert for row in rows for alert in row["alerts"]]
    return {
        "session_date": session.isoformat(),
        "mode": "paper",
        "broker_orders": "none",
        "alert_destination": ALERT_DESTINATION,
        "phase_gate": "No live MCP orders before Phase 3B. Paper is this book only.",
        "operator_as_of": max(
            (doc.get("as_of") for doc in operator_docs if doc.get("as_of")),
            default=None,
        ),
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
        "- Daily direction comes from the confluence verdict or a daily operator chart.",
        "  A 4-hour or weekly chart stays a watch until the thesis states that daily direction.",
        "  Daily holding above is up. Daily holding below is down.",
        "  A thesis that puts the name in chop stays a watch.",
        "  A 4H fight does not flat the daily swing. It withholds the scalp add.",
        "  A fresh `NO_TRADE` stays flat.",
        "- Enter at the test (discount 40% of the zone for longs, premium 40% for shorts).",
        "  A level more than 3% of price away is the target, not a wider entry.",
        "  A gap, a volume print, or an A/D print is confluence. It is not the entry.",
        f"- A bar moving more than {CHASE_ABS_CHANGE_PCT:g}% does not get a paper fill.",
        "- Add on a claim through the far side of the zone. Trim that add if price",
        "  crosses back through the paper entry. The core stays until invalidation or the target.",
        "- Invalidation is the nearest opposing cluster. Its price is the fib, then the",
        "  volume shelf, then the higher-period SMA (200, then 100, then 50, then 20).",
        "  A longer-timeframe fib beats a shorter one in that same cluster.",
        "  A channel bound written with a tilde price joins that cluster.",
        "  A stacked price beats a lone nearer level of that same kind.",
        "- Target prefers a king node over the first fib when both are on the sketch.",
        "  On a new operator chart, a starred positive king above is the long target,",
        "  and a starred negative king below is the short target, when that king is",
        "  larger than the negative nodes in the path.",
        "  A newer operator chart keeps GEX/VEX nodes from the prior session. A target",
        "  that is not larger than a negative node in the path stays a watch.",
        "- Contract is weekly or shorter, ATM to slightly ITM, sized for 0 (premium is the risk).",
        "- Weekly expiry is this Friday for a Mon–Wed decision, and the next Friday after that.",
        "- An open paper position carries until invalidation, the target, expiry, or a newer tape.",
        "- A dated earnings session does not open. A carried position flattens that morning.",
        "- A long with RSI white under 50, white under the yellow signal, or",
        "  buyer_strength false stays a watch. A marked buyer_strength true holds.",
        "- Operator SMA colors: blue 20, green 50, orange 200. A long under the green 50",
        "  stays a watch, including when that price is blank and the chart says below.",
        "  A long under the blue 20 or the orange 200 still opens while it holds the green 50.",
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
            "## Alert path",
            "",
            "Robinhood tool `create_alert` and a TradingView price alert share each level.",
            "Create the TradingView alert only on rows marked create. Withheld means the tape is stale.",
            "Paste the session Pine on each ticker's chart. It plots that ticker's levels.",
            "Arm Any alert() function call. No webhook is configured.",
            "The alert does not place an order.",
            "",
            "| Ticker | Create | Condition | Role |",
            "|--------|--------|-----------|------|",
        ]
    )
    for row in book["rows"]:
        shown = row["shadow"] or row
        alerts = shown.get("alerts") or []
        create = "withheld" if row["status"] == "stale" else "create"
        if not alerts:
            lines.append(f"| {row['ticker']} | no | - | - |")
            continue
        for alert in alerts:
            tv = alert.get("tradingview") or {}
            lines.append(
                f"| {row['ticker']} | {create} | {tv.get('condition')} {_fmt(alert.get('price'))} | {alert['role']} |"
            )
    lines.extend(
        [
            "",
            "## Questions",
            "",
            "1. Newest confluence `as_of` in this book is "
            + (max((row["as_of"] for row in book["rows"]), default="none"))
            + ". Newest operator chart on disk is "
            + str(book.get("operator_as_of") or "none")
            + ". Paste the day-before or pre-market charts if that is not the live plan.",
            "2. A claim through the far side adds at that edge in the same session and stays",
            "   open. A cross back through the paper entry trims the add and keeps the core.",
            "   Say if you want that add only after you confirm the claim held.",
            "3. Invalidation is the nearest cluster. Inside it, a fib beats a shelf, and a",
            "   200 SMA beats a 20. Should that flatten the weekly on an intraday break,",
            "   or only on a daily close?",
            "4. A missing 4H note does not block the paper open. An explicit 4H fight",
            "   withholds the scalp add and leaves the daily swing on. Say if a 4H fight",
            "   should flat the swing too.",
            "5. Robinhood `create_alert` can notify the Agentic account without an order.",
            "   MCP trade approvals default off, which lets a connected agent place live",
            "   orders. Confirm approvals stay on, and confirm the next fresh book may push",
            "   price alerts only.",
            "6. A dated earnings session does not open, and a carried position flattens that",
            "   morning. A later ISO earnings date stays open until that open. Vague text",
            "   such as early September does not count. Say if the whole earnings week",
            "   should be a pass instead.",
            "7. A target that is not larger than a negative node between spot and the target",
            "   stays a watch. Confirm that size check is the rug rule you want.",
            "",
        ]
    )
    return "\n".join(lines)


def _crossed(trigger, level, quote):
    if trigger == "cross_below":
        return quote <= level
    if trigger == "cross_above":
        return quote >= level
    return False


def _flatten_adds(row):
    for item in row.get("adds") or []:
        if isinstance(item, dict) and item.get("status") == "open":
            item["status"] = "flat"


def _mark_open(row, quote):
    """Invalidation and the target flatten. A claim adds; a failed claim trims."""
    ticker = row.get("ticker")
    invalidation = _alert_by_role(row, "invalidation")
    target = _alert_by_role(row, "target")
    if invalidation and _crossed(invalidation.get("trigger"), invalidation.get("price"), quote):
        invalidation["fired"] = True
        _flatten_adds(row)
        row["status"] = "invalidated"
        row["action"] = "flat"
        row["reason"] = "invalidation_tagged"
        return {
            "ticker": ticker,
            "result": "invalidated",
            "price": invalidation.get("price"),
            "quote": quote,
            "status": row["status"],
        }
    if target and _crossed(target.get("trigger"), target.get("price"), quote):
        target["fired"] = True
        _flatten_adds(row)
        row["status"] = "target_hit"
        row["action"] = "flat"
        row["reason"] = "target_tagged"
        return {
            "ticker": ticker,
            "result": "target_hit",
            "price": target.get("price"),
            "quote": quote,
            "status": row["status"],
        }
    adds = [item for item in (row.get("adds") or []) if isinstance(item, dict)]
    open_adds = [item for item in adds if item.get("status") == "open"]
    entry = _num(row.get("paper_entry"))
    bias = row.get("bias")
    fail_trigger = "cross_below" if bias == "long" else "cross_above"
    if (
        open_adds
        and entry is not None
        and bias in {"long", "short"}
        and _crossed(fail_trigger, entry, quote)
    ):
        for item in open_adds:
            item["status"] = "trimmed"
        claim = _alert_by_role(row, "claim")
        if claim:
            claim["fired"] = False
        row["status"] = "paper_open"
        row["action"] = "paper_open"
        row["reason"] = "claim_failed"
        return {
            "ticker": ticker,
            "result": "claim_failed",
            "price": entry,
            "quote": quote,
            "status": "paper_open",
        }
    _ensure_claim_alert(row)
    claim = _alert_by_role(row, "claim")
    if claim and not open_adds and _crossed(claim.get("trigger"), claim.get("price"), quote):
        claim["fired"] = True
        row.setdefault("adds", []).append({"price": claim.get("price"), "status": "open"})
        row["status"] = "paper_open"
        row["action"] = "paper_open"
        row["reason"] = "claim_add"
        return {
            "ticker": ticker,
            "result": "claim_add",
            "price": claim.get("price"),
            "quote": quote,
            "status": "paper_open",
        }
    return {"ticker": ticker, "result": "unchanged", "quote": quote, "status": "paper_open"}


def _alert_by_role(row, role):
    for alert in row.get("alerts") or []:
        if alert.get("role") == role:
            return alert
    return None


def apply_marks(book, quotes):
    """Advance a fresh book when a quote tags a level. Stale rows stay flat.

    This is the paper alert loop. It does not call Robinhood or TradingView.
    """
    marks = []
    for row in book.get("rows") or []:
        ticker = row.get("ticker")
        quote = _num((quotes or {}).get(ticker)) if isinstance(quotes, dict) else None
        status = row.get("status")
        if status in {"stale", "flat"} or quote is None:
            marks.append(
                {"ticker": ticker, "result": "unchanged", "quote": quote, "status": status}
            )
            continue
        if status == "armed_wait":
            entry = _alert_by_role(row, "entry_test")
            if entry and _crossed(entry.get("trigger"), entry.get("price"), quote):
                entry["fired"] = True
                row["status"] = "paper_open"
                row["action"] = "paper_open"
                row["reason"] = "test_tagged"
                row["paper_entry"] = entry.get("price")
                if row.get("contract") is None and row.get("bias") in {"long", "short"}:
                    row["contract"] = _contract(
                        row["bias"], row.get("session_date"), row.get("four_hour")
                    )
                _ensure_claim_alert(row)
                marks.append(
                    {
                        "ticker": ticker,
                        "result": "paper_open",
                        "price": entry.get("price"),
                        "quote": quote,
                        "status": "paper_open",
                    }
                )
            else:
                marks.append(
                    {"ticker": ticker, "result": "unchanged", "quote": quote, "status": status}
                )
            continue
        if status == "watch":
            entry = _alert_by_role(row, "entry_test")
            if entry and _crossed(entry.get("trigger"), entry.get("price"), quote):
                entry["fired"] = True
                row["reason"] = "test_tagged_watch"
                marks.append(
                    {
                        "ticker": ticker,
                        "result": "watch_tagged",
                        "price": entry.get("price"),
                        "quote": quote,
                        "status": "watch",
                    }
                )
            else:
                marks.append(
                    {"ticker": ticker, "result": "unchanged", "quote": quote, "status": status}
                )
            continue
        if status == "paper_open":
            marks.append(_mark_open(row, quote))
            continue
        marks.append({"ticker": ticker, "result": "unchanged", "quote": quote, "status": status})
    book["marks"] = marks
    book["open_count"] = sum(
        1 for row in book.get("rows") or [] if row.get("status") == "paper_open"
    )
    book["armed_count"] = sum(
        1 for row in book.get("rows") or [] if row.get("status") == "armed_wait"
    )
    return book


def parse_yahoo_chart(payload):
    """Last regular-session price from a Yahoo chart JSON body."""
    if not isinstance(payload, dict):
        return None
    results = (payload.get("chart") or {}).get("result") or []
    if not results or not isinstance(results[0], dict):
        return None
    return _num((results[0].get("meta") or {}).get("regularMarketPrice"))


def fetch_last_prices(tickers, getter):
    """Last prices via an injected HTTP getter. One failure does not drop the rest."""
    quotes = {}
    errors = []
    for ticker in tickers:
        symbol = str(ticker or "").upper()
        if not symbol:
            continue
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
        try:
            payload = json.loads(getter(url))
            price = parse_yahoo_chart(payload)
        except (OSError, ValueError, TypeError) as exc:
            errors.append({"ticker": symbol, "error": str(exc)})
            continue
        if price is None:
            errors.append({"ticker": symbol, "error": "no price"})
            continue
        quotes[symbol] = price
    return {"quotes": quotes, "errors": errors}


def yahoo_getter(url):
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": "paper-book/1.0"})
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.read().decode("utf-8")


_ALERT_ARGUMENT_FIELDS = (
    ("symbol", lambda alert: alert.get("symbol")),
    ("ticker", lambda alert: alert.get("symbol")),
    ("price", lambda alert: alert.get("price")),
    ("trigger_price", lambda alert: alert.get("price")),
    ("direction", lambda alert: "down" if alert.get("trigger") == "cross_below" else "up"),
    ("condition", lambda alert: alert.get("trigger")),
    ("note", lambda alert: alert.get("note")),
)


def create_alert_arguments(alert, properties):
    """Map a paper alert onto whatever fields the live create_alert schema allows.

    Robinhood's published pages name the tool and not its arguments. A push
    waits until tools/list supplies the property names.
    """
    allowed = set(properties or [])
    if not allowed:
        return None
    arguments = {}
    for key, getter in _ALERT_ARGUMENT_FIELDS:
        if key in allowed:
            arguments[key] = getter(alert)
    has_symbol = "symbol" in arguments or "ticker" in arguments
    has_price = "price" in arguments or "trigger_price" in arguments
    if not has_symbol or not has_price:
        return None
    return arguments


def push_create_alerts(book, caller, properties, *, allow=False):
    """Send create_alert only. Never places an order. Stale tapes send nothing."""
    if not allow:
        return {"pushed": 0, "reason": "push_not_allowed", "calls": []}
    rows = book.get("rows") or []
    if any(row.get("status") == "stale" for row in rows):
        return {"pushed": 0, "reason": "stale_tape", "calls": []}
    calls = []
    for row in rows:
        for alert in row.get("alerts") or []:
            if alert.get("fired"):
                continue
            arguments = create_alert_arguments(alert, properties)
            if arguments is None:
                return {"pushed": 0, "reason": "schema_unverified", "calls": []}
            calls.append({"tool": "create_alert", "arguments": arguments})
    for call in calls:
        if call["tool"] != "create_alert":
            raise ValueError("paper book only creates alerts")
        caller(call["tool"], call["arguments"])
    for row in rows:
        for alert in row.get("alerts") or []:
            if not alert.get("fired"):
                alert["pushed"] = True
    return {"pushed": len(calls), "reason": "create_alert", "calls": calls}


def _pine_price(value):
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return str(number)


def render_pine(book):
    """Paste on a TradingView chart. Arm Any alert() function call. No order."""
    lines = [
        "//@version=6",
        f'indicator("Paper book {book.get("session_date")}", overlay=true)',
        "// Paper book. No brokerage order.",
    ]
    live = []
    for row in book.get("rows") or []:
        if row.get("status") == "stale":
            continue
        for alert in row.get("alerts") or []:
            price = _num(alert.get("price"))
            trigger = alert.get("trigger")
            if price is None or trigger not in {"cross_above", "cross_below"}:
                continue
            live.append((row.get("ticker"), alert, price))
    if not live:
        lines.append("// No alerts. Stale tape stays flat.")
        return "\n".join(lines) + "\n"
    for index, (ticker, alert, price) in enumerate(live):
        cross = "ta.crossover" if alert["trigger"] == "cross_above" else "ta.crossunder"
        message = str((alert.get("tradingview") or {}).get("message") or alert.get("note") or "")
        message = message.replace("\\", "\\\\").replace('"', '\\"')
        role = re.sub(r"[^A-Za-z0-9]", "", str(alert.get("role") or "level"))
        symbol = re.sub(r"[^A-Za-z0-9]", "", str(ticker or "sym"))
        name = f"{symbol}_{role}_{index}"
        level = _pine_price(price)
        title = f"{ticker} {alert.get('role')}".replace('"', "")
        lines.append(f'{name} = syminfo.ticker == "{ticker}" ? {level} : na')
        lines.append(f'plot({name}, "{title}")')
        lines.append(f'if syminfo.ticker == "{ticker}" and {cross}(close, {level})')
        lines.append(f'    alert("{message}", alert.freq_once_per_bar)')
    return "\n".join(lines) + "\n"


def latest_prior(output_dir: Path, session: date):
    """Most recent paper book strictly before this session."""
    if not output_dir.is_dir():
        return None
    best = None
    best_day = None
    for path in output_dir.glob("paper_book_*.json"):
        try:
            book = json.loads(path.read_text(encoding="utf-8"))
            day = date.fromisoformat(book["session_date"])
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if not isinstance(book, dict) or day >= session:
            continue
        if best_day is None or day > best_day:
            best = book
            best_day = day
    return best


def write_book(book, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / f"paper_book_{book['session_date']}"
    stem.with_suffix(".json").write_text(json.dumps(book, indent=2) + "\n", encoding="utf-8")
    stem.with_suffix(".md").write_text(render_markdown(book), encoding="utf-8")
    stem.with_suffix(".pine").write_text(render_pine(book), encoding="utf-8")
    return stem.with_suffix(".md")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Record a paper options book from confluence")
    parser.add_argument("--session-date", required=True, help="YYYY-MM-DD paper session")
    parser.add_argument("--confluence-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--quotes",
        type=Path,
        help="JSON object of ticker to last price. Advances fresh rows only.",
    )
    parser.add_argument(
        "--fetch-quotes",
        action="store_true",
        help="Fetch last prices and advance fresh rows. Stale rows stay unchanged.",
    )
    args = parser.parse_args(argv)
    if not args.confluence_dir.is_dir():
        print(f"ERROR: confluence dir not found: {args.confluence_dir}", file=sys.stderr)
        return 1
    session = date.fromisoformat(args.session_date)
    book = build_book(args.confluence_dir, session, latest_prior(args.output_dir, session))
    if args.fetch_quotes:
        fetched = fetch_last_prices([row["ticker"] for row in book["rows"]], yahoo_getter)
        book["quote_errors"] = fetched["errors"]
        apply_marks(book, fetched["quotes"])
    elif args.quotes:
        quotes = json.loads(args.quotes.read_text(encoding="utf-8"))
        if not isinstance(quotes, dict):
            print("ERROR: quotes JSON must be an object of ticker to price", file=sys.stderr)
            return 1
        apply_marks(book, quotes)
    path = write_book(book, args.output_dir)
    print(
        f"paper book {book['session_date']}: open={book['open_count']} "
        f"armed={book['armed_count']} alerts={len(book['alerts'])} -> {path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
