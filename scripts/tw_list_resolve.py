"""Resolve TradeWhisperer list colors into per-ticker HTF stacks.

Lists under reports/charts/tradewhisperer/list_tw_{period}_{date}.json are the
candle-color source of truth. Charts remain optional for structure only.

Also ranks HTF overlap and compares tickers to persisted sector benchmarks
(config/tw_sector_map.yaml).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml
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

VS_BENCHMARK = frozenset(
    {
        "aligned",
        "leading",
        "lagging",
        "divergent",
        "benchmark_absent",
        "unmapped",
    }
)

_COLOR_STRENGTH = {
    "BLUE_GREEN": 5,
    "PINK_RED": 5,
    "GREEN": 4,
    "RED": 4,
    "BLUE": 3,
    "PINK": 3,
    "TRIM_OPTION": 1,
}

DEFAULT_SECTOR_MAP = "config/tw_sector_map.yaml"


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


def _list_as_of_from_name(path: Path, period_key: str) -> date | None:
    """Parse YYYY-MM-DD from list_tw_{period}_{date}*.json filename."""
    prefix = f"list_tw_{period_key}_"
    name = path.name
    if not name.startswith(prefix) or not name.endswith(".json"):
        return None
    rest = name[len(prefix) : -len(".json")]
    date_part = rest.split("_", 1)[0]
    try:
        return date.fromisoformat(date_part)
    except ValueError:
        return None


def find_list(repo_root: Path, period: str, as_of: date) -> Path | None:
    """Return newest list_tw_{period}_* on or before *as_of*.

    Prefers exact-date matches; otherwise the latest prior dated list for the period
    (so weekly/monthly HTF stacks work when list titles predate the session day).
    """
    period_key = period.strip().lower()
    if period_key not in PERIODS:
        raise ValueError(f"period must be one of {PERIODS}, got {period!r}")
    directory = artifact_dir(repo_root, "tradewhisperer_charts")
    if not directory.exists():
        return None
    date_str = as_of.isoformat()
    exact = sorted(directory.glob(f"list_tw_{period_key}_{date_str}*.json"))
    if exact:
        return exact[-1]

    candidates: list[tuple[date, Path]] = []
    for path in directory.glob(f"list_tw_{period_key}_*.json"):
        list_date = _list_as_of_from_name(path, period_key)
        if list_date is None or list_date > as_of:
            continue
        candidates.append((list_date, path))
    if not candidates:
        return None
    # Latest list date, then newest filename among that date
    best_date = max(d for d, _ in candidates)
    same_day = sorted(p for d, p in candidates if d == best_date)
    return same_day[-1]


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


def color_camp(color: str | None) -> str | None:
    """Return bull/bear/trim camp for a normalized color, or None."""
    if not color:
        return None
    key = normalize_bucket(color)
    if key in BULLISH_COLORS:
        return "bull"
    if key in BEARISH_COLORS:
        return "bear"
    if key == "TRIM_OPTION":
        return "trim"
    return None


def score_overlap(stack: dict[str, Any]) -> dict[str, Any]:
    """Score HTF color overlap for ranking.

    Prefer 3-TF same-camp stacks, then daily triggers, then exact color matches.
    """
    daily = stack.get("daily")
    weekly = stack.get("weekly")
    monthly = stack.get("monthly")
    present = [c for c in (daily, weekly, monthly) if c]
    n_tf = len(present)
    camps = {color_camp(c) for c in present if color_camp(c)}
    camps.discard(None)
    camp: str | None
    if len(camps) == 1:
        camp = next(iter(camps))
    elif not camps:
        camp = None
    else:
        camp = "mixed"

    aligned = camp in ("bull", "bear")
    all_three = aligned and n_tf == 3
    daily_trigger = bool(daily and normalize_bucket(str(daily)) in EITHER_TRIGGERS)

    score = 0
    if all_three:
        score += 100
    elif aligned and n_tf == 2:
        score += 60
    elif aligned and n_tf == 1:
        score += 20
    if daily_trigger and aligned:
        score += 20
    score += sum(_COLOR_STRENGTH.get(normalize_bucket(str(c)), 0) for c in present)
    if daily and weekly and daily == weekly:
        score += 10
    if weekly and monthly and weekly == monthly:
        score += 10
    if daily and monthly and daily == monthly:
        score += 5

    return {
        "score": score,
        "camp": camp,
        "n_tf": n_tf,
        "all_three": all_three,
        "daily_trigger": daily_trigger,
        "aligned": aligned,
    }


def default_sector_map_path(repo_root: Path) -> Path:
    """Return default config/tw_sector_map.yaml under repo root."""
    return repo_root / DEFAULT_SECTOR_MAP


def load_sector_map(path: Path) -> dict[str, Any]:
    """Load sector map YAML; ensure benchmarks/tickers/pending dicts."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: sector map must be a mapping")
    for key in ("benchmarks", "tickers", "pending"):
        section = raw.get(key)
        if section is None:
            raw[key] = {}
        elif not isinstance(section, dict):
            raise ValueError(f"{path}: {key} must be a mapping")
    return raw


def resolve_benchmark(sector_map: dict[str, Any], ticker: str) -> dict[str, Any] | None:
    """Resolve ticker to benchmark metadata, or None if unmapped."""
    symbol = ticker.strip().upper()
    benchmarks = sector_map.get("benchmarks") or {}
    tickers = sector_map.get("tickers") or {}
    if symbol in benchmarks:
        meta = benchmarks[symbol] or {}
        return {
            "benchmark": symbol,
            "class": str(meta.get("class") or "sector"),
            "source": "benchmarks",
        }
    if symbol in tickers:
        meta = tickers[symbol] or {}
        bench = meta.get("benchmark")
        if not bench:
            return None
        return {
            "benchmark": str(bench).strip().upper(),
            "class": str(meta.get("class") or "equity"),
            "source": "tickers",
        }
    return None


def _trigger_rank(color: str | None) -> int:
    if not color:
        return 0
    key = normalize_bucket(color)
    if key in ("BLUE_GREEN", "PINK_RED"):
        return 3
    if key in ("BLUE", "PINK"):
        return 2
    if key in ("GREEN", "RED"):
        return 1
    return 0


def compare_to_benchmark(
    ticker_stack: dict[str, Any],
    bench_stack: dict[str, Any] | None,
) -> str:
    """Compare ticker HTF camp/trigger strength to benchmark stack."""
    if bench_stack is None:
        return "benchmark_absent"
    bench_colors = [
        bench_stack.get("daily"),
        bench_stack.get("weekly"),
        bench_stack.get("monthly"),
    ]
    if not any(bench_colors):
        return "benchmark_absent"

    t_score = score_overlap(ticker_stack)
    b_score = score_overlap(bench_stack)
    t_camp = t_score.get("camp")
    b_camp = b_score.get("camp")
    if t_camp in ("bull", "bear") and b_camp in ("bull", "bear") and t_camp != b_camp:
        return "divergent"
    if t_camp not in ("bull", "bear") or b_camp not in ("bull", "bear"):
        # Mixed/trim vs defined camp — treat as divergent when both have colors
        if t_camp and b_camp and t_camp != b_camp:
            return "divergent"
        return "aligned"

    t_trig = _trigger_rank(ticker_stack.get("daily"))
    b_trig = _trigger_rank(bench_stack.get("daily"))
    if t_trig > b_trig:
        return "leading"
    if t_trig < b_trig:
        return "lagging"
    return "aligned"


def write_pending_stubs(map_path: Path, tickers: list[str]) -> list[str]:
    """Append unknown tickers under pending; return newly added symbols."""
    data = load_sector_map(map_path)
    benchmarks = data.get("benchmarks") or {}
    known = data.get("tickers") or {}
    pending = data.setdefault("pending", {})
    if not isinstance(pending, dict):
        pending = {}
        data["pending"] = pending

    added: list[str] = []
    for raw in tickers:
        symbol = str(raw).strip().upper()
        if not symbol:
            continue
        if symbol in benchmarks or symbol in known or symbol in pending:
            continue
        pending[symbol] = {"benchmark": None, "class": "unknown"}
        added.append(symbol)

    if added:
        # Stable key order for readable diffs
        data["pending"] = dict(sorted(pending.items()))
        map_path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    return added


def _stack_colors(stack: dict[str, Any]) -> dict[str, str | None]:
    return {
        "daily": stack.get("daily"),
        "weekly": stack.get("weekly"),
        "monthly": stack.get("monthly"),
    }


def rank_overlap(
    repo_root: Path,
    as_of: date,
    *,
    bias: str = "either",
    top: int = 40,
    map_path: Path | None = None,
) -> dict[str, Any]:
    """Rank daily-list tickers by HTF overlap and compare to sector benchmarks."""
    bias_key = bias.strip().lower()
    if bias_key not in VALID_BIAS:
        raise ValueError(f"bias must be one of {sorted(VALID_BIAS)}, got {bias!r}")

    daily_path = find_list(repo_root, "daily", as_of)
    if daily_path is None:
        raise FileNotFoundError(f"No list_tw_daily_* on or before {as_of.isoformat()}")
    daily_data = load_list(daily_path)
    index = daily_data["extracted"]["ticker_index"]

    sector_path = map_path or default_sector_map_path(repo_root)
    sector_map = (
        load_sector_map(sector_path)
        if sector_path.is_file()
        else {
            "benchmarks": {},
            "tickers": {},
            "pending": {},
        }
    )
    benchmarks = set(sector_map.get("benchmarks") or {})

    ranked: list[dict[str, Any]] = []
    unmapped: list[str] = []
    sources = {
        "daily": str(daily_path.as_posix()),
        "weekly": None,
        "monthly": None,
        "sector_map": str(sector_path.as_posix()) if sector_path.is_file() else None,
    }
    # Capture HTF list sources once
    for period in ("weekly", "monthly"):
        path = find_list(repo_root, period, as_of)
        if path is not None:
            sources[period] = str(path.as_posix())

    for symbol in sorted(index):
        if symbol in benchmarks:
            continue
        stack = resolve_color_stack(repo_root, symbol, as_of)
        scored = score_overlap(stack)
        if scored["n_tf"] < 2:
            continue
        if bias_key == "long" and scored["camp"] != "bull":
            continue
        if bias_key == "short" and scored["camp"] != "bear":
            continue

        mapping = resolve_benchmark(sector_map, symbol)
        bench_name: str | None = None
        bench_stack_colors: dict[str, str | None] | None = None
        vs: str
        if mapping is None:
            vs = "unmapped"
            unmapped.append(symbol)
        else:
            bench_name = mapping["benchmark"]
            bench_full = resolve_color_stack(repo_root, bench_name, as_of)
            bench_stack_colors = _stack_colors(bench_full)
            vs = compare_to_benchmark(_stack_colors(stack), bench_stack_colors)

        ranked.append(
            {
                "ticker": symbol,
                "daily": stack.get("daily"),
                "weekly": stack.get("weekly"),
                "monthly": stack.get("monthly"),
                "score": scored["score"],
                "camp": scored["camp"],
                "daily_trigger": scored["daily_trigger"],
                "all_three": scored["all_three"],
                "benchmark": bench_name,
                "benchmark_stack": bench_stack_colors,
                "vs_benchmark": vs,
            }
        )

    ranked.sort(key=lambda r: (-int(r["score"]), str(r["ticker"])))
    if top > 0:
        ranked = ranked[:top]

    return {
        "as_of": as_of.isoformat(),
        "bias": bias_key,
        "sources": sources,
        "ranked": ranked,
        "unmapped": sorted(set(unmapped)),
        "counts": {
            "daily_indexed": len(index),
            "ranked": len(ranked),
            "unmapped": len(set(unmapped)),
        },
    }


def write_overlap_artifacts(repo_root: Path, payload: dict[str, Any]) -> tuple[Path, Path]:
    """Write overlap_tw_{as_of}.json + .md under tradewhisperer_charts."""
    as_of = str(payload["as_of"])
    out_dir = artifact_dir(repo_root, "tradewhisperer_charts", mkdir=True)
    json_path = out_dir / f"overlap_tw_{as_of}.json"
    md_path = out_dir / f"overlap_tw_{as_of}.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ranked = payload.get("ranked") or []
    unmapped = payload.get("unmapped") or []
    lines = [
        f"# TradeWhisperer — HTF overlap ({as_of})",
        "",
        f"**Bias:** {payload.get('bias')} · **Ranked:** {len(ranked)} · "
        f"**Unmapped:** {len(unmapped)}",
        "",
        "## Top overlaps",
        "",
        "| Ticker | Camp | D / W / M | Score | Benchmark | vs |",
        "|--------|------|-----------|------:|-----------|----|",
    ]
    for row in ranked:
        stack = (
            f"{row.get('daily') or '-'} / {row.get('weekly') or '-'} / {row.get('monthly') or '-'}"
        )
        lines.append(
            f"| {row.get('ticker')} | {row.get('camp')} | {stack} | {row.get('score')} | "
            f"{row.get('benchmark') or '—'} | {row.get('vs_benchmark')} |"
        )
    lines.extend(["", f"JSON: `{json_path.as_posix()}`", ""])
    if unmapped:
        lines.append("## Unmapped (add to config/tw_sector_map.yaml)")
        lines.append("")
        lines.append(", ".join(unmapped[:80]) + (" …" if len(unmapped) > 80 else ""))
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


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

    overlap_p = sub.add_parser(
        "overlap",
        help="Rank best HTF overlaps and compare each ticker to its sector benchmark",
    )
    overlap_p.add_argument("--as-of", required=True, help="YYYY-MM-DD")
    overlap_p.add_argument(
        "--bias",
        default="either",
        choices=sorted(VALID_BIAS),
        help="Filter ranked camps (default: either)",
    )
    overlap_p.add_argument(
        "--top",
        type=int,
        default=40,
        help="Max ranked rows to keep (default: 40)",
    )
    overlap_p.add_argument(
        "--map",
        default=None,
        help="Path to tw_sector_map.yaml (default: config/tw_sector_map.yaml)",
    )
    overlap_p.add_argument(
        "--write-pending",
        action="store_true",
        help="Append unmapped daily-list tickers under pending: in the sector map",
    )
    _add_repo(overlap_p)
    overlap_p.set_defaults(func=_cmd_overlap)

    map_p = sub.add_parser("map-lookup", help="Look up a ticker in the sector map")
    map_p.add_argument("ticker", help="Ticker symbol")
    map_p.add_argument(
        "--map",
        default=None,
        help="Path to tw_sector_map.yaml (default: config/tw_sector_map.yaml)",
    )
    _add_repo(map_p)
    map_p.set_defaults(func=_cmd_map_lookup)

    return parser


def _cmd_overlap(args: argparse.Namespace) -> int:
    repo = Path(args.repo) if args.repo else get_repo_root()
    as_of = date.fromisoformat(args.as_of)
    map_path = Path(args.map) if args.map else default_sector_map_path(repo)
    try:
        payload = rank_overlap(
            repo,
            as_of,
            bias=args.bias,
            top=args.top,
            map_path=map_path,
        )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.write_pending:
        if not map_path.is_file():
            print(f"Sector map missing; cannot write pending: {map_path}", file=sys.stderr)
            return 1
        # Pending stubs for full daily index unknowns (not only ranked slice)
        daily_path = find_list(repo, "daily", as_of)
        if daily_path is not None:
            daily_index = load_list(daily_path)["extracted"]["ticker_index"]
            added = write_pending_stubs(map_path, list(daily_index))
            payload["pending_added"] = added
        else:
            payload["pending_added"] = []

    json_path, md_path = write_overlap_artifacts(repo, payload)
    payload["artifacts"] = {
        "json": str(json_path.as_posix()),
        "md": str(md_path.as_posix()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_map_lookup(args: argparse.Namespace) -> int:
    repo = Path(args.repo) if args.repo else get_repo_root()
    map_path = Path(args.map) if args.map else default_sector_map_path(repo)
    if not map_path.is_file():
        print(f"Sector map not found: {map_path}", file=sys.stderr)
        return 1
    data = load_sector_map(map_path)
    symbol = args.ticker.strip().upper()
    mapping = resolve_benchmark(data, symbol)
    pending = (data.get("pending") or {}).get(symbol)
    payload: dict[str, Any] = {
        "ticker": symbol,
        "map": str(map_path.as_posix()),
        "benchmark": mapping["benchmark"] if mapping else None,
        "class": mapping["class"] if mapping else None,
        "source": mapping["source"] if mapping else None,
        "pending": pending,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if mapping or pending else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
