"""Research dashboard helpers — thin wrapper over scripts/research_watchlist.py."""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import utils
import yaml

sys.path.insert(0, str(utils.get_repo_root() / "scripts"))
from research_watchlist import (  # noqa: E402
    build_staleness_rows,
    eligibility_for_tickers,
    eligible_tickers,
    get_repo_root,
    load_exclude_config,
    load_watchlist_config,
    resolve_exclude_path_for_filter,
)

STALE_THRESHOLD_DAYS = 14
_REPORT_DATE_RE = re.compile(r"^(.+)_(20\d{2}-\d{2}-\d{2})\.md$")
_PREFETCH_DATE_RE = re.compile(r"^(.+)_(20\d{2}-\d{2}-\d{2})\.json$")
_STATUS_PRIORITY = {"ACTIVE": 0, "ENTRY_READY": 1, "IDEA": 2}


def _repo() -> Path:
    return get_repo_root()


def _state_dir() -> Path:
    return _repo() / "state" / "theses"


def _research_dir() -> Path:
    return _repo() / "reports" / "research"


def _prefetch_dir() -> Path:
    return _repo() / "reports" / "logs" / "research_prefetch"


def _queue_path() -> Path:
    return _repo() / "state" / "research_update_queue.json"


def resolve_watchlist_path() -> Path:
    path = _repo() / "config" / "research_watchlist.yaml"
    if path.exists():
        return path
    return _repo() / "config" / "research_watchlist.yaml.example"


def resolve_exclude_path() -> Path:
    """Path for exclude editor (user file or example template)."""
    path = _repo() / "config" / "research_exclude.yaml"
    if path.exists():
        return path
    return _repo() / "config" / "research_exclude.yaml.example"


def _archive_research_dir() -> Path:
    return _repo() / "reports" / "archive" / "research"


def excluded_ticker_set() -> set[str]:
    exclude_path = resolve_exclude_path_for_filter()
    if not exclude_path:
        return set()
    return set(load_exclude_config(exclude_path).keys())


def staleness_badge(days: int | None) -> str:
    if days is None:
        return "MISSING"
    if days <= 7:
        return "OK"
    if days <= STALE_THRESHOLD_DAYS:
        return "WARN"
    return "STALE"


def _parse_report_file(path: Path) -> tuple[str, date] | None:
    """Return (ticker, report_date) for a report filename, or None if not parseable."""
    match = _REPORT_DATE_RE.match(path.name)
    if match:
        return match.group(1).upper(), date.fromisoformat(match.group(2))
    if "_" not in path.stem:
        return None
    ticker_part, _, date_part = path.stem.partition("_")
    try:
        return ticker_part.upper(), date.fromisoformat(date_part)
    except ValueError:
        return None


def open_report_path(ticker: str) -> Path | None:
    reports = list_reports_for_ticker(ticker)
    return reports[0]["path"] if reports else None


def list_report_tickers() -> list[str]:
    research_dir = _research_dir()
    if not research_dir.exists():
        return []
    excluded = excluded_ticker_set()
    tickers: set[str] = set()
    for path in research_dir.glob("*.md"):
        parsed = _parse_report_file(path)
        if parsed and parsed[0] not in excluded:
            tickers.add(parsed[0])
    return sorted(tickers)


def archive_report(path: Path) -> Path:
    """Move a research report into reports/archive/research/."""
    if not path.is_file():
        raise FileNotFoundError(f"Report not found: {path}")
    dest_dir = _archive_research_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    if dest.exists():
        raise FileExistsError(f"Archive already exists: {dest}")
    path.rename(dest)
    return dest


def list_reports_for_ticker(ticker: str) -> list[dict]:
    research_dir = _research_dir()
    if not research_dir.exists():
        return []
    ticker_upper = ticker.upper()
    entries: list[dict] = []
    for path in research_dir.glob(f"{ticker_upper}_*.md"):
        report_date: date | None = None
        match = _REPORT_DATE_RE.match(path.name)
        if match and match.group(1).upper() == ticker_upper:
            report_date = date.fromisoformat(match.group(2))
        elif path.name.startswith(f"{ticker_upper}_"):
            try:
                report_date = date.fromisoformat(path.name[len(ticker_upper) + 1 : -3])
            except ValueError:
                continue
        if report_date is not None:
            entries.append({"date": report_date, "path": path})
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries


def load_report_markdown(path: Path) -> str | None:
    try:
        if path.is_file():
            return path.read_text(encoding="utf-8")
    except OSError:
        return None
    return None


def latest_prefetch_path(ticker: str) -> Path | None:
    prefetch_dir = _prefetch_dir()
    if not prefetch_dir.exists():
        return None
    latest: tuple[date, Path] | None = None
    prefix = f"{ticker.upper()}_"
    for path in prefetch_dir.glob(f"{ticker.upper()}_*.json"):
        file_date: date | None = None
        match = _PREFETCH_DATE_RE.match(path.name)
        if match and match.group(1).upper() == ticker.upper():
            file_date = date.fromisoformat(match.group(2))
        elif path.name.startswith(prefix):
            try:
                file_date = date.fromisoformat(path.name[len(prefix) : -5])
            except ValueError:
                continue
        if file_date and (latest is None or file_date > latest[0]):
            latest = (file_date, path)
    return latest[1] if latest else None


def load_update_queue() -> dict | None:
    path = _queue_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError):
        return None


def _thesis_status_map() -> dict[str, str]:
    status_map: dict[str, str] = {}
    for thesis in utils.load_theses(["ACTIVE", "ENTRY_READY", "IDEA"]):
        ticker = str(thesis.get("ticker", "")).upper()
        status = str(thesis.get("status", "")).upper()
        if not ticker or status not in _STATUS_PRIORITY:
            continue
        existing = status_map.get(ticker)
        if existing is None or _STATUS_PRIORITY[status] < _STATUS_PRIORITY[existing]:
            status_map[ticker] = status
    return status_map


def _queue_status_map(queue: dict | None) -> dict[str, str]:
    if not queue:
        return {}
    result: dict[str, str] = {}
    for entry in queue.get("tickers") or []:
        if not isinstance(entry, dict):
            continue
        ticker = str(entry.get("ticker", "")).upper()
        status = str(entry.get("status", "queued"))
        if ticker:
            result[ticker] = status
    return result


def _derive_ui_status(
    row: dict,
    queue_map: dict[str, str],
    ticker: str,
) -> str:
    if row["status"] == "needs_deep_research":
        return "missing"
    if row["status"] == "needs_update":
        return "stale"
    if ticker in queue_map:
        return "queued"
    return "fresh"


def get_research_dashboard_rows(as_of: date | None = None) -> list[dict]:
    as_of = as_of or date.today()
    watchlist_path = resolve_watchlist_path()
    exclude_path = resolve_exclude_path_for_filter()
    state_dir = _state_dir()
    research_dir = _research_dir()

    eligibility_map = eligibility_for_tickers(state_dir, watchlist_path, exclude_path=exclude_path)
    tickers = eligible_tickers(state_dir, watchlist_path, exclude_path=exclude_path)
    stale_rows = build_staleness_rows(
        tickers=tickers,
        research_dir=research_dir,
        as_of=as_of,
        threshold_days=STALE_THRESHOLD_DAYS,
        eligibility_map=eligibility_map,
    )

    watchlist = load_watchlist_config(watchlist_path)
    thesis_map = _thesis_status_map()
    queue = load_update_queue()
    queue_map = _queue_status_map(queue)

    rows: list[dict] = []
    for row in stale_rows:
        ticker = row["ticker"]
        report_path = open_report_path(ticker)
        prefetch_path = latest_prefetch_path(ticker)
        days = row["days_stale"]
        thesis_status = thesis_map.get(ticker, "—")
        watching = watchlist.get(ticker, {}).get("watching", False)
        notes = watchlist.get(ticker, {}).get("notes", "")

        rows.append(
            {
                "ticker": ticker,
                "last_report_date": row["last_report"],
                "days_stale": days,
                "report_path": report_path,
                "thesis_status": thesis_status,
                "watching": watching,
                "eligibility": row["eligibility"],
                "queue_status": queue_map.get(ticker),
                "prefetch_available": prefetch_path is not None,
                "prefetch_path": prefetch_path,
                "ui_status": _derive_ui_status(row, queue_map, ticker),
                "badge": staleness_badge(days),
                "notes": notes,
            }
        )
    return rows


def queue_recent_count(days: int = 7) -> int:
    queue = load_update_queue()
    if not queue:
        return 0
    generated = queue.get("generated_at")
    if not generated:
        return 0
    try:
        ts = datetime.fromisoformat(str(generated).replace("Z", "+00:00"))
        if ts.tzinfo:
            ts = ts.replace(tzinfo=None) - (ts.utcoffset() or timedelta())
        if (datetime.now() - ts).days > days:
            return 0
    except (ValueError, TypeError):
        return 0
    tickers = queue.get("tickers") or []
    return len(tickers) if isinstance(tickers, list) else 0


def build_update_prompt(ticker: str, as_of: date | None = None) -> str:
    as_of = as_of or date.today()
    prefetch = latest_prefetch_path(ticker)
    lines = [f"Follow commands/update-research.md for {ticker}."]
    if prefetch:
        rel = prefetch.relative_to(_repo())
        lines.append(f"Prefetch data: {rel}")
    lines.append(f"Save to reports/research/{ticker}_{as_of.isoformat()}.md")
    return "\n".join(lines)


def build_deep_research_prompt(ticker: str) -> str:
    return f"Follow commands/deep-research.md for {ticker}"


def load_watchlist_for_editor() -> dict[str, dict]:
    return load_watchlist_config(resolve_watchlist_path())


def save_watchlist(entries: dict[str, dict]) -> None:
    """Validate and atomically write config/research_watchlist.yaml."""
    path = _repo() / "config" / "research_watchlist.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized: dict[str, dict] = {}
    for ticker, entry in entries.items():
        t = str(ticker).strip().upper()
        if not t:
            continue
        if t in normalized:
            raise ValueError(f"Duplicate ticker: {t}")
        normalized[t] = {
            "watching": bool(entry.get("watching", False)),
            "notes": str(entry.get("notes", "")),
        }

    payload: dict = {}
    for ticker in sorted(normalized):
        payload[ticker] = normalized[ticker]

    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".yaml")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write("# Research watchlist — tickers tracked without a position\n")
            yaml.safe_dump(payload, fh, default_flow_style=False, sort_keys=False)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_exclude_for_editor() -> dict[str, dict]:
    return load_exclude_config(resolve_exclude_path())


def save_exclude(entries: dict[str, dict]) -> None:
    """Validate and atomically write config/research_exclude.yaml."""
    path = _repo() / "config" / "research_exclude.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized: dict[str, dict] = {}
    for ticker, entry in entries.items():
        t = str(ticker).strip().upper()
        if not t:
            continue
        if t in normalized:
            raise ValueError(f"Duplicate ticker: {t}")
        normalized[t] = {"reason": str(entry.get("reason", "") or "")}

    payload: dict = {}
    for ticker in sorted(normalized):
        payload[ticker] = normalized[ticker]

    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".yaml")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write("# Excluded tickers — hidden from Research, Reports, staleness\n")
            yaml.safe_dump(payload, fh, default_flow_style=False, sort_keys=False)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def add_exclude_ticker(ticker: str, reason: str = "") -> None:
    """Merge one ticker into research_exclude.yaml."""
    user_path = _repo() / "config" / "research_exclude.yaml"
    entries = load_exclude_config(user_path) if user_path.exists() else {}
    t = ticker.strip().upper()
    entries[t] = {"reason": reason.strip()}
    save_exclude(entries)
