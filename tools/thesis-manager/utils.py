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

THESIS_STATUSES = ["IDEA", "ENTRY_READY", "ACTIVE", "CLOSED", "INVALIDATED"]

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


def confidence_level_from_score(score: float | None) -> int:
    """Map confidence_score (0–1) to 1–5 slider level."""
    if not score:
        return 3
    return max(1, min(5, round(float(score) / 0.2)))


def stop_display(thesis: dict) -> str:
    """Format stop for edit forms: numeric stop_loss or first kill criterion."""
    exit_d = thesis.get("exit") or {}
    stop_loss = exit_d.get("stop_loss")
    if stop_loss is not None:
        return str(stop_loss)
    kill = thesis.get("kill_criteria") or []
    return str(kill[0]) if kill else ""


def target_display(thesis: dict) -> str:
    """Format take-profit for edit forms."""
    exit_d = thesis.get("exit") or {}
    take_profit = exit_d.get("take_profit")
    return str(take_profit) if take_profit is not None else ""


def build_update_fields(
    *,
    thesis_text: str,
    confidence: int,
    stop_text: str,
    target_text: str,
    catalyst: str = "",
    setup_type: str | None = None,
    review_interval_days: int | None = None,
    lessons_learned: str | None = None,
    what_happened: str | None = None,
) -> dict:
    """Build fields dict for thesis_store.update() from form values."""
    stop_price = parse_price(stop_text)
    target_price = parse_price(target_text)
    kill: list[str] = []
    if stop_text.strip() and stop_price is None:
        kill = [stop_text.strip()]

    fields: dict[str, Any] = {
        "thesis_statement": thesis_text.strip(),
        "confidence_score": round(confidence * 0.2, 1),
        "exit": {
            "stop_loss": stop_price if stop_text.strip() else None,
            "take_profit": target_price if target_text.strip() else None,
        },
        "kill_criteria": kill,
    }
    fields["catalyst"] = catalyst.strip() or None
    if setup_type is not None:
        fields["setup_type"] = setup_type.strip() or None
    if review_interval_days is not None:
        fields["monitoring"] = {"review_interval_days": review_interval_days}
    if lessons_learned is not None or what_happened is not None:
        outcome: dict[str, Any] = {}
        if lessons_learned is not None:
            outcome["lessons_learned"] = lessons_learned.strip() or None
        if what_happened is not None:
            outcome["what_happened"] = what_happened.strip() or None
        fields["outcome"] = outcome
    return fields


def validate_thesis_update(
    fields: dict,
    *,
    confidence: int | None = None,
) -> list[str]:
    """Return human-readable validation errors for update payloads."""
    errors: list[str] = []
    if not str(fields.get("thesis_statement", "")).strip():
        errors.append("thesis_statement is required")
    if confidence is not None and confidence not in (1, 2, 3, 4, 5):
        errors.append("confidence must be 1–5")
    mon = fields.get("monitoring") or {}
    interval = mon.get("review_interval_days")
    if interval is not None and int(interval) < 1:
        errors.append("review_interval_days must be at least 1")
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


def get_thesis(thesis_id: str) -> dict:
    """Load one thesis by ID."""
    store = import_store()
    return store.get(get_state_dir(), thesis_id)


def sort_theses_for_display(theses: list[dict]) -> list[dict]:
    """Newest created first, then ticker."""

    def sort_key(t: dict) -> tuple[str, str]:
        return (str(t.get("created_at") or ""), str(t.get("ticker") or ""))

    return sorted(theses, key=sort_key, reverse=True)


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
    path = get_pending_ingest_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = json.loads(path.read_text()) if path.exists() else {}
    except (json.JSONDecodeError, OSError):
        existing = {}
    if not isinstance(existing, dict):
        existing = {}
    existing["positions"] = positions
    existing["last_updated"] = datetime.now().isoformat()
    path.write_text(json.dumps(existing, indent=2, default=str) + "\n")


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


def delete_thesis(thesis_id: str, *, force: bool = False) -> str:
    store = import_store()
    return store.delete(get_state_dir(), thesis_id, force=force)


def stop_tracking_thesis(thesis_id: str, reason: str = "stopped tracking") -> dict:
    """Invalidate non-terminal theses without recording P&L."""
    store = import_store()
    state_dir = get_state_dir()
    thesis = store.get(state_dir, thesis_id)
    status = thesis.get("status", "")
    if status in ("CLOSED", "INVALIDATED"):
        return thesis
    return store.terminate(
        state_dir,
        thesis_id,
        "INVALIDATED",
        reason,
        actual_price=None,
        actual_date=None,
    )


def get_synced_positions_path() -> Path:
    return get_repo_root() / "state" / "synced_positions.json"


def get_pending_ingest_path() -> Path:
    return get_repo_root() / "state" / "pending_ingest.json"


def _load_synced_state() -> dict:
    path = get_synced_positions_path()
    if not path.exists():
        return {"ingested_keys": [], "pending_keys": []}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {"ingested_keys": [], "pending_keys": []}
    if not isinstance(data, dict):
        return {"ingested_keys": [], "pending_keys": []}
    data.setdefault("ingested_keys", [])
    data.setdefault("pending_keys", [])
    return data


def block_sync_key(key: str) -> None:
    """Prevent robinhood_sync from re-adding this position key."""
    path = get_synced_positions_path()
    state = _load_synced_state()
    ingested = list(state.get("ingested_keys") or [])
    if key not in ingested:
        ingested.append(key)
    state["ingested_keys"] = ingested
    pending = [k for k in (state.get("pending_keys") or []) if k != key]
    state["pending_keys"] = pending
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n")


def mark_pending_skipped(positions: list[dict], key: str) -> list[dict]:
    """Return updated positions list with one row marked SKIPPED."""
    updated: list[dict] = []
    for row in positions:
        copy = dict(row)
        if copy.get("key") == key:
            copy["status"] = "SKIPPED"
            copy["skipped_at"] = datetime.now().isoformat()
        updated.append(copy)
    return updated


def is_ticker_excluded(ticker: str) -> bool:
    sys.path.insert(0, str(get_repo_root() / "scripts"))
    from research_watchlist import (  # noqa: PLC0415
        load_exclude_config,
        resolve_exclude_path_for_filter,
    )

    exclude_path = resolve_exclude_path_for_filter()
    if not exclude_path:
        return False
    return ticker.upper() in load_exclude_config(exclude_path)


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
