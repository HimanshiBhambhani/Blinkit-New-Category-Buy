# Buy Smart — Implementation Guide 2.0

> **Analysis-first credibility pass** — fixes PM review gaps + **Arindam evaluator criteria** ([`Arindam-feedback.txt`](./Arindam-feedback.txt)).  
> Read first: [`context2.md`](./context2.md) · [`context.md`](./context.md)

**Deadline:** 4 Aug 2026  
**Estimated effort:** 16–22 hours (Must = 8A–8D + **8H** ≈ 14–16 h)  
**Live stack:** Grad-Project → Render · Vercel · Streamlit

---

## 0. Priority stack (Arindam-informed)

Evaluators weight **analysis + clarity** over polish. Build order:

| Priority | Phase | Why |
|----------|-------|-----|
| **P0** | 8H Link A Analyser showcase | *“Via AI Analyser: workflow, data, analyser”* |
| **P0** | 8A–8B Backend scoring + API | Honest, differentiated numbers |
| **P0** | 8C See how evidence UI | Link B’s analyser surface |
| **P0** | 8D Deck + methodology | Metric rationale, LLM failures, moat |
| **P1** | 8E CORPUS B expand | Stronger data story (optional if time) |
| **P2** | 8F Catalog polish | Remove broken chips |
| **P2** | 8G Deploy hygiene | Ops |

**Explicitly deprioritized (Arindam: focus on available data):**

- ❌ Live Blinkit API / Adi Osmani-style external product API for eval day  
- ❌ Live scrape on evaluator click (network risk)  
- ✅ “Re-run analyser on **committed corpus**” button instead  

---

## 0.1 Feasibility matrix

| Fix | Possible? | Before deadline? | Effort |
|-----|-----------|------------------|--------|
| Link A: Workflow + Analyser panels | ✅ | ✅ | 3–4 h |
| “Re-run analysis” on bundled CSV | ✅ | ✅ | 1–2 h |
| Split category vs product trust score | ✅ | ✅ | 3–4 h |
| See how snippets + theme breakdown | ✅ | ✅ | 3–4 h |
| Confidence tier + low-n handling | ✅ | ✅ | 2 h |
| Metric rationale + LLM failure deck slides | ✅ | ✅ | 2 h (deck) |
| Moat / uniqueness slide | ✅ | ✅ | 1 h (deck) |
| Dummy n only when labeled | ✅ | ✅ | Policy in 8A/8C |
| Expand CORPUS B | ✅ | Partial | 2–4 h |
| Live API fetch latest reviews | ⚠️ | ❌ eval day | Out of scope |
| Real repurchase data | ❌ | ❌ | Production |

---

## 1. Phase map (2.0)

| Phase | Name | Arindam criterion |
|-------|------|-------------------|
| **8A** | Backend scoring 2.0 | Honest analyser output |
| **8B** | API contract extensions | Data exposed to UI |
| **8C** | See how + PDP UI | Analysis visible on Link B |
| **8D** | Methodology + deck | Metric why, LLM risks, moat |
| **8E** | CORPUS B expansion | Available data depth |
| **8F** | Catalog + filter polish | Delivery quality |
| **8G** | Deploy hygiene | Runnable flow |
| **8H** | **Link A AI Analyser** | **Workflow · data · analyser** |

**Critical path:** 8H (parallel) + 8A → 8B → 8C → 8D → redeploy all three links

---

## Phase 8H — Link A AI Analyser (P0 — Arindam)

**Goal:** Evaluator opens Streamlit, sees **workflow, data, analyser** without reading repo docs.

**Repo path:** `Grad-Project/app.py` + new `engine/analyser_panel.py` (or section in app.py)

### 8H.1 Three-panel layout (new sidebar tab or expand “Workflow”)

```
┌──────────────────┬──────────────────────────────────────┐
│ 1. WORKFLOW      │  Ingest → Clean → Embed → Classify │
│    (static diag) │  → Theme summary → (Link B scores)  │
├──────────────────┼──────────────────────────────────────┤
│ 2. DATA          │  Rows: 1,504 │ Categories: 8        │
│                  │  Corpus A path │ Last built: date   │
│                  │  Theme distribution (bar chart)      │
├──────────────────┼──────────────────────────────────────┤
│ 3. ANALYSER      │  [Re-run analysis on corpus] btn    │
│                  │  Output: top 5 themes + 3 quotes    │
│                  │  Category filter dropdown            │
└──────────────────┴──────────────────────────────────────┘
```

### 8H.2 “Re-run analysis” behavior

**Not a live scrape.** On button click:

1. `load_data()` — read committed `Output/blinkit_clean_data.csv`  
2. `get_theme_summary(df)` — recompute counts  
3. Show diff banner: *“Analysis complete — N reviews, M themes”*  
4. Optional: clear `st.cache_data` for demo freshness  

Label in UI: **“Re-run analyser on committed corpus (MVP)”**

### 8H.3 Evaluator script (Link A)

| Step | Action | Pass? |
|------|--------|-------|
| 1 | Open Streamlit Link A | |
| 2 | Navigate to Analyser / Workflow tab | |
| 3 | See pipeline diagram + row counts | |
| 4 | Click Re-run → theme counts render | |
| 5 | Insights tab shows quotes matching analyser themes | |

### 8H.4 Files

```
Data-Extraction/
├── app.py                          # Add tab or route to analyser
├── engine/analyser_panel.py        # New — render_workflow(), render_data_stats(), render_analyser()
└── Docs/ or README snippet          # "How to run" for evaluators (optional)
```

### ✅ Phase 8H checklist

- [ ] Workflow diagram visible (mermaid or HTML)
- [ ] Data stats: row count, categories, corpus date
- [ ] Re-run button works offline (no network)
- [ ] Top themes + ≥3 review quotes displayed
- [ ] Copy matches context2 §7 (“committed corpus”)

---

## Phase 8A — Backend scoring 2.0

*(Unchanged core — see previous 8A.1–8A.7)*

**Additions from data-policy discussion:**

### 8A.8 No fake n

- `mention_count` **must** come from corpus query — never hardcode  
- If displaying aggregate “reviews analysed” on category strip, use real `len(sub_a)+len(sub_b)` for category  
- Optional `display_n` field only when `confidence !== "low"`  

### 8A.9 `analysis_meta` block in API

```json
"analysis_meta": {
  "signal_level": "brand",
  "mentions": 16,
  "confidence": "high",
  "data_source": "public_reviews",
  "is_simulated_catalog": true
}
```

### ✅ Phase 8A checklist

- [ ] (previous 8A items)
- [ ] No inflated mention counts
- [ ] `analysis_meta` on product payload

---

## Phase 8B — API contract 2.0

*(Extended product JSON — add `analysis_meta`, `tips[].because`)*

### 8B.3 Category response

Add to category endpoint for Buy Smart strip:

```json
{
  "trust_score": 51,
  "review_count": 380,
  "reviews_analysed": 380,
  "analysis_note": "Category-level score from 353 electronics reviews in CORPUS A"
}
```

Use **real** filtered row counts — not dummy.

---

## Phase 8C — Frontend credibility UI

*(See how layout unchanged — add Link to Link A in methodology footnote)*

### 8C.5 Methodology cross-link

> “Themes classified in [Discovery Engine / Link A]. Trust scores computed deterministically — no LLM at request time on this page.”

### 8C.6 Dummy data banner

When `analysis_meta.confidence === "low"`:

- Replace precise % with “Est.” prefix or em dash  
- Show: *“Not enough brand mentions — showing category-level analysis”*

---

## Phase 8D — Methodology, deck & Arindam Q&A

### 8D.1 New deck slides (sync [`deck-outline.md`](./deck-outline.md))

| Slide | New content |
|-------|-------------|
| **6b** | **Metric rationale table** (from context2 §5.1) |
| **6c** | **LLM failure modes + mitigations** (from context2 §8) |
| **10** | **Moat:** repurchase data + QC-specific corpus (context2 §9) |
| **Appendix** | Link A Analyser screenshot with callouts |

### 8D.2 Arindam 5-minute demo script

| Min | Show | Say |
|-----|------|-----|
| 0–1 | Link A Insights | “1,504 reviews → 6 interviews pivoted us to trust” |
| 1–2 | Link A Analyser → Re-run | “Workflow, data, analyser — committed corpus” |
| 2–4 | Link B boAt See how | “Operationalized: snippets, themes, confidence” |
| 4–5 | Methodology | “Keep rate is proxy; production = repurchase” |

### 8D.3 Evaluator test script (updated)

| # | Test | Arindam / Technical |
|---|------|---------------------|
| 1 | Link A Analyser re-run works | A |
| 2 | Link A shows workflow + data stats | A |
| 3 | boAt See how: snippets + themes | T |
| 4 | Product score ≠ within category | T |
| 5 | Low n → “Low sample” not 0%/100% | T |
| 6 | Deck: metric why + LLM failures | A |
| 7 | Deck: moat slide | A |
| 8 | Methodology matches UI footnotes | T |

### ✅ Phase 8D checklist

- [x] Deck slides 6b, 6c, moat updated — [`deck-outline.md`](./deck-outline.md) · [`deck-slides.md`](./deck-slides.md)
- [x] Demo script — [`demo-script.md`](./demo-script.md) (5-min + evaluator tests; rehearse before eval)
- [x] Methodology mentions no LLM on Link B scoring path — Slide 6c + See how footnote (8C)

---

## Phase 8E — CORPUS B expansion (Should)

**Arindam angle:** “Available data” — expanding B from committed scrape is **good**; live fetch is not required.

Target 200+ rows; time-box 3h. If fail, deck states n=108 with honesty.

---

## Phase 8F — Catalog & filter polish (Should)

Unchanged. Prefer **remove broken chips** over fake filter behavior.

---

## Phase 8G — Deploy hygiene

Add:

- [ ] README or Streamlit header: **3 links** (Link A, Link B UI, Link B API)  
- [ ] Pre-warm Render before eval  
- [ ] Verify Streamlit deployed from Grad-Project `main`

---

## 2. Suggested schedule (Arindam-prioritized)

### Day 1

| Hours | Task |
|-------|------|
| 3h | **8H** Link A Analyser panel + re-run |
| 3h | 8A backend scoring |
| 1h | 8B API |
| 1h | Deploy + smoke |

### Day 2

| Hours | Task |
|-------|------|
| 3h | 8C See how UI |
| 2h | **8D deck** (metric + LLM + moat slides) |
| 1h | 8E B expand (if time) |
| 1h | Full Arindam demo rehearsal |

---

## 3. What we won't build (aligned with Arindam + data policy)

1. Live “fetch latest” from Play Store on eval day  
2. Blinkit internal API dependency  
3. Fake mention counts for credibility  
4. LLM-generated review snippets  
5. In-app analytics (deck spec only)  

---

## 4. Definition of done (2.0)

**Shipped when:**

1. **Arindam test** (context2 §13) — 5/5 demo steps  
2. **Technical test** — 8/8 in §8D.3  
3. All three links live  
4. Deck PDF with analyser + See how annotated screenshots  

---

## 5. Edge-case updates

| ID | Scenario |
|----|----------|
| EC2-05 | Re-run analyser with empty CSV → error state with instructions |
| EC2-06 | Evaluator expects live scrape → UI says “committed corpus MVP” |
| EC2-07 | Groq key missing → Link A chat degrades; Analyser still works |
| EC2-08 | Simulated catalog flagged in `analysis_meta.is_simulated_catalog` |

---

*Implementation 2.0 — Aug 2026 · Arindam feedback + data honesty integrated*
