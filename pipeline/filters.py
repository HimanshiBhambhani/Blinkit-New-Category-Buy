"""
pipeline/filters.py — Three-stage cleaning & noise interception pipeline.

Stage 1: Transactional Noise Filter (blacklisted logistics tokens)
Stage 2: Low-Star / High-Friction Focus (drop 5-star praise)
Stage 3: Vertical Category Isolation (keep only expansion categories)
"""

import logging
import re

import numpy as np
import pandas as pd

import config

logger = logging.getLogger(__name__)


# ─────────────────────── Pre-compile patterns ────────────────────────

_BLACKLIST_PATTERN = re.compile(
    "|".join(re.escape(tok) for tok in config.BLACKLISTED_TOKENS),
    re.IGNORECASE,
)

_PRAISE_PATTERN = re.compile(
    "|".join(re.escape(p) for p in config.PRAISE_PATTERNS),
    re.IGNORECASE,
)

_GROCERY_NOISE_PATTERN = re.compile(
    "|".join(re.escape(tok) for tok in config.GROCERY_NOISE_TOKENS),
    re.IGNORECASE,
)

# Expansion category keywords for detecting non-grocery content in "general" rows
_EXPANSION_KEYWORDS = re.compile(
    r"\b("
    r"electronics|earbuds|earphones|headphones|charger|cable|phone|laptop|tablet|"
    r"speaker|smartwatch|watch|power\s*bank|adapter|usb|bluetooth|"
    r"beauty|skincare|cosmetic|serum|moisturizer|sunscreen|face\s*wash|shampoo|"
    r"makeup|lipstick|foundation|cream|lotion|perfume|fragrance|"
    r"pet|dog|cat|pet\s*food|pet\s*care|kibble|"
    r"baby|diaper|infant|formula|baby\s*food|stroller|"
    r"cleaning|detergent|dishwash|floor\s*cleaner|mop|"
    r"pharmacy|medicine|tablet|vitamin|supplement|health|"
    r"intimate|condom|sanitary|pad|tampon"
    r")\b",
    re.IGNORECASE,
)

# Cross-shopping / inertia keywords — used for curated Reddit threads that were
# hand-picked for relevance but may not mention a specific product category.
_CROSS_SHOPPING_KEYWORDS = re.compile(
    r"\b("
    r"blinkit|zepto|swiggy\s*instamart|instamart|dunzo|bigbasket|big\s*basket|"
    r"amazon|flipkart|myntra|nykaa|meesho|jiomart|"
    r"quick\s*commerce|instant\s*delivery|10.min|"
    r"fake|duplicate|counterfeit|original|genuine|authentic|first\s*copy|"
    r"trust|refund|return|replacement|customer\s*care|"
    r"expensive|overpriced|costly|mrp|cheaper|"
    r"switch|alternative|instead|compare|"
    r"habit|loyalty|stick\s*to|go\s*back|stopped\s*using|never\s*again"
    r")\b",
    re.IGNORECASE,
)

# Blinkit-relevance pattern — checks if text actually mentions Blinkit
_BLINKIT_RELEVANCE = re.compile(
    r"\b(blinkit|blink\s*it|grofers|grof?ers)\b",
    re.IGNORECASE,
)

# Positive sentiment pattern — detects genuinely positive reviews
_POSITIVE_PATTERN = re.compile(
    r"\b("
    r"lifesaver|thank\w*|appreciat\w*|love\s*blinkit|great\s*service|"
    r"saved|impressed|excellent|recommend|relief|kudos|amazing\s*service|"
    r"best\s*service|best\s*delivery|grateful|satisfied|superb|wonderful|"
    r"fantastic|huge\s*thanks|god\s*send|blessing|awesome\s*experience|"
    r"hats\s*off|really\s*happy|so\s*happy|very\s*happy"
    r")\b",
    re.IGNORECASE,
)

# Friction signal pattern — reviews must contain at least one of these to be non-neutral
_FRICTION_SIGNAL = re.compile(
    r"(?:"
    r"\b(?:fake|counterfeit|duplicate|broken|damaged|defective|expired)\b|"
    r"\b(?:frustrated|angry|worst|terrible|pathetic|issue|problem)\b|"
    r"\b(?:expensive|overpriced|costly|cheaper)\b|"
    r"\b(?:didn.t know|had no idea|can.t find|not visible|hidden)\b|"
    r"\b(?:habit|only.*grocery|never tried|don.t explore)\b|"
    r"\b(?:trust|warranty|return|refund|replacement)\b|"
    r"\b(?:quality|authentic|genuine|original)\b|"
    r"\b(?:switch|alternative|compare|better|worse|prefer)\b|"
    r"\b(?:wish|need|want|should|missing|lack)\b|"
    r"\b(?:but|however|although|though|except|unfortunately)\b|"
    r"\b(?:complaint|disappoint|concern|doubt|suspicious|worried)\b|"
    r"\b(?:exchange|cancel|reject|denied|refuse)\b|"
    r"\b(?:nhi|nahi|kharab|galat|ganda|bekar|bakwas|fraud|scam)\b"
    r")",
    re.IGNORECASE,
)


def clean_text(text: str) -> str:
    """Basic text cleanup: strip markdown junk, normalize whitespace."""
    if not isinstance(text, str):
        return ""
    # Remove markdown artifacts
    text = re.sub(r"[#*_~`>]", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def stage1_transactional_noise(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stage 1: Drop rows where text primarily discusses logistics / operations.
    Scans for blacklisted tokens.
    """
    before = len(df)

    mask = df["text"].apply(
        lambda t: not bool(_BLACKLIST_PATTERN.search(str(t)))
    )
    df = df[mask].copy()

    dropped = before - len(df)
    logger.info(
        "Stage 1 (Transactional Noise): %d → %d rows (dropped %d)",
        before, len(df), dropped,
    )
    return df


def stage2_rating_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stage 2: Keep only rows with rating <= 4, or text expressing friction.
    Drop 5-star praise strings.
    """
    before = len(df)

    def _should_keep(row) -> bool:
        text = str(row.get("text", ""))
        rating_str = str(row.get("rating", "")).strip()

        # If no rating (Reddit, etc.), keep based on text content
        if not rating_str or rating_str == "":
            # No rating → keep unless it's pure praise
            return not bool(_PRAISE_PATTERN.search(text))

        try:
            rating = float(rating_str)
        except ValueError:
            return True  # Can't parse rating → keep

        # Drop 5-star reviews that are pure praise
        if rating >= 5:
            # Check if the text has substantive friction/inertia content despite 5 stars
            has_friction = any(
                word in text.lower()
                for word in [
                    "but", "however", "although", "though", "except",
                    "issue", "problem", "complaint", "disappointed",
                    "worried", "anxious", "confused", "frustrat",
                    "fake", "counterfeit", "doubt", "suspicious",
                    "expensive", "costly", "overpriced", "pricey",
                    "didn't know", "had no idea", "can't find",
                    "not available", "out of stock", "unavailable",
                    "quality", "damaged", "broken", "defective",
                    "wish", "should", "could be better", "improve",
                    "missing", "lack", "limited", "only if",
                    "swiggy", "zepto", "amazon", "flipkart", "bigbasket",
                    "competitor", "alternative", "switch", "compared",
                    "still use", "despite", "regardless",
                ]
            )
            if has_friction:
                return True
            return False

        # Keep everything rated 4 or below
        return True

    mask = df.apply(_should_keep, axis=1)
    df = df[mask].copy()

    dropped = before - len(df)
    logger.info(
        "Stage 2 (Rating Filter): %d → %d rows (dropped %d)",
        before, len(df), dropped,
    )
    return df


def stage3_category_isolation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stage 3: Keep only rows tied to expansion categories.
    Drop grocery staples. Inspect 'general' rows contextually.
    """
    before = len(df)

    def _should_keep(row) -> bool:
        category = str(row.get("category", "")).strip().lower()
        text = str(row.get("text", ""))
        source = str(row.get("source", "")).lower()

        # Explicitly in a KEEP category
        if category in config.KEEP_CATEGORIES:
            # But also check it's not actually a grocery complaint
            if _GROCERY_NOISE_PATTERN.search(text):
                return False
            return True

        # Explicitly in a DROP category
        if category in config.DROP_CATEGORIES:
            return False

        # "general" or unknown → contextual inspection
        if category == config.GENERAL_CATEGORY or category == "":
            # Always keep if text references expansion-category products
            if _EXPANSION_KEYWORDS.search(text):
                return True
            # For curated Reddit data: also keep if cross-shopping relevant
            if "reddit" in source:
                return bool(_CROSS_SHOPPING_KEYWORDS.search(text))
            return False

        # Unknown category → try keyword match
        return bool(_EXPANSION_KEYWORDS.search(text))

    mask = df.apply(_should_keep, axis=1)
    df = df[mask].copy()

    dropped = before - len(df)
    logger.info(
        "Stage 3 (Category Isolation): %d → %d rows (dropped %d)",
        before, len(df), dropped,
    )
    return df



def stage4_embedding_relevance(df: pd.DataFrame) -> pd.DataFrame:
    """Stage 4: Semantic Relevance Gate — drops off-topic reviews using embedding similarity."""
    import os
    try:
        import truststore
        truststore.inject_into_ssl()
    except Exception:
        pass
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    from sentence_transformers import SentenceTransformer
    before = len(df)
    texts = df['text'].astype(str).tolist()
    if not texts:
        return df
    logger.info('Stage 4 (Embedding Relevance): Loading model & computing similarities...')
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
    except Exception:
        logger.info("Model not in local cache, downloading...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
    anchor_embeddings = model.encode(config.RELEVANCE_ANCHORS, normalize_embeddings=True, batch_size=32)
    review_embeddings = model.encode([t[:2000] for t in texts], normalize_embeddings=True, batch_size=128, show_progress_bar=True)
    import numpy as np
    similarity_matrix = review_embeddings @ anchor_embeddings.T
    max_similarities = np.max(similarity_matrix, axis=1)
    mask = max_similarities >= config.RELEVANCE_THRESHOLD
    df = df.copy()
    df['_relevance_score'] = max_similarities
    dropped_indices = np.where(~mask)[0]
    if len(dropped_indices) > 0:
        logger.info('Sample dropped reviews (low relevance):')
        for idx in dropped_indices[:5]:
            logger.info('  [%.3f] %s...', max_similarities[idx], texts[idx][:80].replace(chr(10), ' '))
    df = df[mask].copy()
    logger.info('Stage 4 (Embedding Relevance): %d -> %d rows (dropped %d, threshold=%.2f)', before, len(df), before - len(df), config.RELEVANCE_THRESHOLD)
    return df


def run_cleaning_pipeline(
    df: pd.DataFrame,
    *,
    skip_stage2: bool = False,
    skip_stage3: bool = False,
) -> pd.DataFrame:
    """
    Run all four cleaning stages sequentially.

    Input: Raw DataFrame with at least [text, rating, category] columns.
    Output: Cleaned DataFrame with only expansion-relevant friction rows.

    Args:
        skip_stage2: When True, skip the low-star / high-friction rating filter.
            Used for CORPUS B (4–5★ positive scrape) where praise rows must be kept.
        skip_stage3: When True, skip non-grocery category isolation.
            Used for CORPUS B tier-2 expansion keyword recovery after strict tier-1.
    """
    logger.info("=" * 60)
    logger.info("CLEANING PIPELINE START — %d input rows", len(df))
    logger.info("=" * 60)

    # Clean text first
    df["text"] = df["text"].apply(clean_text)

    # Drop empty text
    df = df[df["text"].str.len() > 10].copy()
    logger.info("After empty-text removal: %d rows", len(df))

    # Run four stages
    df = stage1_transactional_noise(df)
    if skip_stage2:
        logger.info("Stage 2 (Rating Filter): SKIPPED (positive corpus mode)")
    else:
        df = stage2_rating_filter(df)
    if skip_stage3:
        logger.info("Stage 3 (Category Isolation): SKIPPED (positive corpus tier-2)")
    else:
        df = stage3_category_isolation(df)
    df = stage4_embedding_relevance(df)

    # Stage 5: Remove anecdotal condom/intimate stories (not friction signals)
    _CONDOM_STORY_PATTERN = re.compile(
        r"(?i)(condom.{0,30}(story|experience|funny|embarrass|awkward|first\s*time|"
        r"girl|cashier|shop|dukan|bhabhi|uncle|chemist|medical))|"
        r"((story|experience|funny|embarrass|awkward).{0,30}condom)"
    )
    before_intimate = len(df)
    intimate_story_mask = df["text"].apply(
        lambda t: bool(_CONDOM_STORY_PATTERN.search(str(t)))
    )
    df = df[~intimate_story_mask].copy()
    dropped_intimate = before_intimate - len(df)
    if dropped_intimate > 0:
        logger.info("Stage 5 (Intimate Stories): dropped %d condom anecdotes", dropped_intimate)

    # ── Post-filter tagging: Blinkit relevance + signal detection ──
    df = df.copy()
    source_col = df.get("source_raw", df.get("source", pd.Series("", index=df.index)))

    # Tag Blinkit-verified: True if from app store OR text mentions Blinkit
    # Historical Dump (blank source) = Play Store/App Store scrapes = inherently Blinkit
    # Blinkit-specific subreddits = inherently Blinkit
    _BLINKIT_SUBREDDITS = {"reddit_fuckblinkit", "reddit_blinkit"}

    def _is_blinkit_verified(row):
        text = str(row.get("text", ""))
        source = str(source_col.get(row.name, "")).lower().strip()
        # Blank source = Historical Play Store/App Store dump (inherently Blinkit)
        if source == "":
            return True
        # App store sources are inherently Blinkit
        if any(s in source for s in ["play store", "play_store", "app store", "appstore", "app_store"]):
            return True
        # Pre-classified data is verified
        if pd.notna(row.get("_preclassified_pillar", "")) and row.get("_preclassified_pillar", "") != "":
            return True
        # Blinkit-specific subreddits
        if source in _BLINKIT_SUBREDDITS:
            return True
        # Text mentions Blinkit
        if _BLINKIT_RELEVANCE.search(text):
            return True
        return False

    df["_blinkit_verified"] = df.apply(_is_blinkit_verified, axis=1)

    # Tag signal type: positive, friction, or neutral
    def _detect_signal(text):
        text = str(text)
        if _POSITIVE_PATTERN.search(text):
            return "positive"
        if _FRICTION_SIGNAL.search(text):
            return "friction"
        return "neutral"

    df["_signal"] = df["text"].apply(_detect_signal)

    verified_count = df["_blinkit_verified"].sum()
    signal_counts = df["_signal"].value_counts().to_dict()
    logger.info("Blinkit-verified: %d / %d", verified_count, len(df))
    logger.info("Signal distribution: %s", signal_counts)

    logger.info("=" * 60)
    logger.info("CLEANING PIPELINE DONE — %d surviving rows", len(df))
    logger.info("=" * 60)

    return df
