"""Shared helpers for research watchlist and staleness detection."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

_REPORT_DATE_RE = re.compile(r"^(.+)_(20\d{2}-\d{2}-\d{2})\.md$")
_POSITION_STATUSES = ("ACTIVE", "ENTRY_READY")


def get_repo_root() -> Path:
    """Walk up from this file until pyproject.toml is found."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Cannot locate repo root (no pyproject.toml found)")


def load_watchlist_config(path: Path) -> dict[str, dict]:
    """Load watchlist YAML; return ticker -> {watching, notes, optional tier_pin}."""
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        return {}
    result: dict[str, dict] = {}
    for ticker, entry in data.items():
        if not isinstance(entry, dict):
            continue
        row: dict = {
            "watching": bool(entry.get("watching", False)),
            "notes": str(entry.get("notes", "")),
        }
        raw_pin = entry.get("tier_pin")
        if raw_pin is not None and str(raw_pin).strip():
            row["tier_pin"] = str(raw_pin).strip().upper()
        result[str(ticker).upper()] = row
    return result


def load_exclude_config(path: Path) -> dict[str, dict]:
    """Load exclude YAML; return ticker -> {reason}."""
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        return {}
    result: dict[str, dict] = {}
    for ticker, entry in data.items():
        if isinstance(entry, dict):
            result[str(ticker).upper()] = {"reason": str(entry.get("reason", ""))}
        elif entry is not None:
            result[str(ticker).upper()] = {"reason": str(entry)}
    return result


def resolve_exclude_path_for_filter(repo_root: Path | None = None) -> Path | None:
    """Return user exclude config path if it exists (not the example file)."""
    root = repo_root or get_repo_root()
    path = root / "config" / "research_exclude.yaml"
    return path if path.exists() else None


def apply_exclude(tickers: list[str] | set[str], exclude_path: Path | None) -> list[str]:
    """Drop tickers present in the exclude config."""
    if not exclude_path or not exclude_path.exists():
        return sorted(tickers)
    excluded = set(load_exclude_config(exclude_path).keys())
    return sorted(t for t in tickers if str(t).upper() not in excluded)


def tickers_from_theses(state_dir: Path, statuses: tuple[str, ...]) -> set[str]:
    """Return tickers from thesis YAML files matching any of the given statuses."""
    if not state_dir.exists():
        return set()
    allowed = {s.upper() for s in statuses}
    tickers: set[str] = set()
    for f in state_dir.glob("*.yaml"):
        if f.name.startswith("_"):
            continue
        try:
            data = yaml.safe_load(f.read_text()) or {}
        except Exception:
            continue
        status = str(data.get("status", "")).upper()
        if status not in allowed:
            continue
        ticker = str(data.get("ticker", f.stem)).upper()
        tickers.add(ticker)
    return tickers


def _watching_tickers(watchlist_path: Path) -> set[str]:
    return {t for t, cfg in load_watchlist_config(watchlist_path).items() if cfg.get("watching")}


def eligibility_for_tickers(
    state_dir: Path,
    watchlist_path: Path,
    exclude_path: Path | None = None,
) -> dict[str, list[str]]:
    """Map each eligible ticker to its eligibility reasons."""
    reasons: dict[str, list[str]] = {}

    for ticker in tickers_from_theses(state_dir, _POSITION_STATUSES):
        reasons.setdefault(ticker, []).append("position")

    watching = _watching_tickers(watchlist_path)
    for ticker in watching:
        if "watchlist" not in reasons.get(ticker, []):
            reasons.setdefault(ticker, []).append("watchlist")

    idea_tickers = tickers_from_theses(state_dir, ("IDEA",))
    for ticker in idea_tickers:
        if ticker in watching and "idea" not in reasons.get(ticker, []):
            reasons.setdefault(ticker, []).append("idea")

    if exclude_path is None:
        exclude_path = resolve_exclude_path_for_filter()
    if exclude_path and exclude_path.exists():
        excluded = set(load_exclude_config(exclude_path).keys())
        reasons = {k: v for k, v in reasons.items() if k not in excluded}

    return reasons


def eligible_tickers(
    state_dir: Path,
    watchlist_path: Path,
    exclude_path: Path | None = None,
) -> list[str]:
    """Union of position tickers and watchlist; IDEA only when also on watchlist."""
    return sorted(eligibility_for_tickers(state_dir, watchlist_path, exclude_path=exclude_path))


def latest_report_date(research_dir: Path, ticker: str) -> date | None:
    """Return the newest report date for a ticker, parsed from filename."""
    if not research_dir.exists():
        return None
    latest: date | None = None
    prefix = f"{ticker.upper()}_"
    for path in research_dir.glob(f"{ticker.upper()}_*.md"):
        match = _REPORT_DATE_RE.match(path.name)
        if match and match.group(1).upper() == ticker.upper():
            report_date = date.fromisoformat(match.group(2))
            if latest is None or report_date > latest:
                latest = report_date
        elif path.name.startswith(prefix):
            suffix = path.name[len(prefix) : -3]
            try:
                report_date = date.fromisoformat(suffix)
            except ValueError:
                continue
            if latest is None or report_date > latest:
                latest = report_date
    return latest


def days_stale(latest: date | None, as_of: date) -> int | None:
    """Days since latest report; None if no report exists."""
    if latest is None:
        return None
    return (as_of - latest).days


def build_staleness_rows(
    tickers: list[str],
    research_dir: Path,
    as_of: date,
    threshold_days: int,
    eligibility_map: dict[str, list[str]],
) -> list[dict]:
    """Build staleness rows for eligible tickers."""
    rows: list[dict] = []
    for ticker in sorted(tickers):
        latest = latest_report_date(research_dir, ticker)
        stale_days = days_stale(latest, as_of)
        eligibility = eligibility_map.get(ticker, [])

        if latest is None:
            status = "needs_deep_research"
            needs_update = True
        elif stale_days is not None and stale_days > threshold_days:
            status = "needs_update"
            needs_update = True
        else:
            status = "current"
            needs_update = False

        rows.append(
            {
                "ticker": ticker,
                "last_report": latest.isoformat() if latest else None,
                "days_stale": stale_days,
                "eligibility": eligibility,
                "reason": ", ".join(eligibility),
                "needs_update": needs_update,
                "status": status,
            }
        )
    return rows
