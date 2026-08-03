"""
engine/analyser_panel.py — Link A AI Analyser (Phase 8H).

Surfaces workflow, data stats, and re-runnable theme analysis on the committed corpus.
No live scraping — offline only for eval stability.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

import config
from engine.themes import get_theme_summary

GITHUB_ACTIONS_URL = "https://github.com/HimanshiBhambhani/Grad-Project/actions"


def _corpus_mtime(path: Path) -> str:
    if not path.exists():
        return "unknown"
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def render_workflow_section() -> None:
    """Static pipeline diagram — ingest through Link B scores."""
    st.markdown("##### 1. Workflow")
    st.caption("End-to-end path from raw reviews to trust signals (Link B uses same classified corpus).")

    steps = [
        ("Ingest", "Play Store · App Store · Reddit · YouTube · CSV dumps"),
        ("Clean", "Dedup → noise filter → rating filter → category isolation"),
        ("Embed", "all-MiniLM-L6-v2 → FAISS index (384-dim vectors)"),
        ("Classify", "Theme labels + Target Category + Friction Pillar"),
        ("Analyse", "Theme summary, quotes, cross-category patterns"),
        ("Operationalise", "Link B trust scores from CORPUS A + B (deterministic)"),
    ]
    cols = st.columns(len(steps))
    for col, (title, detail) in zip(cols, steps):
        with col:
            st.markdown(
                f'<div class="fluent-card" style="padding:12px;text-align:center;min-height:100px;">'
                f'<div style="font-weight:600;font-size:13px;color:var(--neutral-fg-1);">{title}</div>'
                f'<div style="font-size:11px;color:var(--neutral-fg-3);margin-top:6px;line-height:1.4;">{detail}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )


def render_github_actions_link() -> None:
    """CI/CD pipeline link — visible on main Analyser page for evaluators."""
    st.markdown(
        '<div class="fluent-card" style="display:flex;align-items:center;gap:var(--space-lg);'
        'margin:12px 0 4px;padding:var(--space-md) var(--space-lg);">'
        '<div style="flex:1;">'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);margin-bottom:4px;">'
        "GitHub Actions — weekly scrape pipeline"
        "</div>"
        '<div style="font-size:13px;color:var(--neutral-fg-2);">'
        "Automated Play Store / App Store scrape, filter, and corpus rebuild on schedule. "
        "View run history, logs, and workflow YAML."
        "</div>"
        "</div>"
        f'<a href="{GITHUB_ACTIONS_URL}" target="_blank" rel="noopener noreferrer" '
        'style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;'
        "background:var(--brand-primary);color:white;border-radius:var(--radius-sm);"
        'text-decoration:none;font-size:14px;font-weight:600;white-space:nowrap;">'
        "\u2192 View on GitHub Actions</a>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_data_stats(df: pd.DataFrame) -> None:
    """Corpus metadata and theme distribution."""
    st.markdown("##### 2. Data")
    st.caption("Committed corpus in repo — no live fetch required for evaluation.")

    corpus_path = config.CLEAN_OUTPUT_CSV
    mtime = _corpus_mtime(corpus_path)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews", f"{len(df):,}")
    c2.metric("Categories", df["Target Category"].nunique())
    c3.metric("Themes", df["Primary Theme"].nunique())
    c4.metric("Sources", df["Source"].nunique())

    st.markdown(
        f'<div style="font-size:12px;color:var(--neutral-fg-3);margin:8px 0 16px;">'
        f"<strong>Corpus path:</strong> <code>{corpus_path.name}</code> · "
        f"<strong>Last modified:</strong> {mtime} · "
        f"<strong>Policy:</strong> committed corpus (MVP)"
        f"</div>",
        unsafe_allow_html=True,
    )

    theme_counts = df["Primary Theme"].value_counts().head(12)
    st.markdown("**Theme distribution**")
    st.bar_chart(theme_counts, horizontal=True, color="#0F6CBD")


def render_analyser(
    df: pd.DataFrame,
    *,
    badge_fn=None,
    on_rerun=None,
) -> None:
    """Re-run theme summary on corpus; show top themes and quotes."""
    st.markdown("##### 3. Analyser")
    st.caption(
        "Aggregates **pre-classified** themes from the committed CSV — "
        "not a live scrape, embedding pass, or LLM call."
    )

    if "analyser_ran" not in st.session_state:
        st.session_state.analyser_ran = False

    categories = sorted(df["Target Category"].dropna().unique())
    cat_filter = st.selectbox(
        "Filter by category (optional)",
        options=["All categories"] + list(categories),
        index=0,
        key="analyser_category_filter",
    )

    if st.button("Re-run analyser on committed corpus (MVP)", type="primary", use_container_width=False):
        if on_rerun:
            on_rerun()
        st.session_state.analyser_ran = True
        st.session_state.analyser_run_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        st.session_state.analyser_corpus_rows = len(df)
        st.rerun()

    if not st.session_state.analyser_ran:
        st.info(
            "Theme summary is not shown until you run the analyser. "
            "Click **Re-run analyser** to reload the CSV and compute counts + quotes."
        )
        return

    filtered = df if cat_filter == "All categories" else df[df["Target Category"] == cat_filter]

    with st.spinner("Aggregating themes from committed corpus…"):
        themes = get_theme_summary(filtered)
        top_themes = themes[:5]
        analysis_steps = [
            f"Reloaded `{config.CLEAN_OUTPUT_CSV.name}` from disk "
            f"({st.session_state.get('analyser_corpus_rows', len(df)):,} rows in corpus)",
            f"Filtered to **{len(filtered):,}** reviews"
            + (f" · category `{cat_filter}`" if cat_filter != "All categories" else ""),
            f"Counted **{filtered['Primary Theme'].nunique()}** distinct theme labels (pre-baked in CSV)",
            f"Ranked top **{len(top_themes)}** themes by volume and pulled representative quotes",
        ]

    run_at = st.session_state.get("analyser_run_at", "just now")
    st.success(
        f"Analysis complete — {len(filtered):,} reviews, "
        f"{filtered['Primary Theme'].nunique()} themes · last run {run_at}"
    )

    with st.expander("What ran (offline steps)", expanded=True):
        for step in analysis_steps:
            st.markdown(f"- {step}")
        st.markdown(
            "_Themes were classified offline during pipeline build; this button recomputes "
            "summary statistics only._"
        )

    if not top_themes:
        st.info("No themes found for the selected filter.")
        return

    st.markdown(f"**Top {len(top_themes)} themes**")
    for theme in top_themes:
        pct = theme["percentage"]
        badge = badge_fn(str(pct) + "%", "brand") if badge_fn else f"{pct}%"
        count_badge = badge_fn(str(theme["count"]) + " reviews", "neutral") if badge_fn else str(theme["count"])

        quotes_html = ""
        for q in theme.get("representative_quotes", [])[:3]:
            q_trunc = q[:180] + ("…" if len(q) > 180 else "")
            quotes_html += (
                f'<div style="font-size:12px;color:var(--neutral-fg-2);font-style:italic;'
                f'margin-top:6px;border-left:2px solid var(--brand-primary);padding-left:8px;">'
                f"&ldquo;{q_trunc}&rdquo;</div>"
            )

        st.markdown(
            f'<div class="fluent-card" style="padding:var(--space-md) var(--space-lg);margin-bottom:12px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
            f'<div style="font-weight:600;color:var(--neutral-fg-1);">{theme["theme"]}</div>'
            f"<div>{badge + ' ' + count_badge if badge_fn else f'{pct}% · {theme['count']} reviews'}</div>"
            f"</div>{quotes_html}</div>",
            unsafe_allow_html=True,
        )


def render_analyser_page(
    df: pd.DataFrame,
    *,
    badge_fn=None,
    on_rerun=None,
    show_legacy_details: bool = False,
    legacy_details_fn=None,
) -> None:
    """Full AI Analyser tab: workflow + data + analyser (+ optional legacy workflow expanders)."""
    st.markdown(
        '<div class="fluent-hero"><h1>AI Analyser</h1>'
        "<p>Workflow · Data · Analyser — evaluator-facing view of the discovery pipeline "
        "on the <strong>committed corpus</strong>. Re-run recomputes theme summaries from "
        "pre-classified CSV rows (seconds, offline).</p></div>",
        unsafe_allow_html=True,
    )

    render_workflow_section()
    render_github_actions_link()
    st.divider()
    render_data_stats(df)
    st.divider()
    render_analyser(df, badge_fn=badge_fn, on_rerun=on_rerun)

    if show_legacy_details and legacy_details_fn:
        st.divider()
        legacy_details_fn()
