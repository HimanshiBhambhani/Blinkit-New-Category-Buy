#!/usr/bin/env python3
"""
Build CORPUS B — positive Play Store reviews for Buy Smart MVP.

Scrapes 4–5★ Blinkit reviews (+ historical 4–5★ dumps), runs the
Data-Extraction cleaning pipeline (skip Stage 2), offline classification,
and embedding theme assignment. Supplements with favorable expansion
rows from friction_corpus.csv (read-only) to reach target row count.

Writes to data/mvp_trust_corpus.csv only — never touches
friction_corpus.csv or Data-Extraction/Output/blinkit_clean_data.csv.

Usage:
    cd AI-Native-MVP
    python scripts/build_mvp_corpus.py
    python scripts/build_mvp_corpus.py --max-positive 200 --min-rows 100
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

MVP_ROOT = Path(__file__).resolve().parents[1]
DATA_EXTRACTION = MVP_ROOT.parent / "Data-Extraction"
MVP_OUTPUT = MVP_ROOT / "data" / "mvp_trust_corpus.csv"
FRICTION_CORPUS = MVP_ROOT / "data" / "friction_corpus.csv"
DISCOVERY_CHECK = DATA_EXTRACTION / "Output" / "blinkit_clean_data.csv"

MVP_OUTPUT_COLUMNS = [
    "Source",
    "Platform",
    "Target Category",
    "Friction Pillar",
    "Raw Content",
    "Opportunity",
    "Primary Theme",
    "Theme Confidence",
    "Theme Method",
]

FAVORABLE_THEMES = {"Positive Experience", "Trust & Brand Verification"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("build_mvp_corpus")


def _ensure_data_extraction_on_path() -> None:
    root = str(DATA_EXTRACTION)
    if root not in sys.path:
        sys.path.insert(0, root)


def _map_source_labels(df: pd.DataFrame, config) -> pd.DataFrame:
    df = df.copy()
    df["Source"] = df["source_raw"].map(config.SOURCE_LABELS).fillna("")
    reddit_mask = df["source_raw"].str.startswith("reddit_", na=False) & (
        df["Source"] == ""
    )
    df.loc[reddit_mask, "Source"] = "Reddit"
    df["Source"] = df["Source"].replace("", "Historical Dump")
    if "_preclassified_source_label" in df.columns:
        mask = df["_preclassified_source_label"].str.len() > 0
        df.loc[mask, "Source"] = df.loc[mask, "_preclassified_source_label"]
    return df


def _finalize_scrape_rows(df: pd.DataFrame, config, identify_themes) -> pd.DataFrame:
    df = _map_source_labels(df, config)
    df["Platform"] = config.PLATFORM
    df["Raw Content"] = df["text"]
    df = identify_themes(df)
    output = df[MVP_OUTPUT_COLUMNS].copy()
    output = output.fillna("")
    output = output[output["Raw Content"].str.len() > 10]
    return output.reset_index(drop=True)


def _load_positive_sources(max_positive: int):
    from ingestion import load_all_historical
    from scrapers.playstore import scrape_playstore_positive

    live = scrape_playstore_positive(max_per_star=max_positive)
    live = live.copy()
    live["category"] = ""

    historical = load_all_historical()
    ratings = pd.to_numeric(historical["rating"], errors="coerce")
    hist_pos = historical[ratings >= 4].copy()
    if "category" not in hist_pos.columns:
        hist_pos["category"] = ""

    combined = pd.concat([live, hist_pos], ignore_index=True)
    combined = combined.drop_duplicates(subset=["text"], keep="first")
    logger.info(
        "Positive sources: %d live + historical 4–5★ → %d unique texts.",
        len(live),
        len(combined),
    )
    return combined


def _build_scrape_tiers(combined: pd.DataFrame, run_cleaning_pipeline, classify_dataframe_offline, _infer_category, config):
    """Tier 1: skip Stage 2, keep Stage 3+4. Tier 2: skip Stage 2+3, keep expansion rows."""
    tier1 = run_cleaning_pipeline(combined, skip_stage2=True)
    seen = set(tier1["text"].astype(str))

    remainder = combined[~combined["text"].astype(str).isin(seen)]
    tier2 = run_cleaning_pipeline(
        remainder,
        skip_stage2=True,
        skip_stage3=True,
    )
    if not tier2.empty:
        tier2 = classify_dataframe_offline(tier2)
        tier2["Target Category"] = tier2["text"].apply(
            lambda t: _infer_category(str(t))
        )
        keep = set(config.KEEP_CATEGORIES)
        tier2 = tier2[tier2["Target Category"].isin(keep)].copy()
        logger.info("Tier 2 (expansion recovery): %d rows.", len(tier2))

    scrape_df = pd.concat([tier1, tier2], ignore_index=True)
    scrape_df = scrape_df.drop_duplicates(subset=["text"], keep="first")
    logger.info("Scrape tiers combined: %d rows.", len(scrape_df))
    return scrape_df


def _load_favorable_supplement(existing_texts: set[str]) -> pd.DataFrame:
    """Read-only favorable expansion rows from CORPUS A (never writes back)."""
    if not FRICTION_CORPUS.exists():
        logger.warning("friction_corpus.csv missing — skipping supplement.")
        return pd.DataFrame(columns=MVP_OUTPUT_COLUMNS)

    friction = pd.read_csv(FRICTION_CORPUS)
    keep = {
        "electronics",
        "personal_care_beauty",
        "pet",
        "baby",
        "home_cleaning",
        "intimate_personal",
        "pharmacy_health",
    }
    fav = friction[
        friction["Target Category"].isin(keep)
        & (
            friction["Primary Theme"].isin(FAVORABLE_THEMES)
            | (friction["Friction Pillar"] == "Positive Experience")
        )
    ].copy()
    fav = fav[~fav["Raw Content"].astype(str).isin(existing_texts)]

    for col in MVP_OUTPUT_COLUMNS:
        if col not in fav.columns:
            fav[col] = ""

    supplement = fav[MVP_OUTPUT_COLUMNS].copy()
    logger.info("Favorable supplement from friction corpus: %d rows.", len(supplement))
    return supplement


def _verify_friction_unchanged(before_rows: int) -> None:
    for path in (FRICTION_CORPUS, DISCOVERY_CHECK):
        if not path.exists():
            logger.warning("Check file missing: %s", path)
            continue
        rows = len(pd.read_csv(path))
        if rows != before_rows:
            raise RuntimeError(
                f"{path.name} row count changed ({before_rows} → {rows})"
            )
    logger.info(
        "Verified friction + Discovery CSVs unchanged (%d rows each).",
        before_rows,
    )


def build_mvp_corpus(max_positive: int = 200, min_rows: int = 100) -> pd.DataFrame:
    _ensure_data_extraction_on_path()

    import config
    from engine.themes import identify_themes
    from pipeline.classifier import classify_dataframe_offline, _infer_category
    from pipeline.filters import run_cleaning_pipeline

    friction_rows = (
        len(pd.read_csv(FRICTION_CORPUS)) if FRICTION_CORPUS.exists() else 0
    )

    logger.info("=" * 70)
    logger.info("CORPUS B — positive reviews (max %d per star)", max_positive)
    logger.info("=" * 70)

    combined = _load_positive_sources(max_positive)
    scrape_df = _build_scrape_tiers(
        combined,
        run_cleaning_pipeline,
        classify_dataframe_offline,
        _infer_category,
        config,
    )
    if scrape_df.empty:
        raise RuntimeError("Scrape pipeline produced no rows.")

    classified = classify_dataframe_offline(scrape_df)
    scrape_out = _finalize_scrape_rows(classified, config, identify_themes)

    existing = set(scrape_out["Raw Content"].astype(str))
    supplement = _load_favorable_supplement(existing)
    output = pd.concat([scrape_out, supplement], ignore_index=True)
    output = output.drop_duplicates(subset=["Raw Content"], keep="first")

    MVP_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(MVP_OUTPUT, index=False)
    logger.info("Saved CORPUS B: %s (%d rows)", MVP_OUTPUT, len(output))

    _verify_friction_unchanged(friction_rows)

    logger.info("")
    logger.info("Category distribution:")
    for cat, count in output["Target Category"].value_counts().head(10).items():
        logger.info("  %-25s %d", cat, count)
    logger.info("")
    logger.info("Primary Theme distribution:")
    for theme, count in output["Primary Theme"].value_counts().head(10).items():
        logger.info("  %-35s %d", theme, count)

    if len(output) < min_rows:
        raise RuntimeError(
            f"CORPUS B has {len(output)} rows (expected ≥{min_rows}). "
            "Try --max-positive 500 or inspect scrape filters."
        )

    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build CORPUS B (mvp_trust_corpus.csv) for Buy Smart MVP"
    )
    parser.add_argument(
        "--max-positive",
        type=int,
        default=200,
        help="Max 4/5-star reviews per star rating (default: 200)",
    )
    parser.add_argument(
        "--min-rows",
        type=int,
        default=100,
        help="Minimum output rows required (default: 100)",
    )
    args = parser.parse_args()

    output = build_mvp_corpus(
        max_positive=args.max_positive,
        min_rows=args.min_rows,
    )
    logger.info("Done — CORPUS B ready with %d rows.", len(output))


if __name__ == "__main__":
    main()
