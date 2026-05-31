"""Tests for stable earnings-calendar fallback."""

import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fmp_client import FMPClient


def _make_client():
    return FMPClient(api_key="test_key", max_api_calls=50)  # pragma: allowlist secret


def _mock_response(status_code, json_payload, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_payload
    resp.text = text
    return resp


class TestEarningsCalendarStable:
    def test_earnings_calendar_uses_stable_first(self):
        client = _make_client()
        stable_data = [{"symbol": "AAPL", "date": "2026-05-30"}]

        def fake_get(url, params=None, timeout=30):
            if "stable/earnings-calendar" in url:
                return _mock_response(200, stable_data)
            raise AssertionError(f"unexpected url: {url}")

        client.session.get = fake_get
        result = client.get_earnings_calendar("2026-05-29", "2026-05-31")
        assert result == stable_data

    def test_earnings_calendar_falls_back_to_v3(self):
        client = _make_client()
        v3_data = [{"symbol": "MSFT", "date": "2026-05-30"}]

        def fake_get(url, params=None, timeout=30):
            if "stable/earnings-calendar" in url:
                return _mock_response(403, None, "Forbidden")
            if "earning_calendar" in url:
                return _mock_response(200, v3_data)
            raise AssertionError(f"unexpected url: {url}")

        client.session.get = fake_get
        result = client.get_earnings_calendar("2026-05-29", "2026-05-31")
        assert result == v3_data
