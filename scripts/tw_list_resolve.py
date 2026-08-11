"""Resolve TradeWhisperer list colors into per-ticker HTF stacks.

Lists under reports/charts/tradewhisperer/list_tw_{period}_{date}.json are the
candle-color source of truth. Charts remain optional for structure only.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from report_paths import artifact_dir
from research_watchlist import get_repo_root

PERIODS = ("daily", "weekly", "monthly")
VALID_BIAS = frozenset({"long", "short", "either"})

_BUCKET_ALIASES = {
    "BLUE-GREEN": "BLUE_GREEN",
    "PINK-RED": "PINK_RED",
    "TRIM-OPTION": "TRIM_OPTION",
    "YELLOWISH-GREEN": "TRIM_OPTION",
    "YELLOWISH_GREEN": "TRIM_OPTION",
}

LONG_TRIGGERS = frozenset({"BLUE", "BLUE_GREEN"})
SHORT_TRIGGERS = frozenset({"PINK", "PINK_RED"})
EITHER_TRIGGERS = LONG_TRIGGERS | SHORT_TRIGGERS

BULLISH_COLORS = frozenset({"BLUE", "BLUE_GREEN", "GREEN"})
BEARISH_COLORS = frozenset({"PINK", "PINK_RED", "RED"})
FIERCE_BEARISH = frozenset({"RED", "PINK_RED"})
FIERCE_BULLISH = frozenset({"GREEN", "BLUE_GREEN"})


def normalize_bucket(raw: str) -> str:
    """Normalize Patreon/list bucket labels to underscore form."""
    key = str(raw).strip().upper().replace(" ", "_")
    key = _BUCKET_ALIASES.get(key, key)
    key = key.replace("-", "_")
    return key


def _normalize_buckets(buckets: dict[str, Any]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for raw_color, tickers in buckets.items():
        color = normalize_bucket(raw_color)
        if not isinstance(tickers, list):
            continue
        cleaned = sorted({str(t).strip().upper() for t in tickers if str(t).strip()})
        if not cleaned:
            continue
        existing = out.setdefault(color, [])
        for t in cleaned:
            if t not in existing:
                existing.append(t)
    return out


def _index_from_buckets(buckets: dict[str, list[str]]) -> dict[str, str]:
    index: dict[str, str] = {}
    for color, tickers in buckets.items():
        for ticker in tickers:
            index[ticker.upper()] = color
    return index


def find_list(repo_root: Path, period: str, as_of: date) -> Path | None:
    """Return newest list_tw_{period}_{as_of}*.json in the TW charts dir."""
    period_key = period.strip().lower()
    if period_key not in PERIODS:
        raise ValueError(f"period must be one of {PERIODS}, got {period!r}")
    directory = artifact_dir(repo_root, "tradewhisperer_charts")
    if not directory.exists():
        return None
    date_str = as_of.isoformat()
    matches = sorted(directory.glob(f"list_tw_{period_key}_{date_str}*.json"))
    if not matches:
        return None
    return matches[-1]


def load_list(path: Path) -> dict[str, Any]:
    """Load a list artifact; ensure buckets + ticker_index (build index if empty)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    extracted = data.get("extracted")
    if not isinstance(extracted, dict):
        raise ValueError(f"{path}: missing extracted object")
    buckets_raw = extracted.get("buckets")
    if not isinstance(buckets_raw, dict) or not buckets_raw:
        raise ValueError(f"{path}: extracted.buckets required")
    buckets = _normalize_buckets(buckets_raw)
    if not buckets:
        raise ValueError(f"{path}: extracted.buckets empty after normalize")
    extracted["buckets"] = buckets

    index_raw = extracted.get("ticker_index")
    if isinstance(index_raw, dict) and index_raw:
        index = {
            str(t).strip().upper(): normalize_bucket(c)
            for t, c in index_raw.items()
            if str(t).strip()
        }
    else:
        index = _index_from_buckets(buckets)
    extracted["ticker_index"] = index
    data["extracted"] = extracted
    return data


def color_for_ticker(data: dict[str, Any], ticker: str) -> str | None:
    """Return normalized list color for ticker, or None if absent."""
    extracted = data.get("extracted") or {}
    index = extracted.get("ticker_index") or {}
    key = ticker.strip().upper()
    color = index.get(key)
    if color is None:
        return None
    return normalize_bucket(color)


def resolve_color_stack(
    repo_root: Path,
    ticker: str,
    as_of: date,
) -> dict[str, Any]:
    """Resolve daily/weekly/monthly list colors for one ticker on as_of."""
    symbol = ticker.strip().upper()
    stack: dict[str, str | None] = {p: None for p in PERIODS}
    sources: dict[str, str | None] = {p: None for p in PERIODS}
    for period in PERIODS:
        path = find_list(repo_root, period, as_of)
        if path is None:
            continue
        try:
            data = load_list(path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        color = color_for_ticker(data, symbol)
        stack[period] = color
        sources[period] = str(path.as_posix())
    return {
        "ticker": symbol,
        "as_of": as_of.isoformat(),
        "daily": stack["daily"],
        "weekly": stack["weekly"],
        "monthly": stack["monthly"],
        "sources": sources,
    }


def shortlist(data: dict[str, Any], bias: str) -> list[str]:
    """Return trigger-color tickers for bias (sorted)."""
    bias_key = bias.strip().lower()
    if bias_key not in VALID_BIAS:
        raise ValueError(f"bias must be one of {sorted(VALID_BIAS)}, got {bias!r}")
    if bias_key == "long":
        allowed = LONG_TRIGGERS
    elif bias_key == "short":
        allowed = SHORT_TRIGGERS
    else:
        allowed = EITHER_TRIGGERS

    extracted = data.get("extracted") or {}
    buckets = extracted.get("buckets") or {}
    if not isinstance(buckets, dict):
        return []
    # Prefer normalized buckets; rebuild if needed
    if buckets and "BLUE-GREEN" in buckets:
        buckets = _normalize_buckets(buckets)

    names: list[str] = []
    for color, tickers in buckets.items():
        if normalize_bucket(color) not in allowed:
            continue
        if not isinstance(tickers, list):
            continue
        for t in tickers:
            sym = str(t).strip().upper()
            if sym and sym not in names:
                names.append(sym)
    return sorted(names)


def htf_fight(stack: dict[str, Any], bias: str) -> dict[str, Any]:
    """Evaluate HTF fight / hard-stop signals from a color stack.

    Returns fight, fierce, htf_absent, score_guide (full|partial|zero), reason.
    """
    bias_key = bias.strip().lower()
    if bias_key not in VALID_BIAS:
        raise ValueError(f"bias must be one of {sorted(VALID_BIAS)}, got {bias!r}")

    weekly = stack.get("weekly")
    monthly = stack.get("monthly")
    htf_colors = [c for c in (weekly, monthly) if c]
    htf_absent = not htf_colors

    if htf_absent:
        return {
            "fight": False,
            "fierce": False,
            "htf_absent": True,
            "score_guide": "full",
            "reason": "weekly and monthly lists absent",
        }

    if bias_key == "either":
        camps = set()
        for c in htf_colors:
            if c in BULLISH_COLORS:
                camps.add("bull")
            elif c in BEARISH_COLORS:
                camps.add("bear")
        if len(camps) > 1:
            return {
                "fight": True,
                "fierce": False,
                "htf_absent": False,
                "score_guide": "partial",
                "reason": "weekly/monthly colors disagree",
            }
        return {
            "fight": False,
            "fierce": False,
            "htf_absent": False,
            "score_guide": "full",
            "reason": "HTF colors not fighting each other",
        }

    if bias_key == "long":
        opposing = BEARISH_COLORS
        fierce_set = FIERCE_BEARISH
        supporting = BULLISH_COLORS
        label = "bearish"
    else:
        opposing = BULLISH_COLORS
        fierce_set = FIERCE_BULLISH
        supporting = BEARISH_COLORS
        label = "bullish"

    opp = [c for c in htf_colors if c in opposing]
    support = [c for c in htf_colors if c in supporting]
    fierce = any(c in fierce_set for c in opp)

    if not opp:
        return {
            "fight": False,
            "fierce": False,
            "htf_absent": False,
            "score_guide": "full",
            "reason": f"no {label} HTF stack vs {bias_key}",
        }

    if fierce:
        return {
            "fight": True,
            "fierce": True,
            "htf_absent": False,
            "score_guide": "zero",
            "reason": f"fierce {label} HTF stack: {opp}",
        }

    if support:
        return {
            "fight": True,
            "fierce": False,
            "htf_absent": False,
            "score_guide": "partial",
            "reason": f"mixed HTF: opposing={opp} supporting={support}",
        }

    return {
        "fight": True,
        "fierce": False,
        "htf_absent": False,
        "score_guide": "zero",
        "reason": f"clear {label} HTF fight: {opp}",
    }


def _cmd_stack(args: argparse.Namespace) -> int:
    repo = Path(args.repo) if args.repo else get_repo_root()
    as_of = date.fromisoformat(args.as_of)
    stack = resolve_color_stack(repo, args.ticker, as_of)
    fight = htf_fight(stack, args.bias)
    payload = {
        "ticker": stack["ticker"],
        "as_of": stack["as_of"],
        "bias": args.bias,
        "stack": {
            "daily": stack["daily"],
            "weekly": stack["weekly"],
            "monthly": stack["monthly"],
        },
        "sources": stack["sources"],
        "htf": fight,
        "tw_color": stack.get(args.period),
        "period": args.period,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_shortlist(args: argparse.Namespace) -> int:
    repo = Path(args.repo) if args.repo else get_repo_root()
    as_of = date.fromisoformat(args.as_of)
    path = find_list(repo, args.period, as_of)
    if path is None:
        print(
            f"No list_tw_{args.period}_{as_of.isoformat()}*.json found",
            file=sys.stderr,
        )
        return 1
    data = load_list(path)
    names = shortlist(data, args.bias)
    payload = {
        "period": args.period,
        "as_of": as_of.isoformat(),
        "bias": args.bias,
        "source": str(path.as_posix()),
        "shortlist": names,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve TradeWhisperer list color stacks (list-first SoT).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def _add_repo(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--repo",
            default=None,
            help="Repo root (default: auto-detect)",
        )

    stack_p = sub.add_parser("stack", help="Resolve daily/weekly/monthly colors for a ticker")
    stack_p.add_argument("ticker", help="Ticker symbol")
    stack_p.add_argument("--as-of", required=True, help="YYYY-MM-DD")
    stack_p.add_argument(
        "--bias",
        default="long",
        choices=sorted(VALID_BIAS),
        help="Bias for HTF fight evaluation (default: long)",
    )
    stack_p.add_argument(
        "--period",
        default="daily",
        choices=list(PERIODS),
        help="Period whose color is exposed as tw_color (default: daily)",
    )
    _add_repo(stack_p)
    stack_p.set_defaults(func=_cmd_stack)

    short_p = sub.add_parser("shortlist", help="Shortlist tickers from a period list")
    short_p.add_argument("--as-of", required=True, help="YYYY-MM-DD")
    short_p.add_argument(
        "--period",
        default="daily",
        choices=list(PERIODS),
    )
    short_p.add_argument(
        "--bias",
        default="long",
        choices=sorted(VALID_BIAS),
    )
    _add_repo(short_p)
    short_p.set_defaults(func=_cmd_shortlist)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
