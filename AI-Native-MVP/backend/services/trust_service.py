"""Load corpora at startup and expose trust lookups for API routes."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pandas as pd

from engine.trust_engine import (
    build_category_trust,
    build_product_trust,
    find_product,
    list_categories,
    list_products,
    load_corpora,
)

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DEFAULT_CORPUS_A = DATA_DIR / "friction_corpus.csv"
DEFAULT_CORPUS_B = DATA_DIR / "mvp_trust_corpus.csv"

_df_a: pd.DataFrame | None = None
_df_b: pd.DataFrame | None = None


def corpus_paths() -> tuple[Path, Path]:
    """Return configured paths for CORPUS A and B."""
    a = Path(os.getenv("CORPUS_A_PATH", DEFAULT_CORPUS_A))
    b = Path(os.getenv("CORPUS_B_PATH", DEFAULT_CORPUS_B))
    return a, b


def init_corpora() -> None:
    """Load both corpora into memory (call once at app startup)."""
    global _df_a, _df_b
    path_a, path_b = corpus_paths()
    if not path_a.exists():
        raise FileNotFoundError(f"CORPUS A not found: {path_a}")
    if not path_b.exists():
        raise FileNotFoundError(f"CORPUS B not found: {path_b}")
    _df_a, _df_b = load_corpora(path_a, path_b)
    logger.info(
        "Corpora loaded: A=%d rows, B=%d rows",
        len(_df_a),
        len(_df_b),
    )


def _frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    if _df_a is None or _df_b is None:
        init_corpora()
    assert _df_a is not None and _df_b is not None
    return _df_a, _df_b


def get_category(slug: str) -> dict | None:
    """Category trust payload or None if slug unknown."""
    if slug not in list_categories():
        return None
    df_a, df_b = _frames()
    return build_category_trust(df_a, df_b, slug)


def get_product(product_id: str) -> dict | None:
    """Full product trust payload or None if id unknown."""
    found = find_product(product_id)
    if found is None:
        return None
    product, category = found
    df_a, df_b = _frames()
    return build_product_trust(df_a, df_b, product, category)


def list_products_for_category(category: str) -> list[dict] | None:
    """Product cards for category page, or None if category unknown."""
    if category not in list_categories():
        return None
    df_a, df_b = _frames()
    cards: list[dict] = []
    for product in list_products(category):
        trust = build_product_trust(df_a, df_b, product, category)
        cards.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "brand": product["brand"],
                "price": product["price"],
                "emoji": product.get("emoji", "📦"),
                "category": category,
                "keep_rate": trust["keep_rate"],
                "badge": trust["badge"],
                "trust_score": trust["trust_score"],
            }
        )
    return cards


def list_all_categories() -> list[dict]:
    """Home page category list with trust scores."""
    df_a, df_b = _frames()
    return [build_category_trust(df_a, df_b, slug) for slug in list_categories()]
