#!/usr/bin/env python3
"""One-time migration: reorganize reports/ into category-grouped layout."""

from __future__ import annotations

import re
import shutil
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "reports"

# prefix -> destination relative to reports/
MOVE_RULES: list[tuple[str, str]] = [
    ("market_breadth_", "market/breadth"),
    ("uptrend_analysis_", "market/uptrend"),
    ("sector_rotation_", "market/sector"),
    ("market_top_", "market/top"),
    ("exposure_posture_", "market/exposure"),
    ("vcp_screener_", "screeners/vcp"),
    ("canslim_screener_", "screeners/canslim"),
    ("portfolio_review_", "portfolio"),
    ("position_sizer_", "portfolio"),
    ("prompt_run_retro_", "prompts"),
    ("prompt_learning_digest_", "prompts"),
]

META_PREFIXES = (
    "codebase_cleanup_audit_",
    "docs_sync_",
    "fmp_starter_verification_",
    "futures_removal_",
    "phase_1b_kickoff_",
    "thesis_manager_",
)

TIMESTAMPED = re.compile(r"^(.+)_(\d{4}-\d{2}-\d{2})_(\d{6})\.(md|json)$")
DATE_ONLY = re.compile(r"^sector_rotation_(\d{4}-\d{2}-\d{2})\.(md|json)$")

EMPTY_DIRS = [
    "skill-generation-log",
    "skill-improvement-log",
    "edge_pipeline",
    "intraday",
    "options",
    "screeners/breakout",
    "screeners/earnings",
    "screeners/pead",
    "screeners/theme",
]


def dest_for(name: str) -> str | None:
    if name == "market_breadth_history.json":
        return "market/breadth/market_breadth_history.json"
    if name.startswith("options_analysis_"):
        # options_analysis_PENG_2026-05-06.md -> options/PENG_2026-05-06.md
        m = re.match(r"options_analysis_([A-Z]+)_(\d{4}-\d{2}-\d{2})\.md$", name)
        if m:
            return f"options/{m.group(1)}_{m.group(2)}.md"
        return "options/" + name.replace("options_analysis_", "")
    for prefix, dest in MOVE_RULES:
        if name.startswith(prefix):
            return f"{dest}/{name}"
    for prefix in META_PREFIXES:
        if name.startswith(prefix):
            return f"meta/{name}"
    return None


def source_dirs() -> list[Path]:
    dirs = [REPORTS, REPORTS / "pre_market"]
    return [d for d in dirs if d.is_dir()]


def collect_moves() -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    seen_dest: set[Path] = set()
    for src_dir in source_dirs():
        for path in src_dir.iterdir():
            if not path.is_file():
                continue
            rel_dest = dest_for(path.name)
            if rel_dest is None:
                continue
            dest = REPORTS / rel_dest
            if dest in seen_dest:
                continue
            moves.append((path, dest))
            seen_dest.add(dest)
    return moves


def dedupe_directory(directory: Path) -> int:
    """Keep latest timestamp per calendar day; delete older same-day files."""
    if not directory.is_dir():
        return 0
    by_day: dict[str, list[Path]] = defaultdict(list)
    for path in directory.iterdir():
        if not path.is_file():
            continue
        m = TIMESTAMPED.match(path.name)
        if m:
            by_day[m.group(2)].append(path)
            continue
        m2 = DATE_ONLY.match(path.name)
        if m2:
            by_day[m2.group(1)].append(path)
    removed = 0
    for paths in by_day.values():
        if len(paths) <= 1:
            continue
        keep = max(paths, key=lambda p: p.name)
        for path in paths:
            if path != keep:
                path.unlink()
                removed += 1
    return removed


def merge_history_files() -> None:
    """Merge market_breadth_history.json into canonical location."""
    canonical = REPORTS / "market" / "breadth" / "market_breadth_history.json"
    canonical.parent.mkdir(parents=True, exist_ok=True)
    sources = [
        REPORTS / "market_breadth_history.json",
        REPORTS / "pre_market" / "market_breadth_history.json",
    ]
    for src in sources:
        if src.is_file() and src != canonical:
            if not canonical.exists():
                shutil.move(str(src), str(canonical))
            else:
                src.unlink()


def main() -> None:
    for rel in EMPTY_DIRS:
        d = REPORTS / rel
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("")

    for rel in {
        "market/breadth",
        "market/uptrend",
        "market/sector",
        "market/top",
        "market/exposure",
        "screeners/vcp",
        "screeners/canslim",
        "portfolio",
        "meta",
        "prompts",
    }:
        (REPORTS / rel).mkdir(parents=True, exist_ok=True)

    moves = collect_moves()
    for src, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            src.unlink()
        else:
            shutil.move(str(src), str(dest))

    merge_history_files()

    dedupe_dirs = [
        REPORTS / "market" / "breadth",
        REPORTS / "market" / "uptrend",
        REPORTS / "market" / "sector",
        REPORTS / "market" / "top",
        REPORTS / "market" / "exposure",
        REPORTS / "screeners" / "vcp",
        REPORTS / "screeners" / "canslim",
        REPORTS / "portfolio",
    ]
    total_removed = sum(dedupe_directory(d) for d in dedupe_dirs)

    # Stray artifacts
    stray = REPORTS / "posture_history.log"
    if stray.is_file():
        stray.unlink()

    pre_market_db = REPORTS / "pre_market" / "state" / "theses" / "trades.db"
    if pre_market_db.is_file():
        canonical_db = REPO / "state" / "theses" / "trades.db"
        canonical_db.parent.mkdir(parents=True, exist_ok=True)
        if not canonical_db.exists():
            shutil.move(str(pre_market_db), str(canonical_db))
        else:
            pre_market_db.unlink()

    claude_settings = REPORTS / "pre_market" / ".claude" / "settings.local.json"
    if claude_settings.is_file():
        claude_settings.unlink()

    # Archive unification: archive/research -> archives/
    old_archive = REPORTS / "archive" / "research"
    new_archive = REPORTS / "archives"
    new_archive.mkdir(parents=True, exist_ok=True)
    if old_archive.is_dir():
        for path in old_archive.iterdir():
            dest = new_archive / path.name
            if not dest.exists():
                shutil.move(str(path), str(dest))
            else:
                path.unlink()

    # Remove empty pre_market if possible
    pre_market = REPORTS / "pre_market"
    if pre_market.is_dir():
        for path in sorted(pre_market.rglob("*"), reverse=True):
            if path.is_file():
                print(f"WARNING: leftover file {path}")
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        if pre_market.exists() and not any(pre_market.iterdir()):
            pre_market.rmdir()

    print(f"Migrated {len(moves)} files; deduped {total_removed} same-day duplicates")


if __name__ == "__main__":
    main()
