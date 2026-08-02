"""
engine/themes.py — Theme classification for review corpus.

Primary method: embedding similarity (all-MiniLM-L6-v2) against theme anchor
sentences — same model used for FAISS / relevance filtering.

Fallback: regex keyword matching if the embedding model cannot load.
"""

import logging
import os
import re

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

NEUTRAL_THEME = "Neutral / No Signal"
EMBED_MODEL = "all-MiniLM-L6-v2"
# Minimum cosine similarity to assign a theme (else Neutral)
MIN_THEME_SIMILARITY = 0.32

# ─────────────────── Semantic theme anchors (for embeddings) ───────────────────

THEME_ANCHORS: dict[str, list[str]] = {
    "Positive Experience": [
        "Blinkit delivered quickly and the product worked well, I am happy and would order again.",
        "Great experience buying electronics or personal care on Blinkit, lifesaver for urgent needs.",
        "Satisfied with product quality and fast delivery, recommend Blinkit for this category.",
    ],
    "Counterfeit / Fake Products": [
        "Received a fake or counterfeit product, not genuine or original packaging.",
        "Duplicate or first-copy item sold as branded product on quick commerce.",
        "Product seemed tampered or not authentic despite showing a known brand name.",
    ],
    "Warranty & Return Anxiety": [
        "Worried about warranty, return policy, exchange, or no refund on electronics.",
        "Return or replacement was denied, non-returnable item, refund pending or cancelled.",
        "No return option on the app and afraid to buy expensive items without guarantee.",
    ],
    "Dark Store Storage Concerns": [
        "Product arrived expired, damaged packaging, heat exposure, or poor storage conditions.",
        "Seal was broken, tampered box, or product looked like it sat in a dark store too long.",
        "Skincare or food item packaging looked wrong, cheap repack, or suspicious condition.",
    ],
    "Price & Value Concerns": [
        "Blinkit feels overpriced, expensive compared to market, bad value for money on MRP.",
        "Pack size too small or price too high for what you get on quick commerce.",
        "Would compare prices elsewhere before buying non-grocery on Blinkit.",
    ],
    "Category Unawareness": [
        "Did not know Blinkit sells electronics, beauty, or pet products beyond groceries.",
        "Never saw these categories in the app, poor visibility of non-grocery assortment.",
        "Had no idea Blinkit had this category until someone told me.",
    ],
    "Search & Navigation Friction": [
        "Cannot find the category or product in search, hidden or hard to navigate in the app.",
        "Search does not show what I need, category buried in the Blinkit interface.",
    ],
    "Grocery-Only Habit Lock": [
        "I only use Blinkit for groceries and never explore other categories.",
        "Habit of ordering the same grocery items, never tried non-grocery on Blinkit.",
    ],
    "Customer Support Failures": [
        "Customer support was useless, chatbot loops, no response, agents ghosted my complaint.",
        "Had to contact support multiple times with no resolution, escalation went nowhere.",
        "Support closed ticket without helping, unhelpful customer care experience.",
    ],
    "Product Quality Issues": [
        "Product was defective, broken, faulty, or stopped working soon after delivery.",
        "Low quality item, not working as expected, bad build or performance.",
        "Received wrong or damaged product that does not function properly.",
    ],
    "Trust & Brand Verification": [
        "Unsure if product is trustworthy, want verified brand or authenticity checks.",
        "Need trust signals before buying, worried about brand legitimacy on quick commerce.",
        "Would buy if known brand and clear verification, hesitant without proof of authenticity.",
    ],
}

# Back-compat alias used in older docs / CSV exports
THEME_ALIASES = {
    "Price Premium vs Alternatives": "Price & Value Concerns",
}

# ─────────────────── Regex fallback (legacy) ───────────────────

THEME_PATTERNS = {
    "Positive Experience": [
        r"\blifesaver\b", r"\bthank\w*\b", r"\bappreciat\w*\b",
        r"\blove\s*blinkit\b", r"\bgreat\s*service\b", r"\bsaved\b",
        r"\bimpressed\b", r"\bhappy\b", r"\bexcellent\b", r"\brecommend\b",
        r"\brelief\b", r"\bkudos\b", r"\bamazing\s*(service|delivery|app)\b",
        r"\bbest\s*(service|delivery|app|experience)\b", r"\bgrateful\b",
        r"\bsatisfied\b", r"\bsuperb\b", r"\bwonderful\b", r"\bfantastic\b",
    ],
    "Counterfeit / Fake Products": [
        r"\bfake\b", r"\bcounterfeit\b", r"\bduplicate\b", r"\bnot\s*original\b",
        r"\bnot\s*genuine\b", r"\bfirst\s*copy\b",
    ],
    "Warranty & Return Anxiety": [
        r"\bwarranty\b", r"\breturn\b", r"\bno\s*return\b", r"\bexchange\b",
        r"\bnon[\s-]*returnable\b", r"\brefund\s*denied\b", r"\bno\s*replacement\b",
    ],
    "Dark Store Storage Concerns": [
        r"\bstorage\b", r"\bdark\s*store\b", r"\bexpir\w*\b", r"\btampered\b",
        r"\bseal\s*broken\b", r"\bpackag\w*\s*(damaged|open|wrong)\b",
    ],
    "Price & Value Concerns": [
        r"\bexpensive\b", r"\boverpriced\b", r"\bcheaper\b", r"\bprice\b",
        r"\bMRP\b", r"\bcostl\w*\b", r"\bvalue\s*for\s*money\b",
    ],
    "Category Unawareness": [
        r"\bdidn'?t\s*know\b", r"\bhad\s*no\s*idea\b", r"\bnever\s*knew\b",
        r"\bnot\s*aware\b", r"\bdidn'?t\s*realize\b",
    ],
    "Search & Navigation Friction": [
        r"\bcan'?t\s*find\b", r"\bsearch\b", r"\bhidden\b", r"\bnot\s*visible\b",
        r"\bhard\s*to\s*find\b", r"\bwhere\s*is\b",
    ],
    "Grocery-Only Habit Lock": [
        r"\bonly\s*(use|buy|order)\b.*\bgrocery\b", r"\bjust\s*for\s*grocery\b",
    ],
    "Customer Support Failures": [
        r"\bsupport\b", r"\bcustomer\s*care\b", r"\bcustomer\s*service\b",
        r"\bbot\b", r"\bno\s*response\b", r"\bunhelpful\b", r"\bescalat\w*\b",
    ],
    "Product Quality Issues": [
        r"\bdefective\b", r"\bbroken\b", r"\bnot\s*working\b",
        r"\bfaulty\b", r"\blow\s*quality\b", r"\bbad\s*quality\b",
    ],
    "Trust & Brand Verification": [
        r"\btrust\b", r"\bauthentic\w*\b", r"\bverif\w*\b", r"\blegit\b",
        r"\boriginal\b", r"\bknown\s*brand\b",
    ],
}

_COMPILED_THEMES = {
    name: [re.compile(p, re.IGNORECASE) for p in patterns]
    for name, patterns in THEME_PATTERNS.items()
}

_STRONG_NEGATIVE = re.compile(
    r"\b("
    r"worst|terrible|pathetic|disappoint|scam|fraud|cheated|harassment|"
    r"never\s+again|waste\s+of\s+money|refund\s+denied|not\s+working|"
    r"broken|defective|faulty|fake|counterfeit|denied|ghosted|"
    r"kharab|bekar|bakwas|nakli|loot"
    r")\b",
    re.IGNORECASE,
)

_WEAK_POSITIVE = re.compile(
    r"\b("
    r"fantastic|excellent|love|amazing|lifesaver|happy|satisfied|recommend|"
    r"great\s+(app|service|experience|delivery)"
    r")\b",
    re.IGNORECASE,
)


def _text_column(df: pd.DataFrame) -> str:
    if "Raw Content" in df.columns:
        return "Raw Content"
    if "text" in df.columns:
        return "text"
    raise ValueError("DataFrame needs 'Raw Content' or 'text' column")


def _normalize_theme_name(name: str) -> str:
    return THEME_ALIASES.get(name, name)


def _apply_theme_guards(text: str, theme: str, ranked: list[tuple[str, float]]) -> tuple[str, float]:
    """Block obvious mislabels (e.g. negative review tagged Positive)."""
    if theme == "Positive Experience":
        if _STRONG_NEGATIVE.search(text):
            for alt_theme, alt_score in ranked[1:]:
                if alt_theme != "Positive Experience":
                    return alt_theme, alt_score
            return NEUTRAL_THEME, 0.0
        if not _WEAK_POSITIVE.search(text):
            for alt_theme, alt_score in ranked[1:]:
                if alt_theme != "Positive Experience" and alt_score >= MIN_THEME_SIMILARITY:
                    return alt_theme, alt_score
            return NEUTRAL_THEME, 0.0
    return theme, ranked[0][1] if ranked else 0.0


def _load_embed_model():
    try:
        import truststore
        truststore.inject_into_ssl()
    except Exception:
        pass
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    from sentence_transformers import SentenceTransformer

    try:
        return SentenceTransformer(EMBED_MODEL, local_files_only=True)
    except Exception:
        logger.info("Embedding model not cached locally; downloading %s...", EMBED_MODEL)
        return SentenceTransformer(EMBED_MODEL)


def _build_theme_anchor_matrix(model):
    """Returns theme_names list (one per anchor row) and normalized anchor embeddings."""
    theme_names: list[str] = []
    anchor_texts: list[str] = []
    for theme, anchors in THEME_ANCHORS.items():
        for anchor in anchors:
            theme_names.append(theme)
            anchor_texts.append(anchor)

    embeddings = model.encode(
        anchor_texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    )
    return theme_names, np.array(embeddings, dtype="float32")


def _rank_themes_for_text(
    text: str,
    review_embedding: np.ndarray,
    theme_names: list[str],
    anchor_embeddings: np.ndarray,
) -> list[tuple[str, float]]:
    """Max cosine similarity per theme (embedding already normalized)."""
    sims = review_embedding @ anchor_embeddings.T
    per_theme: dict[str, float] = {}
    for idx, theme in enumerate(theme_names):
        score = float(sims[idx])
        per_theme[theme] = max(per_theme.get(theme, 0.0), score)
    ranked = sorted(per_theme.items(), key=lambda x: x[1], reverse=True)
    return ranked


def identify_themes_embedding(df: pd.DataFrame) -> pd.DataFrame:
    """Classify themes using semantic similarity to anchor sentences."""
    col = _text_column(df)
    texts = df[col].astype(str).tolist()
    logger.info("Identifying themes (embedding) across %d reviews...", len(texts))

    model = _load_embed_model()
    theme_names, anchor_embeddings = _build_theme_anchor_matrix(model)
    review_embeddings = model.encode(
        [t[:2000] for t in texts],
        normalize_embeddings=True,
        batch_size=128,
        show_progress_bar=len(texts) > 200,
    )

    assignments = []
    for text, emb in zip(texts, review_embeddings):
        ranked = _rank_themes_for_text(text, emb, theme_names, anchor_embeddings)
        theme, score = ranked[0] if ranked else (NEUTRAL_THEME, 0.0)
        theme, score = _apply_theme_guards(text, theme, ranked)
        if score < MIN_THEME_SIMILARITY:
            theme = NEUTRAL_THEME
            score = 0.0
        assignments.append({
            "primary_theme": theme,
            "theme_confidence": round(score, 3),
            "theme_method": "embedding",
        })

    out = df.copy()
    meta = pd.DataFrame(assignments)
    out["Primary Theme"] = meta["primary_theme"].values
    out["Theme Confidence"] = meta["theme_confidence"].values
    out["Theme Method"] = meta["theme_method"].values

    _log_theme_distribution(out)
    return out


def identify_themes_regex(df: pd.DataFrame) -> pd.DataFrame:
    """Legacy regex classifier — fallback only."""
    col = _text_column(df)
    logger.info("Identifying themes (regex fallback) across %d reviews...", len(df))

    assignments = []
    for text in df[col].astype(str):
        matched = []
        for theme_name, patterns in _COMPILED_THEMES.items():
            hits = sum(1 for p in patterns if p.search(text))
            if hits:
                matched.append((theme_name, hits))
        matched.sort(key=lambda x: x[1], reverse=True)

        if matched:
            theme, conf = matched[0][0], matched[0][1] / 10.0
            ranked = [(t, c / 10.0) for t, c in matched]
            theme, conf = _apply_theme_guards(text, theme, ranked)
            assignments.append({
                "primary_theme": theme,
                "theme_confidence": conf,
                "theme_method": "regex",
            })
        else:
            assignments.append({
                "primary_theme": NEUTRAL_THEME,
                "theme_confidence": 0.0,
                "theme_method": "regex",
            })

    out = df.copy()
    meta = pd.DataFrame(assignments)
    out["Primary Theme"] = meta["primary_theme"].values
    out["Theme Confidence"] = meta["theme_confidence"].values
    out["Theme Method"] = meta["theme_method"].values
    _log_theme_distribution(out)
    return out


def identify_themes(df: pd.DataFrame, method: str = "embedding") -> pd.DataFrame:
    """
    Assign Primary Theme to each review.

    Args:
        method: 'embedding' (default) or 'regex'
    """
    if method == "regex":
        return identify_themes_regex(df)
    try:
        return identify_themes_embedding(df)
    except Exception as exc:
        logger.warning("Embedding theme classification failed (%s); using regex.", exc)
        return identify_themes_regex(df)


def _log_theme_distribution(df: pd.DataFrame) -> None:
    theme_counts = df["Primary Theme"].value_counts()
    logger.info("Theme distribution:")
    for theme, count in theme_counts.items():
        logger.info("  %-35s %d", theme, count)


def get_theme_summary(df: pd.DataFrame) -> list[dict]:
    """Generate theme summaries with representative quotes."""
    if "Primary Theme" not in df.columns:
        df = identify_themes(df)

    summaries = []
    for theme in df["Primary Theme"].unique():
        theme_df = df[df["Primary Theme"] == theme]
        categories = theme_df["Target Category"].value_counts().to_dict()
        pillars = theme_df.get("Friction Pillar", pd.Series(dtype=str)).value_counts().to_dict()
        top_rows = theme_df.nlargest(3, "Theme Confidence")
        col = _text_column(theme_df)
        quotes = top_rows[col].str[:250].tolist()

        summaries.append({
            "theme": theme,
            "count": len(theme_df),
            "percentage": round(len(theme_df) / len(df) * 100, 1),
            "categories": categories,
            "pillars": pillars,
            "representative_quotes": quotes,
        })

    summaries.sort(key=lambda x: x["count"], reverse=True)
    return summaries


def get_cross_theme_patterns(df: pd.DataFrame) -> dict:
    """Theme co-occurrence by category and friction pillar."""
    if "Primary Theme" not in df.columns:
        df = identify_themes(df)

    patterns: dict = {
        "theme_by_category": {},
        "theme_by_pillar": {},
        "category_theme_matrix": {},
    }

    for cat in df["Target Category"].unique():
        cat_df = df[df["Target Category"] == cat]
        patterns["theme_by_category"][cat] = cat_df["Primary Theme"].value_counts().to_dict()

    if "Friction Pillar" in df.columns:
        for pillar in df["Friction Pillar"].unique():
            pillar_df = df[df["Friction Pillar"] == pillar]
            patterns["theme_by_pillar"][pillar] = pillar_df["Primary Theme"].value_counts().to_dict()

    return patterns
