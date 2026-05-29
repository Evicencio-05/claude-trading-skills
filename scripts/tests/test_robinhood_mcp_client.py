"""Tests for robinhood_mcp_client helpers."""

from robinhood_mcp_client import extract_accounts, extract_positions


def test_extract_accounts():
    payload = {
        "data": {
            "accounts": [
                {"account_number": "123", "brokerage_account_type": "individual"},
            ]
        }
    }
    accounts = extract_accounts(payload)
    assert len(accounts) == 1
    assert accounts[0]["account_number"] == "123"


def test_extract_positions():
    payload = {"data": {"positions": [{"symbol": "AAPL", "quantity": "10"}]}}
    positions = extract_positions(payload)
    assert positions[0]["symbol"] == "AAPL"
