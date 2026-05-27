"""Shared utilities: store import, data loading, write wrappers."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


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


def close_thesis(
    thesis_id: str,
    exit_reason: str,
    actual_price: float,
    actual_date: str,
) -> dict:
    store = import_store()
    return store.close(get_state_dir(), thesis_id, exit_reason, actual_price, actual_date)


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
