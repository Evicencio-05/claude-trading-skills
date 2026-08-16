"""Deterministic A/B/C/D conviction tiers for research watchlist and entry focus."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from report_paths import find_screener_for_ticker, logs_dir
from research_artifacts import extract_ticker_row, load_watchlist_symbols
from research_watchlist import (
    get_repo_root,
    load_watchlist_config,
    resolve_exclude_path_for_filter,
)

TIER_A_CAP = 5
STALE_DAYS = 14

_VERDICT_RE = re.compile(r"\*\*Verdict:\*\*\s*(.+)", re.IGNORECASE)
_CONFIDENCE_RE = re.compile(r"\*\*Confidence:\*\*\s*(.+)", re.IGNORECASE)

_TIER_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}

_BUY_VERDICT_MARKERS = ("strong buy", "buy on pullback", "buy (", "buy —", "buy -", "**buy")
_NEGATIVE_VERDICT_MARKERS = ("watch", "avoid", "short", "hold", "sell")

_VCP_STRONG_RATINGS = ("textbook vcp", "strong vcp", "good vcp")

_SCREENER_KEYS = ("vcp_screener", "canslim_screener", "earnings_trade_analyzer")


@dataclass
class TierResult:
    tier: str
    tier_score: int
    tier_reasons: list[str] = field(default_factory=list)
    verdict: str | None = None
    research_confidence: str | None = None
    screener_summary: str = ""
    market_gate: str = "UNKNOWN"
    thesis_confidence_1_5: str = "—"


def parse_quick_glance(text: str) -> dict[str, str | None]:
    """Extract Verdict and Confidence from deep-research Quick Glance section."""
    verdict: str | None = None
    confidence: str | None = None
    for line in text.splitlines():
        vm = _VERDICT_RE.search(line)
        if vm:
            verdict = vm.group(1).strip()
        cm = _CONFIDENCE_RE.search(line)
        if cm:
            raw = cm.group(1).strip()
            confidence = re.sub(r"\*+", "", raw).split("—")[0].split(" - ")[0].strip()
    return {"verdict": verdict, "research_confidence": confidence}


def _strip_verdict_markup(verdict: str | None) -> str:
    if not verdict:
        return ""
    return verdict.replace("**", "").strip()


def is_buy_verdict(verdict: str | None) -> bool:
    v = _strip_verdict_markup(verdict).lower()
    if not v:
        return False
    if any(m in v for m in _NEGATIVE_VERDICT_MARKERS):
        if "buy" in v and ("buy on" in v or "strong buy" in v):
            return True
        if v.startswith("buy") or " buy" in v:
            return True
        return False
    return any(m in v for m in _BUY_VERDICT_MARKERS) or v.startswith("buy")


def is_negative_verdict(verdict: str | None) -> bool:
    v = _strip_verdict_markup(verdict).lower()
    if not v:
        return False
    if is_buy_verdict(verdict):
        return False
    return any(m in v for m in _NEGATIVE_VERDICT_MARKERS)


def screener_is_strong(source: str, row: dict | None) -> bool:
    if not row:
        return False
    if source == "vcp_screener":
        rating = str(row.get("rating", "")).lower()
        return any(r in rating for r in _VCP_STRONG_RATINGS)
    if source == "canslim_screener":
        score = float(row.get("composite_score") or 0)
        rating = str(row.get("rating", "")).lower()
        if score >= 70:
            return True
        return score >= 65 and ("leader" in rating or "above average" in rating)
    if source == "earnings_trade_analyzer":
        return str(row.get("grade", "")).upper() in ("A", "B")
    return False


def _format_screener_summary(source: str, row: dict) -> str:
    if source == "vcp_screener":
        return f"VCP {row.get('rating', '?')}"
    if source == "canslim_screener":
        return f"CANSLIM {row.get('composite_score', '?')}"
    if source == "earnings_trade_analyzer":
        return f"Earnings {row.get('grade', '?')}"
    return source


def best_screener_for_ticker(
    repo_root: Path,
    ticker: str,
    as_of: date,
    watchlist_symbols: list[str] | None = None,
) -> tuple[bool, str]:
    """Return (is_strong, summary) from best same-day screener hit."""
    symbols = watchlist_symbols or load_watchlist_symbols(
        repo_root / "config" / "research_watchlist.yaml"
    )
    best_summary = ""
    for key in _SCREENER_KEYS:
        path = find_screener_for_ticker(repo_root, key, ticker, as_of, symbols)
        if path is None:
            continue
        row = extract_ticker_row(path, ticker)
        if row and screener_is_strong(key, row):
            return True, _format_screener_summary(key, row)
        if row and not best_summary:
            best_summary = _format_screener_summary(key, row)
    return False, best_summary


def load_market_gate(repo_root: Path, as_of: date) -> str:
    """Latest exposure recommendation or market_context posture fallback."""
    date_str = as_of.isoformat()
    exposure_dir = repo_root / "reports" / "market" / "exposure"
    pattern = f"exposure_posture_{date_str}_*.json"
    candidates: list[Path] = []
    if exposure_dir.exists():
        candidates.extend(sorted(exposure_dir.glob(pattern)))
    for path in reversed(candidates):
        try:
            data = json.loads(path.read_text())
            rec = str(data.get("recommendation", "")).strip().upper()
            if rec:
                return rec
        except (json.JSONDecodeError, OSError):
            continue

    ctx_path = logs_dir(repo_root) / f"market_context_{date_str}.json"
    if ctx_path.exists():
        try:
            data = json.loads(ctx_path.read_text())
            posture = str((data.get("synthesis") or {}).get("posture", "")).upper()
            if posture == "CAUTIOUS":
                return "REDUCE_ONLY"
            if posture:
                return posture
        except (json.JSONDecodeError, OSError):
            pass
    return "UNKNOWN"


def _confidence_1_5(score: float | None) -> str:
    if score is None:
        return "—"
    return str(max(1, min(5, round(score * 5))))


def _apply_tier_pin(base_tier: str, pin: str | None, reasons: list[str]) -> str:
    if not pin or base_tier == "D":
        return base_tier
    pin = pin.upper()
    if pin not in _TIER_ORDER:
        return base_tier
    if _TIER_ORDER[pin] < _TIER_ORDER[base_tier]:
        reasons.append(f"tier_pin:{pin}")
        return pin
    return base_tier


def compute_tier_score(
    *,
    thesis_status: str,
    confidence_score: float | None,
    buy_verdict: bool,
    screener_strong: bool,
    days_stale: int | None,
    has_report: bool,
) -> int:
    score = 0
    if thesis_status == "ENTRY_READY":
        score += 100
    elif thesis_status == "ACTIVE":
        score += 90
    elif thesis_status == "IDEA":
        score += 40
    if confidence_score is not None:
        score += int(confidence_score * 20)
    if buy_verdict:
        score += 30
    if screener_strong:
        score += 15
    if has_report and days_stale is not None and days_stale <= STALE_DAYS:
        score += 10
    elif has_report:
        score += 2
    return score


def compute_tier_for_ticker(
    *,
    ticker: str,
    watching: bool,
    thesis_status: str,
    confidence_score: float | None,
    days_stale: int | None,
    verdict: str | None,
    research_confidence: str | None,
    screener_strong: bool,
    screener_summary: str,
    market_gate: str,
    tier_pin: str | None,
    has_report: bool,
) -> TierResult:
    """Assign base tier A/B/C/D before apply_tier_a_cap."""
    reasons: list[str] = []
    status = thesis_status if thesis_status != "—" else ""
    buy = is_buy_verdict(verdict)
    stale = days_stale is not None and days_stale > STALE_DAYS
    conf_ok = confidence_score is not None and confidence_score >= 0.8
    gate = market_gate.upper()

    score = compute_tier_score(
        thesis_status=status or "—",
        confidence_score=confidence_score,
        buy_verdict=buy,
        screener_strong=screener_strong,
        days_stale=days_stale,
        has_report=has_report,
    )

    # D — parked
    if status == "INVALIDATED":
        reasons.append("thesis_invalidated")
        return TierResult(
            tier="D",
            tier_score=0,
            tier_reasons=reasons,
            verdict=verdict,
            research_confidence=research_confidence,
            screener_summary=screener_summary,
            market_gate=gate,
            thesis_confidence_1_5=_confidence_1_5(confidence_score),
        )

    if not watching and status not in ("ACTIVE", "ENTRY_READY", "IDEA"):
        reasons.append("not_watching")
        return TierResult(
            tier="D",
            tier_score=0,
            tier_reasons=reasons,
            verdict=verdict,
            research_confidence=research_confidence,
            screener_summary=screener_summary,
            market_gate=gate,
            thesis_confidence_1_5=_confidence_1_5(confidence_score),
        )

    tier = "C"

    # A candidates
    a_ok = (
        status == "ENTRY_READY"
        and conf_ok
        and has_report
        and not stale
        and buy
        and gate != "CASH_PRIORITY"
    )
    if a_ok:
        tier = "A"
        reasons.append("entry_ready_high_conviction")
    elif status == "ENTRY_READY" and gate == "CASH_PRIORITY":
        tier = "B"
        reasons.append("cash_priority_blocks_tier_a")
    elif status == "ENTRY_READY":
        tier = "B"
        if not conf_ok:
            reasons.append("confidence_below_4_of_5")
        elif not buy:
            reasons.append("verdict_not_buy")
        elif stale:
            reasons.append("report_stale")
    elif has_report and not stale and buy and (status == "IDEA" or screener_strong):
        tier = "B"
        reasons.append("developing_setup")
    elif not has_report:
        tier = "C"
        reasons.append("missing_deep_research")
    elif stale and not tier_pin:
        tier = "C"
        reasons.append("report_stale")
    elif is_negative_verdict(verdict):
        tier = "C"
        reasons.append("watch_or_avoid_verdict")
    else:
        tier = "C"
        reasons.append("probe_default")

    tier = _apply_tier_pin(tier, tier_pin, reasons)

    return TierResult(
        tier=tier,
        tier_score=score,
        tier_reasons=reasons,
        verdict=verdict,
        research_confidence=research_confidence,
        screener_summary=screener_summary,
        market_gate=gate,
        thesis_confidence_1_5=_confidence_1_5(confidence_score),
    )


def tier_order_key(row: dict) -> tuple[int, int]:
    """Sort key: tier A first, then higher score."""
    tier = str(row.get("tier", "D")).upper()
    order = _TIER_ORDER.get(tier, 9)
    score = int(row.get("tier_score") or 0)
    return (order, -score)


def apply_tier_a_cap(rows: list[dict], cap: int = TIER_A_CAP) -> list[dict]:
    """Keep at most `cap` Tier A rows by tier_score; demote overflow to B."""
    a_rows = [r for r in rows if r.get("tier") == "A"]
    if len(a_rows) <= cap:
        return rows

    a_rows_sorted = sorted(a_rows, key=lambda r: int(r.get("tier_score") or 0), reverse=True)
    keep = {r["ticker"] for r in a_rows_sorted[:cap]}
    out: list[dict] = []
    for row in rows:
        r = dict(row)
        if r.get("tier") == "A" and r["ticker"] not in keep:
            r["tier"] = "B"
            r["tier_a_capped"] = True
            reasons = list(r.get("tier_reasons") or [])
            reasons.append("tier_a_cap")
            r["tier_reasons"] = reasons
        else:
            r.setdefault("tier_a_capped", False)
        out.append(r)
    return out


def _load_thesis_map(state_dir: Path) -> dict[str, dict]:
    import yaml

    result: dict[str, dict] = {}
    if not state_dir.exists():
        return result
    for path in state_dir.glob("*.yaml"):
        if path.name.startswith("_"):
            continue
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except Exception:
            continue
        ticker = str(data.get("ticker", "")).upper()
        if ticker:
            result[ticker] = data
    return result


def enrich_dashboard_rows(
    rows: list[dict],
    repo_root: Path,
    as_of: date,
    *,
    state_dir: Path | None = None,
    watchlist_path: Path | None = None,
) -> list[dict]:
    """Add tier fields to research dashboard row dicts."""
    root = repo_root
    state_dir = state_dir or (root / "state" / "theses")
    if watchlist_path is None:
        watchlist_path = root / "config" / "research_watchlist.yaml"
        if not watchlist_path.exists():
            watchlist_path = root / "config" / "research_watchlist.yaml.example"

    watchlist = load_watchlist_config(watchlist_path)
    thesis_map = _load_thesis_map(state_dir)
    market_gate = load_market_gate(root, as_of)
    symbols = load_watchlist_symbols(watchlist_path)

    enriched: list[dict] = []
    for row in rows:
        ticker = row["ticker"]
        wl = watchlist.get(ticker, {})
        thesis = thesis_map.get(ticker, {})
        thesis_status = row.get("thesis_status") or "—"
        if thesis_status == "—" and thesis:
            thesis_status = str(thesis.get("status", "—")).upper()

        report_path = row.get("report_path")
        qg = {"verdict": None, "research_confidence": None}
        if report_path and Path(report_path).exists():
            qg = parse_quick_glance(Path(report_path).read_text())

        screener_strong, screener_summary = best_screener_for_ticker(root, ticker, as_of, symbols)
        has_report = row.get("last_report_date") is not None
        tier_pin = wl.get("tier_pin")
        if tier_pin:
            tier_pin = str(tier_pin).upper()

        result = compute_tier_for_ticker(
            ticker=ticker,
            watching=bool(row.get("watching")),
            thesis_status=thesis_status,
            confidence_score=thesis.get("confidence_score"),
            days_stale=row.get("days_stale"),
            verdict=qg.get("verdict"),
            research_confidence=qg.get("research_confidence"),
            screener_strong=screener_strong,
            screener_summary=screener_summary,
            market_gate=market_gate,
            tier_pin=tier_pin,
            has_report=has_report,
        )

        merged = dict(row)
        merged.update(
            {
                "tier": result.tier,
                "tier_score": result.tier_score,
                "tier_reasons": result.tier_reasons,
                "verdict": _strip_verdict_markup(result.verdict) or "—",
                "research_confidence": result.research_confidence or "—",
                "screener_summary": result.screener_summary or "—",
                "market_gate": result.market_gate,
                "thesis_confidence_1_5": result.thesis_confidence_1_5,
                "tier_a_capped": False,
                "tier_pin": tier_pin or "",
            }
        )
        enriched.append(merged)

    return enriched


def build_entry_watchlist_payload(
    repo_root: Path | None = None,
    as_of: date | None = None,
) -> dict[str, Any]:
    """Build JSON-serializable entry watchlist from eligible tickers."""
    from research_watchlist import (
        build_staleness_rows,
        eligibility_for_tickers,
        eligible_tickers,
    )

    root = repo_root or get_repo_root()
    as_of = as_of or date.today()
    watchlist_path = root / "config" / "research_watchlist.yaml"
    if not watchlist_path.exists():
        watchlist_path = root / "config" / "research_watchlist.yaml.example"
    exclude_path = resolve_exclude_path_for_filter(root)
    state_dir = root / "state" / "theses"
    research_dir = root / "reports" / "research"

    eligibility_map = eligibility_for_tickers(state_dir, watchlist_path, exclude_path)
    tickers = eligible_tickers(state_dir, watchlist_path, exclude_path)
    stale_rows = build_staleness_rows(
        tickers=tickers,
        research_dir=research_dir,
        as_of=as_of,
        threshold_days=STALE_DAYS,
        eligibility_map=eligibility_map,
    )

    watchlist = load_watchlist_config(watchlist_path)
    thesis_map = _load_thesis_map(state_dir)
    base: list[dict] = []
    for row in stale_rows:
        ticker = row["ticker"]
        th = thesis_map.get(ticker, {})
        th_status = str(th.get("status", "")).upper() if th else "—"
        base.append(
            {
                "ticker": ticker,
                "last_report_date": row["last_report"],
                "days_stale": row["days_stale"],
                "thesis_status": th_status if th_status else "—",
                "watching": watchlist.get(ticker, {}).get("watching", False),
                "eligibility": row["eligibility"],
                "notes": watchlist.get(ticker, {}).get("notes", ""),
                "report_path": None,
            }
        )

    # Attach report paths
    from research_watchlist import latest_report_date

    for r in base:
        t = r["ticker"]
        latest = latest_report_date(research_dir, t)
        if latest:
            r["report_path"] = research_dir / f"{t}_{latest.isoformat()}.md"
            if not r["report_path"].exists():
                r["report_path"] = None

    enriched = enrich_dashboard_rows(
        base, root, as_of, state_dir=state_dir, watchlist_path=watchlist_path
    )
    enriched = apply_tier_a_cap(enriched, cap=TIER_A_CAP)
    enriched.sort(key=tier_order_key)

    return {
        "as_of": as_of.isoformat(),
        "tier_a_cap": TIER_A_CAP,
        "market_gate": load_market_gate(root, as_of),
        "tickers": enriched,
        "counts": {t: sum(1 for r in enriched if r.get("tier") == t) for t in ("A", "B", "C", "D")},
    }


def format_entry_watchlist_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Entry Watchlist — {payload.get('as_of', '')}",
        "",
        f"**Market gate:** {payload.get('market_gate', 'UNKNOWN')}",
        f"**Tier A cap:** {payload.get('tier_a_cap', TIER_A_CAP)}",
        "",
        "| Tier | Ticker | Score | Thesis | Conf | Verdict | Screener | Reasons |",
        "|------|--------|-------|--------|------|---------|----------|---------|",
    ]
    for r in payload.get("tickers") or []:
        reasons = "; ".join(r.get("tier_reasons") or [])[:80]
        lines.append(
            f"| {r.get('tier', '')} | {r.get('ticker', '')} | {r.get('tier_score', '')} | "
            f"{r.get('thesis_status', '—')} | {r.get('thesis_confidence_1_5', '—')} | "
            f"{r.get('verdict', '—')[:30]} | {r.get('screener_summary', '—')} | {reasons} |"
        )
    lines.append("")
    counts = payload.get("counts") or {}
    lines.append(
        f"**Counts:** A={counts.get('A', 0)} B={counts.get('B', 0)} "
        f"C={counts.get('C', 0)} D={counts.get('D', 0)}"
    )
    return "\n".join(lines) + "\n"
