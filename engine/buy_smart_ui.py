"""
engine/buy_smart_ui.py — Blinkit-style Buy Smart prototype (polished mobile mock).
"""

from __future__ import annotations

import streamlit as st

from engine.trust_engine import (
    CategoryTrust,
    ProductTrust,
    get_category_trust,
    get_product_trust,
    list_categories,
    list_products,
    CATEGORY_LABELS,
)

# ── Blinkit-inspired design system ─────────────────────────────────────────

BUY_SMART_CSS = """
<style>
/* Scope: only Buy Smart page widgets */
.bs-page-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px 0 32px;
}

.bs-page-label {
    text-align: center;
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 16px;
    max-width: 420px;
}

/* Hide ugly streamlit chrome inside phone */
.bs-phone-shell div[data-testid="stHorizontalBlock"],
.bs-phone-shell div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

.bs-phone-shell div[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #3AB757 0%, #2d9648 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 4px 14px rgba(58, 183, 87, 0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.bs-phone-shell div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(58, 183, 87, 0.45) !important;
    border: none !important;
    color: #fff !important;
}

.bs-phone-shell div[data-testid="stButton"] > button[kind="secondary"] {
    background: #fff !important;
    color: #111 !important;
    border: 1.5px solid #e5e7eb !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 12px !important;
}

.bs-page-bg {
    background: linear-gradient(160deg, #e5e7eb 0%, #d1d5db 100%);
    border-radius: 20px;
    padding: 24px 16px;
    margin: 0 auto;
    max-width: 480px;
}

.bs-phone-shell .stSelectbox > div > div {
    background: #fff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    font-size: 13px !important;
}

.bs-cat-pills div[data-testid="stRadio"] > div {
    flex-direction: row !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    background: transparent !important;
}

.bs-cat-pills div[data-testid="stRadio"] label {
    background: #fff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 999px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #374151 !important;
    margin: 0 !important;
}

.bs-cat-pills div[data-testid="stRadio"] label[data-checked="true"],
.bs-cat-pills div[data-testid="stRadio"] label:has(input:checked) {
    background: #fffbeb !important;
    border-color: #F8C831 !important;
    color: #111 !important;
}

/* Phone frame */
.bs-phone {
    width: 100%;
    max-width: 390px;
    background: #f8f9fa;
    border-radius: 32px;
    overflow: hidden;
    box-shadow:
        0 0 0 8px #1a1a1a,
        0 0 0 10px #333,
        0 24px 48px rgba(0,0,0,0.25);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    position: relative;
}

.bs-status-bar {
    background: #F8C831;
    padding: 10px 20px 6px;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    color: #1a1a1a;
}

.bs-app-header {
    background: #F8C831;
    padding: 4px 16px 14px;
}

.bs-app-header .logo {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1;
}

.bs-app-header .logo span.y { color: #F8C831; background:#111; padding:0 2px; border-radius:3px; }
.bs-app-header .logo span.g { color: #3AB757; }

.bs-location {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    color: #111;
    margin-top: 8px;
}

.bs-location .eta {
    margin-left: auto;
    background: #111;
    color: #F8C831;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 6px;
}

.bs-screen {
    background: #fff;
    min-height: 520px;
    padding-bottom: 16px;
}

.bs-nav-back {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 14px 16px 8px;
    font-size: 15px;
    font-weight: 700;
    color: #111;
    cursor: default;
}

.bs-nav-back .arrow {
    width: 32px;
    height: 32px;
    background: #f3f4f6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

/* Buy Smart strip */
.bs-trust-strip {
    margin: 0 16px 16px;
    padding: 14px 16px;
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1.5px solid #86efac;
    border-radius: 14px;
}

.bs-trust-strip .head {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 800;
    color: #166534;
    margin-bottom: 12px;
}

.bs-trust-strip .shield {
    width: 28px;
    height: 28px;
    background: #3AB757;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.bs-score-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.bs-score-box {
    background: #fff;
    border-radius: 10px;
    padding: 10px 12px;
    border: 1px solid #d1fae5;
}

.bs-score-box .lbl {
    font-size: 10px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.bs-score-box .val {
    font-size: 26px;
    font-weight: 900;
    line-height: 1.1;
    margin-top: 2px;
}

.bs-score-box .val span {
    font-size: 14px;
    font-weight: 600;
    color: #9ca3af;
}

.bs-trust-foot {
    font-size: 10px;
    color: #6b7280;
    margin-top: 10px;
    line-height: 1.4;
}

/* Product grid (category) */
.bs-section-title {
    padding: 0 16px 10px;
    font-size: 13px;
    font-weight: 800;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.bs-product-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    padding: 0 16px;
}

.bs-grid-card {
    background: #fff;
    border: 1px solid #f0f0f0;
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.bs-grid-card .emoji {
    font-size: 32px;
    margin-bottom: 6px;
}

.bs-grid-card .nm {
    font-size: 12px;
    font-weight: 700;
    color: #111;
    line-height: 1.3;
    min-height: 32px;
}

.bs-grid-card .pr {
    font-size: 15px;
    font-weight: 800;
    color: #111;
    margin-top: 4px;
}

.bs-grid-card .badge {
    display: inline-block;
    margin-top: 6px;
    font-size: 10px;
    font-weight: 700;
    color: #166534;
    background: #dcfce7;
    padding: 3px 8px;
    border-radius: 999px;
}

/* Product detail page */
.bs-pdp-hero {
    background: linear-gradient(180deg, #fafafa 0%, #fff 100%);
    padding: 24px 16px 20px;
    text-align: center;
    border-bottom: 1px solid #f0f0f0;
}

.bs-pdp-hero .emoji {
    font-size: 72px;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.08));
}

.bs-pdp-body {
    padding: 16px;
}

.bs-pdp-title {
    font-size: 20px;
    font-weight: 800;
    color: #111;
    letter-spacing: -0.02em;
}

.bs-pdp-price {
    font-size: 24px;
    font-weight: 900;
    color: #111;
    margin: 4px 0 16px;
}

.bs-pdp-price .mrp {
    font-size: 14px;
    color: #9ca3af;
    text-decoration: line-through;
    font-weight: 500;
    margin-left: 8px;
}

.bs-meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 16px;
}

.bs-meta-item {
    flex: 1 1 30%;
    min-width: 100px;
    padding: 12px 10px;
    text-align: center;
    border-right: 1px solid #e5e7eb;
    background: #fafafa;
}

.bs-meta-item:last-child { border-right: none; }

.bs-meta-item .ico { font-size: 18px; margin-bottom: 4px; }
.bs-meta-item .tx {
    font-size: 11px;
    font-weight: 600;
    color: #374151;
    line-height: 1.3;
}

.bs-meta-item .tx strong {
    display: block;
    font-size: 12px;
    color: #111;
    margin-bottom: 2px;
}

.bs-safe-chip {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
    font-size: 14px;
    font-weight: 700;
    color: #166534;
}

/* Trust sheet — inline panel */
.bs-sheet-inline {
    margin: 0 16px 16px;
    background: #fff;
    border-radius: 16px;
    padding: 4px 16px 20px;
    border: 2px solid #86efac;
    box-shadow: 0 8px 32px rgba(58, 183, 87, 0.12);
}

.bs-sheet-handle {
    width: 40px;
    height: 4px;
    background: #d1d5db;
    border-radius: 999px;
    margin: 8px auto 16px;
}

.bs-sheet-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
}

.bs-sheet-score {
    font-size: 48px;
    font-weight: 900;
    line-height: 1;
    margin: 4px 0 8px;
    letter-spacing: -0.03em;
}

.bs-sheet-verdict {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    font-size: 13px;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 999px;
    margin-bottom: 20px;
}

.bs-tip {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 14px 0;
    border-bottom: 1px solid #f3f4f6;
}

.bs-tip:last-of-type { border-bottom: none; }

.bs-tip-icon {
    width: 36px;
    height: 36px;
    background: #f0fdf4;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.bs-tip-text {
    font-size: 14px;
    color: #374151;
    line-height: 1.45;
    font-weight: 500;
}

.bs-sheet-note {
    font-size: 10px;
    color: #9ca3af;
    line-height: 1.5;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid #f3f4f6;
}

.bs-proto-tag {
    text-align: center;
    font-size: 10px;
    color: #92400e;
    background: #fffbeb;
    padding: 6px;
    border-bottom: 1px solid #fde68a;
}
</style>
"""


def _score_color(score: int) -> str:
    if score >= 70:
        return "#166534"
    if score >= 55:
        return "#c2410c"
    return "#b91c1c"


def _phone_header_html() -> str:
    return """
    <div class="bs-status-bar">
        <span>9:41</span>
        <span>●●●</span>
    </div>
    <div class="bs-app-header">
        <div class="logo"><span style="color:#111;">blinki</span><span class="g">t</span></div>
        <div class="location">
            <span>📍</span>
            <span>Home · Sector 14, Gurugram</span>
            <span class="eta">⚡ 10 min</span>
        </div>
    </div>
    """


def _trust_strip_html(cat: CategoryTrust) -> str:
    cond = " · ".join(cat.buy_smart_conditions)
    return f"""
    <div class="bs-trust-strip">
        <div class="head">
            <div class="shield">🛡️</div>
            Buy Smart · {cat.label}
        </div>
        <div class="bs-score-row">
            <div class="bs-score-box">
                <div class="lbl">Overall risk</div>
                <div class="val" style="color:{_score_color(cat.overall_score)};">{cat.overall_score}<span>/100</span></div>
            </div>
            <div class="bs-score-box">
                <div class="lbl">Buy smart path</div>
                <div class="val" style="color:#166534;">{cat.buy_smart_score}<span>/100</span></div>
            </div>
        </div>
        <div class="bs-trust-foot">*{cond}<br>From {cat.review_count} reviews in our AI analysis corpus</div>
    </div>
    """


def _category_grid_html(products: list[dict], category: str, df) -> str:
    cards = []
    for prod in products:
        pt = get_product_trust(df, prod, category)
        cards.append(
            f"""<div class="bs-grid-card">
                <div class="emoji">{pt.emoji}</div>
                <div class="nm">{pt.name}</div>
                <div class="pr">₹{pt.price:,}</div>
                <span class="badge">{pt.score}/100 · {pt.verdict}</span>
            </div>"""
        )
    return f'<div class="bs-section-title">Popular in this category</div><div class="bs-product-grid">{"".join(cards)}</div>'


def _pdp_html(pt: ProductTrust) -> str:
    keep = pt.keep_rate if pt.keep_rate is not None else "—"
    mrp = int(pt.price * 1.15)
    warranty_short = pt.warranty.replace(" manufacturer warranty", "").replace(" warranty", "")
    if len(warranty_short) > 22:
        warranty_short = warranty_short[:20] + "…"
    return f"""
    <div class="bs-pdp-hero">
        <div class="emoji">{pt.emoji}</div>
    </div>
    <div class="bs-pdp-body">
        <div class="bs-pdp-title">{pt.name}</div>
        <div class="bs-pdp-price">₹{pt.price:,}<span class="mrp">₹{mrp:,}</span></div>
        <div class="bs-meta-row">
            <div class="bs-meta-item">
                <div class="ico">🔄</div>
                <div class="tx"><strong>{pt.replacement_days}-day</strong>replacement</div>
            </div>
            <div class="bs-meta-item">
                <div class="ico">📋</div>
                <div class="tx"><strong>Warranty</strong>{warranty_short}</div>
            </div>
            <div class="bs-meta-item">
                <div class="ico">👍</div>
                <div class="tx"><strong>{keep}%</strong>positive mentions*</div>
            </div>
        </div>
        <div class="bs-safe-chip">✅ {pt.verdict} · Tap below to see how</div>
    </div>
    """


def _sheet_html(pt: ProductTrust) -> str:
    tips = ""
    icons = ["🎬", "🏷️", "📦", "✅"]
    for i, tip in enumerate(pt.tips):
        ico = icons[i % len(icons)]
        tips += f'<div class="bs-tip"><div class="bs-tip-icon">{ico}</div><div class="bs-tip-text">{tip}</div></div>'

    return f"""
    <div class="bs-sheet-inline">
        <div class="bs-sheet-handle"></div>
        <div class="bs-sheet-label">Buy Smart trust sheet</div>
        <div class="bs-sheet-score" style="color:{_score_color(pt.score)};">{pt.score}<span style="font-size:20px;color:#9ca3af;">/100</span></div>
        <div class="bs-sheet-verdict">{pt.verdict}</div>
        {tips}
        <div class="bs-sheet-note">*{pt.keep_rate}% positive mentions from {pt.evidence_label}. Prototype data — not Blinkit internal metrics.</div>
    </div>
    """


def _init_state() -> None:
    defaults = {
        "bs_view": "category",
        "bs_category": "electronics",
        "bs_product_id": None,
        "bs_show_sheet": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_buy_smart_page(df) -> None:
    _init_state()
    st.markdown(BUY_SMART_CSS, unsafe_allow_html=True)

    st.markdown(
        '<div class="bs-page-wrap"><div class="bs-page-label">'
        "📱 <b>Buy Smart MVP</b> — Simulated in-app experience for evaluators"
        "</div></div>",
        unsafe_allow_html=True,
    )

    # Category pills — outside phone, cleaner
    st.markdown('<div class="bs-cat-pills">', unsafe_allow_html=True)
    cat = st.radio(
        "Category",
        list_categories(),
        format_func=lambda x: CATEGORY_LABELS.get(x, x),
        horizontal=True,
        label_visibility="collapsed",
        key="bs_cat_radio",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.bs_category = cat

    # Reset to category view when user switches category
    if st.session_state.get("_bs_last_cat") != cat:
        st.session_state.bs_view = "category"
        st.session_state.bs_product_id = None
        st.session_state.bs_show_sheet = False
        st.session_state._bs_last_cat = cat

    cat_trust = get_category_trust(df, cat)
    products = list_products(cat)
    product_map = {p["id"]: p for p in products}

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown('<div class="bs-page-bg"><div class="bs-phone-shell"><div class="bs-phone">', unsafe_allow_html=True)
        st.markdown('<div class="bs-proto-tag">AI trust layer · production prototype demo</div>', unsafe_allow_html=True)
        st.markdown(_phone_header_html(), unsafe_allow_html=True)
        st.markdown('<div class="bs-screen">', unsafe_allow_html=True)

        view = st.session_state.bs_view

        # ── Category list view ──
        if view == "category":
            st.markdown(
                f'<div class="bs-nav-back"><div class="arrow">‹</div> {cat_trust.label}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(_trust_strip_html(cat_trust), unsafe_allow_html=True)
            st.markdown(_category_grid_html(products, cat, df), unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="bs-section-title">Tap to open product</div>', unsafe_allow_html=True)
            cols = st.columns(2)
            for i, prod in enumerate(products):
                with cols[i % 2]:
                    if st.button(prod["name"], key=f"open_{prod['id']}", use_container_width=True, type="secondary"):
                        st.session_state.bs_product_id = prod["id"]
                        st.session_state.bs_view = "product"
                        st.session_state.bs_show_sheet = False
                        st.rerun()

        # ── Product detail view ──
        elif view == "product" and st.session_state.bs_product_id in product_map:
            prod = product_map[st.session_state.bs_product_id]
            pt = get_product_trust(df, prod, cat)

            if st.button("← Back to category", type="secondary"):
                st.session_state.bs_view = "category"
                st.session_state.bs_show_sheet = False
                st.rerun()

            st.markdown(_pdp_html(pt), unsafe_allow_html=True)

            if st.button(f"✅ {pt.verdict} · See how →", use_container_width=True):
                st.session_state.bs_show_sheet = True
                st.rerun()

            if st.session_state.bs_show_sheet:
                st.markdown(_sheet_html(pt), unsafe_allow_html=True)
                if st.button("Close trust sheet", use_container_width=True):
                    st.session_state.bs_show_sheet = False
                    st.rerun()

        st.markdown("</div></div></div></div>", unsafe_allow_html=True)

    # Evaluator notes — outside phone
    with st.expander("ℹ️ How this MVP works (for evaluators)"):
        st.markdown(
            f"""
- **Not the real Blinkit app** — simulated UI showing where Buy Smart would live
- **Scores** computed from {cat_trust.review_count} reviews in our AI analysis engine
- **Overall {cat_trust.overall_score}** = risk signal in complaint-heavy corpus
- **Buy smart {cat_trust.buy_smart_score}** = score on the safe path (known brand + urgent + low ticket)
- **No chatbot · no competitor links** — trust cards only
            """
        )
