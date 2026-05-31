"""Tests for stable quote batch behavior (per-symbol on FMP Starter)."""

import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fmp_client import FMPClient


def _make_client():
    client = FMPClient(api_key="test_key")
    client.max_retries = 0
    return client


def _mock_response(status_code, json_payload, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_payload
    resp.text = text
    return resp


class TestQuoteBatchPerSymbol:
    def test_comma_separated_fetches_each_symbol_on_stable(self):
        client = _make_client()

        def fake_get(url, params=None, timeout=30):
            sym = (params or {}).get("symbol", "")
            if sym == "MRAM":
                return _mock_response(200, [{"symbol": "MRAM", "price": 26.0}])
            if sym == "MU":
                return _mock_response(200, [{"symbol": "MU", "price": 97.0}])
            return _mock_response(403, None, "Forbidden")

        client.session.get = MagicMock(side_effect=fake_get)
        result = client.get_quote("MRAM,MU")
        assert result is not None
        assert len(result) == 2
        symbols = {r["symbol"] for r in result}
        assert symbols == {"MRAM", "MU"}
        assert client.session.get.call_count == 2

    def test_batch_quotes_uses_per_symbol(self):
        client = _make_client()

        def fake_get(url, params=None, timeout=30):
            sym = (params or {}).get("symbol", "")
            return _mock_response(200, [{"symbol": sym, "price": 1.0}])

        client.session.get = MagicMock(side_effect=fake_get)
        result = client.get_batch_quotes(["A", "B", "C"])
        assert len(result) == 3
        assert client.session.get.call_count == 3

    def test_comma_batch_empty_stable_never_calls_v3(self):
        client = _make_client()
        v3_called = False

        def fake_get(url, params=None, timeout=30):
            nonlocal v3_called
            if "api/v3" in url:
                v3_called = True
                return _mock_response(403, None, "Legacy forbidden")
            sym = (params or {}).get("symbol", "")
            return _mock_response(200, [{"symbol": sym, "price": 10.0}])

        client.session.get = fake_get
        result = client.get_quote("AAPL,MSFT")
        assert result is not None
        assert len(result) == 2
        assert v3_called is False


class TestSp500Constituents:
    def test_sp500_402_prints_premium_hint(self, capsys):
        client = _make_client()

        def fake_get(url, params=None, timeout=30, **kwargs):
            return _mock_response(
                402,
                None,
                "Restricted Endpoint: upgrade to Premium",
            )

        client.session.get = MagicMock(side_effect=fake_get)
        result = client.get_sp500_constituents()
        assert result is None
        err = capsys.readouterr().err
        assert "Premium" in err
        assert "watchlist" in err.lower() or "--universe" in err
