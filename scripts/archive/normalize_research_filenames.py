#!/usr/bin/env python3
"""
Normalize deep-research report filenames to TICKER_YYYY-MM-DD.md and move
them into reports/research/.

Old patterns handled:
  reports/{TICKER}.md                         (bare ticker, date read from content)
  reports/{TICKER}_deep_research_{date}.md
  reports/deep_research_{TICKER}_{date}.md

Target: reports/research/{TICKER}_{date}.md

Run without --execute to preview moves (dry-run is default).
Use --verbose to verify that files already in reports/research/ conform to the
TICKER_YYYY-MM-DD.md pattern without moving anything.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
RESEARCH_DIR = REPORTS_DIR / "research"

DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
GENERATED_RE = re.compile(r"\*\*Generated:\*\*\s*(\d{4}-\d{2}-\d{2})")

# Patterns: (regex, ticker_group, date_group_or_None)
PATTERNS = [
    # MRAM_deep_research_2026-05-10.md  /  INO_deep_research_2026-05-10.md
    (re.compile(r"^([A-Z]{1,6})_deep_research_(\d{4}-\d{2}-\d{2})\.md$"), 1, 2),
    # deep_research_FPS_2026-05-13.md  /  deep_research_VECO_2026-05-06.md
    (re.compile(r"^deep_research_([A-Z]{1,6})_(\d{4}-\d{2}-\d{2})\.md$"), 1, 2),
    # P.md  /  VECO.md  (bare ticker — date extracted from file content)
    (re.compile(r"^([A-Z]{1,6})\.md$"), 1, None),
]


def extract_date_from_content(path: Path) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8").splitlines()[:20]:
            m = GENERATED_RE.search(line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return None


def classify(path: Path) -> tuple[str, str] | None:
    """Return (ticker, date) if path matches a research report pattern, else None."""
    name = path.name
    for pattern, t_grp, d_grp in PATTERNS:
        m = pattern.match(name)
        if not m:
            continue
        ticker = m.group(t_grp)
        if d_grp is not None:
            date = m.group(d_grp)
        else:
            date = extract_date_from_content(path)
            if date is None:
                print(f"  SKIP {path.name}: no Generated date found in content", file=sys.stderr)
                return None
        return ticker, date
    return None


def plan_moves() -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    for f in sorted(REPORTS_DIR.glob("*.md")):
        result = classify(f)
        if result is None:
            continue
        ticker, date = result
        dest = RESEARCH_DIR / f"{ticker}_{date}.md"
        moves.append((f, dest))
    return moves


CANONICAL_RE = re.compile(r"^([A-Z]{1,6})_(\d{4}-\d{2}-\d{2})\.md$")


def verify_research_dir() -> None:
    """Print a conformance report for all files currently in reports/research/."""
    files = sorted(RESEARCH_DIR.glob("*.md"))
    if not files:
        print("reports/research/ is empty or does not exist.")
        return

    ok: list[str] = []
    bad: list[str] = []
    for f in files:
        if CANONICAL_RE.match(f.name):
            ok.append(f.name)
        else:
            bad.append(f.name)

    print(f"reports/research/ — {len(files)} file(s):\n")
    for name in ok:
        m = CANONICAL_RE.match(name)
        assert m
        print(f"  OK  {name}  (ticker={m.group(1)}, date={m.group(2)})")
    for name in bad:
        print(f"  FAIL  {name}  <- does not match TICKER_YYYY-MM-DD.md")

    print()
    if bad:
        print(
            f"FAIL: {len(bad)} file(s) do not conform. Re-run without --verbose to preview moves."
        )
    else:
        print(f"OK: all {len(ok)} file(s) conform to TICKER_YYYY-MM-DD.md format.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--execute", action="store_true", help="Actually move files (default: preview only)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verify existing reports/research/ files; do not move anything",
    )
    args = parser.parse_args()

    if args.verbose:
        verify_research_dir()
        return

    moves = plan_moves()

    if not moves:
        print("No research report files found to normalize.")
        return

    print(f"{'PREVIEW' if not args.execute else 'EXECUTING'} — {len(moves)} file(s):\n")
    for src, dst in moves:
        rel_src = src.relative_to(REPO_ROOT)
        rel_dst = dst.relative_to(REPO_ROOT)
        conflict = " [CONFLICT — destination exists]" if dst.exists() else ""
        print(f"  {rel_src}")
        print(f"    → {rel_dst}{conflict}")

    if not args.execute:
        print("\nRun with --execute to apply.")
        return

    errors = 0
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    for src, dst in moves:
        if dst.exists():
            print(f"SKIP (exists): {dst.relative_to(REPO_ROOT)}", file=sys.stderr)
            errors += 1
            continue
        shutil.move(str(src), str(dst))
        print(f"Moved: {src.name} → {dst.relative_to(REPO_ROOT)}")

    print(f"\nDone. {len(moves) - errors} moved, {errors} skipped.")


if __name__ == "__main__":
    main()
