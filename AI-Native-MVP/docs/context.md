# Blinkit Buy Smart — Project Context

> Working context for the AI-Native MVP repo. Kept in sync with [`problemstatement.txt`](./problemstatement.txt).

**Deadline:** 4 Aug 2026  
**Role:** PM — Blinkit Growth Team  
**Repo:** `AI-Native-MVP/` (MVP + docs) · Legacy pipeline: `../Data-Extraction/`

---

## North Star

Increase the **% of Monthly Active Customers (MAC)** who purchase from at least **one new non-grocery category per month**.

Example: a user who only buys groceries also buys electronics or beauty that month → counts toward growth.

---

## Target User — Cautious Dabblers

| Trait | Detail |
|-------|--------|
| Frequency | Blinkit 2–3×/week for groceries |
| Behavior | Tried non-grocery once or twice; **does not repeat** |
| Status | Not churned — needs a reason to **trust and come back** |
| Mental model | *"Amazon for non-grocery, Blinkit for urgent groceries"* |

### Research base

- **6 user interviews** — primary evidence
- **1,505 cleaned public reviews** — AI analysis corpus
- **Google Form (45 responses)** — interview recruitment only, not primary evidence

### Key interview voices

| Person | Insight |
|--------|---------|
| **Manushri** | Default moves to Amazon for non-grocery |
| **Sarthak** | Retries on low-ticket known brand; return worked |
| **Sayra** | Pet/protein work on Blinkit; repeat categories exist |
| **Shrishti** | ₹11k HDD failed; CS ghosted — pre-purchase trust alone cannot fix post-purchase failure |

---

## Problem (Post-Research Pivot)

| Stage | Finding |
|-------|---------|
| **Initial AI hypothesis** | Discovery problem — users don't know Blinkit sells non-grocery |
| **Validated finding** | **Trust problem** — users already know; they don't trust or repeat |

**Root cause:** Blinkit is seen as *"kaam-chalau"* — last-minute convenience, not a quality destination for non-grocery.

**Critical constraint:** Urgency is **current behavior**, not the habit we want to build. Reinforcing *"only order when urgent"* keeps users in grocery-only emergency mode and **does not move MAC**.

**User pain:** *"Should I risk buying this on Blinkit?"* — mental tax before every non-grocery purchase → no repeat → flat cross-category MAC.

**Current workarounds:**

- Amazon — planned buys, reviews, returns
- Nykaa — beauty
- Blinkit — often one-off under urgency, **never becomes repeat habit**

---

## Solution — Buy Smart

An **AI-powered trust layer** inside the Blinkit app (simulated MVP for evaluators).

### What it is

- Pre-purchase **trust signals** derived from real review data
- Helps Cautious Dabblers build **repeat non-grocery habits**
- Removes re-decision tax: *"I know boAt under ₹2k works on Blinkit — I'll reorder here"*

### What it is NOT

- ❌ Chatbot
- ❌ Recommendation engine
- ❌ Amazon / competitor price comparison
- ❌ Urgency-first messaging (*"need it in 10 minutes?"* as primary CTA)

Speed stays in Blinkit's core brand. Buy Smart answers: **"Can I make this category a habit on Blinkit?"**

### What makes this AI-native

The trust score is an **output**, not the whole story. AI-native = how signals are produced and surfaced:

| Layer | AI-native element |
|-------|-------------------|
| **Theme classification** | `all-MiniLM-L6-v2` embeddings + anchor sentences (`themes.py`) |
| **Trust score** | Weighted favorable (CORPUS B) + risk (CORPUS A) theme signals |
| **Keep rate** | Review proxy from classified brand/category mentions (`compute_keep_rate`) |
| **Tips** | Dynamic from friction themes per product — not static copy |
| **Evidence** | Optional FAISS retrieval of review snippets in See how sheet |
| **Discovery Engine (Link A)** | AI finds trust problem; **Buy Smart (Link B)** operationalizes it in-app |

**Not AI-native:** hardcoded scores, chatbot UI, Amazon price comparison, urgency-first CTAs.

---

## MVP UX Spec

Simulated in-app Blinkit prototype — **not** a chat interface.

### Surfaces

| Screen | Element |
|--------|---------|
| **Category page** | Buy Smart strip — trust score + category guidance |
| **Product page (PDP)** | Replacement · warranty · **% keep this product*** · badge + `See how →` |
| **Trust sheet** ("See how") | Full score breakdown, tips, positive-mention %, evidence footnote |

**PDP shows keep rate only.** Positive mentions %, trust score math, and risks live in the sheet — not on the main product line.

### Example PDP copy

```
boAt Airdopes 141   ₹1,299
7-day replacement | 1 year warranty | 81% keep this product*
✅ Safe to repeat · See how →
```

`*` Footnote on PDP (small): *Keep rate estimated from public review signals. Production uses Blinkit repurchase data.

### "See how" trust sheet (same product)

```
Trust score: 71

81% keep this product
62% positive mentions in our data
Based on 47 public review mentions (boAt · electronics)

Tips
• Known brand — lower counterfeit risk
• Record unboxing video before opening
• Test on delivery — 7-day replacement window

Top concern from reviews: warranty & return anxiety

* Keep rate = review proxy in MVP (favorable sentiment in brand mentions).
  Production: Blinkit internal repurchase / return data — same UI, different source.
```

### Keep rate — review proxy (Option A)

**Do not hardcode keep rates.** Compute from real classified reviews via `compute_keep_rate()` in `trust_engine.py`.

**How it works**

1. Match reviews to product by **brand + category** (regex on review text)
2. Count **favorable vs negative themes** (embedding-classified `Primary Theme`)
3. `keep_rate = favorable_mentions / total_mentions` (clamped 35–85%)
4. Return `mention_count` for transparency in See how sheet

**Fallback when data is thin**

| Condition | Keep rate source | Label in See how |
|-----------|------------------|------------------|
| ≥ 3 brand mentions | Brand-level review proxy | `"Based on N public review mentions"` |
| 1–2 mentions | Category-level proxy | `"Category estimate (N brand mentions)"` |
| 0 mentions | Category favorable rate from CORPUS B | `"Category estimate (no brand-specific mentions)"` |

**Example outputs** (from pipeline — not hardcoded; will vary with corpus):

| Product | Price | Keep rate (computed) | Trust score | Badge |
|---------|-------|----------------------|-------------|-------|
| boAt Airdopes 141 | ₹1,299 | ~81% | ~71 | Safe to repeat |
| Apple EarPods (USB-C) | ₹1,799 | ~78% | ~68 | Safe to repeat |
| CeraVe Moisturizing Cream | ₹349 | ~86% | ~74 | Safe to repeat |
| realme Buds T300 | ₹2,199 | ~74% | ~63 | Verify warranty · See how |
| JBL GO 3 | ₹2,799 | ~71% | ~61 | Verify warranty · See how |

**Production swap:** Same PDP field (`keep_rate`); Blinkit replaces review proxy with internal repurchase metric — no UI change.

### Buy Smart paths (MVP messaging)

Promote **repeat & habit**, not urgency:

1. **Known brand + low ticket** (under ~₹2,000) — safe enough to buy again monthly
2. **Repeat-proven categories** — pet food, protein, personal care (Sayra)
3. **Clear return/warranty** on PDP — reduces risk for planned buys

### Price-tier badges (supportive — never anti-Blinkit)

Messages reduce anxiety and set expectations. **Never tell users not to buy on Blinkit.**

| Tier | Price | PDP badge | Tone |
|------|-------|-----------|------|
| **Repeat-safe** | ≤ ₹2,000 | `✅ Safe to repeat · See how →` | Encourage habit / reorder |
| **Mid ticket** | ₹2,001 – ₹5,000 | `Verify warranty · See how →` | Helpful checks, still shoppable |
| **High ticket** | > ₹5,000 | `Check return policy · See how →` | Caution tips in sheet, not a "don't buy" label |

**Do not use on any tier:** "Not a safe buy", "Skip this", "Don't buy here", "Use Amazon instead".

High-ticket **See how** sheet adds practical tips (unboxing video, test on delivery, warranty on PDP) — same supportive tone as lower tiers, more detail on returns.

### Copy guardrails

| Do | Don't |
|----|-------|
| "Safe to repeat" (≤ ₹2k) | "Only order when urgent" |
| "Verify warranty · See how" (> ₹2k) | "Not a safe first buy" / "Don't buy" |
| "X% keep this product" on PDP | "X% positive mentions" on PDP (sheet only) |
| Lead with trust + repeat signals | Lead with speed as trust reason |

### Habit shift ladder

```
Today     → Groceries on Blinkit; Amazon for everything else
First win → ONE low-risk category with trust signals (not fear)
Repeat    → Same category next month without re-deciding
Expand    → One NEW category/month → MAC metric moves
```

**Research note:** Urgency explains how people *discovered* non-grocery on Blinkit — useful for research, **not** for MVP CTAs.

### Out of scope for MVP

- Post-purchase CS failures (Shrishti case)
- High-AOV planned purchases without ops/CS improvements

---

## Deliverables & Deploy Links

| Part | Deliverable | Deploy | Stack |
|------|-------------|--------|-------|
| **Link A** | AI Discovery Engine | Separate URL | Streamlit — lives in `../Data-Extraction/` |
| **Link B** | Buy Smart MVP | Separate URL | Next.js (Vercel) + FastAPI (Render) |
| Deck | 10 slides, PDF, no name, ≤40MB | — | Screenshots from both links |

**Submission:** Deck PDF + Link A + Link B

---

## Architecture

See **[`architecture.md`](./architecture.md)** for system diagrams, repo layout, API contracts, scoring pipeline, deployment, and build phases.

---

## Dual Data Strategy

**Two corpora. Do not merge into the Discovery Engine.**

### CORPUS A — Discovery Engine (Link A)

| Field | Value |
|-------|-------|
| **Purpose** | Friction, themes, root causes, PM insights |
| **Source** | ~1,505 reviews, ≤4★ bias by design |
| **Filter** | Stage 2 keeps complaints; drops generic 5★ praise |
| **Used by** | Streamlit Discovery Engine only |
| **File** | `../Data-Extraction/Output/blinkit_clean_data.csv` |
| **Rule** | **Do not add positive reviews here** — dilutes friction signals |

### CORPUS B — Buy Smart MVP (Link B)

| Field | Value |
|-------|-------|
| **Purpose** | Consumer-facing trust scores (fair, balanced) |
| **Source** | 4★ + 5★ Play Store reviews (separate scrape) |
| **Filter** | Non-grocery only + embedding relevance; no Stage 2 low-star filter |
| **Used by** | FastAPI + Next.js MVP only |
| **File** | `data/mvp_trust_corpus.csv` |

### Extract CORPUS B

```bash
cd ../Data-Extraction
python main.py --positive --max-positive 200 --classify offline
# Export to AI-Native-MVP/data/mvp_trust_corpus.csv
# Uses scrapers/playstore.py → scrape_playstore_positive()
```

### Score logic (honest labeling)

**Trust score uses both corpora** — weighted theme signals, not raw star counts:

```
trust_score = baseline + (0.6 × favorable_from_CORPUS_B) − (0.4 × risk_from_CORPUS_A)
```

| Signal | Source | Where it shows |
|--------|--------|----------------|
| **Trust score** | A + B (weighted above) | See how sheet |
| **Keep rate** | **Review proxy** (`compute_keep_rate`) · Prod: Blinkit repurchase | **PDP** + sheet |
| **Positive mentions %** | CORPUS B | See how sheet only |
| **Tips & top concern** | CORPUS A (mainly) | See how sheet |
| **Mention count** | Brand-matched reviews | See how sheet (transparency) |

Deck line: *Trust score blends favorable 4–5★ signals (60%) with friction risk themes (40%). Keep rate is a review-sentiment proxy in MVP; production swaps in Blinkit repurchase data without UI changes.*

---

## Data Honesty (Required in Deck)

- Friction corpus is **complaint-biased by design** — scores are risk signals, not CSAT
- **Keep rate on PDP** = **review proxy** (favorable theme ratio on brand/category mentions), not Blinkit repurchase data — label in deck and See how footnote
- **Positive mentions %** = public review corpus only — shown in See how, not on PDP
- Product catalog in MVP is **simulated** — not live Blinkit API
- State openly that **two corpora exist** — shows PM rigour

**Do not:**

- Present MVP scores as official Blinkit CSAT
- Merge positive reviews into Discovery Engine CSV
- Hide corpus separation in the deck

---

## Key Product Principles

1. **Trust over discovery** — users know Blinkit sells non-grocery; they don't repeat
2. **Habit over urgency** — repeat monthly beats one-off rush orders
3. **Honest scores** — balanced display with clear data-source labeling
4. **Pre-purchase only** — MVP cannot fix broken post-purchase CS
5. **Separate concerns** — friction corpus for research; positive supplement for consumer UI

---

## Related Files

| File | Purpose |
|------|---------|
| [`problemstatement.txt`](./problemstatement.txt) | Full problem statement (submission reference) |
| [`deck-outline.md`](./deck-outline.md) | 10-slide deck structure, metrics, limitations |
| [`architecture.md`](./architecture.md) | System design, API, deployment, data flow |
| [`implementation.md`](./implementation.md) | Step-by-step build guide, phases, checklists |
| [`edge-cases.md`](./edge-cases.md) | Failure modes, boundary tests, QA script |
| `../Data-Extraction/engine/trust_engine.py` | Trust score logic (legacy) |
| `../Data-Extraction/engine/themes.py` | Embedding-based theme classification |
| `../Data-Extraction/Output/blinkit_clean_data.csv` | CORPUS A |
