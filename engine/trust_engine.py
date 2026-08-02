"""
engine/trust_engine.py — Buy Smart trust scores from review corpus.

Scores are computed from the friction-focused review dataset (not Blinkit internal data).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

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
    "boat", "jbl", "apple", "samsung", "boat", "noise", "realme", "oneplus",
    "sandisk", "loreal", "lakme", "maybelline", "cerave", "minimalist",
}

# Demo catalog — simulated Blinkit listings (not live API)
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
            "name": "JBL GO 3 Portable Speaker",
            "brand": "jbl",
            "price": 2799,
            "replacement_days": 7,
            "warranty": "1 year manufacturer warranty",
            "emoji": "🔊",
        },
        {
            "id": "apple-earpods",
            "name": "Apple EarPods (USB-C)",
            "brand": "apple",
            "price": 1799,
            "replacement_days": 7,
            "warranty": "1 year Apple warranty",
            "emoji": "🎵",
        },
        {
            "id": "realme-buds",
            "name": "realme Buds T300",
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
            "name": "CeraVe Moisturizing Cream",
            "brand": "cerave",
            "price": 349,
            "replacement_days": 3,
            "warranty": "Check seal — no warranty on opened personal care",
            "emoji": "🧴",
        },
        {
            "id": "minimalist-serum",
            "name": "Minimalist 10% Niacinamide Serum",
            "brand": "minimalist",
            "price": 599,
            "replacement_days": 3,
            "warranty": "Verify batch code on package",
            "emoji": "💧",
        },
    ],
}

CATEGORY_LABELS = {
    "electronics": "Electronics",
    "personal_care_beauty": "Beauty & Personal Care",
    "pharmacy_health": "Pharmacy & Health",
}


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
    buy_smart_conditions: list[str] = field(default_factory=lambda: [
        "Known brand",
        "Under ₹2,000",
        "Urgent need today",
    ])


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


def _clamp(score: float, lo: int = 12, hi: int = 92) -> int:
    return int(max(lo, min(hi, round(score))))


def _score_from_subset(subset: pd.DataFrame) -> tuple[int, float, float]:
    n = len(subset)
    if n == 0:
        return 50, 0.0, 0.0
    pos = (subset["Primary Theme"] == POSITIVE_THEME).sum()
    neg = subset["Primary Theme"].isin(NEGATIVE_THEMES).sum()
    pos_pct = pos / n
    neg_pct = neg / n
    # Complaint corpus baseline ~38 for electronics; scale from theme ratios
    score = 50 + (pos_pct * 35) - (neg_pct * 55)
    return _clamp(score), round(pos_pct * 100, 1), round(neg_pct * 100, 1)


def get_category_trust(df: pd.DataFrame, category: str) -> CategoryTrust:
    subset = df[df["Target Category"] == category]
    overall, pos_pct, neg_pct = _score_from_subset(subset)

    # Buy-smart path: boost for known-brand + low-ticket urgent use case
    buy_smart = _clamp(overall + 22 + (5 if category == "electronics" else 0))
    if buy_smart > 88:
        buy_smart = 88

    top_risk = "Mixed signals"
    if len(subset) > 0:
        neg_subset = subset[subset["Primary Theme"].isin(NEGATIVE_THEMES)]
        if len(neg_subset) > 0:
            top_risk = neg_subset["Primary Theme"].value_counts().index[0]

    return CategoryTrust(
        category=category,
        label=CATEGORY_LABELS.get(category, category.replace("_", " ").title()),
        overall_score=overall,
        buy_smart_score=buy_smart,
        review_count=len(subset),
        positive_pct=pos_pct,
        negative_pct=neg_pct,
        top_risk=top_risk,
    )


def _brand_reviews(df: pd.DataFrame, brand: str, category: str | None = None) -> pd.DataFrame:
    pattern = re.compile(re.escape(brand), re.IGNORECASE)
    col = "Raw Content" if "Raw Content" in df.columns else "text"
    mask = df[col].astype(str).str.contains(pattern, na=False)
    subset = df[mask]
    if category:
        subset = subset[subset["Target Category"] == category]
    return subset


def compute_keep_rate(subset: pd.DataFrame) -> tuple[int | None, int]:
    """
    Proxy for 'users keep this product' from public review sentiment.
    Returns (rate 0-100, mention_count).
    """
    n = len(subset)
    if n == 0:
        return None, 0
    neg = subset["Primary Theme"].isin(NEGATIVE_THEMES).sum()
    pos = subset["Primary Theme"] == POSITIVE_THEME
    # Positive + non-negative themes count as favorable mentions
    favorable = (pos | ~subset["Primary Theme"].isin(NEGATIVE_THEMES)).sum()
    rate = _clamp(100 * favorable / n, lo=35, hi=85)
    return rate, n


def get_product_trust(df: pd.DataFrame, product: dict, category: str) -> ProductTrust:
    brand = product["brand"]
    subset = _brand_reviews(df, brand, category)
    score, _, _ = _score_from_subset(subset)

    # Known brand boost on product page
    if brand.lower() in KNOWN_BRANDS:
        score = _clamp(score + 18)

    keep_rate, mentions = compute_keep_rate(subset)
    if keep_rate is None:
        # Fall back to category-level favorable rate
        cat = get_category_trust(df, category)
        keep_rate = _clamp(100 - cat.negative_pct, lo=45, hi=72)
        mentions = 0
        evidence = f"Category-level estimate ({cat.review_count} reviews)"
    else:
        evidence = f"{mentions} public review mentions analyzed"

    # Blend mention sentiment when we have enough brand-specific evidence
    if mentions >= 3 and keep_rate is not None:
        score = _clamp(max(score, int(keep_rate * 0.88)))

    tips = _build_tips(subset, brand)

    if score >= 70:
        verdict = "Safe buy"
    elif score >= 55:
        verdict = "Okay with caution"
    else:
        verdict = "High risk — skip unless urgent"

    return ProductTrust(
        product_id=product["id"],
        name=product["name"],
        brand=brand,
        price=product["price"],
        replacement_days=product["replacement_days"],
        warranty=product["warranty"],
        emoji=product.get("emoji", "📦"),
        category=category,
        score=score,
        keep_rate=keep_rate,
        mention_count=mentions,
        verdict=verdict,
        tips=tips,
        evidence_label=evidence,
    )


def _build_tips(subset: pd.DataFrame, brand: str) -> list[str]:
    tips: list[str] = []

    if brand.lower() in KNOWN_BRANDS:
        tips.append("Known brand — lower counterfeit risk on Blinkit")

    if len(subset) == 0:
        tips.extend([
            "Record a full unboxing video before opening sealed packaging",
            "Keep invoice screenshot until return window ends",
        ])
        return tips

    theme_counts = subset["Primary Theme"].value_counts()
    top = theme_counts.index.tolist()[:3]

    if "Warranty & Return Anxiety" in top or "Customer Support Failures" in top:
        tips.append("Record unboxing video — helps if you need a return")
    if "Counterfeit / Fake Products" in top or "Dark Store Storage Concerns" in top:
        tips.append("Check seal and MRP sticker at delivery — refuse if tampered")
    if "Product Quality Issues" in top:
        tips.append("Test immediately on delivery — report defects within 24 hours")
    if POSITIVE_THEME in top:
        tips.append("Most mentions in our data are favorable for urgent buys")

    if not tips:
        tips.append("Stick to sealed products from recognizable brands")
        tips.append("Record unboxing video — helps if you need a return")

    return tips[:4]


def list_categories() -> list[str]:
    return list(PRODUCT_CATALOG.keys())


def list_products(category: str) -> list[dict]:
    return PRODUCT_CATALOG.get(category, [])
