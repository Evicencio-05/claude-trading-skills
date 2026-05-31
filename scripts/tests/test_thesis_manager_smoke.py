"""AppTest smoke tests — each Thesis Manager page loads without exception."""

from __future__ import annotations

from pathlib import Path

import pytest

try:
    from streamlit.testing.v1 import AppTest

    _HAS_STREAMLIT = True
except ImportError:
    _HAS_STREAMLIT = False

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "tools" / "thesis-manager" / "app.py"
PAGES = ["Dashboard", "Market", "Research", "Reports", "Theses", "Review"]


@pytest.mark.skipif(not _HAS_STREAMLIT, reason="streamlit not installed")
@pytest.mark.parametrize("page", PAGES)
def test_page_loads_without_exception(page: str) -> None:
    at = AppTest.from_file(str(APP), default_timeout=60)
    at.session_state["sidebar_page"] = page
    at.run()
    assert len(at.exception) == 0, at.exception
