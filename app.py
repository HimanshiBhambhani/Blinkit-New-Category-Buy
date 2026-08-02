"""
app.py — Streamlit Discovery Engine Dashboard.

Interactive dashboard for exploring Blinkit customer feedback insights.
Styled after Microsoft Fluent 2 Design System.

Usage:
    streamlit run app.py
"""

import os
import sys
from pathlib import Path

# ── SSL & HF fixes (must run before any HuggingFace / model imports) ──
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from engine.themes import identify_themes, get_theme_summary, get_cross_theme_patterns
from engine.insights import STRATEGIC_QUESTIONS, generate_insight_offline
from engine.chatbot import RAGChatbot


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FLUENT 2 DESIGN SYSTEM — CSS THEME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FLUENT_CSS = """
<style>
/* ── Fluent 2 Design Tokens (Light Mode) ── */
:root {
    /* Brand */
    --brand-primary: #0F6CBD;
    --brand-hover: #115EA3;
    --brand-pressed: #0C3B5E;
    --brand-light: #B4D6FA;
    --brand-bg: #EBF3FC;
    --brand-gradient: linear-gradient(135deg, #0F6CBD 0%, #0E4775 100%);

    /* Neutral */
    --neutral-bg-1: #FFFFFF;
    --neutral-bg-2: #FAFAFA;
    --neutral-bg-3: #F5F5F5;
    --neutral-bg-4: #E0E0E0;
    --neutral-fg-1: #242424;
    --neutral-fg-2: #616161;
    --neutral-fg-3: #9E9E9E;
    --neutral-stroke-1: #E8E8E8;
    --neutral-stroke-2: #D1D1D1;
    --neutral-stroke-subtle: rgba(0,0,0,0.05);

    /* Semantic */
    --status-success: #107C10;
    --status-success-bg: #DFF6DD;
    --status-warning: #F7630C;
    --status-warning-bg: #FFF4CE;
    --status-danger: #BC2F32;
    --status-danger-bg: #FDE7E9;
    --status-info: #0F6CBD;
    --status-info-bg: #EBF3FC;

    /* Elevation (Fluent shadow tokens) */
    --shadow-2: 0px 1px 2px rgba(0,0,0,0.08), 0px 0px 2px rgba(0,0,0,0.06);
    --shadow-4: 0px 2px 4px rgba(0,0,0,0.08), 0px 0px 2px rgba(0,0,0,0.06);
    --shadow-8: 0px 4px 8px rgba(0,0,0,0.08), 0px 0px 4px rgba(0,0,0,0.04);
    --shadow-16: 0px 8px 16px rgba(0,0,0,0.10), 0px 0px 4px rgba(0,0,0,0.06);
    --shadow-28: 0px 14px 28px rgba(0,0,0,0.12), 0px 0px 8px rgba(0,0,0,0.06);

    /* Shapes */
    --radius-xs: 4px;
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-pill: 999px;

    /* Spacing */
    --space-2xs: 4px;
    --space-xs: 8px;
    --space-sm: 12px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    --space-2xl: 48px;

    /* Typography */
    --font-family: 'Segoe UI Variable', 'Segoe UI', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    --font-body: 14px/20px var(--font-family);
    --font-caption: 12px/16px var(--font-family);
    --font-subtitle-2: 600 16px/22px var(--font-family);
    --font-subtitle-1: 600 20px/26px var(--font-family);
    --font-title-3: 600 24px/32px var(--font-family);
    --font-title-2: 600 28px/36px var(--font-family);
    --font-display: 600 40px/52px var(--font-family);

    /* Motion */
    --duration-fast: 0.1s;
    --duration-normal: 0.2s;
    --duration-slow: 0.3s;
    --easing-standard: cubic-bezier(0.33, 0, 0.67, 1);
    --easing-decelerate: cubic-bezier(0, 0, 0, 1);
    --easing-accelerate: cubic-bezier(1, 0, 1, 1);
}

/* ── Fluent 2 Dark Mode Tokens ── */
@media (prefers-color-scheme: dark) {
    :root {
        --brand-primary: #479EF5;
        --brand-hover: #62ABF5;
        --brand-pressed: #2886DE;
        --brand-light: #0C3B5E;
        --brand-bg: #0D2D4A;
        --brand-gradient: linear-gradient(135deg, #1B6EC2 0%, #0A3A6B 100%);

        --neutral-bg-1: #1E1E1E;
        --neutral-bg-2: #141414;
        --neutral-bg-3: #2A2A2A;
        --neutral-bg-4: #3D3D3D;
        --neutral-fg-1: #E8E8E8;
        --neutral-fg-2: #B3B3B3;
        --neutral-fg-3: #8A8A8A;
        --neutral-stroke-1: #383838;
        --neutral-stroke-2: #4A4A4A;
        --neutral-stroke-subtle: rgba(255,255,255,0.06);

        --status-success: #54B054;
        --status-success-bg: #0D2D0D;
        --status-warning: #F7894A;
        --status-warning-bg: #3D2000;
        --status-danger: #E37D80;
        --status-danger-bg: #3B0509;
        --status-info: #479EF5;
        --status-info-bg: #0D2D4A;

        --shadow-2: 0px 1px 2px rgba(0,0,0,0.36), 0px 0px 2px rgba(0,0,0,0.28);
        --shadow-4: 0px 2px 4px rgba(0,0,0,0.36), 0px 0px 2px rgba(0,0,0,0.28);
        --shadow-8: 0px 4px 8px rgba(0,0,0,0.36), 0px 0px 4px rgba(0,0,0,0.24);
        --shadow-16: 0px 8px 16px rgba(0,0,0,0.40), 0px 0px 4px rgba(0,0,0,0.28);
        --shadow-28: 0px 14px 28px rgba(0,0,0,0.48), 0px 0px 8px rgba(0,0,0,0.32);
    }
}

/* Streamlit's own dark theme detection */
[data-testid="stAppViewContainer"][data-theme="dark"],
.stApp[data-theme="dark"],
html[data-theme="dark"] {
    --brand-primary: #479EF5;
    --brand-hover: #62ABF5;
    --brand-pressed: #2886DE;
    --brand-light: #0C3B5E;
    --brand-bg: #0D2D4A;
    --brand-gradient: linear-gradient(135deg, #1B6EC2 0%, #0A3A6B 100%);

    --neutral-bg-1: #1E1E1E;
    --neutral-bg-2: #141414;
    --neutral-bg-3: #2A2A2A;
    --neutral-bg-4: #3D3D3D;
    --neutral-fg-1: #E8E8E8;
    --neutral-fg-2: #B3B3B3;
    --neutral-fg-3: #8A8A8A;
    --neutral-stroke-1: #383838;
    --neutral-stroke-2: #4A4A4A;
    --neutral-stroke-subtle: rgba(255,255,255,0.06);

    --status-success: #54B054;
    --status-success-bg: #0D2D0D;
    --status-warning: #F7894A;
    --status-warning-bg: #3D2000;
    --status-danger: #E37D80;
    --status-danger-bg: #3B0509;
    --status-info: #479EF5;
    --status-info-bg: #0D2D4A;

    --shadow-2: 0px 1px 2px rgba(0,0,0,0.36), 0px 0px 2px rgba(0,0,0,0.28);
    --shadow-4: 0px 2px 4px rgba(0,0,0,0.36), 0px 0px 2px rgba(0,0,0,0.28);
    --shadow-8: 0px 4px 8px rgba(0,0,0,0.36), 0px 0px 4px rgba(0,0,0,0.24);
    --shadow-16: 0px 8px 16px rgba(0,0,0,0.40), 0px 0px 4px rgba(0,0,0,0.28);
    --shadow-28: 0px 14px 28px rgba(0,0,0,0.48), 0px 0px 8px rgba(0,0,0,0.32);
}

/* ── Global ── */
html, body, .stApp {
    font-family: var(--font-family) !important;
    color: var(--neutral-fg-1);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.stApp {
    background-color: var(--neutral-bg-2) !important;
}

.stApp > header {
    background-color: var(--neutral-bg-1) !important;
    border-bottom: 1px solid var(--neutral-stroke-1) !important;
    backdrop-filter: blur(12px);
}

/* Ensure text inherits correct color everywhere */
.stApp p, .stApp span, .stApp li, .stApp td, .stApp th,
.stApp div, .stApp label, .stMarkdown {
    color: var(--neutral-fg-1);
}
.stApp .stCaption, .stApp caption {
    color: var(--neutral-fg-3) !important;
}

/* ── Sidebar — Fluent 2 nav pane ── */
section[data-testid="stSidebar"] {
    background-color: var(--neutral-bg-1) !important;
    border-right: 1px solid var(--neutral-stroke-1) !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: var(--neutral-fg-1);
}

section[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important;
    padding: 10px 16px !important;
    border-radius: var(--radius-sm) !important;
    margin-bottom: 2px;
    transition: background-color var(--duration-fast) var(--easing-standard),
                color var(--duration-fast) var(--easing-standard);
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background-color: var(--neutral-bg-3) !important;
}

section[data-testid="stSidebar"] hr {
    border-color: var(--neutral-stroke-1) !important;
    margin: var(--space-md) 0 !important;
}

/* ── Typography ── */
.stApp h1 {
    font: var(--font-title-2) !important;
    color: var(--neutral-fg-1) !important;
    letter-spacing: -0.02em;
    margin-bottom: var(--space-xs) !important;
}

.stApp h2 {
    font: var(--font-title-3) !important;
    color: var(--neutral-fg-1) !important;
    margin-top: var(--space-lg) !important;
    margin-bottom: var(--space-sm) !important;
}

.stApp h3 {
    font: var(--font-subtitle-1) !important;
    color: var(--neutral-fg-1) !important;
}

.stApp h5 {
    font: var(--font-subtitle-2) !important;
    color: var(--neutral-fg-1) !important;
    margin-top: var(--space-lg) !important;
    margin-bottom: var(--space-sm) !important;
}

/* ── Metric Cards — elevated with accent bar ── */
div[data-testid="stMetric"] {
    background: var(--neutral-bg-1);
    border: 1px solid var(--neutral-stroke-1);
    border-radius: var(--radius-lg);
    padding: var(--space-lg) var(--space-lg);
    box-shadow: var(--shadow-4);
    transition: box-shadow var(--duration-normal) var(--easing-decelerate),
                transform var(--duration-normal) var(--easing-decelerate);
    position: relative;
    overflow: hidden;
}

div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--brand-gradient);
    opacity: 0;
    transition: opacity var(--duration-normal) var(--easing-decelerate);
}

div[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-8);
    transform: translateY(-2px);
}

div[data-testid="stMetric"]:hover::before {
    opacity: 1;
}

div[data-testid="stMetric"] label {
    font: var(--font-caption) !important;
    color: var(--neutral-fg-3) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600 !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 32px !important;
    font-weight: 600 !important;
    color: var(--brand-primary) !important;
    letter-spacing: -0.02em;
}

/* ── Expander Cards — refined ── */
details[data-testid="stExpander"] {
    background: var(--neutral-bg-1) !important;
    border: 1px solid var(--neutral-stroke-1) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-2);
    margin-bottom: var(--space-sm) !important;
    overflow: hidden;
    transition: box-shadow var(--duration-normal) var(--easing-standard);
}

details[data-testid="stExpander"]:hover {
    box-shadow: var(--shadow-4);
}

details[data-testid="stExpander"] summary {
    font: var(--font-subtitle-2) !important;
    color: var(--neutral-fg-1) !important;
    padding: var(--space-md) var(--space-lg) !important;
    transition: background-color var(--duration-fast) var(--easing-standard);
}

details[data-testid="stExpander"] summary:hover {
    background-color: var(--neutral-bg-3) !important;
}

details[data-testid="stExpander"][open] summary {
    border-bottom: 1px solid var(--neutral-stroke-1);
}

/* ── Buttons — Fluent 2 with micro-interactions ── */
.stButton button {
    font-family: var(--font-family) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: var(--radius-sm) !important;
    padding: 8px 20px !important;
    transition: all var(--duration-fast) var(--easing-standard) !important;
    border: 1px solid transparent !important;
    color: var(--neutral-fg-1) !important;
    position: relative;
    overflow: hidden;
}

.stButton button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background-color: var(--brand-primary) !important;
    color: white !important;
    border-color: var(--brand-primary) !important;
    box-shadow: 0 1px 2px rgba(15, 108, 189, 0.3);
}

.stButton button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background-color: var(--brand-hover) !important;
    border-color: var(--brand-hover) !important;
    box-shadow: 0 2px 8px rgba(15, 108, 189, 0.4);
    transform: translateY(-1px);
}

.stButton button[kind="primary"]:active,
button[data-testid="stBaseButton-primary"]:active {
    background-color: var(--brand-pressed) !important;
    transform: translateY(0);
    box-shadow: none;
}

.stButton button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {
    background-color: var(--neutral-bg-1) !important;
    color: var(--neutral-fg-1) !important;
    border-color: var(--neutral-stroke-2) !important;
}

.stButton button[kind="secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background-color: var(--neutral-bg-3) !important;
    box-shadow: var(--shadow-2);
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
textarea {
    font-family: var(--font-family) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--neutral-stroke-2) !important;
    font-size: 14px !important;
    color: var(--neutral-fg-1) !important;
    background-color: var(--neutral-bg-1) !important;
    transition: border-color var(--duration-fast) var(--easing-standard),
                box-shadow var(--duration-fast) var(--easing-standard) !important;
    padding: 8px 12px !important;
}

div[data-testid="stTextInput"] input:focus,
textarea:focus {
    border-color: var(--brand-primary) !important;
    box-shadow: 0 0 0 2px rgba(15, 108, 189, 0.15) !important;
    outline: none !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: var(--neutral-fg-1) !important;
}

div[data-baseweb="popover"] li {
    color: var(--neutral-fg-1) !important;
}

/* ── Chat — polished conversation UI ── */
div[data-testid="stChatMessage"] {
    border-radius: var(--radius-lg) !important;
    padding: var(--space-md) var(--space-lg) !important;
    margin-bottom: var(--space-sm) !important;
    border: 1px solid var(--neutral-stroke-1) !important;
    animation: fadeSlideIn var(--duration-slow) var(--easing-decelerate);
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

div[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: var(--brand-bg) !important;
    border-color: rgba(15, 108, 189, 0.15) !important;
}

div[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: var(--neutral-bg-1) !important;
    box-shadow: var(--shadow-4);
}

div[data-testid="stChatInputContainer"] {
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--neutral-stroke-2) !important;
    box-shadow: var(--shadow-8) !important;
    transition: box-shadow var(--duration-normal) var(--easing-standard);
}

div[data-testid="stChatInputContainer"]:focus-within {
    border-color: var(--brand-primary) !important;
    box-shadow: var(--shadow-16), 0 0 0 2px rgba(15, 108, 189, 0.1) !important;
}

/* ── Alerts (Fluent semantic colors) ── */
div[data-testid="stAlert"][data-baseweb*="notification"] {
    border-radius: var(--radius-md) !important;
    border-left: 4px solid !important;
    font-size: 14px !important;
}

.stAlert div[role="alert"] {
    border-radius: var(--radius-md) !important;
}

/* ── DataFrames ── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--neutral-stroke-1) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden;
    box-shadow: var(--shadow-2);
}

/* ── Charts ── */
div[data-testid="stVegaLiteChart"] {
    background: var(--neutral-bg-1);
    border: 1px solid var(--neutral-stroke-1);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    box-shadow: var(--shadow-2);
}

/* ── Dividers — subtle ── */
hr {
    border: none !important;
    border-top: 1px solid var(--neutral-stroke-subtle) !important;
    margin: var(--space-xl) 0 !important;
}

/* ── Tabs — refined ── */
button[data-baseweb="tab"] {
    font-family: var(--font-family) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    transition: color var(--duration-fast) var(--easing-standard);
}

/* ── Download button ── */
.stDownloadButton button {
    background-color: var(--neutral-bg-1) !important;
    border: 1px solid var(--neutral-stroke-2) !important;
    color: var(--neutral-fg-1) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: all var(--duration-fast) var(--easing-standard) !important;
}

.stDownloadButton button:hover {
    background-color: var(--neutral-bg-3) !important;
    box-shadow: var(--shadow-2) !important;
    transform: translateY(-1px);
}

/* ── Spinner ── */
div[data-testid="stSpinner"] {
    color: var(--brand-primary) !important;
}

/* ── Blockquotes — elegant evidence ── */
blockquote {
    border-left: 3px solid var(--brand-primary) !important;
    background-color: var(--neutral-bg-3) !important;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
    padding: var(--space-sm) var(--space-md) !important;
    margin: var(--space-xs) 0 !important;
    color: var(--neutral-fg-2) !important;
    font-size: 13px !important;
    font-style: italic;
}

/* ── Fluent Badge ── */
.fluent-badge {
    display: inline-flex;
    align-items: center;
    font-size: 12px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: var(--radius-pill);
    margin-right: 4px;
    margin-bottom: 4px;
    letter-spacing: 0.01em;
    line-height: 1.3;
}

.fluent-badge--brand {
    background-color: var(--brand-bg);
    color: var(--brand-primary);
}

.fluent-badge--success {
    background-color: var(--status-success-bg);
    color: var(--status-success);
}

.fluent-badge--warning {
    background-color: var(--status-warning-bg);
    color: var(--status-warning);
}

.fluent-badge--danger {
    background-color: var(--status-danger-bg);
    color: var(--status-danger);
}

.fluent-badge--neutral {
    background-color: var(--neutral-bg-3);
    color: var(--neutral-fg-2);
    border: 1px solid var(--neutral-stroke-1);
}

/* ── Fluent Card ── */
.fluent-card {
    background: var(--neutral-bg-1);
    border: 1px solid var(--neutral-stroke-1);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    box-shadow: var(--shadow-4);
    margin-bottom: var(--space-md);
    transition: box-shadow var(--duration-normal) var(--easing-standard),
                transform var(--duration-normal) var(--easing-standard);
}

.fluent-card:hover {
    box-shadow: var(--shadow-8);
}

.fluent-card__title {
    font: var(--font-subtitle-2);
    color: var(--neutral-fg-1);
    margin-bottom: var(--space-xs);
}

.fluent-card__subtitle {
    font-size: 11px;
    font-weight: 700;
    color: var(--neutral-fg-3);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: var(--space-sm);
}

.fluent-card__value {
    font-size: 36px;
    font-weight: 600;
    color: var(--brand-primary);
    line-height: 1.1;
    letter-spacing: -0.02em;
}

.fluent-card__value--sm {
    font-size: 20px;
}

/* ── Hero Section — gradient with depth ── */
.fluent-hero {
    background: var(--brand-gradient);
    color: white;
    border-radius: var(--radius-xl);
    padding: var(--space-2xl) var(--space-2xl);
    margin-bottom: var(--space-lg);
    box-shadow: var(--shadow-16);
    position: relative;
    overflow: hidden;
}

.fluent-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}

.fluent-hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
}

.fluent-hero h1 {
    font-size: 36px !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: var(--space-sm) !important;
    position: relative;
    z-index: 1;
    letter-spacing: -0.02em;
}

.fluent-hero p {
    color: rgba(255,255,255,0.88);
    font-size: 16px;
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
    max-width: 680px;
}

/* ── Pipeline Funnel — polished ── */
.fluent-funnel {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.fluent-funnel__step {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md);
    background: var(--neutral-bg-1);
    border: 1px solid var(--neutral-stroke-1);
    transition: box-shadow var(--duration-fast) var(--easing-standard);
}

.fluent-funnel__step:hover {
    box-shadow: var(--shadow-2);
}

.fluent-funnel__bar {
    height: 6px;
    border-radius: var(--radius-pill);
    background: var(--brand-gradient);
    transition: width 0.6s var(--easing-decelerate);
}

.fluent-funnel__label {
    flex: 1;
    font-size: 13px;
    color: var(--neutral-fg-2);
}

.fluent-funnel__count {
    font-weight: 600;
    font-size: 14px;
    color: var(--neutral-fg-1);
    min-width: 60px;
    text-align: right;
    font-variant-numeric: tabular-nums;
}

/* ── Status indicator ── */
.fluent-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--neutral-fg-2);
}

.fluent-status__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.fluent-status__dot--green { background: var(--status-success); }
.fluent-status__dot--yellow { background: var(--status-warning); }
.fluent-status__dot--red { background: var(--status-danger); }

/* ── Methodology steps ── */
.fluent-steps {
    counter-reset: step;
}

.fluent-step {
    display: flex;
    gap: var(--space-md);
    padding: var(--space-md) 0;
    border-bottom: 1px solid var(--neutral-stroke-1);
}

.fluent-step:last-child {
    border-bottom: none;
}

.fluent-step::before {
    counter-increment: step;
    content: counter(step);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    min-width: 28px;
    border-radius: 50%;
    background: var(--brand-primary);
    color: white;
    font-size: 13px;
    font-weight: 600;
}

/* ── Radio pills (nav style) ── */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    border-radius: var(--radius-sm) !important;
    margin-bottom: 2px !important;
    padding: 10px 16px !important;
    transition: all var(--duration-fast) var(--easing-standard);
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] {
    background: var(--brand-bg) !important;
    color: var(--brand-primary) !important;
    font-weight: 600;
}

/* ── Scrollbar — subtle ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--neutral-bg-4);
    border-radius: var(--radius-pill);
}
::-webkit-scrollbar-thumb:hover { background: var(--neutral-fg-3); }

/* ── Toggle ── */
div[data-testid="stToggle"] label span {
    font-size: 14px !important;
}

/* ── Table cells in cards ── */
.fluent-card table td,
.fluent-card table th {
    color: var(--neutral-fg-1) !important;
}

/* ── Secondary buttons text color override ── */
.stButton button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    color: white !important;
}
</style>

<script>
// Detect Streamlit dark mode and apply CSS class to :root
(function() {
    function applyTheme() {
        const el = document.querySelector('[data-testid="stAppViewContainer"]');
        const bg = el ? window.getComputedStyle(el).backgroundColor : '';
        const isDark = bg && (bg.includes('14, 17, 23') || bg.includes('rgb(14') ||
                       bg.includes('rgb(0,') || bg.includes('rgb(30,') ||
                       bg.includes('rgb(17,'));
        // Also check if body has dark background
        const bodyBg = window.getComputedStyle(document.body).backgroundColor;
        const bodyDark = bodyBg && (bodyBg.includes('14, 17, 23') || bodyBg.includes('rgb(14') ||
                         bodyBg.includes('rgb(0,') || bodyBg.includes('rgb(30,'));

        if (isDark || bodyDark || window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    }
    // Run on load and observe DOM changes
    applyTheme();
    setTimeout(applyTheme, 500);
    setTimeout(applyTheme, 2000);
    const observer = new MutationObserver(applyTheme);
    observer.observe(document.body, { attributes: true, childList: true, subtree: true });
})();
</script>
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fluent_badge(text: str, variant: str = "brand") -> str:
    """Return HTML for a Fluent 2 pill badge."""
    return f'<span class="fluent-badge fluent-badge--{variant}">{text}</span>'


def fluent_card_html(label: str, value: str, subtitle: str = "") -> str:
    """Return HTML for a metric card with Fluent 2 elevation."""
    sub = f'<div class="fluent-card__subtitle">{subtitle}</div>' if subtitle else ""
    return (
        f'<div class="fluent-card">{sub}'
        f'<div class="fluent-card__title">{label}</div>'
        f'<div class="fluent-card__value">{value}</div>'
        f'</div>'
    )


def fluent_funnel_html(steps: list[tuple[str, int]], max_val: int) -> str:
    """Build a Fluent 2 funnel visualization."""
    rows = ""
    for label, count in steps:
        pct = (count / max_val * 100) if max_val else 0
        rows += (
            f'<div class="fluent-funnel__step">'
            f'<div class="fluent-funnel__label">{label}</div>'
            f'<div style="flex:2;background:var(--neutral-bg-3);border-radius:var(--radius-pill);overflow:hidden;">'
            f'<div class="fluent-funnel__bar" style="width:{pct}%"></div></div>'
            f'<div class="fluent-funnel__count">{count:,}</div>'
            f'</div>'
        )
    return f'<div class="fluent-funnel">{rows}</div>'


def confidence_badge(level: str) -> str:
    """Return a confidence-level badge."""
    level_lower = level.lower() if level else "medium"
    if "high" in level_lower:
        return fluent_badge("High confidence", "success")
    elif "low" in level_lower:
        return fluent_badge("Low confidence", "danger")
    return fluent_badge("Medium confidence", "warning")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PAGE CONFIG & THEME INJECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="Blinkit Discovery Engine",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230F6CBD'/><text x='16' y='22' font-size='18' text-anchor='middle' fill='white' font-family='Segoe UI'>B</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(FLUENT_CSS, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA LOADING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@st.cache_data
def load_data():
    df = pd.read_csv(str(config.CLEAN_OUTPUT_CSV))
    # Use pre-baked themes if present in CSV, otherwise compute
    if "Primary Theme" not in df.columns or df["Primary Theme"].isna().all():
        df = identify_themes(df)
    else:
        # Ensure Theme Confidence column exists for sorting
        if "Theme Confidence" not in df.columns:
            df["Theme Confidence"] = 1
    return df

@st.cache_data
def get_themes(_df_hash):
    df = load_data()
    return get_theme_summary(df)

@st.cache_data
def get_patterns(_df_hash):
    df = load_data()
    return get_cross_theme_patterns(df)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR — Fluent 2 Navigation Pane
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BLINKIT_LOGO_SVG = '<svg viewBox="0 0 120 28" width="120" height="28" xmlns="http://www.w3.org/2000/svg"><text x="0" y="22" font-family="Segoe UI Variable, Segoe UI, -apple-system, sans-serif" font-size="22" font-weight="800" letter-spacing="-0.5"><tspan fill="#F8C831">blinki</tspan><tspan fill="#4CAF50">t</tspan></text></svg>'

with st.sidebar:
    st.markdown(f'<div style="padding:4px 0 12px 0;"><div style="display:flex;align-items:center;gap:10px;">{BLINKIT_LOGO_SVG}<div><div style="font-weight:600;font-size:14px;color:var(--neutral-fg-1);line-height:1.2;">Discovery Engine</div><div style="font-size:11px;color:var(--neutral-fg-3);">Cross-shopping inertia analysis</div></div></div></div>', unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Insights",
            "AI Chatbot",
            "Workflow \u2014 How It Works",
        ],
        label_visibility="collapsed",
    )

# Load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("No cleaned data found. Run `python main.py` first to generate the output CSV.")
    st.stop()




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TAB 1 — INSIGHTS (Dashboard + Themes + Search + Validation)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if page == "Insights":
    # Hero banner
    st.markdown(
        f'<div class="fluent-hero"><h1>Insights</h1>'
        f'<p>{len(df):,} cleaned reviews from multi-channel sources, filtered through a 3-stage pipeline. Explore cross-shopping friction patterns below.</p></div>',
        unsafe_allow_html=True,
    )

    # ── Key Metrics ──
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total reviews", f"{len(df):,}")
    c2.metric("Categories", df["Target Category"].nunique())
    c3.metric("Friction pillars", df["Friction Pillar"].nunique())
    c4.metric("Themes", df["Primary Theme"].nunique())
    c5.metric("Sources", df["Source"].nunique())

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Key Findings (Top 5 Themes — compact cards) ──
    st.markdown("##### Key findings")
    st.caption("Top friction themes surfaced from cross-shopping inertia signals.")

    themes = get_theme_summary(df)
    top_themes = themes[:5]

    for theme in top_themes:
        pct = theme["percentage"]
        theme_name = theme["theme"]
        # Color coding: green for positive, gray for neutral, severity-based for friction
        if theme_name == "Positive Experience":
            badge_variant = "success"
        elif theme_name == "Neutral / No Signal":
            badge_variant = "neutral"
        else:
            badge_variant = "danger" if pct > 20 else ("warning" if pct > 10 else "brand")

        # Category pills
        top_cats = sorted(theme["categories"].items(), key=lambda x: -x[1])[:4]
        cat_pills = " ".join(fluent_badge(cat, "neutral") for cat, _ in top_cats)

        # Top 2 quotes
        quotes_html = ""
        for q in theme["representative_quotes"][:2]:
            q_truncated = q[:150] + ("..." if len(q) > 150 else "")
            quotes_html += f'<div style="font-size:12px;color:var(--neutral-fg-2);font-style:italic;margin-top:6px;border-left:2px solid var(--brand-primary);padding-left:8px;">&ldquo;{q_truncated}&rdquo;</div>'

        card_html = (
            '<div class="fluent-card" style="padding:var(--space-md) var(--space-lg);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">'
            f'<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">{theme["theme"]}</div>'
            f'<div>{fluent_badge(str(pct) + "% of reviews", badge_variant)} {fluent_badge(str(theme["count"]) + " reviews", "neutral")}</div>'
            f'</div>'
            f'<div style="margin-bottom:8px;">{cat_pills}</div>'
            f'{quotes_html}'
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Review Explorer ──
    st.markdown("##### Review explorer")
    st.caption("Filter, search, and browse cleaned review data.")

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        cat_filter = st.multiselect("Category", options=sorted(df["Target Category"].dropna().unique()), default=[])
    with fc2:
        pillar_filter = st.multiselect("Friction pillar", options=sorted(df["Friction Pillar"].dropna().unique()), default=[])
    with fc3:
        theme_filter = st.multiselect("Theme", options=sorted(df["Primary Theme"].dropna().unique()), default=[])

    search_text = st.text_input("Search reviews", placeholder="e.g., fake earbuds warranty")

    # Apply filters
    filtered = df.copy()
    if cat_filter:
        filtered = filtered[filtered["Target Category"].isin(cat_filter)]
    if pillar_filter:
        filtered = filtered[filtered["Friction Pillar"].isin(pillar_filter)]
    if theme_filter:
        filtered = filtered[filtered["Primary Theme"].isin(theme_filter)]
    if search_text:
        filtered = filtered[filtered["Raw Content"].str.contains(search_text, case=False, na=False)]

    st.markdown(
        f"**{len(filtered):,} reviews** matching filters "
        + (" ".join(fluent_badge(c, "brand") for c in cat_filter) if cat_filter else ""),
        unsafe_allow_html=True,
    )

    display_cols = ["Target Category", "Friction Pillar", "Primary Theme", "Raw Content", "Source"]
    st.dataframe(
        filtered[display_cols].head(100),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Raw Content": st.column_config.TextColumn("Review", width="large"),
            "Target Category": st.column_config.TextColumn("Category"),
            "Friction Pillar": st.column_config.TextColumn("Pillar"),
            "Primary Theme": st.column_config.TextColumn("Theme"),
        },
    )

    csv_data = filtered[display_cols].to_csv(index=False)
    st.download_button("Download filtered data", csv_data, "filtered_reviews.csv", "text/csv")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Source & Pipeline (2-column) ──
    col_src, col_pipe = st.columns(2)

    with col_src:
        st.markdown("##### Source distribution")
        source_counts = df["Source"].value_counts()
        badges_html = " ".join(
            fluent_badge(f"{src} ({cnt})", "brand" if "Reddit" in str(src) else "neutral")
            for src, cnt in source_counts.head(6).items()
        )
        st.markdown(badges_html, unsafe_allow_html=True)
        st.bar_chart(source_counts.head(10), horizontal=True, color="#0F6CBD")

    with col_pipe:
        st.markdown("##### Data pipeline funnel")
        funnel_steps = [
            ("Raw input (CSVs + Reddit + Play Store)", 29478),
            ("After deduplication", 28274),
            ("Stage 1: Transactional noise filter", 27589),
            ("Stage 2: Rating & praise filter", 26680),
            ("Stage 3: Category isolation", len(df)),
        ]
        st.markdown(fluent_funnel_html(funnel_steps, funnel_steps[0][1]), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TAB 2 — AI CHATBOT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "AI Chatbot":
    st.markdown("## AI Chatbot")

    # Initialize chatbot
    if "chatbot" not in st.session_state:
        faiss_index, faiss_meta = None, None
        try:
            from engine import load_index
            faiss_index, faiss_meta = load_index()
        except Exception:
            pass
        st.session_state.chatbot = RAGChatbot(df, faiss_index, faiss_meta)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    bot = st.session_state.chatbot

    # Sidebar controls for chatbot
    with st.sidebar:
        st.divider()

        # Mode indicator
        mode_dot = "green" if "Full" in bot.mode_label else ("yellow" if "AI" in bot.mode_label or "FAISS" in bot.mode_label else "red")
        st.markdown(
            f'<div class="fluent-status"><span class="fluent-status__dot fluent-status__dot--{mode_dot}"></span> {bot.mode_label}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown(
            f'<div style="font-size:12px;color:var(--neutral-fg-3);">'
            f'<div style="margin-bottom:4px"><strong>Pipeline stats</strong></div>'
            f'<div>Clean: {len(df):,} reviews</div>'
            f'<div>Categories: {df["Target Category"].nunique()}</div>'
            f'<div>Sources: {df["Source"].nunique()}</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        brief_mode = st.toggle("Brief answers", value=False, help="Toggle between brief and detailed responses")

        if st.session_state.chat_messages:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("Clear chat", use_container_width=True):
                    st.session_state.chat_messages.clear()
                    bot.clear_history()
                    st.rerun()
            with cc2:
                export_text = bot.export_history()
                st.download_button(
                    "Export",
                    export_text,
                    file_name="blinkit_chat_export.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    # Welcome message
    if not st.session_state.chat_messages:
        st.markdown(
            f'<div class="fluent-card" style="border-left:4px solid var(--brand-primary);">'
            f'<div class="fluent-card__title">Welcome to the Discovery Engine</div>'
            f'<div style="font-size:14px;line-height:1.7;color:var(--neutral-fg-2);">'
            f'I analyze <strong>{len(df):,} user reviews</strong> across '
            f'<strong>{df["Target Category"].nunique()} non-grocery categories</strong> '
            f'to surface friction patterns and user insights.<br><br>'
            f'<strong>Try asking:</strong><br>'
            f'&bull; What are the top frustrations with electronics on Blinkit?<br>'
            f'&bull; Why don\'t users explore new categories?<br>'
            f'&bull; What do users say about beauty product authenticity?<br>'
            f'&bull; Which friction pillar has the highest impact?<br><br>'
            f'<span style="color:var(--status-warning);font-size:12px;">'
            f'Data-backed analysis only &mdash; no buying advice, platform comparisons, or recommendations.'
            f'</span></div></div>',
            unsafe_allow_html=True,
        )

    # Suggested questions
    with st.expander("Suggested questions for evaluators", expanded=False):
        suggestions = [
            "Why do users repeatedly buy from the same categories?",
            "What prevents users from exploring new categories?",
            "How do users discover products today?",
            "What role do habits play in shopping behavior?",
            "What information do users need before trying a new category?",
            "What frustrations emerge repeatedly?",
            "Which user segments are more likely to experiment?",
            "What unmet needs emerge consistently across discussions?",
        ]
        for s in suggestions:
            if st.button(s, key=f"suggest_{hash(s)}", use_container_width=True):
                st.session_state._pending_question = s

    # Chat history display
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("meta"):
                meta = msg["meta"]
                conf = meta.get("confidence", {})
                if conf.get("emoji"):
                    st.caption(f"{conf['emoji']} {conf.get('description', '')}")

                if meta.get("thin_warning"):
                    st.warning(meta["thin_warning"])

                if meta.get("contradiction_note"):
                    st.info(meta["contradiction_note"])

                with st.expander(f"Evidence details \u2014 {meta['evidence_count']} reviews retrieved", expanded=False):
                    badges = (
                        fluent_badge(meta["mode"], "brand")
                        + " ".join(fluent_badge(s, "neutral") for s in meta.get("sources_used", []))
                    )
                    st.markdown(badges, unsafe_allow_html=True)
                    st.markdown(f"**Categories:** {', '.join(meta.get('categories_in_evidence', []))}")
                    st.markdown(f"**Retrieval:** {'FAISS semantic search' if bot.has_faiss else 'Keyword overlap'}")

                if meta.get("follow_ups"):
                    st.markdown("**Suggested follow-ups**")
                    for fu in meta["follow_ups"]:
                        if st.button(f"\u00a0\u00a0{fu}", key=f"fu_{hash(fu)}_{hash(msg['content'][:20])}"):
                            st.session_state._pending_question = fu

    # Chat input
    pending = st.session_state.pop("_pending_question", None)
    user_input = st.chat_input("Ask a question about Blinkit cross-shopping data...")
    question = pending or user_input

    if question:
        st.session_state.chat_messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner(f"Searching {len(df):,} reviews..."):
                result = bot.ask(question, top_k=15, brief=brief_mode)

            st.markdown(result["answer"])

            conf = result.get("confidence", {})
            if conf.get("emoji"):
                st.caption(f"{conf['emoji']} {conf.get('description', '')}")

            if result.get("thin_warning"):
                st.warning(result["thin_warning"])

            if result.get("contradiction_note"):
                st.info(result["contradiction_note"])

            with st.expander(f"Evidence details \u2014 {result['evidence_count']} reviews retrieved", expanded=False):
                badges = (
                    fluent_badge(result["mode"], "brand")
                    + " ".join(fluent_badge(s, "neutral") for s in result.get("sources_used", []))
                )
                st.markdown(badges, unsafe_allow_html=True)
                st.markdown(f"**Categories:** {', '.join(result.get('categories_in_evidence', []))}")
                st.markdown(f"**Retrieval:** {'FAISS semantic search' if bot.has_faiss else 'Keyword overlap'}")

            if result.get("follow_ups") and not result.get("was_refused"):
                st.markdown("**Suggested follow-ups**")
                for fu in result["follow_ups"]:
                    if st.button(f"\u00a0\u00a0{fu}", key=f"fu_new_{hash(fu)}"):
                        st.session_state._pending_question = fu

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": result["answer"],
            "meta": {
                "evidence_count": result["evidence_count"],
                "mode": result["mode"],
                "sources_used": result.get("sources_used", []),
                "categories_in_evidence": result.get("categories_in_evidence", []),
                "confidence": result.get("confidence", {}),
                "thin_warning": result.get("thin_warning"),
                "contradiction_note": result.get("contradiction_note"),
                "follow_ups": result.get("follow_ups", []),
            },
        })


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TAB 3 — WORKFLOW — HOW IT WORKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "Workflow \u2014 How It Works":
    st.markdown("## Workflow \u2014 How It Works")
    st.caption("End-to-end pipeline from raw data sources to AI-powered insights.")

    # ── Animated Pipeline Flow ──
    PIPELINE_FLOW_HTML = (
        '<div style="display:flex;flex-direction:column;gap:0;align-items:center;margin:24px 0;">'
        # Node 1
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.3s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F4E5</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">Data Sources</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">Play Store \u2022 App Store \u2022 Reddit \u2022 YouTube \u2022 HackerNews \u2022 PissedConsumer</div>'
        '<div style="margin-top:6px;">' + fluent_badge("29,478 raw items", "neutral") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 2
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.4s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F504</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">Ingestion & Deduplication</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">Merge CSVs, normalize fields, remove exact duplicates</div>'
        '<div style="margin-top:6px;">' + fluent_badge("28,274 unique", "brand") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 3
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.5s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F6AB</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">Stage 1: Transactional Noise</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">Remove delivery/logistics/app-crash complaints</div>'
        '<div style="margin-top:6px;">' + fluent_badge("27,589 remain", "brand") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 4
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.6s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\u2B50</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">Stage 2: Rating & Praise Filter</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">Remove generic 5-star praise without friction signal</div>'
        '<div style="margin-top:6px;">' + fluent_badge("26,680 remain", "warning") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 5
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.7s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F3AF</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">Stage 3: Category Isolation</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">Keep only non-grocery cross-shopping friction mentions</div>'
        '<div style="margin-top:6px;">' + fluent_badge(f"{len(df):,} final reviews", "success") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 6
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.8s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F3F7\uFE0F</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">Classification & Theming</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">Assign Target Category, Friction Pillar, Primary Theme</div>'
        '<div style="margin-top:6px;">' + fluent_badge(f"{df['Target Category'].nunique()} categories", "neutral") + " " + fluent_badge(f"{df['Friction Pillar'].nunique()} pillars", "neutral") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 7
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);animation:fadeSlideIn 0.9s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F9E0</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">FAISS Vector Index</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">all-MiniLM-L6-v2 embeddings (384 dims) for semantic search</div>'
        '<div style="margin-top:6px;">' + fluent_badge(f"{len(df):,} vectors indexed", "brand") + '</div>'
        '</div>'
        '<div style="font-size:20px;color:var(--neutral-fg-3);margin:4px 0;">\u2193</div>'
        # Node 8
        '<div class="fluent-card" style="width:100%;max-width:600px;text-align:center;padding:var(--space-md);border-left:4px solid var(--brand-primary);animation:fadeSlideIn 1.0s ease-out;">'
        '<div style="font-size:24px;margin-bottom:4px;">\U0001F916</div>'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);">AI Chatbot (Groq Llama 3.3 70B)</div>'
        '<div style="font-size:12px;color:var(--neutral-fg-3);">RAG-powered Q&A with guardrails, confidence scoring, evidence grounding</div>'
        '<div style="margin-top:6px;">' + fluent_badge("Semantic + Keyword retrieval", "success") + '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(PIPELINE_FLOW_HTML, unsafe_allow_html=True)

    st.divider()

    # ── Detailed Stage Descriptions (expandable) ──
    st.markdown("##### Stage details")

    with st.expander("Data ingestion architecture", expanded=False):
        st.markdown(
            '<div class="fluent-card">'
            '<table style="width:100%;font-size:14px;border-collapse:collapse;">'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;font-weight:600;">Pathway</td>'
            '<td style="padding:8px 12px;font-weight:600;">Source</td>'
            '<td style="padding:8px 12px;font-weight:600;">Method</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;"><span class="fluent-badge fluent-badge--brand">A: Live</span></td>'
            '<td style="padding:8px 12px;">Play Store + App Store</td>'
            '<td style="padding:8px 12px;">Programmatic API scraping</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;"><span class="fluent-badge fluent-badge--neutral">B: Historical</span></td>'
            '<td style="padding:8px 12px;">Play Store, App Store, Reddit, YouTube, HackerNews, PissedConsumer</td>'
            '<td style="padding:8px 12px;">Pre-collected CSV dumps</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;"><span class="fluent-badge fluent-badge--success">B: Curated</span></td>'
            '<td style="padding:8px 12px;">32 Reddit thread URLs</td>'
            '<td style="padding:8px 12px;">Playwright browser scraping (1,243 items)</td></tr>'
            '<tr>'
            '<td style="padding:8px 12px;"><span class="fluent-badge fluent-badge--warning">B: Expert</span></td>'
            '<td style="padding:8px 12px;">19 pre-classified Reddit threads</td>'
            '<td style="padding:8px 12px;">Expert-labeled categories + friction pillars</td></tr>'
            '</table></div>',
            unsafe_allow_html=True,
        )

    with st.expander("Theme identification methodology", expanded=False):
        st.markdown("""**Two complementary approaches:**

1. **Rule-based theme detection** (offline, deterministic) \u2014 10 predefined theme patterns with regex keyword lists. Each review matched against all patterns; highest-match theme assigned.

2. **AI-powered semantic clustering** (Groq + local embeddings) \u2014 Reviews embedded via `all-MiniLM-L6-v2` (384 dims). FAISS index enables semantic search. Groq Llama 3.3 70B generates structured theme analysis grounded in evidence.""")

    with st.expander("Validation framework", expanded=False):
        st.markdown(
            '<div class="fluent-card">'
            '<table style="width:100%;font-size:14px;border-collapse:collapse;">'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;font-weight:600;">Method</td>'
            '<td style="padding:8px 12px;font-weight:600;">Description</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;">Data quality gate</td>'
            '<td style="padding:8px 12px;">3-stage filter removes logistics noise, 5-star praise, and grocery complaints</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;">Source triangulation</td>'
            '<td style="padding:8px 12px;">Reviews from 7+ channels \u2014 same patterns across sources = higher confidence</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;">Quote grounding</td>'
            '<td style="padding:8px 12px;">Every theme cites verbatim user quotes \u2014 no unsubstantiated claims</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;">Confidence scoring</td>'
            '<td style="padding:8px 12px;">Each insight rated high / medium / low based on evidence density</td></tr>'
            '<tr style="border-bottom:1px solid var(--neutral-stroke-1);">'
            '<td style="padding:8px 12px;">Evidence gap disclosure</td>'
            '<td style="padding:8px 12px;">Explicitly states what data is missing to strengthen each finding</td></tr>'
            '<tr>'
            '<td style="padding:8px 12px;">Cross-pattern validation</td>'
            '<td style="padding:8px 12px;">Theme x Category matrix reveals category-specific vs systemic patterns</td></tr>'
            '</table></div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── GitHub Actions Status & Link ──
    st.markdown("##### CI/CD Pipeline")

    github_actions_html = (
        '<div class="fluent-card" style="display:flex;align-items:center;gap:var(--space-lg);">'
        '<div style="flex:1;">'
        '<div style="font:var(--font-subtitle-2);color:var(--neutral-fg-1);margin-bottom:4px;">GitHub Actions</div>'
        '<div style="font-size:13px;color:var(--neutral-fg-2);">Automated data pipeline runs on schedule and push events. Includes scraping, filtering, embedding, and index rebuilding.</div>'
        '</div>'
        '<a href="https://github.com/HimanshiBhambhani/Grad-Project/actions" target="_blank" '
        'style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;'
        'background:var(--brand-primary);color:white;border-radius:var(--radius-sm);'
        'text-decoration:none;font-size:14px;font-weight:600;white-space:nowrap;">'
        '\u2192 View on GitHub Actions</a>'
        '</div>'
    )
    st.markdown(github_actions_html, unsafe_allow_html=True)

    # Pipeline stats footer
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("##### Pipeline statistics")
    ps1, ps2 = st.columns(2)
    with ps1:
        st.markdown(f"""- **Raw input rows:** 29,478
- **After dedup:** 28,274
- **Stage 1 (noise):** 27,589
- **Stage 2 (rating):** 26,680
- **Stage 3 (category):** {len(df):,}""")
    with ps2:
        st.markdown(f"""- **Source channels:** {df['Source'].nunique()}
- **Categories:** {df['Target Category'].nunique()}
- **Friction pillars:** {df['Friction Pillar'].nunique()}
- **Themes identified:** {df['Primary Theme'].nunique()}
- **Retention rate:** {len(df)/28274*100:.1f}%""")
