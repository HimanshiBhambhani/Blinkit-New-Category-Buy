"""
config.py — Central configuration for the Blinkit Data Extraction Engine.
All constants, filter rules, and schema definitions live here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────── Paths ───────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "Data"
OUTPUT_DIR = PROJECT_ROOT / "Output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Input files
REVIEWS_RAW_CSV = DATA_DIR / "reviews_raw.csv"
ANKESH_REVIEWS_RAW_CSV = DATA_DIR / "Ankesh-reviews_raw.csv"
REDDIT_URLS_FILE = DATA_DIR / "Reddit Data URLs"
REDDIT_LINKS_DOCX = DATA_DIR / "links-data.docx"
PRECLASSIFIED_CSV = DATA_DIR / "SourceThreadTitleSite-PlatformBlinkit-TargetCatego.csv"

# Output
CLEAN_OUTPUT_CSV = OUTPUT_DIR / "blinkit_clean_data.csv"
CLEAN_OUTPUT_PARQUET = OUTPUT_DIR / "blinkit_clean_data.parquet"

# ─────────────────────────── Play Store Scraper ──────────────
PLAY_STORE_PACKAGE = "com.grofers.customerapp"
PLAY_STORE_COUNTRY = "in"
PLAY_STORE_LANG = "en"
PLAY_STORE_BATCH_SIZE = 60  # reviews per invocation

# ─────────────────────────── App Store Scraper ───────────────
APPSTORE_APP_NAME = "blinkit-groceries-more"
APPSTORE_APP_ID = 960335206  # Blinkit iOS app ID
APPSTORE_COUNTRY = "in"

# ─────────────────────────── Scrape Outputs (for GH Actions) ─
SCRAPE_OUTPUT_DIR = OUTPUT_DIR / "scrapes"
SCRAPE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────── Reddit API (Pathway B) ──────────
# Set these in a .env file or export as environment variables
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "blinkit-data-engine/1.0")

# ─────────────────────────── LLM Provider (Groq — Llama 3.3 70B) ────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ─────────────────────────── Embedding Provider (Gemini) ─────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

# ─────────────────────────── RAG Settings ────────────────────
TOP_K = int(os.getenv("TOP_K", "5"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# ─────────────────────────── Category Taxonomy ───────────────
# Primary expansion targets
PRIMARY_CATEGORIES = [
    "electronics",
    "personal_care_beauty",
    "pet",
    "baby",
]

# Secondary expansion categories
SECONDARY_CATEGORIES = [
    "home_cleaning",
    "intimate_personal",
    "pharmacy_health",
]

# All categories we want to KEEP
KEEP_CATEGORIES = PRIMARY_CATEGORIES + SECONDARY_CATEGORIES

# Categories to DROP (grocery / noise)
DROP_CATEGORIES = [
    "groceries_fresh",
    "snacks_beverages",
]

# "general" needs contextual inspection — handled separately
GENERAL_CATEGORY = "general"

# Mapping from pre-classified CSV labels → canonical labels
CATEGORY_ALIAS_MAP = {
    "Electronics/Accessories": "electronics",
    "Electronics/Accessories (implied)": "electronics",
    "Beauty/Skincare/Cosmetics": "personal_care_beauty",
    "Pet Care": "pet",
    "Baby Products": "baby",
    "General (affects non‑grocery basket too)": "general",
    "General (can include non‑grocery)": "general",
    "General (documents/accessories)": "general",
    "General (non‑grocery implied)": "general",
    "General (non‑grocery possible)": "general",
}

# Multi-label split: some rows have ";" separated categories
MULTI_CATEGORY_SEPARATOR = ";"

# ─────────────────────────── Stage 1: Noise Filter ───────────
BLACKLISTED_TOKENS = [
    "late delivery",
    "delivery boy rude",
    "refund pending",
    "money deducted",
    "payment failed",
    "upi failed",
    "gpay",
    "app crash",
    "coupon code invalid",
    "driver behavior",
    "otp not received",
    "delivery partner",
    "delivery boy",
    "wrong item delivered",
    "order cancelled automatically",
]

# ─────────────────────────── Stage 2: Rating Filter ──────────
MAX_STAR_RATING = 4  # keep <= 4 stars

# 5-star praise strings to drop even if text has some signal
PRAISE_PATTERNS = [
    "good app",
    "very fast",
    "best app",
    "love this app",
    "nice app",
    "great app",
    "awesome app",
    "superb app",
    "excellent app",
    "amazing app",
    "wonderful app",
]

# ─────────────────────────── Stage 3: Grocery Noise ──────────
GROCERY_NOISE_TOKENS = [
    "potatoes were rotten",
    "milk packet leaked",
    "vegetables were stale",
    "fruits were bad",
    "onion",
    "tomato",
    "dal",
    "atta",
    "rice packet",
    "bread was expired",
    "curd was spoiled",
]

# ─────────────────────────── Friction Pillars ────────────────
FRICTION_PILLARS = [
    "Habitual Tunnel Vision",
    "Quality & Authenticity Risk",
    "Discovery Blind Spots",
    "Immediate Value Disconnection",
    "Positive Experience",
    "Unverified Source",
    "Neutral / No Signal",
]

# ─────────────────────────── Output Schema ───────────────────
OUTPUT_COLUMNS = [
    "Source",
    "Platform",
    "Target Category",
    "Friction Pillar",
    "Raw Content",
    "Opportunity",
    "Primary Theme",
]

PLATFORM = "Blinkit"

# Source label mapping — preserve actual platform names
SOURCE_LABELS = {
    "Play Store": "Play Store",
    "App Store": "App Store",
    "Reddit (post)": "Reddit",
    "Reddit (comment)": "Reddit",
    "HackerNews": "HackerNews",
    "YouTube": "YouTube",
    "PissedConsumer": "PissedConsumer",
    "play_store_live": "Play Store (Live)",
    "play_store_positive": "Play Store (4-5 Star)",
    "appstore_live": "App Store (Live)",
    "reddit_live": "Reddit (Live)",
}

# ─────────────────────────── Embedding Relevance Filter ──────
# Anchor texts define "what a relevant review looks like".
# Reviews are kept only if semantically close to at least one anchor.
RELEVANCE_ANCHORS = [
    # Electronics friction
    "Blinkit sells fake electronics, I got counterfeit earbuds that stopped working",
    "I ordered a charger from Blinkit but the quality was terrible compared to Amazon",
    "Didn't know Blinkit sells electronics, I only use it for groceries",
    # Beauty / Personal care friction
    "The skincare products on Blinkit might be expired or duplicate, I don't trust them",
    "Blinkit beauty products are overpriced compared to Nykaa and Amazon",
    "I never explore beauty category on Blinkit, only buy groceries from there",
    # Pet care friction
    "Blinkit doesn't stock good pet food brands, very limited options for dogs",
    "I didn't know Blinkit has pet supplies, the app never showed me",
    # Baby products friction
    "Baby products on Blinkit have no return policy, what if the size doesn't fit",
    # Cross-shopping inertia (general)
    "I only use Blinkit for groceries and snacks, never tried other categories",
    "Quick commerce is only for urgent grocery needs, for other stuff I use Amazon",
    "Blinkit should show more non-grocery categories, I had no idea they sell electronics",
    # Price comparison friction
    "Why would I buy electronics on Blinkit when Amazon has better prices and reviews",
    "Blinkit charges MRP while Amazon and Flipkart give discounts on the same products",
    # Trust / authenticity friction
    "I don't trust Blinkit for expensive items, what if it's fake and they don't refund",
    "How can I verify if products on Blinkit are genuine, there are no customer reviews",
]

# Minimum cosine similarity to nearest anchor (0.0 to 1.0)
# Lower = more permissive, Higher = stricter
# 0.25 is conservative; increase to 0.30 if still seeing junk
RELEVANCE_THRESHOLD = 0.25
