"""Shared utilities: store import, data loading, write wrappers."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

THESIS_TYPES = [
    "growth_momentum",
    "pivot_breakout",
    "earnings_drift",
    "mean_reversion",
    "dividend_income",
]

EXIT_REASONS = ["stop_hit", "target_hit", "time_stop", "invalidated", "manual"]

IRA_ELIGIBLE_STRATEGIES = frozenset({"long_call", "long_put", ""})


def arrow_safe_df(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Cast display columns to str for PyArrow / Streamlit dataframe serialization."""
    out = df[columns].copy()
    for col in out.columns:
        out[col] = out[col].astype(str)
    return out


def get_repo_root() -> Path:
    """Walk up from this file until pyproject.toml is found."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Cannot locate repo root (no pyproject.toml found)")


def get_state_dir() -> Path:
    return get_repo_root() / "state" / "theses"


def _ensure_store_on_path() -> None:
    scripts_dir = str(get_repo_root() / "skills" / "trader-memory-core" / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)


def import_store() -> Any:
    """Return thesis_store module, adding its directory to sys.path first."""
    _ensure_store_on_path()
    import thesis_store  # noqa: PLC0415

    return thesis_store


# ── display / validation helpers ──────────────────────────────────────────────


def fmt_account(raw: str) -> str:
    """Convert a raw Robinhood account URL to a short display string."""
    if not raw:
        return "—"
    if raw.startswith("http"):
        parts = [p for p in raw.rstrip("/").split("/") if p]
        return f"rh:{parts[-1]}" if parts else raw
    return raw


def ira_options_eligible(account: str, strategy: str) -> bool:
    """Return False when an IRA account holds a non-covered options strategy."""
    if "ira" not in account.lower():
        return True
    return strategy in IRA_ELIGIBLE_STRATEGIES


def ira_badge_html(account: str, strategy: str) -> str | None:
    """Return badge HTML for IRA accounts, else None."""
    if "ira" not in account.lower():
        return None
    if ira_options_eligible(account, strategy):
        return (
            '<span style="background:#2d6a4f;color:#fff;'
            'padding:2px 8px;border-radius:4px;font-size:0.85em">'
            "IRA Eligible</span>"
        )
    return (
        '<span style="background:#b5192b;color:#fff;'
        'padding:2px 8px;border-radius:4px;font-size:0.85em">'
        "NOT IRA Eligible — check before submitting</span>"
    )


def days_to_expiry(expiry_str: str | None, as_of: date | None = None) -> int | None:
    """Days until expiry (negative if past). None when not parseable."""
    if not expiry_str:
        return None
    try:
        return (date.fromisoformat(str(expiry_str)) - (as_of or date.today())).days
    except (ValueError, TypeError):
        return None


def parse_price(text: str) -> float | None:
    """Try to parse a price string as float. Returns None if not numeric."""
    try:
        return float(text.strip().lstrip("$"))
    except (ValueError, AttributeError):
        return None


def build_thesis_data(
    ticker: str,
    thesis_type: str,
    thesis_text: str,
    confidence: int,
    stop_text: str,
    target_text: str,
    avg_cost: float,
    strategy: str = "",
) -> dict:
    """Assemble a thesis_data dict that thesis_store.register() accepts."""
    stop_price = parse_price(stop_text)
    target_price = parse_price(target_text)
    kill = []
    if stop_text.strip() and stop_price is None:
        kill = [stop_text.strip()]
    return {
        "ticker": ticker.upper(),
        "thesis_type": thesis_type,
        "thesis_statement": thesis_text.strip(),
        "setup_type": strategy or "manual",
        "catalyst": "",
        "mechanism_tag": "uncertain",
        "evidence": [],
        "kill_criteria": kill,
        "confidence": None,
        "confidence_score": round(confidence * 0.2, 1),
        "entry": {
            "target_price": avg_cost if avg_cost else None,
            "conditions": [],
        },
        "exit": {
            "stop_loss": stop_price,
            "stop_loss_pct": None,
            "take_profit": target_price,
            "take_profit_rr": None,
            "time_stop_days": None,
        },
        "origin": {
            "skill": "manual",
            "output_file": "manual",
            "screening_grade": None,
            "screening_score": None,
            "raw_provenance": {},
        },
        "monitoring": {"review_interval_days": 7},
    }


def validate_thesis_submit(
    thesis_data: dict,
    *,
    account: str = "",
    strategy: str = "",
    confidence: int | None = None,
) -> list[str]:
    """Return human-readable validation errors (empty list = OK)."""
    errors: list[str] = []
    statement = str(thesis_data.get("thesis_statement", "")).strip()
    if not statement:
        errors.append("thesis_statement is required")
    thesis_type = thesis_data.get("thesis_type", "")
    if thesis_type not in THESIS_TYPES:
        errors.append(f"Invalid thesis_type: {thesis_type!r}")
    if confidence is not None and confidence not in (1, 2, 3, 4, 5):
        errors.append("confidence must be 1–5")
    if account and strategy is not None and not ira_options_eligible(account, strategy):
        errors.append("NOT IRA Eligible — adjust strategy or account before submitting")
    return errors


def pending_duplicate_tickers(open_theses: list[dict], pending: list[dict]) -> set[str]:
    """Tickers present in both open theses and PENDING_THESIS rows."""
    open_tickers = {str(t.get("ticker", "")).upper() for t in open_theses}
    return {
        str(p.get("ticker", "")).upper()
        for p in pending
        if p.get("status") == "PENDING_THESIS" and str(p.get("ticker", "")).upper() in open_tickers
    }


def position_from_pending(pending: dict) -> dict:
    """Build thesis position block from a pending_ingest row."""
    asset_type = pending.get("asset_type", "")
    size = pending.get("contracts") if asset_type == "options" else pending.get("size")
    shares = int(size) if size else None
    raw_source: dict = {
        "skill": "pending_ingest",
        "file": "state/pending_ingest.json",
        "asset_type": asset_type,
        "direction": pending.get("direction"),
        "strategy": pending.get("strategy"),
        "strike": pending.get("strike"),
        "expiry": pending.get("expiry"),
        "option_type": pending.get("option_type"),
        "synced_at": pending.get("synced_at"),
    }
    return {
        "account_type": pending.get("account"),
        "shares": shares,
        "raw_source": {k: v for k, v in raw_source.items() if v is not None},
    }


def mark_pending_ingested(positions: list[dict], key: str, thesis_id: str) -> list[dict]:
    """Return updated positions list with one row marked INGESTED."""
    updated: list[dict] = []
    for row in positions:
        copy = dict(row)
        if copy.get("key") == key:
            copy["status"] = "INGESTED"
            copy["thesis_id"] = thesis_id
            copy["ingested_at"] = datetime.now().isoformat()
        updated.append(copy)
    return updated


def _entry_date_from_pending(pending: dict) -> str:
    synced = pending.get("synced_at")
    if synced:
        try:
            dt = datetime.fromisoformat(str(synced).replace("Z", "+00:00"))
            return f"{dt.date().isoformat()}T00:00:00+00:00"
        except (ValueError, TypeError):
            pass
    return format_exit_datetime(date.today())


# ── read helpers ──────────────────────────────────────────────────────────────


def load_theses(statuses: list[str] | None = None) -> list[dict]:
    """Return full thesis objects filtered by status list. Empty list if store missing."""
    store = import_store()
    state_dir = get_state_dir()
    if not state_dir.exists():
        return []
    if statuses is None:
        index_entries = store.query(state_dir)
    else:
        index_entries = []
        for s in statuses:
            index_entries.extend(store.query(state_dir, status=s))
    full_theses = []
    for entry in index_entries:
        tid = entry.get("thesis_id")
        if tid:
            try:
                full_theses.append(store.get(state_dir, tid))
            except Exception:  # noqa: BLE001
                full_theses.append(entry)
    return full_theses


def load_pending_ingest() -> list[dict]:
    """Read state/pending_ingest.json positions. Returns [] if file missing."""
    path = get_repo_root() / "state" / "pending_ingest.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        return data.get("positions", [])
    except (json.JSONDecodeError, OSError):
        return []


def save_pending_ingest(positions: list[dict]) -> None:
    """Overwrite positions list in state/pending_ingest.json."""
    path = get_repo_root() / "state" / "pending_ingest.json"
    try:
        existing = json.loads(path.read_text()) if path.exists() else {}
    except (json.JSONDecodeError, OSError):
        existing = {}
    existing["positions"] = positions
    path.write_text(json.dumps(existing, indent=2, default=str))


# ── write wrappers ─────────────────────────────────────────────────────────────


def register_thesis(thesis_data: dict) -> str:
    """Call thesis_store.register(). Returns thesis_id string."""
    store = import_store()
    return store.register(get_state_dir(), thesis_data)


def register_pending_position(thesis_data: dict, pending: dict) -> str:
    """Register thesis from pending ingest and promote to ACTIVE with position metadata."""
    account = str(pending.get("account", ""))
    strategy = str(pending.get("strategy", ""))
    errors = validate_thesis_submit(thesis_data, account=account, strategy=strategy)
    if errors:
        raise ValueError("; ".join(errors))

    store = import_store()
    state_dir = get_state_dir()
    thesis_id = store.register(state_dir, thesis_data)
    thesis = store.get(state_dir, thesis_id)
    if thesis["status"] == "IDEA":
        store.transition(state_dir, thesis_id, "ENTRY_READY", "position confirmed open")

    avg_cost = float(
        pending.get("avg_cost") or thesis_data.get("entry", {}).get("target_price") or 0
    )
    entry_date = _entry_date_from_pending(pending)
    size = (
        pending.get("contracts") if pending.get("asset_type") == "options" else pending.get("size")
    )
    shares = int(size) if size else None

    if store.get(state_dir, thesis_id)["status"] == "ENTRY_READY":
        store.open_position(
            state_dir,
            thesis_id,
            actual_price=avg_cost,
            actual_date=entry_date,
            reason="logged from pending ingest",
            shares=shares,
        )

    position = position_from_pending(pending)
    store.update(state_dir, thesis_id, {"position": position})
    return thesis_id


def format_exit_datetime(d: date) -> str:
    """RFC 3339 date-time required by thesis.schema.json (not bare YYYY-MM-DD)."""
    return f"{d.isoformat()}T00:00:00+00:00"


def close_thesis(
    thesis_id: str,
    exit_reason: str,
    actual_price: float,
    actual_date: str,
) -> dict:
    store = import_store()
    return store.close(get_state_dir(), thesis_id, exit_reason, actual_price, actual_date)


def terminate_thesis(
    thesis_id: str,
    terminal_status: str,
    exit_reason: str,
    actual_price: float | None = None,
    actual_date: str | None = None,
) -> dict:
    store = import_store()
    return store.terminate(
        get_state_dir(),
        thesis_id,
        terminal_status,
        exit_reason,
        actual_price=actual_price,
        actual_date=actual_date,
    )


def finalize_thesis(
    thesis_id: str,
    exit_reason: str,
    actual_price: float,
    exit_date: date,
) -> dict:
    """Close ACTIVE theses; terminate ENTRY_READY/IDEA as expired (INVALIDATED)."""
    store = import_store()
    state_dir = get_state_dir()
    thesis = store.get(state_dir, thesis_id)
    status = thesis.get("status", "")
    actual_date = format_exit_datetime(exit_date)
    if status == "ACTIVE":
        return store.close(state_dir, thesis_id, exit_reason, actual_price, actual_date)
    if status in ("ENTRY_READY", "IDEA"):
        label = exit_reason if exit_reason != "time_stop" else "expired worthless"
        return store.terminate(
            state_dir,
            thesis_id,
            "INVALIDATED",
            label,
            actual_price=actual_price,
            actual_date=actual_date,
        )
    raise ValueError(f"Cannot finalize thesis in status {status}")


def mark_reviewed(thesis_id: str, notes: str = "") -> dict:
    store = import_store()
    return store.mark_reviewed(
        get_state_dir(),
        thesis_id,
        review_date=date.today().isoformat(),
        notes=notes or None,
    )


def transition_thesis(thesis_id: str, new_status: str, reason: str) -> dict:
    store = import_store()
    return store.transition(get_state_dir(), thesis_id, new_status, reason)


def update_thesis(thesis_id: str, fields: dict) -> dict:
    store = import_store()
    return store.update(get_state_dir(), thesis_id, fields)


# ── derived metrics ───────────────────────────────────────────────────────────


def days_since_last_entry() -> int | None:
    """Days since most recent thesis created_at. None if no theses exist."""
    theses = load_theses()
    if not theses:
        return None
    dates: list[date] = []
    for t in theses:
        ca = t.get("created_at")
        if not ca:
            continue
        try:
            dt = datetime.fromisoformat(str(ca).replace("Z", "+00:00"))
            dates.append(dt.date())
        except (ValueError, TypeError):
            pass
    if not dates:
        return None
    return (date.today() - max(dates)).days
