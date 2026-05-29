"""Load Robinhood account map from config/robinhood_accounts.yaml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_CONFIG = _REPO_ROOT / "config" / "robinhood_accounts.yaml"


def load_accounts_config(path: Path | None = None) -> dict[str, Any]:
    cfg_path = path or _DEFAULT_CONFIG
    if not cfg_path.exists():
        return {"accounts": {}}
    data = yaml.safe_load(cfg_path.read_text()) or {}
    return data if isinstance(data, dict) else {"accounts": {}}


def thesis_store_for_account(account_number: str, path: Path | None = None) -> str:
    accounts = load_accounts_config(path).get("accounts", {})
    entry = accounts.get(str(account_number), {})
    if isinstance(entry, dict) and entry.get("thesis_store"):
        return str(entry["thesis_store"])
    return str(account_number)


def robin_stocks_url_for_account(account_number: str, path: Path | None = None) -> str | None:
    accounts = load_accounts_config(path).get("accounts", {})
    entry = accounts.get(str(account_number), {})
    if isinstance(entry, dict):
        url = entry.get("robin_stocks_url")
        return str(url) if url else None
    return None


def build_robin_stocks_account_map(path: Path | None = None) -> dict[str, str]:
    """URL → thesis_store for robinhood_sync.py ACCOUNT_MAP."""
    accounts = load_accounts_config(path).get("accounts", {})
    out: dict[str, str] = {}
    for _num, entry in accounts.items():
        if not isinstance(entry, dict):
            continue
        url = entry.get("robin_stocks_url")
        store = entry.get("thesis_store")
        if url and store:
            out[str(url)] = str(store)
    return out
