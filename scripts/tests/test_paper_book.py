"""Paper book: record option plays from confluence, never place brokerage orders."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from paper_book import (
    CHASE_ABS_CHANGE_PCT,
    build_book,
    decide_play,
    render_markdown,
    weekday_lag,
)
from report_paths import artifact_dir


def _play(**overrides):
    payload = {
        "ticker": "TSEM",
        "as_of": "2026-10-15",
        "verdict": "PLAY",
        "bias": "long",
        "spot": 249.0,
        "change_pct": 1.2,
        "hard_stops": [],
        "operator_thesis": "RSI white holding 50 into the fib test.",
        "judgment": {
            "one_thing_to_verify": "RSI white holds 50.",
            "rr_sketch": {
                "entry_zone": "248-255",
                "stop": 230.0,
                "targets": [
                    {"level": 268.0, "note": "first fib"},
                    {"level": 300.0, "note": "map king"},
                ],
            },
            "invalidation": {"operator": "daily close below 236"},
        },
    }
    payload.update(overrides)
    return payload


def test_weekday_lag_friday_to_monday_is_one_session():
    assert weekday_lag(date(2026, 10, 16), date(2026, 10, 19)) == 1
    assert weekday_lag(date(2026, 10, 16), date(2026, 10, 16)) == 0
    assert weekday_lag(date(2026, 8, 16), date(2026, 10, 16)) > 1


def test_stale_play_stays_flat_and_withholds_alerts():
    row = decide_play(_play(as_of="2026-08-09", spot=252.49, change_pct=12.37), date(2026, 10, 16))

    assert row["status"] == "stale"
    assert row["action"] == "flat"
    assert row["alerts"] == []
    assert row["shadow"]["status"] == "armed_wait"
    assert row["shadow"]["alerts"]
    assert row["shadow"]["target"] == 300.0


def test_quiet_discount_play_opens_a_paper_option():
    row = decide_play(_play(), date(2026, 10, 16))

    assert row["status"] == "paper_open"
    assert row["paper_entry"] == 249.0
    assert row["contract"]["right"] == "call"
    assert row["contract"]["tenor"] == "weekly_or_shorter"
    assert row["contract"]["moneyness"] == "atm_to_slightly_itm"
    assert row["contract"]["size_for_zero"] is True
    roles = {alert["role"] for alert in row["alerts"]}
    assert roles == {"invalidation", "target"}
    assert row["target"] == 300.0


def test_expansion_inside_the_zone_waits_for_the_test():
    row = decide_play(_play(spot=252.49, change_pct=CHASE_ABS_CHANGE_PCT + 0.1), date(2026, 10, 16))

    assert row["status"] == "armed_wait"
    assert row["paper_entry"] is None
    entry = next(alert for alert in row["alerts"] if alert["role"] == "entry_test")
    assert entry["price"] == 248.0
    assert entry["trigger"] == "cross_below"
    assert entry["pushed"] is False


def test_extended_long_does_not_chase():
    row = decide_play(_play(spot=260.0, change_pct=1.0), date(2026, 10, 16))

    assert row["status"] == "armed_wait"
    entry = next(alert for alert in row["alerts"] if alert["role"] == "entry_test")
    assert entry["price"] == 255.0
    assert entry["trigger"] == "cross_below"


def test_short_opens_only_at_the_upper_test():
    row = decide_play(
        _play(
            ticker="CRWD",
            bias="short",
            spot=226.0,
            change_pct=-1.0,
            judgment={
                "rr_sketch": {
                    "entry_zone": "220-227",
                    "stop": 227.08,
                    "targets": [{"level": 187.5, "note": "VEX king"}],
                }
            },
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "paper_open"
    assert row["contract"]["right"] == "put"
    invalidation = next(alert for alert in row["alerts"] if alert["role"] == "invalidation")
    assert invalidation["trigger"] == "cross_above"
    assert invalidation["price"] == 227.08


def test_no_trade_is_flat_without_alerts():
    row = decide_play(_play(verdict="NO_TRADE"), date(2026, 10, 16))

    assert row["status"] == "flat"
    assert row["reason"] == "no_trade"
    assert row["alerts"] == []


def test_watch_alerts_the_reclaim_without_a_fill():
    row = decide_play(
        _play(
            verdict="WATCH",
            spot=9.11,
            change_pct=4.18,
            judgment={
                "rr_sketch": {
                    "entry_zone": "9.25-9.50",
                    "stop": 8.45,
                    "targets": [{"level": 10.0, "note": "king"}],
                }
            },
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["paper_entry"] is None
    assert row["contract"] is None
    assert row["alerts"][0]["trigger"] == "cross_above"
    assert row["alerts"][0]["price"] == 9.25
    assert row["alerts"][0]["tradingview"]["condition"] == "Crossing up"
    assert row["four_hour"] == "absent"


def test_watch_hard_stop_still_alerts_the_pullback():
    row = decide_play(
        _play(
            verdict="WATCH",
            spot=31.59,
            change_pct=6.54,
            hard_stops=["max WATCH; pullback is the upgrade"],
            judgment={
                "rr_sketch": {
                    "entry_zone": "27.42-28.50",
                    "stop": 24.0,
                    "targets": [{"level": 35.0, "note": "king"}],
                }
            },
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["paper_entry"] is None
    assert row["alerts"][0]["price"] == 28.5
    assert row["alerts"][0]["trigger"] == "cross_below"
    assert "_hard_stop" not in row


def test_play_hard_stop_does_not_open():
    row = decide_play(_play(hard_stops=["fierce HTF fight"]), date(2026, 10, 16))

    assert row["status"] == "watch"
    assert row["reason"] == "hard_stop"
    assert row["paper_entry"] is None
    assert row["contract"] is None
    assert {alert["role"] for alert in row["alerts"]} == {"entry_test"}


def test_nearest_indicator_cluster_sets_invalidation():
    row = decide_play(
        _play(
            spot=252.49,
            change_pct=12.37,
            operator_extracted={
                "fib_levels": [{"price": 236.75}, {"price": 186.0}],
                "sma": {"50": 240.0, "100": 230.0},
                "vp": {"peak_nodes": [186.0, 252.0]},
                "sr_levels": [186.13],
                "rsi": {"white": 54.0},
            },
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "armed_wait"
    assert row["invalidation"] == 236.75
    assert row["invalidation_cluster"]["families"] == ["fib", "sma"]
    invalidation = next(alert for alert in row["alerts"] if alert["role"] == "invalidation")
    assert invalidation["price"] == 236.75
    assert invalidation["tradingview"]["condition"] == "Crossing down"


def test_near_sma_beats_a_distant_indicator_stack():
    row = decide_play(
        _play(
            spot=249.89,
            change_pct=8.22,
            judgment={
                "rr_sketch": {
                    "entry_zone": "240-250",
                    "stop": 232.0,
                    "targets": [{"level": 300.0, "note": "king"}],
                }
            },
            operator_extracted={
                "sma": {"50": 236.0},
                "fib_levels": [{"price": 210.68}],
                "sr_levels": [210.0],
                "rsi": {"white": 57.0},
            },
        ),
        date(2026, 10, 16),
    )

    assert row["invalidation"] == 236.0
    assert row["invalidation_cluster"]["families"] == ["sma"]


def test_rsi_below_50_blocks_a_long_fill():
    row = decide_play(
        _play(operator_extracted={"rsi": {"white": 47.0}}),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "rsi_against"
    assert row["paper_entry"] is None


def test_smaller_target_than_opposing_gex_does_not_open():
    row = decide_play(
        _play(
            map_nodes=[
                {"strike": 300.0, "value_k": 100, "sign": "pos"},
                {"strike": 260.0, "value_k": -500, "sign": "neg"},
            ]
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "target_smaller_than_opposing"
    assert row["paper_entry"] is None


def test_larger_king_does_not_block_the_wait():
    row = decide_play(
        _play(
            spot=252.49,
            change_pct=12.37,
            map_nodes=[
                {"strike": 300.0, "value_k": 13567, "sign": "pos"},
                {"strike": 250.0, "value_k": -283, "sign": "neg"},
            ],
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "armed_wait"
    assert row["reason"] == "wait_for_test"


def test_four_hour_fight_caps_a_play():
    row = decide_play(_play(four_hour="fight"), date(2026, 10, 16))

    assert row["status"] == "watch"
    assert row["reason"] == "four_hour_fight"
    assert row["paper_entry"] is None
    assert row["four_hour"] == "fight"


def test_play_missing_invalidation_does_not_open():
    row = decide_play(
        _play(
            judgment={
                "rr_sketch": {"entry_zone": "248-255", "targets": [{"level": 300, "note": "king"}]}
            }
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "missing_invalidation"
    assert row["paper_entry"] is None


def test_build_book_keeps_latest_ticker_and_writes_no_orders(tmp_path: Path):
    src = tmp_path / "confluence"
    src.mkdir()
    older = _play(as_of="2026-10-14", spot=249.0)
    newer = _play(as_of="2026-10-15", spot=249.2, change_pct=0.4)
    (src / "TSEM_confluence_2026-10-14.json").write_text(json.dumps(older))
    (src / "TSEM_confluence_2026-10-15.json").write_text(json.dumps(newer))
    (src / "session_confluence_daily_2026-10-15.json").write_text(json.dumps({"verdict": "PLAY"}))

    book = build_book(src, date(2026, 10, 16))

    assert [row["ticker"] for row in book["rows"]] == ["TSEM"]
    assert book["rows"][0]["as_of"] == "2026-10-15"
    assert book["rows"][0]["paper_entry"] == 249.2
    assert book["open_count"] == 1
    assert book["broker_orders"] == "none"
    text = render_markdown(book)
    assert "No brokerage order" in text
    assert "TSEM" in text


def test_uploaded_august_tape_is_flat_on_october_16():
    root = Path(__file__).resolve().parents[2]
    book = build_book(root / "reports" / "charts" / "confluence", date(2026, 10, 16))
    by_ticker = {row["ticker"]: row for row in book["rows"]}

    assert book["open_count"] == 0
    assert book["alerts"] == []
    assert set(by_ticker) == {
        "BE",
        "CRDO",
        "CRWD",
        "HIMS",
        "HOOD",
        "ONDS",
        "RIVN",
        "TSEM",
        "UMAC",
    }
    assert all(row["status"] == "stale" for row in book["rows"])
    assert by_ticker["TSEM"]["shadow"]["status"] == "armed_wait"
    assert by_ticker["TSEM"]["shadow"]["alerts"][0]["price"] == 248.0
    assert by_ticker["CRDO"]["shadow"]["status"] == "armed_wait"
    assert by_ticker["CRWD"]["shadow"]["status"] == "flat"
    assert by_ticker["BE"]["shadow"]["status"] == "flat"
    onds = by_ticker["ONDS"]["shadow"]["alerts"][0]
    assert onds["price"] == 9.25
    assert onds["trigger"] == "cross_above"
    assert onds["destination"] == "robinhood_create_alert"
    assert onds["tradingview"]["condition"] == "Crossing up"
    assert onds["pushed"] is False
    text = render_markdown(book)
    assert "withheld" in text
    assert "create_alert" in text
    assert "rug" not in book["pattern_notes"]["named_rug_setups"]


def test_paper_book_dir_is_registered(tmp_path: Path):
    assert artifact_dir(tmp_path, "paper_book") == tmp_path / "reports" / "paper"
