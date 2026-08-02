# Buy Smart — Implementation Guide

> Step-by-step build plan for the graduation project.  
> Read first: [`context.md`](./context.md) (product) · [`architecture.md`](./architecture.md) (system design) · [`problemstatement.txt`](./problemstatement.txt) (submission framing)

**Deadline:** 4 Aug 2026  
**Current repo state:** `AI-Native-MVP/` has docs only · `Data-Extraction/` has working pipeline + Streamlit

---

## 0. Prerequisites

### Tools

| Tool | Version | Used for |
|------|---------|----------|
| Python | 3.11+ | Backend, data pipeline |
| Node.js | 18+ | Next.js frontend (after Lovable export) |
| **Lovable** or **Stitch** | — | **Generate Buy Smart UI (Link B)** |
| Git | — | Both repos |
| Render account | — | FastAPI deploy (Link B API) |
| Vercel account | — | Next.js deploy (Link B UI) |
| Streamlit Cloud / local | — | Discovery Engine (Link A) |

### Existing assets (already built)

| Asset | Location | Status |
|-------|----------|--------|
| CORPUS A (~1,505 reviews) | `Data-Extraction/Output/blinkit_clean_data.csv` | ✅ Ready |
| Theme classifier (embeddings) | `Data-Extraction/engine/themes.py` | ✅ Ready |
| Trust engine (needs updates) | `Data-Extraction/engine/trust_engine.py` | ✅ Ported to `backend/engine/trust_engine.py` |
| Discovery Streamlit app | `Data-Extraction/app.py` | ✅ Ready (Link A) |
| FAISS index | Rebuild via `retheme_reviews.py` | ✅ If CSV updated |
| CORPUS B | `AI-Native-MVP/data/mvp_trust_corpus.csv` | ✅ Ready (108 rows) |
| FastAPI backend | `AI-Native-MVP/backend/` | ✅ Ready (Phase 3) |
| Next.js frontend | `AI-Native-MVP/frontend/` | ❌ Not yet |

### Environment — Data-Extraction

```bash
cd "../Data-Extraction"
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optional `.env` for Groq (Discovery LLM tab only — not required for offline classify):

```
GROQ_API_KEY=your_key_here
```

---

## 1. Implementation Phases (Summary)

| Phase | Goal | Est. effort | Blocker for |
|-------|------|-------------|-------------|
| **0** | Repo scaffold | 1–2 h | Everything |
| **1** | CORPUS B + data copy | 2–3 h | Backend scores |
| **2** | Trust engine updates | 3–4 h | API correctness |
| **3** | FastAPI backend | 4–6 h | Frontend + Lovable prompt |
| **4** | **Lovable / Stitch — generate UI** | 2–4 h | Import + wire |
| **5** | Import repo + wire API + polish | 3–5 h | Deploy Link B |
| **6** | Deploy both links | 2–3 h | Deck screenshots |
| **7** | Deck + QA | 4–6 h | Submission |

**Critical path:** Phase 1 → 2 → 3 → **4 → 5** → 6

> **Frontend path:** UI is **not** hand-coded from scratch. Phase 4 generates the Blinkit-style prototype in Lovable/Stitch; Phase 5 pulls it into `frontend/` and connects live trust API.

---

## Phase 0 — Repo Scaffold

### 0.1 Create folder structure

```bash
cd "AI-Native-MVP"
mkdir -p data backend/routes backend/services backend/engine frontend
```

### 0.2 Target tree

```
AI-Native-MVP/
├── data/
│   ├── friction_corpus.csv      # symlink or copy of CORPUS A
│   └── mvp_trust_corpus.csv     # CORPUS B
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── routes/trust.py
│   ├── services/trust_service.py
│   └── engine/
│       ├── trust_engine.py      # ported + updated
│       └── themes.py            # copy if needed for re-classify
├── frontend/                    # create via create-next-app
└── docs/
```

### 0.3 Copy CORPUS A into MVP repo (read-only for API)

```bash
cp "../Data-Extraction/Output/blinkit_clean_data.csv" data/friction_corpus.csv
```

**Rule:** Never write back to `Data-Extraction/Output/blinkit_clean_data.csv` from the MVP pipeline.

### ✅ Phase 0 checklist

- [x] `data/` folder exists
- [x] `backend/` folder exists
- [x] `friction_corpus.csv` copied (1,504 reviews)
- [x] `frontend/` folder ready for Lovable / Next.js (Phase 4)

---

## Phase 1 — Build CORPUS B

### 1.1 Scrape + classify positive reviews

From `Data-Extraction/` (uses existing `--positive` flag):

```bash
cd "../Data-Extraction"
source .venv/bin/activate
python main.py --positive --max-positive 200 --classify offline
```

This runs `scrape_playstore_positive()` → Stage 3 (category) → Stage 4 (embedding relevance) → **skips** Stage 2 friction filter.

### 1.2 Export MVP-only CSV

After pipeline completes, export rows that came from the positive scrape path into a **separate file**. Options:

**Option A — Manual export script** (recommended — add `scripts/export_mvp_corpus.py`):

```python
# Pseudocode — filter positive-scrape rows, keep columns:
# Raw Content, Target Category, Primary Theme, Rating, Source, ...
# Save to ../AI-Native-MVP/data/mvp_trust_corpus.csv
```

**Option B — Dedicated positive-only run** (implemented — `scripts/build_mvp_corpus.py`):

```bash
cd AI-Native-MVP
../Data-Extraction/.venv/bin/python scripts/build_mvp_corpus.py --max-positive 200
```

This scrapes 4–5★ reviews + historical 4–5★ dumps, runs Stage 1 → **skip Stage 2** → Stage 3 → Stage 4, plus a tier-2 expansion recovery pass. Favorable expansion rows from `friction_corpus.csv` are merged read-only if needed to reach 100+ rows. Output: `data/mvp_trust_corpus.csv` only — never writes to Discovery CSV.

### 1.3 Validate CORPUS B

```bash
cd "../AI-Native-MVP"
python -c "
import pandas as pd
df = pd.read_csv('data/mvp_trust_corpus.csv')
print('rows:', len(df))
print('categories:', df['Target Category'].value_counts().head())
print('themes:', df['Primary Theme'].value_counts().head())
"
```

Expected:

- Non-grocery categories present (`electronics`, `personal_care_beauty`, etc.)
- Meaningful `Positive Experience` theme count
- **No merge** into `blinkit_clean_data.csv`

### ✅ Phase 1 checklist

- [x] `mvp_trust_corpus.csv` exists with 100+ rows
- [x] `Primary Theme` column populated (embedding classification)
- [x] Discovery CSV unchanged
- [x] Both CSVs copied/symlinked under `data/`

---

## Phase 2 — Update Trust Engine

Port `Data-Extraction/engine/trust_engine.py` → `backend/engine/trust_engine.py` and apply these **required changes** before wiring the API.

### 2.1 Remove urgency-first copy (habit framing)

In `CategoryTrust.buy_smart_conditions` and product `verdict` strings:

| Remove | Replace with |
|--------|--------------|
| `"Urgent need today"` | `"Known brand under ₹2,000"` |
| `"High risk — skip unless urgent"` | `"Buy with checks — see warranty"` |
| `"favorable for urgent buys"` (tips) | `"favorable for repeat buys in this category"` |

### 2.2 Implement 60/40 trust score blend

Add function `compute_trust_score(df_a, df_b, category)`:

```python
def compute_trust_score(df_a: pd.DataFrame, df_b: pd.DataFrame, category: str) -> int:
    """60% favorable from B, 40% risk from A — per category theme ratios."""
    sub_a = df_a[df_a["Target Category"] == category]
    sub_b = df_b[df_b["Target Category"] == category]
    _, pos_b, _ = _score_from_subset(sub_b)   # favorable leg
    _, _, neg_a = _score_from_subset(sub_a) # risk leg (negative theme %)
    favorable_b = pos_b / 100.0
    risk_a = neg_a / 100.0
    raw = 50 + (0.6 * favorable_b * 35) - (0.4 * risk_a * 55)
    return _clamp(raw)
```

Use **separate dataframes** for A and B — do not concat rows (volume bias).

### 2.3 Keep rate — review proxy (Option A)

Keep existing `compute_keep_rate()` logic:

1. Brand + category match on review text
2. Favorable vs negative theme count
3. Clamp 35–85%
4. Fallback tiers (≥3 / 1–2 / 0 mentions)

**Do not hardcode** keep rates in API responses.

### 2.4 Positive mentions % — CORPUS B only

```python
def positive_mentions_pct(df_b, brand, category) -> float:
    subset = _brand_reviews(df_b, brand, category)
    if len(subset) == 0:
        subset = df_b[df_b["Target Category"] == category]
    pos = (subset["Primary Theme"] == POSITIVE_THEME).sum()
    return round(100 * pos / max(len(subset), 1), 1)
```

### 2.5 Badge logic (price-tier)

```python
def compute_badge(price: int, brand: str, trust_score: int) -> str:
    known = brand.lower() in KNOWN_BRANDS
    if price <= 2000 and known and trust_score >= 60:
        return "Safe to repeat · See how →"
    if price <= 5000:
        return "Verify warranty · See how →"
    return "Check return policy · See how →"
```

Never return: `"Not a safe buy"`, `"Skip"`, `"Don't buy"`, `"Use Amazon"`.

### 2.6 Unified product response builder

```python
def build_product_trust(df_a, df_b, product, category) -> dict:
    trust_score = compute_trust_score(df_a, df_b, category)
    pt = get_product_trust(df_a, product, category)  # tips from A
    keep_rate, mentions = compute_keep_rate(_brand_reviews(df_a, product["brand"], category))
    # apply fallbacks, badge, positive_pct from B
    return { ... }  # matches architecture.md JSON contract
```

### 2.7 Local smoke test

```bash
cd backend
python -c "
from engine.trust_engine import build_product_trust, load_corpora  # after implementing
df_a, df_b = load_corpora('../data/friction_corpus.csv', '../data/mvp_trust_corpus.csv')
from engine.trust_engine import PRODUCT_CATALOG
p = PRODUCT_CATALOG['electronics'][0]
print(build_product_trust(df_a, df_b, p, 'electronics'))
"
```

### ✅ Phase 2 checklist

- [x] No urgency copy in engine output
- [x] Trust score uses A + B weighted blend
- [x] Keep rate computed, not hardcoded
- [x] Badge follows price tiers
- [x] Smoke test prints sensible JSON for boAt + JBL

---

## Phase 3 — FastAPI Backend

### 3.1 Dependencies — `backend/requirements.txt`

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
pandas>=2.0.0
python-dotenv>=1.0.0
sentence-transformers>=2.2.0   # only if re-classifying at runtime
```

### 3.2 `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.trust import router as trust_router

app = FastAPI(title="Buy Smart Trust API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to Vercel URL in prod
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.include_router(trust_router, prefix="/api/trust")

@app.get("/api/health")
def health():
    return {"status": "ok"}
```

### 3.3 `backend/services/trust_service.py`

- Load CSVs once at startup (`@lru_cache` or `lifespan` hook)
- Expose `get_category(slug)`, `get_product(id)`, `list_products(category)`

### 3.4 `backend/routes/trust.py`

| Method | Path | Handler |
|--------|------|---------|
| GET | `/category/{slug}` | Category trust + guidance |
| GET | `/product/{product_id}` | Full product trust payload |
| GET | `/products?category={slug}` | Product list for category page |

Return **404** for unknown slug/id.

### 3.5 Environment variables

| Var | Default | Purpose |
|-----|---------|---------|
| `CORPUS_A_PATH` | `data/friction_corpus.csv` | Friction corpus |
| `CORPUS_B_PATH` | `data/mvp_trust_corpus.csv` | Positive corpus |
| `PORT` | `8000` | Render |

### 3.6 Run locally

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Test:

```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/trust/category/electronics
curl http://localhost:8000/api/trust/product/boat-airdopes-141
```

### ✅ Phase 3 checklist

- [x] All three endpoints return JSON matching `architecture.md`
- [x] CORS allows local Next.js (`localhost:3000`)
- [x] Cold start loads CSVs in < 5s
- [x] Product not found → 404

---

## Phase 4 — Generate Frontend (Lovable / Stitch)

**Goal:** Produce a mobile-first Blinkit-style Buy Smart prototype in Lovable or Google Stitch **before** importing into this repo.

**Prerequisite:** Phase 3 API running locally (or deployed) so you can test with real JSON. For generation, mock JSON in the prompt is fine.

### 4.1 Choose tool

| Tool | Best for | Export |
|------|----------|--------|
| **Lovable** (lovable.dev) | Full Next.js/React app, fast iteration | GitHub sync or download |
| **Stitch** (Google) | UI mock → code | Export to codebase |

Use **one** tool — don't rebuild in both.

### 4.2 What to generate (scope)

**Four screens** — same **1920×1080px** Figma frame each, **minimum font 26px** (project rule). Simulated Blinkit app, **not** a chatbot:

| Screen | Route | Must include |
|--------|-------|--------------|
| **Home** | `/` | Category tiles: Electronics, Beauty & Personal Care |
| **Category** | `/category/[slug]` | Product grid + Buy Smart strip (trust score + guidance) |
| **Product (PDP)** | `/product/[id]` | Trust row + badge → **navigates to Screen 4** |
| **See how** | `/product/[id]/see-how` | Full trust breakdown page — **NOT a bottom sheet** |

Full copy-paste prompt: [`stitch-prompt.md`](./stitch-prompt.md)

### 4.3 Lovable / Stitch prompt (copy-paste)

**Use [`stitch-prompt.md`](./stitch-prompt.md)** — includes 4 pages, 1920×1080 frames, 26px min font, dedicated See how route.

Legacy short prompt (Lovable only — prefer stitch-prompt.md for Stitch):

```
Build a mobile-first Blinkit quick-commerce prototype (390px width) for a feature called "Buy Smart" — a pre-purchase trust layer. NOT a chatbot. NOT Amazon price comparison.

STACK: Next.js App Router, TypeScript, Tailwind CSS.

SCREENS:
1) Home — grid of non-grocery categories (Electronics, Beauty & Personal Care). Blinkit-style yellow/green header.
2) Category page — Buy Smart strip at top showing trust score + line "Start repeat habits with known brands under ₹2k". Product cards below.
3) Product page (PDP) — product name, price, then trust row:
   "7-day replacement | 1 year warranty | {keep_rate}% keep this product*"
   Badge below (from API): e.g. "✅ Safe to repeat · See how →"
   Tapping badge or "See how" opens a BOTTOM SHEET (not new page).

BOTTOM SHEET ("See how") shows:
- Trust score: 71
- 81% keep this product
- 62% positive mentions in our data
- Based on 47 public review mentions
- Tips (bullet list)
- Top concern from reviews: warranty & return anxiety
- Small footnote: keep rate = review proxy in MVP; production uses Blinkit data

API (fetch on client — use env NEXT_PUBLIC_API_URL):
- GET {API}/api/trust/category/{slug}
- GET {API}/api/trust/product/{product_id}
- GET {API}/api/trust/products?category={slug}

Example product response:
{
  "product_id": "boat-airdopes-141",
  "name": "boAt Airdopes 141",
  "price": 1299,
  "keep_rate": 81,
  "trust_score": 71,
  "positive_pct": 62,
  "mention_count": 47,
  "badge": "Safe to repeat · See how →",
  "replacement_days": 7,
  "warranty": "1 year manufacturer warranty",
  "tips": ["Known brand — lower counterfeit risk", "Record unboxing video"],
  "top_concern": "Warranty & Return Anxiety",
  "evidence_label": "Based on 47 public review mentions"
}

RULES:
- PDP shows keep_rate ONLY on the trust row — NOT positive_pct
- positive_pct and trust_score only in bottom sheet
- Price ≤ ₹2000 + known brand → badge "Safe to repeat · See how →"
- Price ₹2001–5000 → "Verify warranty · See how →"
- Price > ₹5000 → "Check return policy · See how →"
- NEVER use: chat input, Amazon links, "only order when urgent", "don't buy", "skip"

DESIGN: Clean Blinkit-like UI — white cards, green accent, mobile bottom nav optional. Loading skeleton on trust row while fetching.
```

### 4.4 Generation workflow

1. Create new project in Lovable (or Stitch)
2. Paste prompt above → generate v1
3. Review on mobile preview:
   - [ ] Three routes exist
   - [ ] Bottom sheet opens from PDP
   - [ ] No chat UI
4. Iterate in tool (2–3 rounds max):
   - Fix spacing / Blinkit colors
   - Ensure trust row format matches spec
   - Remove any hardcoded "urgent" or Amazon copy
5. **Stop when layout is correct** — API wiring happens in Phase 5

### 4.5 Mock data during generation

If API is not ready, tell Lovable to use mock fetch with the JSON example above for:

- `boat-airdopes-141` (₹1,299 — Safe to repeat)
- `jbl-go-3` (₹2,799 — Verify warranty)
- `cerave-moisturizer` (₹349 — Safe to repeat)

Label mocks clearly in code comments — Phase 5 replaces with real fetch.

### 4.6 Export from Lovable / Stitch

**Lovable:**

1. Project → Connect to GitHub **or** Download ZIP
2. If GitHub: create repo `buy-smart-mvp-ui` or export into `AI-Native-MVP/frontend`

**Stitch:**

1. Export generated Next.js/React code
2. Save as starting point for `frontend/` folder

### ✅ Phase 4 checklist

- [ ] Lovable/Stitch project created
- [ ] Home + Category + PDP screens render
- [ ] Bottom sheet ("See how") works
- [ ] No chatbot, no Amazon, no urgency CTA
- [ ] PDP shows `% keep this product` not `% positive mentions`
- [ ] Code exported (GitHub or ZIP)

---

## Phase 5 — Import Frontend + Wire API

**Goal:** Move generated code into `AI-Native-MVP/frontend/` and connect to FastAPI from Phase 3.

### 5.1 Import into repo

```bash
cd AI-Native-MVP

# Option A — clone Lovable GitHub export
git clone https://github.com/YOU/buy-smart-mvp-ui.git frontend

# Option B — unzip Lovable download
unzip lovable-export.zip -d frontend
```

If Lovable created its own git root, nest contents so `frontend/package.json` sits at `AI-Native-MVP/frontend/package.json`.

### 5.2 Environment

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Production (Vercel): `NEXT_PUBLIC_API_URL=https://your-api.onrender.com`

### 5.3 Replace mocks with live API

Create or update `frontend/lib/trust-api.ts`:

```typescript
const BASE = process.env.NEXT_PUBLIC_API_URL;

export async function getCategoryTrust(slug: string) {
  const res = await fetch(`${BASE}/api/trust/category/${slug}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Category not found");
  return res.json();
}

export async function getProductTrust(id: string) {
  const res = await fetch(`${BASE}/api/trust/product/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Product not found");
  return res.json();
}

export async function listProducts(category: string) {
  const res = await fetch(`${BASE}/api/trust/products?category=${category}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Products not found");
  return res.json();
}
```

Wire these into PDP, category page, and TrustSheet — **remove hardcoded scores**.

### 5.4 Verify PDP vs sheet split

| Field | PDP | Trust sheet |
|-------|-----|-------------|
| `keep_rate` | ✅ Trust row | ✅ |
| `positive_pct` | ❌ | ✅ |
| `trust_score` | ❌ | ✅ |
| `tips`, `top_concern` | ❌ | ✅ |

### 5.5 Local run

```bash
# Terminal 1 — API
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — UI
cd frontend && npm install && npm run dev
```

Flow: `http://localhost:3000` → Electronics → boAt → See how.

### 5.6 Polish pass (manual fixes after import)

Common Lovable fixes:

- CORS errors → confirm FastAPI `allow_origins` includes `localhost:3000`
- Badge not tappable → wrap in button, `onClick` opens sheet
- Sheet not bottom-anchored → use fixed bottom modal / vaul drawer
- Wrong field on PDP → delete `positive_pct` from product line component

### ✅ Phase 5 checklist

- [ ] `frontend/` lives in `AI-Native-MVP` repo
- [ ] All trust data from API (no hardcoded 81% etc.)
- [ ] boAt PDP: Safe to repeat badge
- [ ] JBL PDP: Verify warranty badge
- [ ] Trust sheet shows full breakdown + footnote
- [ ] Mobile ~390px looks correct

---

## Phase 6 — Deploy

### 6.1 Link A — Discovery Engine

```bash
cd "../Data-Extraction"
streamlit run app.py
```

Deploy to Streamlit Cloud pointing at `Data-Extraction/app.py`. Ensure `Output/blinkit_clean_data.csv` is committed or loaded on startup.

**Do not** expose Buy Smart tab as Link B — evaluators get separate URLs.

### 6.2 Link B — API (Render)

1. New Web Service → root `AI-Native-MVP/backend`
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Upload or bundle `data/*.csv` in repo (required for Render filesystem)
5. Set env: `CORPUS_A_PATH`, `CORPUS_B_PATH`

### 6.3 Link B — UI (Vercel)

1. Import `AI-Native-MVP/frontend`
2. Set `NEXT_PUBLIC_API_URL=https://your-api.onrender.com`
3. Deploy

### 6.4 Post-deploy verification

```bash
curl https://YOUR-API.onrender.com/api/trust/product/boat-airdopes-141
# Open Vercel URL on phone-width viewport
```

### ✅ Phase 6 checklist

- [ ] Link A URL loads Streamlit dashboard
- [ ] Link B UI loads without CORS errors
- [ ] API responds on Render (watch cold start)
- [ ] Both URLs saved for deck

---

## Phase 7 — Deck & Submission QA

### 7.1 Suggested 10-slide flow

1. Problem + North Star (MAC cross-category)
2. Segment — Cautious Dabblers
3. Research pivot — trust not discovery
4. Solution — Buy Smart trust layer
5. MVP UX screenshot (PDP + See how)
6. AI-native — embeddings, dual corpus, scoring
7. Data honesty — two corpora, review proxy keep rate
8. Discovery Engine screenshot (Link A)
9. Habit shift + what's out of scope
10. Next steps for Blinkit production

### 7.2 Pre-submission test script

| # | Test | Pass? |
|---|------|-------|
| 1 | Link A loads, shows friction themes | |
| 2 | Link B category page shows Buy Smart strip | |
| 3 | boAt PDP: keep rate visible, no positive % on line | |
| 4 | JBL PDP: "Verify warranty" badge (>₹2k) | |
| 5 | See how sheet: trust score + tips + footnote | |
| 6 | No chatbot, no Amazon, no urgency CTA | |
| 7 | Deck states two corpora + review proxy keep rate | |
| 8 | PDF ≤ 40MB, no name on deck | |

---

## Known Gaps in Legacy Code (Fix During Phase 2)

| File | Issue | Fix |
|------|-------|-----|
| `trust_engine.py` | `"Urgent need today"` in conditions | Remove — habit copy |
| `trust_engine.py` | Single-corpus `_score_from_subset` for trust | Split A/B blend |
| `trust_engine.py` | `get_product_trust` uses friction df only | Pass `df_a` + `df_b` |
| `buy_smart_ui.py` | Streamlit Buy Smart tab | Ignore for Link B — use Lovable/Stitch + Next.js |
| `main.py` | Positive output mixed with friction file | Dedicated export to CORPUS B |

---

## File Ownership Reference

| Concern | Owner doc |
|---------|-----------|
| Why we're building this | `problemstatement.txt` |
| UX copy + guardrails | `context.md` |
| API shape + deployment | `architecture.md` |
| How to build it (this file) | `implementation.md` |
| Edge cases & QA | [`edge-cases.md`](./edge-cases.md) |

---

## Quick Command Reference

```bash
# Retheme + rebuild FAISS (Discovery only)
cd Data-Extraction && .venv/bin/python retheme_reviews.py

# Scrape positive corpus
cd Data-Extraction && .venv/bin/python main.py --positive --max-positive 200 --classify offline

# Run Discovery Engine locally
cd Data-Extraction && .venv/bin/streamlit run app.py

# Run Buy Smart stack locally
cd AI-Native-MVP/backend && uvicorn main:app --reload
cd AI-Native-MVP/frontend && npm run dev
```

---

## Related Documents

| File | Role |
|------|------|
| [`context.md`](./context.md) | Product context, UX spec, scoring rules |
| [`architecture.md`](./architecture.md) | System design, API contracts |
| [`problemstatement.txt`](./problemstatement.txt) | Submission problem definition |
| `../Data-Extraction/engine/trust_engine.py` | Base scoring code to port |
| `../Data-Extraction/main.py` | Positive scrape entry point |
