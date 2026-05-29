"""Tests for robinhood_accounts config loader."""

from pathlib import Path

from robinhood_accounts import (
    build_robin_stocks_account_map,
    thesis_store_for_account,
)


def test_thesis_store_for_known_account():
    cfg = Path(__file__).resolve().parents[2] / "config" / "robinhood_accounts.yaml"
    assert thesis_store_for_account("487509309", cfg) == "robinhood_taxable"
    assert thesis_store_for_account("888653854", cfg) == "ira_robinhood"
    assert thesis_store_for_account("647977016", cfg) == "robinhood_agentic"


def test_build_robin_stocks_account_map():
    cfg = Path(__file__).resolve().parents[2] / "config" / "robinhood_accounts.yaml"
    m = build_robin_stocks_account_map(cfg)
    assert m["https://api.robinhood.com/accounts/487509309/"] == "robinhood_taxable"
