"""Thesis Manager — fast UI for trader-memory-core thesis entry and review."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
import research_utils  # noqa: E402
import utils  # noqa: E402

PAGES = ["Dashboard", "Research", "Reports", "Add Thesis", "Review"]

# ── constants ─────────────────────────────────────────────────────────────────

# Must match thesis.schema.json enum exactly — flow_play/lottery are not valid
THESIS_TYPES = utils.THESIS_TYPES
CONFIDENCE_LABELS: dict[int, str] = {
    1: "1 — Lottery",
    2: "2 — Speculative",
    3: "3 — Moderate",
    4: "4 — Conviction",
    5: "5 — High Conviction",
}
EXIT_REASONS = utils.EXIT_REASONS
EXIT_REASON_LABELS: dict[str, str] = {
    "stop_hit": "Stop hit",
    "target_hit": "Target hit",
    "time_stop": "Expired / time stop",
    "invalidated": "Thesis invalidated",
    "manual": "Manual exit",
}
ACCOUNTS = ["robinhood_taxable", "ira_robinhood", "robinhood_agentic", "lucid_eval"]


# ── shared helpers ─────────────────────────────────────────────────────────────


def _fmt_account(raw: str) -> str:
    return utils.fmt_account(raw)


def _ira_badge(account: str, strategy: str) -> str | None:
    return utils.ira_badge_html(account, strategy)


def _days_to_expiry(expiry_str: str | None) -> int | None:
    return utils.days_to_expiry(expiry_str)


def _parse_price(text: str) -> float | None:
    return utils.parse_price(text)


def _run_safe(fn, *args, **kwargs):
    """Call fn(*args, **kwargs). Returns (result, None) or (None, error_str)."""
    try:
        return fn(*args, **kwargs), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def _build_thesis_data(
    ticker: str,
    thesis_type: str,
    thesis_text: str,
    confidence: int,
    stop_text: str,
    target_text: str,
    avg_cost: float,
    strategy: str = "",
) -> dict:
    return utils.build_thesis_data(
        ticker=ticker,
        thesis_type=thesis_type,
        thesis_text=thesis_text,
        confidence=confidence,
        stop_text=stop_text,
        target_text=target_text,
        avg_cost=avg_cost,
        strategy=strategy,
    )


# ── cached data loaders ────────────────────────────────────────────────────────


@st.cache_data(ttl=60)
def _theses(statuses_key: str) -> list[dict]:
    if not statuses_key:
        return utils.load_theses(None)
    return utils.load_theses(statuses_key.split(","))


@st.cache_data(ttl=60)
def _pending() -> list[dict]:
    return utils.load_pending_ingest()


@st.cache_data(ttl=60)
def _research_rows() -> list[dict]:
    return research_utils.get_research_dashboard_rows()


# ── page 1: dashboard ─────────────────────────────────────────────────────────


def show_dashboard() -> None:
    st.header("Dashboard")

    open_theses = _theses("ACTIVE,ENTRY_READY")
    pending_all = _pending()
    pending_thesis = [p for p in pending_all if p.get("status") == "PENDING_THESIS"]
    # --- metric cards ---
    expiring_count = sum(
        1
        for t in open_theses
        if _days_to_expiry(((t.get("position") or {}).get("raw_source") or {}).get("expiry"))
        is not None
        and _days_to_expiry(((t.get("position") or {}).get("raw_source") or {}).get("expiry")) <= 7
    ) + sum(
        1
        for p in pending_thesis
        if _days_to_expiry(p.get("expiry")) is not None and _days_to_expiry(p.get("expiry")) <= 7
    )

    days_since = utils.days_since_last_entry()
    if days_since is None:
        days_label = "—"
        days_note = "No entries yet"
    else:
        indicator = " 🔴" if days_since > 7 else (" 🟡" if days_since > 3 else "")
        days_label = f"{days_since}{indicator}"
        days_note = ""

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Positions", len(open_theses))
    c2.metric(
        "Pending Thesis",
        len(pending_thesis),
        delta=f"⚠ {len(pending_thesis)}" if pending_thesis else None,
        delta_color="inverse" if pending_thesis else "off",
    )
    c3.metric(
        "Expiring ≤ 7 days",
        expiring_count,
        delta=f"⚠ {expiring_count}" if expiring_count else None,
        delta_color="inverse" if expiring_count else "off",
    )
    with c4:
        st.metric("Days Since Last Entry", days_label)
        if days_note:
            st.caption(days_note)

    research_rows = _research_rows()
    stale_n = sum(1 for r in research_rows if r["ui_status"] in ("stale", "missing"))
    rc1, rc2 = st.columns([3, 1])
    with rc1:
        st.caption(f"Research stale: **{stale_n}** — open Research page for update prompts")
    with rc2:
        if st.button("Go to Research", key="dash_go_research"):
            st.session_state["nav_page"] = "Research"
            st.rerun()

    st.divider()

    dupes = utils.pending_duplicate_tickers(open_theses, pending_all)
    if dupes:
        st.warning(
            f"Duplicate tickers already logged as open theses: {', '.join(sorted(dupes))}. "
            "Close or skip pending rows to avoid double-counting."
        )

    # --- position table ---
    if not open_theses and not pending_thesis:
        st.info("No positions logged yet. Use **Add Thesis** to get started.")
        _show_refresh_button()
        return

    rows = []
    for t in open_theses:
        pos = t.get("position") or {}
        raw = pos.get("raw_source") or {}
        expiry = raw.get("expiry")
        dte = _days_to_expiry(expiry)
        cs = t.get("confidence_score") or 0
        rows.append(
            {
                "_id": t.get("thesis_id", ""),
                "Ticker": t.get("ticker", ""),
                "Type": t.get("thesis_type", ""),
                "Account": _fmt_account(pos.get("account_type") or ""),
                "Expiry": expiry or "—",
                "Confidence": str(int(cs * 5)) if cs else "—",
                "Days Left": str(dte) if dte is not None else "—",
                "Status": t.get("status", ""),
            }
        )
    for p in pending_thesis:
        expiry = p.get("expiry")
        dte = _days_to_expiry(expiry)
        rows.append(
            {
                "_id": p.get("key", ""),
                "Ticker": p.get("ticker", ""),
                "Type": p.get("asset_type", ""),
                "Account": _fmt_account(p.get("account", "")),
                "Expiry": expiry or "—",
                "Confidence": "—",
                "Days Left": str(dte) if dte is not None else "—",
                "Status": "PENDING_THESIS",
            }
        )

    df_display = pd.DataFrame(rows)

    def _style_row(row):
        status = row.get("Status", "")
        try:
            dte = int(row.get("Days Left", ""))
        except (ValueError, TypeError):
            dte = None
        bg = ""
        if status == "PENDING_THESIS":
            bg = "background-color: #3d3500"
        elif dte is not None and dte <= 7:
            bg = "background-color: #3d0000"
        elif dte is not None and dte <= 14:
            bg = "background-color: #3d2000"
        return [bg] * len(row)

    display_cols = ["Ticker", "Type", "Account", "Expiry", "Confidence", "Days Left", "Status"]
    styled = df_display[display_cols].style.apply(_style_row, axis=1)

    event = st.dataframe(
        styled,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        key="dash_table",
    )

    sel = (event.selection.rows if hasattr(event, "selection") else []) or []
    if sel:
        idx = sel[0]
        row = rows[idx]
        row_id = row["_id"]
        thesis = next((t for t in open_theses if t.get("thesis_id") == row_id), None)
        ppos = next((p for p in pending_thesis if p.get("key") == row_id), None)

        with st.container(border=True):
            if thesis:
                st.subheader(f"{row['Ticker']} — {row['Status']}")
                lc, rc = st.columns(2)
                with lc:
                    st.write("**Thesis:**", thesis.get("thesis_statement") or "—")
                    exit_d = thesis.get("exit") or {}
                    st.write("**Stop:**", exit_d.get("stop_loss") or "—")
                    st.write("**Target:**", exit_d.get("take_profit") or "—")
                    st.write(
                        "**Kill criteria:**", "; ".join(thesis.get("kill_criteria") or []) or "—"
                    )
                with rc:
                    mon = thesis.get("monitoring") or {}
                    st.write("**Last reviewed:**", mon.get("last_review_date") or "never")
                    cs = thesis.get("confidence_score") or 0
                    st.write("**Confidence:**", f"{int(cs * 5)}/5" if cs else "—")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Mark for Review", key=f"rev_{row_id}"):
                        _, err = _run_safe(utils.mark_reviewed, row_id)
                        if err:
                            st.error(f"Failed: {err}")
                        else:
                            st.success("Marked reviewed.")
                            st.cache_data.clear()
                            st.rerun()
                with b2:
                    if st.button("Close Position", key=f"close_{row_id}"):
                        st.session_state[f"closing_{row_id}"] = True

                if st.session_state.get(f"closing_{row_id}"):
                    with st.form(key=f"close_form_{row_id}"):
                        ep = st.number_input("Exit price", min_value=0.0, format="%.4f")
                        ed = st.date_input("Exit date", value=date.today())
                        reason = st.selectbox(
                            "Exit reason",
                            EXIT_REASONS,
                            format_func=lambda x: EXIT_REASON_LABELS.get(x, x),
                        )
                        if st.form_submit_button("Confirm Close"):
                            _, err = _run_safe(utils.finalize_thesis, row_id, reason, ep, ed)
                            if err:
                                st.error(
                                    f"Close failed (finalize_thesis {row_id!r} {reason!r} {ep} {ed.isoformat()!r}):\n{err}"
                                )
                            else:
                                st.success(f"Closed {row['Ticker']}.")
                                st.session_state.pop(f"closing_{row_id}", None)
                                st.cache_data.clear()
                                st.rerun()
            elif ppos:
                st.subheader(f"{row['Ticker']} — PENDING_THESIS")
                st.write("Go to **Add Thesis** to fill in the thesis for this position.")

    st.divider()
    _show_refresh_button()


def _show_refresh_button() -> None:
    if st.button("Refresh Positions"):
        sync_script = utils.get_repo_root() / "scripts" / "robinhood_sync.py"
        try:
            result = subprocess.run(
                [sys.executable, str(sync_script)],
                capture_output=True,
                text=True,
                timeout=90,
            )
            if result.returncode == 0:
                st.success(f"Synced via robinhood_sync.py\n{result.stdout[:300]}")
            else:
                st.error(f"Sync failed (python3 scripts/robinhood_sync.py):\n{result.stderr[:500]}")
        except FileNotFoundError:
            st.warning("scripts/robinhood_sync.py not found.")
        except subprocess.TimeoutExpired:
            st.error("Sync timed out after 90s.")
        st.caption(f"Last attempted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.cache_data.clear()
        st.rerun()


# ── page 2: add thesis ─────────────────────────────────────────────────────────


def _pending_position_form(pos: dict, key_prefix: str) -> None:
    """Render the fill-in form for one pending position."""
    ticker = pos.get("ticker", "?")
    account = pos.get("account", "")
    asset_type = pos.get("asset_type", "")
    strategy = pos.get("strategy", "")
    expiry = pos.get("expiry", "")
    strike = pos.get("strike", "")
    contracts = pos.get("contracts", "")
    avg_cost = pos.get("avg_cost", 0.0)

    hdr_cols = st.columns([4, 1])
    with hdr_cols[0]:
        st.markdown(f"### {ticker}")
        badge = _ira_badge(account, strategy)
        if badge:
            st.markdown(badge, unsafe_allow_html=True)
    with hdr_cols[1]:
        if st.button("Skip", key=f"skip_{key_prefix}"):
            st.session_state[f"collapsed_{key_prefix}"] = True
            st.rerun()

    meta = st.columns(4)
    meta[0].caption(f"Account: {_fmt_account(account)}")
    meta[0].caption(f"Type: {asset_type}")
    if strike:
        meta[1].caption(f"Strike: {strike}")
    if expiry:
        meta[1].caption(f"Expiry: {expiry}")
    if contracts:
        meta[2].caption(f"Contracts: {contracts}")
    meta[2].caption(f"Avg cost: {avg_cost}")
    dte = _days_to_expiry(expiry)
    if dte is not None:
        color = "red" if dte <= 7 else ("orange" if dte <= 14 else "green")
        meta[3].markdown(
            f"<span style='color:{color};font-weight:bold'>{dte}d left</span>",
            unsafe_allow_html=True,
        )

    thesis_type = st.selectbox(
        "Thesis type",
        THESIS_TYPES,
        index=0,
        key=f"tt_{key_prefix}",
    )
    thesis_text = st.text_area(
        "Thesis *",
        placeholder="Why did you enter? What's the catalyst? What would make this wrong?",
        height=100,
        key=f"th_{key_prefix}",
    )
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        confidence = st.select_slider(
            "Confidence",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: CONFIDENCE_LABELS[x],
            key=f"conf_{key_prefix}",
        )
    with fc2:
        stop_val = st.text_input(
            "Stop",
            placeholder="Price or condition that invalidates the thesis",
            key=f"stop_{key_prefix}",
        )
    with fc3:
        target_val = st.text_input(
            "Target",
            placeholder="Exit condition or price target",
            key=f"tgt_{key_prefix}",
        )

    if st.button("Submit", key=f"sub_{key_prefix}"):
        if not thesis_text.strip():
            st.warning("Thesis text is required.")
            return
        td = _build_thesis_data(
            ticker=ticker,
            thesis_type=thesis_type,
            thesis_text=thesis_text,
            confidence=confidence,
            stop_text=stop_val,
            target_text=target_val,
            avg_cost=float(avg_cost) if avg_cost else 0.0,
            strategy=strategy,
        )
        val_errors = utils.validate_thesis_submit(
            td, account=account, strategy=strategy, confidence=confidence
        )
        if val_errors:
            st.error("\n".join(val_errors))
            return
        thesis_id, err = _run_safe(utils.register_pending_position, td, pos)
        if err:
            st.error(f"Register failed (register_pending_position for {ticker}):\n{err}")
            return
        all_positions = utils.load_pending_ingest()
        utils.save_pending_ingest(
            utils.mark_pending_ingested(all_positions, pos.get("key", ""), thesis_id)
        )
        st.success(f"Registered {ticker} → {thesis_id} (ACTIVE)")
        st.session_state[f"collapsed_{key_prefix}"] = True
        st.cache_data.clear()
        st.rerun()


def show_add_thesis() -> None:
    st.header("Add Thesis")

    # ── Section A: pending positions ──────────────────────────────────────────
    st.subheader("A — Pending Positions")
    pending = utils.load_pending_ingest()
    pending_thesis = sorted(
        [p for p in pending if p.get("status") == "PENDING_THESIS"],
        key=lambda p: p.get("expiry") or "9999",
    )

    if not pending_thesis:
        st.info("No pending sync data. Run **Robinhood sync** from the Dashboard.")
    else:
        open_theses = utils.load_theses(["ACTIVE", "ENTRY_READY"])
        dupes = utils.pending_duplicate_tickers(open_theses, pending)
        if dupes:
            st.warning(
                f"These pending tickers already have open theses: {', '.join(sorted(dupes))}"
            )
        for i, pos in enumerate(pending_thesis):
            ticker = pos.get("ticker", "?")
            key_prefix = f"pend_{i}_{ticker}"
            if st.session_state.get(f"collapsed_{key_prefix}"):
                continue
            with st.container(border=True):
                _pending_position_form(pos, key_prefix)

    st.divider()

    # ── Section B: manual entry ───────────────────────────────────────────────
    with st.expander("Add position manually", expanded=False):
        mc1, mc2 = st.columns(2)
        with mc1:
            m_ticker = (
                st.text_input("Ticker *", placeholder="AAPL", key="man_ticker").strip().upper()
            )
            m_asset = st.selectbox("Asset type", ["stock", "options", "futures"], key="man_asset")
            m_dir = st.selectbox("Direction", ["long", "short"], key="man_dir")
            m_account = st.selectbox("Account", ACCOUNTS, key="man_account")
        with mc2:
            st.number_input("Size (shares/contracts)", min_value=0.0, key="man_size")
            m_cost = st.number_input("Avg cost", min_value=0.0, format="%.4f", key="man_cost")
            st.date_input("Entry date", value=date.today(), key="man_entry_date")

        m_strategy = ""
        if m_asset == "options":
            oc1, oc2, oc3 = st.columns(3)
            with oc1:
                st.number_input("Strike", min_value=0.0, format="%.2f", key="man_strike")
            with oc2:
                st.date_input("Expiry", key="man_expiry")
            with oc3:
                m_opt_type = st.selectbox("Option type", ["call", "put"], key="man_opt_type")
            m_strategy = f"{m_dir}_{m_opt_type}"
            st.text_input("Strategy (auto)", value=m_strategy, disabled=True, key="man_strat_disp")
            badge = _ira_badge(m_account, m_strategy)
            if badge:
                st.markdown(badge, unsafe_allow_html=True)
        elif "ira" in m_account.lower():
            st.markdown(
                _ira_badge(m_account, "long_call") or "",
                unsafe_allow_html=True,
            )

        m_thesis_type = st.selectbox("Thesis type *", THESIS_TYPES, key="man_tt")
        m_thesis = st.text_area(
            "Thesis *",
            placeholder="Why did you enter? What's the catalyst? What would make this wrong?",
            height=100,
            key="man_thesis",
        )
        bf1, bf2, bf3 = st.columns(3)
        with bf1:
            m_conf = st.select_slider(
                "Confidence",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: CONFIDENCE_LABELS[x],
                key="man_conf",
            )
        with bf2:
            m_stop = st.text_input(
                "Stop",
                placeholder="Price or condition that invalidates the thesis",
                key="man_stop",
            )
        with bf3:
            m_target = st.text_input(
                "Target",
                placeholder="Exit condition or price target",
                key="man_target",
            )

        if st.button("Submit", key="man_submit"):
            if not m_ticker:
                st.warning("Ticker is required.")
            elif not m_thesis.strip():
                st.warning("Thesis text is required.")
            else:
                td = _build_thesis_data(
                    ticker=m_ticker,
                    thesis_type=m_thesis_type,
                    thesis_text=m_thesis,
                    confidence=m_conf,
                    stop_text=m_stop,
                    target_text=m_target,
                    avg_cost=float(m_cost),
                    strategy=m_strategy,
                )
                val_errors = utils.validate_thesis_submit(
                    td, account=m_account, strategy=m_strategy, confidence=m_conf
                )
                if val_errors:
                    st.error("\n".join(val_errors))
                else:
                    thesis_id, err = _run_safe(utils.register_thesis, td)
                    if err:
                        st.error(f"Register failed (register_thesis for {m_ticker}):\n{err}")
                    else:
                        st.success(f"Registered {m_ticker} → {thesis_id}")
                        st.cache_data.clear()


# ── page 3: review ─────────────────────────────────────────────────────────────


def show_review() -> None:
    st.header("Review")

    # ── Section A: urgent flags ───────────────────────────────────────────────
    st.subheader("A — Urgent Flags")

    open_theses = utils.load_theses(["ACTIVE", "ENTRY_READY"])
    flagged: list[tuple[dict, list[str]]] = []
    for t in open_theses:
        reasons: list[str] = []
        raw = (t.get("position") or {}).get("raw_source") or {}
        dte = _days_to_expiry(raw.get("expiry"))
        if dte is not None and dte <= 7:
            reasons.append(f"Options expiring in {dte} days")
        mon = t.get("monitoring") or {}
        last_rev = mon.get("last_review_date")
        if last_rev:
            try:
                stale = (date.today() - date.fromisoformat(str(last_rev))).days
                if stale > 14:
                    reasons.append(f"Not reviewed in {stale} days")
            except (ValueError, TypeError):
                pass
        else:
            reasons.append("Never reviewed")
        cs = t.get("confidence_score") or 0
        if 0 < cs <= 0.4:
            reasons.append(f"Low confidence ({int(cs * 5)}/5)")
        if reasons:
            flagged.append((t, reasons))

    if not flagged:
        st.success("No urgent flags. All positions look current.")
    else:
        for t, reasons in flagged:
            tid = t.get("thesis_id", "")
            ticker = t.get("ticker", "")
            summary = (t.get("thesis_statement") or "—")[:100]
            exit_d = t.get("exit") or {}

            with st.container(border=True):
                st.markdown(f"**{ticker}** — {', '.join(reasons)}")
                st.caption(f"Thesis: {summary}")
                st.caption(
                    f"Stop: {exit_d.get('stop_loss') or '—'} | "
                    f"Target: {exit_d.get('take_profit') or '—'}"
                )

                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("Still Valid", key=f"valid_{tid}"):
                        _, err = _run_safe(utils.mark_reviewed, tid)
                        if err:
                            st.error(f"Failed: {err}")
                        else:
                            st.success("Marked reviewed.")
                            st.cache_data.clear()
                            st.rerun()
                with b2:
                    if st.button("Close Position", key=f"urg_close_{tid}"):
                        st.session_state[f"urg_closing_{tid}"] = True
                with b3:
                    if st.button("Roll", key=f"roll_{tid}"):
                        st.session_state[f"rolling_{tid}"] = True

            if st.session_state.get(f"urg_closing_{tid}"):
                with st.form(key=f"urg_close_form_{tid}"):
                    ep = st.number_input(
                        "Exit price", min_value=0.0, format="%.4f", key=f"uc_ep_{tid}"
                    )
                    ed = st.date_input("Exit date", value=date.today(), key=f"uc_ed_{tid}")
                    reason = st.selectbox(
                        "Exit reason",
                        EXIT_REASONS,
                        format_func=lambda x: EXIT_REASON_LABELS.get(x, x),
                        key=f"uc_r_{tid}",
                    )
                    if st.form_submit_button("Confirm Close"):
                        _, err = _run_safe(utils.finalize_thesis, tid, reason, ep, ed)
                        if err:
                            st.error(
                                f"Close failed (finalize_thesis {tid!r} {reason!r} {ep} {ed.isoformat()!r}):\n{err}"
                            )
                        else:
                            st.success(f"Closed {ticker}.")
                            st.session_state.pop(f"urg_closing_{tid}", None)
                            st.cache_data.clear()
                            st.rerun()

            if st.session_state.get(f"rolling_{tid}"):
                with st.form(key=f"roll_form_{tid}"):
                    r_strike = st.number_input(
                        "New strike", min_value=0.0, format="%.2f", key=f"rr_s_{tid}"
                    )
                    r_expiry = st.date_input("New expiry", key=f"rr_e_{tid}")
                    r_cost = st.number_input(
                        "New avg cost", min_value=0.0, format="%.4f", key=f"rr_c_{tid}"
                    )
                    r_note = st.text_input("Roll rationale", key=f"rr_n_{tid}")
                    if st.form_submit_button("Confirm Roll"):
                        _, close_err = _run_safe(
                            utils.finalize_thesis, tid, "manual", 0.0, date.today()
                        )
                        if close_err:
                            st.error(f"Close original failed:\n{close_err}")
                        else:
                            cs = t.get("confidence_score") or 0.6
                            roll_text = (
                                f"Roll from {tid} → {r_strike} strike exp {r_expiry}. {r_note}"
                            ).strip()
                            new_td = _build_thesis_data(
                                ticker=ticker,
                                thesis_type=t.get("thesis_type") or "growth_momentum",
                                thesis_text=roll_text,
                                confidence=max(1, round(cs * 5)),
                                stop_text="",
                                target_text="",
                                avg_cost=float(r_cost),
                            )
                            new_id, reg_err = _run_safe(utils.register_thesis, new_td)
                            if reg_err:
                                st.error(f"New thesis failed:\n{reg_err}")
                            else:
                                st.success(f"Rolled {ticker} → {new_id}")
                                st.session_state.pop(f"rolling_{tid}", None)
                                st.cache_data.clear()
                                st.rerun()

    st.divider()

    # ── Section B: needs post-trade review ────────────────────────────────────
    st.subheader("B — Needs Post-Trade Review")

    closed_theses = utils.load_theses(["CLOSED"])
    thirty_ago = (date.today() - timedelta(days=30)).isoformat()
    needs_review = [
        t
        for t in closed_theses
        if ((t.get("exit") or {}).get("actual_date") or "") >= thirty_ago
        and not ((t.get("outcome") or {}).get("lessons_learned"))
    ]

    if not needs_review:
        st.success("All recently closed positions have been reviewed.")
    else:
        for t in needs_review:
            tid = t.get("thesis_id", "")
            ticker = t.get("ticker", "")
            entry_p = (t.get("entry") or {}).get("actual_price")
            exit_p = (t.get("exit") or {}).get("actual_price")
            pnl = "—"
            if isinstance(entry_p, (int, float)) and isinstance(exit_p, (int, float)) and entry_p:
                pnl = f"{(exit_p - entry_p) / entry_p * 100:+.1f}%"
            cs = t.get("confidence_score") or 0
            pos = t.get("position") or {}

            with st.container(border=True):
                rc1, rc2, rc3, rc4, rc5 = st.columns([3, 1, 1, 1, 1])
                rc1.write(f"**{ticker}**")
                rc2.caption(f"Entry: {entry_p or '—'}")
                rc3.caption(f"Exit: {exit_p or '—'}")
                rc4.caption(f"P&L: {pnl}")
                rc5.caption(f"Conf: {int(cs * 5)}/5" if cs else "—")
                st.caption(f"Account: {_fmt_account(pos.get('account_type') or '')}")

                with st.form(key=f"review_form_{tid}"):
                    what = st.text_area(
                        "What happened? (2-3 sentences)", height=80, key=f"rv_w_{tid}"
                    )
                    lesson = st.text_input("Key lesson? (one sentence)", key=f"rv_l_{tid}")
                    if st.form_submit_button("Submit Review"):
                        existing_outcome = dict(t.get("outcome") or {})
                        existing_outcome["lessons_learned"] = lesson.strip()
                        existing_outcome["what_happened"] = what.strip()
                        _, err = _run_safe(utils.update_thesis, tid, {"outcome": existing_outcome})
                        if err:
                            st.error(f"Update failed (update_thesis {tid!r} outcome):\n{err}")
                        else:
                            st.success("Review saved.")
                            st.cache_data.clear()
                            st.rerun()

    st.divider()

    # ── Section C: closed this week ───────────────────────────────────────────
    st.subheader("C — Closed This Week")

    seven_ago = (date.today() - timedelta(days=7)).isoformat()
    week_closed = [
        t for t in closed_theses if ((t.get("exit") or {}).get("actual_date") or "") >= seven_ago
    ]

    if not week_closed:
        st.info("No positions closed in the last 7 days.")
    else:
        rows = []
        for t in week_closed:
            exit_d = t.get("exit") or {}
            entry_d = t.get("entry") or {}
            pos = t.get("position") or {}
            ep = entry_d.get("actual_price")
            xp = exit_d.get("actual_price")
            pnl = "—"
            if isinstance(ep, (int, float)) and isinstance(xp, (int, float)) and ep:
                pnl = f"{(xp - ep) / ep * 100:+.1f}%"
            cs = t.get("confidence_score") or 0
            rows.append(
                {
                    "Ticker": t.get("ticker", ""),
                    "Account": _fmt_account(pos.get("account_type") or ""),
                    "Entry": str(ep) if ep is not None else "—",
                    "Exit": str(xp) if xp is not None else "—",
                    "P&L": pnl,
                    "Confidence": f"{int(cs * 5)}/5" if cs else "—",
                    "Outcome": exit_d.get("exit_reason") or "—",
                }
            )
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


# ── page 4: research ───────────────────────────────────────────────────────────


def _research_row_style(row: pd.Series, meta: dict) -> list[str]:
    ticker = row.get("Ticker", "")
    info = meta.get(ticker, {})
    ui_status = info.get("ui_status", "")
    badge = info.get("badge", "")
    thesis_status = info.get("thesis_status", "")
    bg = ""
    if ui_status == "stale" or (
        ui_status == "missing" and thesis_status in ("ACTIVE", "ENTRY_READY")
    ):
        bg = "background-color: #3d0000"
    elif badge == "WARN":
        bg = "background-color: #3d2000"
    elif badge == "OK":
        bg = "background-color: #0a2e1a"
    return [bg] * len(row)


def _run_stale_research_scan(dry_run: bool) -> tuple[str, int]:
    script = utils.get_repo_root() / "scripts" / "update_stale_research.py"
    cmd = [sys.executable, str(script)]
    if dry_run:
        cmd.append("--dry-run")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=utils.get_repo_root(),
        timeout=120,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return output.strip(), result.returncode


def show_research() -> None:
    st.header("Research")

    rows = _research_rows()
    if not rows:
        st.info("No eligible tickers — add positions or edit research_watchlist.yaml")
        _show_research_refresh()
        return

    stale_count = sum(1 for r in rows if r["ui_status"] == "stale" or r["badge"] == "STALE")
    missing_count = sum(1 for r in rows if r["ui_status"] in ("missing", "needs_deep_research"))
    queued_count = research_utils.queue_recent_count()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tracked tickers", len(rows))
    m2.metric(
        "Stale (>14d)",
        stale_count,
        delta=f"⚠ {stale_count}" if stale_count else None,
        delta_color="inverse" if stale_count else "off",
    )
    m3.metric(
        "Missing report",
        missing_count,
        delta=f"⚠ {missing_count}" if missing_count else None,
        delta_color="inverse" if missing_count else "off",
    )
    m4.metric("Queued updates", queued_count)

    st.divider()

    meta = {r["ticker"]: r for r in rows}
    table_rows = []
    for r in rows:
        table_rows.append(
            {
                "_ticker": r["ticker"],
                "Ticker": r["ticker"],
                "Last Report": r["last_report_date"] or "—",
                "Days": str(r["days_stale"]) if r["days_stale"] is not None else "—",
                "Thesis": r["thesis_status"],
                "Watching": "yes" if r["watching"] else "—",
                "Status": r["ui_status"],
                "Badge": r["badge"],
            }
        )

    df = pd.DataFrame(table_rows)
    display_cols = ["Ticker", "Last Report", "Days", "Thesis", "Watching", "Status", "Badge"]
    styled = df[display_cols].style.apply(
        lambda row: _research_row_style(row, meta),
        axis=1,
    )

    event = st.dataframe(
        styled,
        width="stretch",
        on_select="rerun",
        selection_mode="single-row",
        key="research_table",
        hide_index=True,
    )

    sel = (event.selection.rows if hasattr(event, "selection") else []) or []
    if sel:
        selected = table_rows[sel[0]]
        ticker = selected["_ticker"]
        info = meta[ticker]

        with st.container(border=True):
            st.subheader(f"{ticker} — {info['ui_status']}")
            if info.get("notes"):
                st.caption(info["notes"])
            st.caption(f"Eligibility: {', '.join(info['eligibility']) or '—'}")

            if info.get("prefetch_available") and info.get("prefetch_path"):
                with st.expander("Open prefetch", expanded=False):
                    try:
                        prefetch_data = json.loads(Path(info["prefetch_path"]).read_text())
                        st.json(prefetch_data)
                    except (json.JSONDecodeError, OSError) as exc:
                        st.error(f"Could not read prefetch: {exc}")

            if info["ui_status"] != "missing":
                st.text_area(
                    "Copy update prompt",
                    value=research_utils.build_update_prompt(ticker),
                    height=120,
                    key=f"upd_prompt_{ticker}",
                )
            if info["ui_status"] == "missing":
                st.text_area(
                    "Copy deep-research prompt",
                    value=research_utils.build_deep_research_prompt(ticker),
                    height=80,
                    key=f"deep_prompt_{ticker}",
                )

    st.divider()

    with st.container(border=True):
        st.subheader("Watchlist")
        st.caption(
            f"File: {research_utils.resolve_watchlist_path().relative_to(utils.get_repo_root())}"
        )
        watchlist = research_utils.load_watchlist_for_editor()
        editor_rows = [
            {
                "Ticker": t,
                "Watching": cfg.get("watching", False),
                "Notes": cfg.get("notes", ""),
            }
            for t, cfg in sorted(watchlist.items())
        ]
        if not editor_rows:
            editor_rows = [{"Ticker": "", "Watching": True, "Notes": ""}]

        edited = st.data_editor(
            pd.DataFrame(editor_rows),
            num_rows="dynamic",
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", required=True),
                "Watching": st.column_config.CheckboxColumn("Watching"),
                "Notes": st.column_config.TextColumn("Notes"),
            },
            hide_index=True,
            key="watchlist_editor",
        )

        if st.button("Save watchlist", key="save_watchlist"):
            entries: dict[str, dict] = {}
            for _, row in edited.iterrows():
                t = str(row.get("Ticker", "")).strip().upper()
                if not t:
                    continue
                entries[t] = {
                    "watching": bool(row.get("Watching", False)),
                    "notes": str(row.get("Notes", "") or ""),
                }
            try:
                research_utils.save_watchlist(entries)
                st.success("Watchlist saved.")
                st.cache_data.clear()
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except OSError as exc:
                st.error(f"Save failed: {exc}")

    st.divider()

    queue = research_utils.load_update_queue()
    with st.container(border=True):
        st.subheader("Update queue")
        if queue:
            st.caption(
                f"Generated: {queue.get('generated_at', '—')} | "
                f"Threshold: {queue.get('threshold_days', research_utils.STALE_THRESHOLD_DAYS)}d"
            )
            q_rows = []
            for entry in queue.get("tickers") or []:
                if not isinstance(entry, dict):
                    continue
                q_rows.append(
                    {
                        "Ticker": entry.get("ticker", ""),
                        "Status": entry.get("status", ""),
                        "Days stale": entry.get("days_stale", "—"),
                        "Last report": entry.get("last_report") or "—",
                    }
                )
            if q_rows:
                st.dataframe(pd.DataFrame(q_rows), width="stretch", hide_index=True)
        else:
            st.info("No queue file yet. Regenerate to create state/research_update_queue.json.")

        b1, b2 = st.columns(2)
        with b1:
            if st.button("Refresh queue now", key="research_dry_run"):
                with st.spinner("Running dry-run scan..."):
                    output, code = _run_stale_research_scan(dry_run=True)
                st.code(output or "(no output)")
                st.caption(f"Exit code: {code}")
        with b2:
            if st.button("Regenerate queue", key="research_regen_queue"):
                with st.spinner("Regenerating queue..."):
                    output, code = _run_stale_research_scan(dry_run=False)
                if code in (0, 2):
                    st.success("Queue regenerated.")
                    if output:
                        st.code(output[:2000])
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Scan failed (exit {code}):\n{output[:2000]}")

    st.divider()
    _show_research_refresh()


# ── page: reports ──────────────────────────────────────────────────────────────


def show_reports() -> None:
    st.header("Reports")

    tickers = research_utils.list_report_tickers()
    if not tickers:
        st.info(
            "No research reports in reports/research/. "
            "Run deep-research or update-research, then return here."
        )
        if st.button("Go to Research", key="reports_empty_go_research"):
            st.session_state["nav_page"] = "Research"
            st.rerun()
        return

    ticker = st.selectbox("Ticker", tickers, key="reports_ticker")
    entries = research_utils.list_reports_for_ticker(ticker)
    if not entries:
        st.warning(f"No report files found for {ticker}.")
        return

    if len(entries) > 1:
        date_options = [e["date"].isoformat() for e in entries]
        selected_date = st.selectbox("Report date", date_options, key="reports_date")
        selected = next(e for e in entries if e["date"].isoformat() == selected_date)
    else:
        selected = entries[0]

    report_path: Path = selected["path"]
    report_date: date = selected["date"]
    days_old = (date.today() - report_date).days
    try:
        rel_path = report_path.relative_to(utils.get_repo_root())
    except ValueError:
        rel_path = report_path
    st.caption(f"{rel_path} · {days_old} days old")

    content = research_utils.load_report_markdown(report_path)
    if content:
        with st.container(height=500):
            st.markdown(content)
    else:
        st.warning("Could not read report file.")

    if days_old > research_utils.STALE_THRESHOLD_DAYS:
        st.caption(f"Report is stale (>{research_utils.STALE_THRESHOLD_DAYS} days).")
    if st.button("Go to Research", key="reports_go_research"):
        st.session_state["nav_page"] = "Research"
        st.rerun()


def _show_research_refresh() -> None:
    if st.button("Refresh data", key="research_refresh_data"):
        st.cache_data.clear()
        st.rerun()


# ── entry point ────────────────────────────────────────────────────────────────


def main() -> None:
    st.set_page_config(page_title="Thesis Manager", page_icon="📊", layout="wide")

    if "nav_page" in st.session_state:
        st.session_state["sidebar_page"] = st.session_state.pop("nav_page")

    page = st.sidebar.radio(
        "Page",
        PAGES,
        label_visibility="collapsed",
        key="sidebar_page",
    )
    st.sidebar.caption("trader-memory-core UI")

    if page == "Dashboard":
        show_dashboard()
    elif page == "Research":
        show_research()
    elif page == "Reports":
        show_reports()
    elif page == "Add Thesis":
        show_add_thesis()
    else:
        show_review()


if __name__ == "__main__":
    main()
