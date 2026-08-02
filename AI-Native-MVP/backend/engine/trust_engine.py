"""
backend/engine/trust_engine.py — Buy Smart trust scores (dual corpus).

CORPUS A (friction): risks, tips, keep-rate proxy, top concerns.
CORPUS B (positive): favorable leg for trust score + positive mentions %.

Phase 8A: category vs product scores, confidence tiers, analysis_meta.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

NEGATIVE_THEMES = {
    "Warranty & Return Anxiety",
    "Counterfeit / Fake Products",
    "Product Quality Issues",
    "Customer Support Failures",
    "Dark Store Storage Concerns",
}

POSITIVE_THEME = "Positive Experience"

KNOWN_BRANDS = {
    "boat",
    "jbl",
    "apple",
    "samsung",
    "noise",
    "realme",
    "oneplus",
    "sandisk",
    "loreal",
    "lakme",
    "maybelline",
    "cerave",
    "minimalist",
}

PRODUCT_CATALOG: dict[str, list[dict]] = {
    "electronics": [
        {
            "id": "boat-airdopes-141",
            "name": "boAt Airdopes 141",
            "brand": "boat",
            "price": 1299,
            "replacement_days": 7,
            "warranty": "1 year manufacturer warranty",
            "emoji": "🎧",
        },
        {
            "id": "jbl-go-3",
            "name": "JBL Go 3 Portable Bluetooth Speaker",
            "brand": "jbl",
            "price": 2969,
            "replacement_days": 7,
            "warranty": "1 year manufacturer warranty",
            "emoji": "🔊",
        },
        {
            "id": "apple-earpods",
            "name": "Apple EarPods (USB-C)",
            "brand": "apple",
            "price": 1649,
            "replacement_days": 7,
            "warranty": "1 year Apple warranty",
            "emoji": "🎵",
        },
        {
            "id": "realme-buds",
            "name": "realme Buds T310 TWS Earbuds",
            "brand": "realme",
            "price": 2199,
            "replacement_days": 7,
            "warranty": "1 year manufacturer warranty",
            "emoji": "🎧",
        },
    ],
    "personal_care_beauty": [
        {
            "id": "cerave-moisturizer",
            "name": "CeraVe Moisturizing Cream (with Ceramides)",
            "brand": "cerave",
            "price": 422,
            "replacement_days": 3,
            "warranty": "Check seal — no warranty on opened personal care",
            "emoji": "🧴",
        },
        {
            "id": "minimalist-serum",
            "name": "Minimalist Niacinamide 10% Face Serum",
            "brand": "minimalist",
            "price": 570,
            "replacement_days": 3,
            "warranty": "Verify batch code on package",
            "emoji": "💧",
        },
    ],
}

# Product-specific keywords for evidence snippets (exact-SKU matching).
PRODUCT_EVIDENCE_TERMS: dict[str, list[str]] = {
    "boat-airdopes-141": ["airdopes", "141"],
    "jbl-go-3": ["jbl go", "go 3", "go3"],
    "apple-earpods": ["earpod", "earpods"],
    "realme-buds": ["t310", "realme bud", "buds t310"],
    "cerave-moisturizer": ["cerave", "moisturizing cream", "moisturiz"],
    "minimalist-serum": ["minimalist", "niacinamide", "serum"],
}

BLINKIT_SOURCES = {"Play Store", "Historical Dump"}

CATEGORY_LABELS = {
    "electronics": "Electronics",
    "personal_care_beauty": "Beauty & Personal Care",
    "pharmacy_health": "Pharmacy & Health",
}

BANNED_BADGE_PHRASES = (
    "not a safe buy",
    "skip",
    "don't buy",
    "use amazon",
)


@dataclass
class CategoryTrust:
    category: str
    label: str
    overall_score: int
    buy_smart_score: int
    review_count: int
    positive_pct: float
    negative_pct: float
    top_risk: str
    buy_smart_conditions: list[str] = field(
        default_factory=lambda: [
            "Known brand",
            "Under ₹2,000",
            "Known brand under ₹2,000",
        ]
    )


@dataclass
class ProductTrust:
    product_id: str
    name: str
    brand: str
    price: int
    replacement_days: int
    warranty: str
    emoji: str
    category: str
    score: int
    keep_rate: int | None
    mention_count: int
    verdict: str
    tips: list[str]
    evidence_label: str


def load_corpora(
    path_a: str | Path | None = None,
    path_b: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load CORPUS A (friction) and CORPUS B (positive) CSVs."""
    if path_a is None or path_b is None:
        data_dir = Path(__file__).resolve().parents[2] / "data"
        path_a = path_a or data_dir / "friction_corpus.csv"
        path_b = path_b or data_dir / "mvp_trust_corpus.csv"
    return pd.read_csv(path_a), pd.read_csv(path_b)


def _clamp(score: float, lo: int = 12, hi: int = 92) -> int:
    return int(max(lo, min(hi, round(score))))


def _text_column(df: pd.DataFrame) -> str:
    if "Raw Content" in df.columns:
        return "Raw Content"
    if "text" in df.columns:
        return "text"
    return df.columns[0]


def confidence_tier(mentions: int) -> str:
    """High / medium / low from brand mention count in CORPUS A."""
    if mentions >= 10:
        return "high"
    if mentions >= 3:
        return "medium"
    return "low"


def _score_from_subset(subset: pd.DataFrame) -> tuple[int, float, float]:
    n = len(subset)
    if n == 0:
        return 50, 0.0, 0.0
    pos = (subset["Primary Theme"] == POSITIVE_THEME).sum()
    neg = subset["Primary Theme"].isin(NEGATIVE_THEMES).sum()
    pos_pct = pos / n
    neg_pct = neg / n
    score = 50 + (pos_pct * 35) - (neg_pct * 55)
    return _clamp(score), round(pos_pct * 100, 1), round(neg_pct * 100, 1)


def compute_trust_score(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    category: str,
) -> int:
    """Category Trust Score — 60% favorable B, 40% risk A."""
    sub_a = df_a[df_a["Target Category"] == category]
    sub_b = df_b[df_b["Target Category"] == category]
    _, pos_b, _ = _score_from_subset(sub_b)
    _, _, neg_a = _score_from_subset(sub_a)
    favorable_b = pos_b / 100.0
    risk_a = neg_a / 100.0
    raw = 50 + (0.6 * favorable_b * 35) - (0.4 * risk_a * 55)
    return _clamp(raw)


def compute_product_delta(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    brand: str,
    category: str,
    price: int,
) -> int:
    """
    Product Confidence Adjustment ∈ [-12, +12] from brand signals, price band,
    mention volume, and favorable/negative theme mix.
    """
    delta = 0
    subset_a = _brand_reviews(df_a, brand, category)
    mentions = len(subset_a)

    if brand.lower() in KNOWN_BRANDS:
        delta += 3
    if price <= 2000:
        delta += 2
    elif price > 5000:
        delta -= 2

    if mentions >= 10:
        delta += 3
    elif mentions >= 3:
        delta += 1
    elif mentions == 0:
        delta -= 3
    else:
        delta -= 1

    pos_pct = positive_mentions_pct(df_b, brand, category)
    if pos_pct >= 55:
        delta += 2
    elif pos_pct < 35:
        delta -= 2

    if mentions > 0:
        neg = subset_a["Primary Theme"].isin(NEGATIVE_THEMES).sum()
        if neg / mentions > 0.5:
            delta -= 3

    return max(-12, min(12, delta))


def _brand_reviews(
    df: pd.DataFrame,
    brand: str,
    category: str | None = None,
) -> pd.DataFrame:
    pattern = re.compile(re.escape(brand), re.IGNORECASE)
    col = _text_column(df)
    mask = df[col].astype(str).str.contains(pattern, na=False)
    subset = df[mask]
    if category:
        subset = subset[subset["Target Category"] == category]
    return subset


def compute_keep_rate(subset: pd.DataFrame) -> tuple[int | None, int]:
    """
    Review proxy for 'users keep this product' from public review sentiment.
    Returns (rate 0-100, mention_count).
    """
    n = len(subset)
    if n == 0:
        return None, 0
    pos = subset["Primary Theme"] == POSITIVE_THEME
    favorable = (pos | ~subset["Primary Theme"].isin(NEGATIVE_THEMES)).sum()
    rate = _clamp(100 * favorable / n, lo=35, hi=85)
    return rate, n


def _category_favorable_rate_b(df_b: pd.DataFrame, category: str) -> int:
    subset = df_b[df_b["Target Category"] == category]
    if len(subset) == 0:
        subset = df_b
    _, pos_pct, _ = _score_from_subset(subset)
    return _clamp(pos_pct, lo=45, hi=72)


def resolve_keep_rate(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    brand: str,
    category: str,
) -> tuple[int, int, str]:
    """Keep rate proxy with fallback tiers: ≥3 / 1–2 / 0 brand mentions."""
    subset = _brand_reviews(df_a, brand, category)
    rate, mentions = compute_keep_rate(subset)

    if mentions >= 3 and rate is not None:
        return rate, mentions, f"Keep-rate proxy from {mentions} public review mentions"

    if mentions >= 1:
        cat_subset = df_a[df_a["Target Category"] == category]
        cat_rate, _ = compute_keep_rate(cat_subset)
        if cat_rate is None:
            cat_rate = _category_favorable_rate_b(df_b, category)
        return cat_rate, mentions, f"Category keep-rate proxy ({mentions} brand mentions)"

    cat_rate = _category_favorable_rate_b(df_b, category)
    return cat_rate, 0, "Category keep-rate proxy (no brand-specific mentions)"


def positive_mentions_pct(
    df_b: pd.DataFrame,
    brand: str,
    category: str,
) -> float:
    subset = _brand_reviews(df_b, brand, category)
    if len(subset) == 0:
        subset = df_b[df_b["Target Category"] == category]
    if len(subset) == 0:
        subset = df_b
    pos = (subset["Primary Theme"] == POSITIVE_THEME).sum()
    return round(100 * pos / max(len(subset), 1), 1)


def compute_badge(
    price: int,
    brand: str,
    product_trust: int,
    keep_rate: int,
    confidence: str,
) -> str:
    known = brand.lower() in KNOWN_BRANDS
    if confidence == "low":
        badge = "Category estimate · See how →"
    elif (
        price <= 2000
        and known
        and product_trust >= 55
        and keep_rate >= 70
    ):
        badge = "Safe to repeat · See how →"
    elif price <= 5000:
        badge = "Verify warranty · See how →"
    else:
        badge = "Check return policy · See how →"

    lower = badge.lower()
    for phrase in BANNED_BADGE_PHRASES:
        if phrase in lower:
            raise ValueError(f"Badge must not contain discouraging copy: {phrase!r}")
    return badge


def _top_concern(subset_a: pd.DataFrame) -> str:
    if len(subset_a) == 0:
        return "Mixed signals"
    neg = subset_a[subset_a["Primary Theme"].isin(NEGATIVE_THEMES)]
    if len(neg) == 0:
        return "Mixed signals"
    return neg["Primary Theme"].value_counts().index[0]


def _verdict(trust_score: int) -> str:
    if trust_score >= 70:
        return "Safe buy"
    if trust_score >= 55:
        return "Okay with caution"
    return "Buy with checks — see warranty"


def _product_search_terms(product: dict) -> list[str]:
    terms = PRODUCT_EVIDENCE_TERMS.get(product["id"], [])
    if terms:
        return terms
    # Fallback: distinctive tokens from catalog name (skip generic words).
    skip = {"with", "and", "the", "for", "usb-c", "unit", "black", "blue"}
    tokens = re.findall(r"[a-z0-9]+", product["name"].lower())
    return [t for t in tokens if len(t) > 3 and t not in skip][:4]


def _is_blinkit_context(row: pd.Series) -> bool:
    text = str(row.get("Raw Content", row.get("text", ""))).lower()
    if "blinkit" in text:
        return True
    if str(row.get("Platform", "")).strip().lower() == "blinkit":
        return True
    if str(row.get("Source", "")).strip() == "Play Store":
        return True
    return False


def _is_positive_review(row: pd.Series) -> bool:
    theme = str(row.get("Primary Theme", ""))
    pillar = str(row.get("Friction Pillar", ""))
    if theme in NEGATIVE_THEMES:
        return False
    return theme == POSITIVE_THEME or pillar == "Positive Experience"


def _product_evidence_rows(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    product: dict,
    category: str,
) -> pd.DataFrame:
    """Positive, product-specific, Blinkit-context reviews only."""
    brand = product["brand"]
    terms = _product_search_terms(product)
    brand_pat = re.compile(re.escape(brand), re.IGNORECASE)
    term_pats = [re.compile(re.escape(t), re.IGNORECASE) for t in terms]

    frames = []
    for df in (df_b, df_a):
        if df.empty:
            continue
        col = _text_column(df)
        subset = df[df["Target Category"] == category].copy()
        text_series = subset[col].astype(str)
        brand_mask = text_series.str.contains(brand_pat, na=False)
        if term_pats:
            term_mask = text_series.apply(
                lambda t: any(p.search(t) for p in term_pats)
            )
        else:
            term_mask = True
        subset = subset[brand_mask & term_mask]
        subset = subset[subset.apply(_is_positive_review, axis=1)]
        subset = subset[subset.apply(_is_blinkit_context, axis=1)]
        if len(subset) > 0:
            frames.append(subset)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    if combined.empty:
        return combined
    col = _text_column(combined)
    return combined.drop_duplicates(subset=[col], keep="first")


def theme_breakdown(subset: pd.DataFrame, limit: int = 5) -> list[dict]:
    """Deprecated for customer UI — kept for internal/debug use only."""
    if len(subset) == 0 or "Primary Theme" not in subset.columns:
        return []
    counts = subset["Primary Theme"].value_counts().head(limit)
    return [{"theme": str(theme), "count": int(count)} for theme, count in counts.items()]


def review_snippets(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    product: dict,
    category: str,
    limit: int = 2,
) -> list[dict]:
    """Positive, product-specific Blinkit review excerpts only."""
    pool = _product_evidence_rows(df_a, df_b, product, category)
    if len(pool) == 0:
        return []

    col = _text_column(pool)
    snippets: list[dict] = []
    for _, row in pool.head(limit * 3).iterrows():
        text = str(row[col]).strip()
        if len(text) < 20:
            continue
        snippets.append(
            {
                "text": text[:280] + ("…" if len(text) > 280 else ""),
                "source": str(row.get("Source", "Blinkit review")),
            }
        )
        if len(snippets) >= limit:
            break
    return snippets


def build_analysis_meta(
    brand: str,
    category: str,
    mentions: int,
    confidence: str,
) -> dict:
    signal = "brand" if mentions >= 3 else "category"
    return {
        "signal_level": signal,
        "mentions": mentions,
        "confidence": confidence,
        "data_source": "public_reviews",
        "is_simulated_catalog": True,
        "category": category,
        "brand": brand,
    }


def get_category_trust(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    category: str,
) -> CategoryTrust:
    sub_a = df_a[df_a["Target Category"] == category]
    sub_b = df_b[df_b["Target Category"] == category]
    overall = compute_trust_score(df_a, df_b, category)
    _, pos_pct, neg_pct = _score_from_subset(sub_a)
    buy_smart = _clamp(overall + 12)

    return CategoryTrust(
        category=category,
        label=CATEGORY_LABELS.get(category, category.replace("_", " ").title()),
        overall_score=overall,
        buy_smart_score=buy_smart,
        review_count=len(sub_a) + len(sub_b),
        positive_pct=pos_pct,
        negative_pct=neg_pct,
        top_risk=_top_concern(sub_a),
    )


def build_category_trust(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    category: str,
) -> dict:
    """API-shaped category trust payload."""
    cat = get_category_trust(df_a, df_b, category)
    sub_a = df_a[df_a["Target Category"] == category]
    sub_b = df_b[df_b["Target Category"] == category]
    n_a, n_b = len(sub_a), len(sub_b)
    return {
        "category": cat.category,
        "label": cat.label,
        "trust_score": cat.overall_score,
        "category_trust_score": cat.overall_score,
        "review_count": cat.review_count,
        "reviews_analysed": n_a + n_b,
        "corpus_a_count": n_a,
        "corpus_b_count": n_b,
        "guidance": "Start repeat habits with known brands under ₹2k",
        "top_concern": cat.top_risk,
        "analysis_note": (
            f"Category-level score from {n_a} friction (CORPUS A) + "
            f"{n_b} favorable (CORPUS B) reviews"
        ),
    }


def get_product_trust(
    df_a: pd.DataFrame,
    product: dict,
    category: str,
) -> ProductTrust:
    """Tips and brand-level mention counts from CORPUS A (friction)."""
    brand = product["brand"]
    subset = _brand_reviews(df_a, brand, category)
    _, mentions = compute_keep_rate(subset)
    tips = _build_tips(subset, brand)

    return ProductTrust(
        product_id=product["id"],
        name=product["name"],
        brand=brand,
        price=product["price"],
        replacement_days=product["replacement_days"],
        warranty=product["warranty"],
        emoji=product.get("emoji", "📦"),
        category=category,
        score=0,
        keep_rate=None,
        mention_count=mentions,
        verdict="",
        tips=tips,
        evidence_label="",
    )


def build_product_trust(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    product: dict,
    category: str,
) -> dict:
    """Unified product response — category + product scores, confidence, evidence."""
    brand = product["brand"]
    category_score = compute_trust_score(df_a, df_b, category)
    delta = compute_product_delta(df_a, df_b, brand, category, product["price"])
    product_score = _clamp(category_score + delta)

    pt = get_product_trust(df_a, product, category)
    keep_rate, mention_count, evidence_label = resolve_keep_rate(
        df_a, df_b, brand, category
    )
    confidence = confidence_tier(mention_count)
    sub_a = df_a[df_a["Target Category"] == category]

    analysis_meta = build_analysis_meta(brand, category, mention_count, confidence)
    snippets = review_snippets(df_a, df_b, product, category)

    payload = {
        "product_id": product["id"],
        "name": product["name"],
        "brand": brand,
        "price": product["price"],
        "category": category,
        "replacement_days": product["replacement_days"],
        "warranty": product["warranty"],
        "emoji": product.get("emoji", "📦"),
        "category_trust_score": category_score,
        "product_delta": delta,
        "trust_score": product_score,
        "keep_rate": keep_rate,
        "keep_rate_label": "Review-sentiment proxy (not Blinkit repurchase)",
        "positive_pct": positive_mentions_pct(df_b, brand, category),
        "mention_count": mention_count,
        "badge": compute_badge(
            product["price"], brand, product_score, keep_rate, confidence
        ),
        "tips": pt.tips,
        "top_concern": _top_concern(sub_a),
        "verdict": _verdict(product_score),
        "evidence_label": evidence_label,
        "analysis_meta": analysis_meta,
        "snippets": snippets,
        "snippets_note": (
            "Positive Blinkit reviews that mention this exact product."
            if snippets
            else (
                "No product-specific positive Blinkit reviews in our public corpus yet. "
                "Trust score uses category and brand signals instead."
            )
        ),
    }

    if confidence != "low":
        payload["display_n"] = mention_count

    return payload


def _build_tips(subset: pd.DataFrame, brand: str) -> list[str]:
    tips: list[str] = []

    if brand.lower() in KNOWN_BRANDS:
        tips.append("Known brand — lower counterfeit risk on Blinkit")

    if len(subset) == 0:
        tips.extend(
            [
                "Record a full unboxing video before opening sealed packaging",
                "Keep invoice screenshot until return window ends",
            ]
        )
        return tips

    theme_counts = subset["Primary Theme"].value_counts()
    top = theme_counts.index.tolist()[:3]

    if "Warranty & Return Anxiety" in top or "Customer Support Failures" in top:
        n = int(theme_counts.get("Warranty & Return Anxiety", 0) + theme_counts.get("Customer Support Failures", 0))
        tips.append(f"Record unboxing video — {n} mentions cite return/support friction")
    if "Counterfeit / Fake Products" in top or "Dark Store Storage Concerns" in top:
        n = int(theme_counts.get("Counterfeit / Fake Products", 0) + theme_counts.get("Dark Store Storage Concerns", 0))
        tips.append(f"Check seal at delivery — {n} mentions cite authenticity/storage")
    if "Product Quality Issues" in top:
        n = int(theme_counts.get("Product Quality Issues", 0))
        tips.append(f"Test on delivery — {n} mentions cite quality issues")
    if POSITIVE_THEME in top:
        n = int(theme_counts.get(POSITIVE_THEME, 0))
        tips.append(f"Favorable repeat-buy signals in {n} mentions for this brand")

    if not tips:
        tips.append("Stick to sealed products from recognizable brands")
        tips.append("Record unboxing video — helps if you need a return")

    return tips[:4]


def find_product(product_id: str) -> tuple[dict, str] | None:
    """Return (product dict, category slug) for a catalog id."""
    for category, products in PRODUCT_CATALOG.items():
        for product in products:
            if product["id"] == product_id:
                return product, category
    return None


def list_categories() -> list[str]:
    return list(PRODUCT_CATALOG.keys())


def list_products(category: str) -> list[dict]:
    return PRODUCT_CATALOG.get(category, [])
