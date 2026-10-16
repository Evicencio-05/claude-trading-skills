"""Paper book: record option plays from confluence, never place brokerage orders."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from paper_book import (
    CHASE_ABS_CHANGE_PCT,
    apply_marks,
    build_book,
    create_alert_arguments,
    decide_play,
    fetch_last_prices,
    merge_carried,
    parse_yahoo_chart,
    plan_from_operator,
    push_create_alerts,
    render_markdown,
    render_pine,
    weekday_lag,
    weekly_expiry,
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


def test_weekly_expiry_uses_this_friday_only_through_wednesday():
    assert weekly_expiry(date(2026, 10, 12)) == date(2026, 10, 16)
    assert weekly_expiry(date(2026, 10, 14)) == date(2026, 10, 16)
    assert weekly_expiry(date(2026, 10, 15)) == date(2026, 10, 23)
    assert weekly_expiry(date(2026, 10, 16)) == date(2026, 10, 23)
    assert weekly_expiry(date(2026, 10, 17)) == date(2026, 10, 23)
    assert weekly_expiry(date(2026, 10, 18)) == date(2026, 10, 23)


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
    assert row["contract"]["expiry"] == "2026-10-23"
    roles = {alert["role"] for alert in row["alerts"]}
    assert roles == {"invalidation", "target", "claim"}
    claim = next(alert for alert in row["alerts"] if alert["role"] == "claim")
    assert claim["price"] == 255.0
    assert claim["trigger"] == "cross_above"
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


def test_fib_sets_the_cluster_invalidation_ahead_of_a_lower_shelf():
    row = decide_play(
        _play(
            spot=26.11,
            change_pct=1.0,
            judgment={
                "rr_sketch": {
                    "entry_zone": "24.5-26.5",
                    "stop": 20.0,
                    "targets": [{"level": 30.0, "note": "king"}],
                }
            },
            operator_extracted={
                "fib_levels": [{"price": 23.46}],
                "vp": {"peak_nodes": [23.0]},
                "sr_levels": [22.93],
                "rsi": {"white": 55.0},
            },
        ),
        date(2026, 10, 16),
    )

    assert row["invalidation"] == 23.46
    assert row["invalidation_cluster"]["families"] == ["fib", "shelf", "sr"]


def test_higher_period_sma_sets_invalidation_ahead_of_the_20():
    row = decide_play(
        _play(
            spot=250.0,
            change_pct=1.0,
            judgment={
                "rr_sketch": {
                    "entry_zone": "248-255",
                    "stop": 200.0,
                    "targets": [{"level": 300.0, "note": "king"}],
                }
            },
            operator_extracted={
                "sma": {"20": 230.0, "200": 236.0},
                "rsi": {"white": 55.0},
            },
        ),
        date(2026, 10, 16),
    )

    assert row["invalidation"] == 236.0
    assert row["invalidation_cluster"]["families"] == ["sma"]


def test_stacked_shelf_beats_a_lone_nearer_shelf():
    row = decide_play(
        _play(
            spot=9.11,
            change_pct=1.0,
            judgment={
                "rr_sketch": {
                    "entry_zone": "9.25-9.5",
                    "stop": 8.0,
                    "targets": [{"level": 10.0, "note": "next shelf"}],
                }
            },
            operator_extracted={
                "sma": {"200": 8.75},
                "vp": {"peak_nodes": [9.0, 8.75]},
                "rsi": {"white": 55.0},
            },
        ),
        date(2026, 10, 16),
    )

    assert row["invalidation"] == 8.75
    assert row["invalidation_cluster"]["families"] == ["shelf", "sma"]


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


def test_fresh_operator_plan_keeps_the_prior_sessions_gex_nodes(tmp_path: Path):
    confluence = tmp_path / "confluence"
    operator = tmp_path / "operator"
    confluence.mkdir()
    operator.mkdir()
    prior = _play(
        ticker="AAPL",
        as_of="2026-10-14",
        map_nodes=[
            {"strike": 360.0, "value_k": 100, "sign": "pos"},
            {"strike": 350.0, "value_k": -500, "sign": "neg"},
        ],
    )
    (confluence / "AAPL_confluence_2026-10-14.json").write_text(json.dumps(prior))
    (operator / "AAPL_operator_2026-10-15.json").write_text(
        json.dumps(_operator_plan(operator_thesis="Long AAPL. Daily is up. Test 340, target 360."))
    )

    book = build_book(confluence, date(2026, 10, 16))
    row = book["rows"][0]

    assert row["ticker"] == "AAPL"
    assert row["as_of"] == "2026-10-15"
    assert row["status"] == "watch"
    assert row["reason"] == "target_smaller_than_opposing"
    assert row["paper_entry"] is None


def test_stale_gex_nodes_do_not_follow_a_new_operator_plan(tmp_path: Path):
    confluence = tmp_path / "confluence"
    operator = tmp_path / "operator"
    confluence.mkdir()
    operator.mkdir()
    prior = _play(
        ticker="AAPL",
        as_of="2026-08-09",
        map_nodes=[
            {"strike": 360.0, "value_k": 100, "sign": "pos"},
            {"strike": 350.0, "value_k": -500, "sign": "neg"},
        ],
    )
    (confluence / "AAPL_confluence_2026-08-09.json").write_text(json.dumps(prior))
    (operator / "AAPL_operator_2026-10-15.json").write_text(
        json.dumps(_operator_plan(operator_thesis="Long AAPL. Daily is up. Test 340, target 360."))
    )

    book = build_book(confluence, date(2026, 10, 16))
    row = book["rows"][0]

    assert row["as_of"] == "2026-10-15"
    assert row["status"] == "paper_open"
    assert row["reason"] == "paper_open"


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
    assert by_ticker["TSEM"]["shadow"]["contract"]["expiry"] == "2026-08-14"
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


def test_below_50_sma_blocks_a_long_fill():
    row = decide_play(
        _play(operator_extracted={"sma": {"50": 260.0}, "rsi": {"white": 54.0}}),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "below_50_sma"
    assert row["paper_entry"] is None


def test_quote_at_the_test_opens_a_fresh_arm():
    row = decide_play(_play(spot=252.49, change_pct=12.37), date(2026, 10, 16))
    book = {"rows": [row], "open_count": 0, "armed_count": 1}

    apply_marks(book, {"TSEM": 247.5})

    assert book["rows"][0]["status"] == "paper_open"
    assert book["rows"][0]["paper_entry"] == 248.0
    assert book["open_count"] == 1
    assert book["marks"][0]["result"] == "paper_open"


def test_quote_above_the_test_leaves_the_arm():
    row = decide_play(_play(spot=252.49, change_pct=12.37), date(2026, 10, 16))
    book = {"rows": [row]}

    apply_marks(book, {"TSEM": 252.0})

    assert book["rows"][0]["status"] == "armed_wait"
    assert book["marks"][0]["result"] == "unchanged"


def test_stale_october_tape_ignores_quotes_through_the_levels():
    root = Path(__file__).resolve().parents[2]
    book = build_book(root / "reports" / "charts" / "confluence", date(2026, 10, 16))

    apply_marks(book, {"TSEM": 200.0, "CRDO": 200.0, "ONDS": 20.0})

    assert book["open_count"] == 0
    assert book["marks"]
    assert all(mark["result"] == "unchanged" for mark in book["marks"])


def test_watch_tag_does_not_open_a_position():
    row = decide_play(
        _play(
            verdict="WATCH",
            spot=9.11,
            change_pct=1.0,
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
    book = {"rows": [row]}

    apply_marks(book, {"TSEM": 9.5})

    assert row["status"] == "watch"
    assert row["reason"] == "test_tagged_watch"
    assert row["paper_entry"] is None


def test_open_paper_invalidation_and_target():
    opened = decide_play(_play(), date(2026, 10, 16))
    book = {"rows": [opened]}
    apply_marks(book, {"TSEM": 229.0})
    assert opened["status"] == "invalidated"
    assert opened["reason"] == "invalidation_tagged"

    live = decide_play(_play(), date(2026, 10, 16))
    book = {"rows": [live]}
    apply_marks(book, {"TSEM": 301.0})
    assert live["status"] == "target_hit"
    assert live["reason"] == "target_tagged"


def test_claim_through_the_zone_adds_and_a_failed_claim_trims():
    opened = decide_play(_play(), date(2026, 10, 16))
    book = {"rows": [opened]}

    apply_marks(book, {"TSEM": 256.0})

    assert opened["status"] == "paper_open"
    assert opened["reason"] == "claim_add"
    assert opened["paper_entry"] == 249.0
    assert opened["adds"] == [{"price": 255.0, "status": "open"}]
    assert book["open_count"] == 1

    apply_marks(book, {"TSEM": 257.0})
    assert opened["adds"] == [{"price": 255.0, "status": "open"}]
    assert book["marks"][0]["result"] == "unchanged"

    apply_marks(book, {"TSEM": 249.0})
    assert opened["status"] == "paper_open"
    assert opened["reason"] == "claim_failed"
    assert opened["paper_entry"] == 249.0
    assert opened["adds"] == [{"price": 255.0, "status": "trimmed"}]

    apply_marks(book, {"TSEM": 256.0})
    assert [item for item in opened["adds"] if item["status"] == "open"] == [
        {"price": 255.0, "status": "open"}
    ]


def test_invalidation_flattens_the_core_and_the_add():
    opened = decide_play(_play(), date(2026, 10, 16))
    book = {"rows": [opened]}
    apply_marks(book, {"TSEM": 256.0})
    apply_marks(book, {"TSEM": 229.0})

    assert opened["status"] == "invalidated"
    assert opened["reason"] == "invalidation_tagged"
    assert opened["action"] == "flat"
    assert opened["adds"] == [{"price": 255.0, "status": "flat"}]


def test_dip_to_the_entry_without_an_add_keeps_the_core():
    opened = decide_play(_play(), date(2026, 10, 16))
    book = {"rows": [opened]}

    apply_marks(book, {"TSEM": 248.5})

    assert opened["status"] == "paper_open"
    assert opened["reason"] == "paper_open"
    assert book["marks"][0]["result"] == "unchanged"


def test_short_claim_adds_at_the_zone_low_and_trims_on_a_reclaim():
    opened = decide_play(
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
    book = {"rows": [opened]}

    apply_marks(book, {"CRWD": 219.0})

    assert opened["status"] == "paper_open"
    assert opened["adds"] == [{"price": 220.0, "status": "open"}]
    claim = next(alert for alert in opened["alerts"] if alert["role"] == "claim")
    assert claim["trigger"] == "cross_below"

    apply_marks(book, {"CRWD": 226.0})
    assert opened["status"] == "paper_open"
    assert opened["reason"] == "claim_failed"
    assert opened["adds"] == [{"price": 220.0, "status": "trimmed"}]


def test_yahoo_chart_parser_reads_the_regular_price():
    assert (
        parse_yahoo_chart({"chart": {"result": [{"meta": {"regularMarketPrice": 248.2}}]}}) == 248.2
    )
    assert parse_yahoo_chart({"chart": {"result": []}}) is None


def test_fetch_last_prices_keeps_going_after_one_failure():
    def getter(url):
        if url.endswith("BAD?interval=1d&range=1d") or "BAD?" in url:
            raise OSError("offline")
        return '{"chart":{"result":[{"meta":{"regularMarketPrice": 11.5}}]}}'

    fetched = fetch_last_prices(["ONDS", "BAD"], getter)

    assert fetched["quotes"] == {"ONDS": 11.5}
    assert fetched["errors"][0]["ticker"] == "BAD"


def test_push_create_alerts_refuses_stale_tape_and_order_tools():
    stale = build_book(
        Path(__file__).resolve().parents[2] / "reports" / "charts" / "confluence",
        date(2026, 10, 16),
    )
    calls = []
    result = push_create_alerts(
        stale, lambda tool, args: calls.append(tool), ["symbol", "price"], allow=True
    )
    assert result["reason"] == "stale_tape"
    assert calls == []

    fresh = {"rows": [decide_play(_play(spot=252.49, change_pct=12.37), date(2026, 10, 16))]}
    refused = push_create_alerts(
        fresh, lambda tool, args: calls.append(tool), ["symbol", "price"], allow=False
    )
    assert refused["reason"] == "push_not_allowed"
    assert calls == []

    unverified = push_create_alerts(
        fresh, lambda tool, args: calls.append((tool, args)), [], allow=True
    )
    assert unverified["reason"] == "schema_unverified"
    assert calls == []

    pushed = push_create_alerts(
        fresh,
        lambda tool, args: calls.append((tool, args)),
        ["symbol", "price", "direction"],
        allow=True,
    )
    assert pushed["reason"] == "create_alert"
    assert pushed["pushed"] == len(fresh["rows"][0]["alerts"])
    assert {call[0] for call in calls} == {"create_alert"}
    assert (
        create_alert_arguments(fresh["rows"][0]["alerts"][0], ["symbol", "price"])["symbol"]
        == "TSEM"
    )


def test_earnings_session_does_not_open():
    row = decide_play(_play(earnings_on="2026-10-16"), date(2026, 10, 16))

    assert row["status"] == "flat"
    assert row["reason"] == "earnings_open"
    assert row["paper_entry"] is None
    assert row["alerts"] == []
    assert row["earnings_on"] == "2026-10-16"


def test_later_earnings_stays_open_until_that_morning():
    row = decide_play(_play(earnings_on="2026-10-20"), date(2026, 10, 16))

    assert row["status"] == "paper_open"
    assert row["earnings_on"] == "2026-10-20"


def test_vague_earnings_text_does_not_block():
    row = decide_play(
        _play(operator_extracted={"earnings_markers": "E visible early September"}),
        date(2026, 10, 16),
    )

    assert row["status"] == "paper_open"
    assert row.get("earnings_on") is None


def test_open_carries_across_a_stale_session_until_expiry():
    opened = decide_play(_play(as_of="2026-10-15"), date(2026, 10, 16))
    stale = decide_play(_play(as_of="2026-10-15"), date(2026, 10, 20))
    assert stale["status"] == "stale"

    carried = merge_carried([stale], {"rows": [opened]}, date(2026, 10, 20))

    assert carried[0]["status"] == "paper_open"
    assert carried[0]["paper_entry"] == 249.0
    assert carried[0]["carried"] is True

    expired = merge_carried(
        [decide_play(_play(as_of="2026-10-15"), date(2026, 10, 26))],
        {"rows": [opened]},
        date(2026, 10, 26),
    )
    assert expired[0]["status"] == "expired"
    assert expired[0]["reason"] == "expired"
    assert expired[0]["alerts"] == []


def test_carried_position_flattens_on_its_earnings_morning():
    opened = decide_play(_play(earnings_on="2026-10-20"), date(2026, 10, 16))
    stale = decide_play(_play(as_of="2026-10-15"), date(2026, 10, 20))

    carried = merge_carried([stale], {"rows": [opened]}, date(2026, 10, 20))

    assert carried[0]["status"] == "flat"
    assert carried[0]["reason"] == "earnings_open"


def test_newer_tape_replaces_a_carried_position():
    opened = decide_play(_play(as_of="2026-10-15"), date(2026, 10, 16))
    fresh = decide_play(_play(as_of="2026-10-19", verdict="NO_TRADE"), date(2026, 10, 19))

    merged = merge_carried([fresh], {"rows": [opened]}, date(2026, 10, 19))

    assert merged[0]["status"] == "flat"
    assert merged[0]["reason"] == "no_trade"
    assert merged[0].get("carried") is not True


def test_same_tape_keeps_the_recorded_add():
    opened = decide_play(_play(), date(2026, 10, 16))
    opened["adds"] = [{"price": 255.0, "status": "open"}]
    again = decide_play(_play(), date(2026, 10, 19))

    merged = merge_carried([again], {"rows": [opened]}, date(2026, 10, 19))

    assert merged[0]["status"] == "paper_open"
    assert merged[0]["adds"] == [{"price": 255.0, "status": "open"}]


def test_pine_script_arms_fresh_crosses_and_withholds_a_stale_tape():
    armed = decide_play(_play(spot=252.49, change_pct=12.37), date(2026, 10, 16))
    text = render_pine({"session_date": "2026-10-16", "rows": [armed]})

    assert "//@version=6" in text
    assert 'syminfo.ticker == "TSEM"' in text
    assert "ta.crossunder(close, 248)" in text
    assert "plot(" in text
    assert "No brokerage order" in text

    root = Path(__file__).resolve().parents[2]
    stale = render_pine(build_book(root / "reports" / "charts" / "confluence", date(2026, 10, 16)))
    assert "No alerts" in stale
    assert "alert(" not in stale
    assert "plot(" not in stale


def _operator_plan(**extracted_overrides):
    extracted = {
        "timeframe": "4H",
        "last": 341.0,
        "change_pct": 0.4,
        "sma": {"20": None, "50": 330.0, "200": 300.0},
        "fib_levels": [
            {"ratio": "1.0", "price": 340.0},
            {"ratio": "1.618", "price": 360.0},
        ],
        "vp": {"peak_nodes": [338.0]},
        "sr_levels": [336.0],
        "rsi": {"white": 55.0},
        "operator_thesis": "Long AAPL. Daily is up and the 4H agrees. Test 340.",
    }
    extracted.update(extracted_overrides)
    return {
        "ticker": "AAPL",
        "as_of": "2026-10-15",
        "extracted": extracted,
    }


def test_daily_chart_is_the_direction_without_the_word_daily():
    thesis = "Long AAPL. Test 340, target 360."
    opened = decide_play(
        plan_from_operator(_operator_plan(timeframe="1D", operator_thesis=thesis)),
        date(2026, 10, 16),
    )

    assert opened["verdict"] == "PLAY"
    assert opened["status"] == "paper_open"
    assert opened["four_hour"] == "absent"
    assert opened["one_thing_to_verify"] == ""

    weekly = decide_play(
        plan_from_operator(_operator_plan(timeframe="1W", operator_thesis=thesis)),
        date(2026, 10, 16),
    )

    assert weekly["verdict"] == "WATCH"
    assert weekly["status"] == "watch"
    assert weekly["paper_entry"] is None

    stated = decide_play(
        plan_from_operator(
            _operator_plan(
                timeframe="1W",
                operator_thesis="Long AAPL. Daily is up. Test 340, target 360.",
            )
        ),
        date(2026, 10, 16),
    )

    assert stated["verdict"] == "PLAY"
    assert stated["status"] == "paper_open"


def test_daily_chart_against_its_own_thesis_stays_a_watch():
    row = decide_play(
        plan_from_operator(
            _operator_plan(
                timeframe="1D",
                operator_thesis="Long AAPL. Daily is down. Test 340, target 360.",
            )
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "four_hour_fight"
    assert row["paper_entry"] is None


def test_four_hour_plan_without_daily_direction_stays_a_watch():
    doc = _operator_plan(
        operator_thesis="Long AAPL. 4H test of the 340 fib toward 360.",
        last=345.0,
    )
    row = decide_play(plan_from_operator(doc), date(2026, 10, 16))

    assert row["status"] == "watch"
    assert row["paper_entry"] is None
    assert row["verdict"] == "WATCH"
    assert row["alerts"][0]["price"] == 340.0


def test_far_target_does_not_widen_the_entry_above_the_test():
    row = decide_play(
        plan_from_operator(
            _operator_plan(
                last=360.0,
                sma={"20": None, "50": 300.0, "200": None},
                fib_levels=[
                    {"ratio": "1.0", "price": 340.0},
                    {"ratio": "1.618", "price": 400.0},
                ],
                vp={"peak_nodes": []},
                sr_levels=[],
                operator_thesis="Long AAPL. Daily is up. Test 340, target 400.",
            )
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "armed_wait"
    assert row["paper_entry"] is None
    assert row["target"] == 400.0
    assert row["entry_zone"] == [340.0, 340.0]
    entry = next(alert for alert in row["alerts"] if alert["role"] == "entry_test")
    assert entry["price"] == 340.0
    assert entry["trigger"] == "cross_below"
    assert all(alert["role"] != "claim" for alert in row["alerts"])


def test_nearby_level_is_the_claim_and_the_far_level_is_the_target():
    row = decide_play(
        plan_from_operator(
            _operator_plan(
                last=341.0,
                sma={"20": None, "50": 300.0, "200": None},
                fib_levels=[
                    {"ratio": "1.0", "price": 340.0},
                    {"ratio": "1.272", "price": 345.0},
                    {"ratio": "1.618", "price": 400.0},
                ],
                vp={"peak_nodes": []},
                sr_levels=[],
                operator_thesis="Long AAPL. Daily is up. Test 340, target 400.",
            )
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "paper_open"
    assert row["entry_zone"] == [340.0, 345.0]
    assert row["target"] == 400.0
    claim = next(alert for alert in row["alerts"] if alert["role"] == "claim")
    assert claim["price"] == 345.0
    assert claim["trigger"] == "cross_above"


def test_daily_long_at_the_test_opens_from_an_operator_plan():
    row = decide_play(plan_from_operator(_operator_plan()), date(2026, 10, 16))

    assert row["status"] == "paper_open"
    assert row["bias"] == "long"
    assert row["paper_entry"] == 341.0
    assert row["target"] == 360.0
    assert row["four_hour"] == "agree"
    assert row["invalidation"] < 340.0
    assert row["contract"]["expiry"] == "2026-10-23"
    assert row["contract"]["size_for_zero"] is True


def test_thesis_sentence_sets_the_test_and_the_target():
    doc = _operator_plan(
        fib_levels=[],
        vp={"peak_nodes": []},
        sr_levels=[],
        operator_thesis="Long AAPL. Daily is up and the 4H agrees. Test 340, target 360.",
    )
    row = decide_play(plan_from_operator(doc), date(2026, 10, 16))

    assert row["status"] == "paper_open"
    assert row["target"] == 360.0
    assert row["entry_zone"][0] == 340.0


def test_break_below_from_the_thesis_arms_a_short_watch():
    doc = _operator_plan(
        last=531.99,
        sma={"20": None, "50": None, "200": None},
        fib_levels=[],
        vp={"peak_nodes": []},
        sr_levels=[],
        operator_thesis=(
            "Retesting the channel top near the 4-hour 20 SMA, under a 4-hour volume shelf. "
            "Break below 520 (also the 4-hour 50 SMA) targets the mid-band near 515."
        ),
    )
    row = decide_play(plan_from_operator(doc), date(2026, 10, 16))

    assert row["bias"] == "short"
    assert row["status"] == "watch"
    assert row["paper_entry"] is None
    assert row["target"] == 515.0
    entry = next(alert for alert in row["alerts"] if alert["role"] == "entry_test")
    assert entry["price"] == 520.0
    assert entry["trigger"] == "cross_below"


def test_daily_direction_against_the_trade_does_not_open():
    row = decide_play(
        plan_from_operator(
            _operator_plan(operator_thesis="Long AAPL. Daily is down. Test 340, target 360.")
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "four_hour_fight"
    assert row["paper_entry"] is None

    short = decide_play(
        plan_from_operator(
            _operator_plan(
                last=350.0,
                rsi={"white": 40.0},
                operator_thesis="Short AAPL. Daily is up. Break below 348 targets 340.",
                fib_levels=[
                    {"ratio": "1.0", "price": 348.0},
                    {"ratio": "0.5", "price": 340.0},
                ],
            )
        ),
        date(2026, 10, 16),
    )

    assert short["bias"] == "short"
    assert short["status"] == "watch"
    assert short["reason"] == "four_hour_fight"


def test_blank_sma_colors_do_not_block_the_plan():
    row = decide_play(
        plan_from_operator(_operator_plan(sma={"20": None, "50": None, "200": None})),
        date(2026, 10, 16),
    )

    assert row["status"] == "paper_open"
    assert row["reason"] != "below_50_sma"


def test_unlabeled_green_50_below_blocks_a_long():
    row = decide_play(
        plan_from_operator(
            _operator_plan(
                sma={"20": None, "50": None, "200": None},
                price_vs_sma={"20": "below", "50": "below", "200": "above"},
            )
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "watch"
    assert row["reason"] == "below_50_sma"
    assert row["paper_entry"] is None


def test_pullback_under_blue_20_and_orange_200_holds_when_above_green_50():
    row = decide_play(
        plan_from_operator(
            _operator_plan(
                sma={"20": 350.0, "50": 330.0, "200": 400.0},
                price_vs_sma={"20": "below", "50": "below", "200": "below"},
            )
        ),
        date(2026, 10, 16),
    )

    assert row["status"] == "paper_open"
    assert row["reason"] == "paper_open"
    assert row["spot"] < 350.0
    assert row["spot"] < 400.0


def test_short_under_the_green_50_still_opens():
    row = decide_play(
        plan_from_operator(
            _operator_plan(
                last=339.0,
                sma={"20": None, "50": None, "200": None},
                price_vs_sma={"50": "below"},
                rsi={"white": 40.0},
                fib_levels=[
                    {"ratio": "1.0", "price": 340.0},
                    {"ratio": "0.5", "price": 330.0},
                ],
                vp={"peak_nodes": []},
                sr_levels=[350.0],
                operator_thesis="Short AAPL. Daily is down. Break below 340 targets 330.",
            )
        ),
        date(2026, 10, 16),
    )

    assert row["bias"] == "short"
    assert row["status"] == "paper_open"
    assert row["reason"] == "paper_open"


def test_paper_book_dir_is_registered(tmp_path: Path):
    assert artifact_dir(tmp_path, "paper_book") == tmp_path / "reports" / "paper"
