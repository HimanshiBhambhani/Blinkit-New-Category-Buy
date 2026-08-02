# Blinkit Buy Smart — Context 2.0

> **Analysis-first credibility pass** after Link B went live. Aligns product truth, evaluator narrative, and **Arindam feedback** ([`Arindam-feedback.txt`](./Arindam-feedback.txt)).  
> Supplements [`context.md`](./context.md) — does not replace problem statement or north star.  
> Build plan: [`implementation2.md`](./implementation2.md)

**Deadline:** 4 Aug 2026  
**Live URLs:** Link A (Streamlit) · Link B UI `ai-native-mvp.vercel.app` · API `buy-smart-api.onrender.com`  
**Repo:** `Grad-Project/` monorepo (`AI-Native-MVP/` + Discovery Engine at root)

---

## 1. Why Context 2.0?

Phase 1–6 shipped a **runnable demo**. Two reviews surfaced the same gap:

1. **PM credibility review** — UI implies more precision than backend computes  
2. **Arindam feedback** — evaluators reward **analysis depth + clarity of thought**, not “we built a UI”

> *“Focus on actual analysis not on getting the project build n solutioning.”* — Arindam

Context 2.0 reframes the MVP:

| Old framing (weak) | New framing (2.0) |
|--------------------|-------------------|
| “Buy Smart app with trust scores” | **AI analysis pipeline** → operationalized as in-app trust layer |
| “AI-native because embeddings” | **Show workflow, data, analyser** — evaluator runs it and sees insights |
| “Keep rate 81%” | **Review-sentiment proxy** — labeled, with confidence tier |
| “Trust score for this product” | **Category baseline + product signals** — show the math |
| Chase live APIs / fake n | **Use available classified corpus** — honest n, illustrative only when labeled |

**Goal of 2.0:** Evaluator leaves thinking *“they understood the problem deeply, showed their analysis, and built a defensible prototype”* — not *“nice Figma clone.”*

---

## 2. Insights from Arindam feedback (what evaluators optimize for)

Source: [`Arindam-feedback.txt`](./Arindam-feedback.txt)

### 2.1 Analysis > build

| Arindam signal | What it means for us | 2.0 response |
|----------------|----------------------|--------------|
| Industry + review signals + **why** (consumer + tech) | Don’t skip from data → UI | Link A shows **theme insights + quotes**; Link B **See how shows snippets + theme counts** |
| Fetch reviews, get signs, go deep | Pipeline must be visible | **Workflow tab** in Discovery Engine: ingest → classify → theme summary |
| Focus on analysis, not solutioning | Deck time on *findings*, not screens | Slide 3–4 = pivot evidence; Slide 6 = pipeline diagram + corpus stats |

### 2.2 Metric rationale (must articulate)

| Arindam signal | 2.0 response |
|----------------|--------------|
| *“Why are you choosing the metric?”* | Document **MAC north star → leading metrics → MVP proxies** (§8) |
| *“Does it make sense?”* | Keep rate = **proxy** until repurchase data; trust score = **category habit risk**, not product quality |
| *“Which metric to track?”* | Deck table: exposure → See how tap → repeat category (production) |

### 2.3 LLM / AI failure & mitigation

| Arindam signal | 2.0 response |
|----------------|--------------|
| *“How can LLM fail?”* | Hallucinated tips, wrong theme, stale corpus, overconfidence on low n |
| *“Risk mitigation”* | Pre-classified CSV (no LLM at request time on Link B), confidence tiers, banned badge phrases, human-readable evidence, **no LLM-generated numbers** |

**Positioning:** Link A may use Groq for insights chat; Link B scores are **deterministic from classified corpus** — faster, auditable, safer for eval demo.

### 2.4 Clarity, structure, edge cases

| Arindam signal | 2.0 response |
|----------------|--------------|
| Structure of thought, tie the story | Two-link narrative: A finds trust problem → B operationalizes |
| Edge cases where solution fails | [`edge-cases.md`](./edge-cases.md) + in-app methodology “What we don’t know” |
| Step by step | Methodology page: Step 1 corpus → Step 2 themes → Step 3 score → Step 4 UI |

### 2.5 Solution creativity & moat

| Arindam criterion | Our answer |
|-------------------|------------|
| Solves problem identified? | Yes — re-decision tax for Cautious Dabblers, not discovery |
| Unique / novel? | **Pre-purchase trust layer inside QC app** — not chatbot, not Amazon compare |
| Stands test of time / hard to copy? | Moat = **Blinkit repurchase + return data** wired to same UI (competitors lack dark-store habit data); MVP uses public reviews as stand-in |

Deck must state moat explicitly — evaluators will ask.

### 2.6 Presentation & visual clarity

| Arindam signal | 2.0 response |
|----------------|--------------|
| Core message obvious | One hero line per slide; no interpret-yourself walls of text |
| Wireframes / thinking visible | Deck: pipeline mermaid + See how screenshot with callouts |
| Discovery · Delivery · Planning | Link A = Discovery · Link B = Delivery · context2/impl2 = Planning |

### 2.7 Runnable flow + AI Analyser

| Arindam signal | 2.0 response |
|----------------|--------------|
| *“Anyone can run it”* | ✅ Streamlit + Vercel + Render (done) |
| *“Insights pulled out + analysis of data points”* | Link A Insights tab + Link B See how evidence |
| *“Live analyser — fetch latest data”* | **Optional** “Refresh sample” in Link A (re-run theme summary on bundled CSV) — **not** blocked on external API |
| *“Getting API data is difficult — focus on available data”* | **Explicit policy:** no dependency on Blinkit internal API or live scrape for eval day; corpus committed in repo |
| *“Via AI Analyser: workflow, data, analyser”* | New **Analyser** section in Link A (Phase 8H): 3 panels — Workflow \| Data stats \| Analyser output |

---

## 3. Data policy — real, thin, simulated (reconciles dummy-n discussion)

Three layers — **never mix without labels:**

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1 — REAL (lead with this in demo)                 │
│ • 1,504 classified reviews (CORPUS A)                   │
│ • Theme labels from embedding classifier (Link A)       │
│ • Review snippets in See how (truncated, PII-scrubbed)  │
│ • Real n in evidence_label when mentions exist          │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 2 — THIN / ESTIMATED (disclose confidence)        │
│ • CORPUS B (~210 rows) — favorable supplement           │
│ • Brand mention counts (often low n)                    │
│ • Category fallback when n < 3 → “Low sample” UI        │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 3 — SIMULATED (never pretend otherwise)         │
│ • 6-SKU catalog, prices, warranty copy                │
│ • Optional deck-only “production n” as future-state    │
│ • Mock API fallback — ONLY with “Demo mode” banner      │
└─────────────────────────────────────────────────────────┘
```

**Arindam-aligned rule:** *Focus on available data.* Do **not** inflate n or chase live fetch if it risks eval stability. **Do not** show fake precision (JBL 0%, Apple 100% on 2–5 mentions).

**Acceptable:** “Insufficient brand data” instead of a number.  
**Not acceptable:** Hardcoded `mention_count: 500` to look credible.

---

## 4. What evaluators will challenge (technical + Arindam)

| # | Issue | Severity | Fixable? | Arindam lens |
|---|--------|----------|----------|--------------|
| E1 | Trust score identical per category | P0 | ✅ | Shows shallow analysis |
| E2 | “Keep rate” implies repurchase | P0 | ✅ | Metric rationale |
| E3 | CORPUS B tiny vs A | P1 | Partial | Disclose + optional expand |
| E4 | See how lacks auditable evidence | P0 | ✅ | **Analysis visible** |
| E5 | Tips are generic templates | P1 | Partial | Tie tips to themes + n |
| E6 | “Safe to repeat” never appears | P1 | ✅ | Align badge to wedge |
| E7 | Brand regex ≠ SKU | P1 | Partial | Label “brand-level signals” |
| E8 | Hardcoded catalog | P2 | Disclose | Simulated shelf — OK |
| E9 | Non-functional filters | P2 | ✅ | Fix or remove |
| E10 | Silent mock fallback | P1 | ✅ | Edge case / honesty |
| E11 | No metrics experiment story | P2 | Deck | Which metric to track |
| E12 | Misleading positive % on low n | P1 | ✅ | Confidence tier |
| **A1** | **Can’t see workflow / analyser** | **P0** | ✅ | Link A Analyser panel |
| **A2** | **No LLM failure discussion** | **P1** | ✅ | Deck + methodology |
| **A3** | **Moat / uniqueness unclear** | **P1** | ✅ | Deck slide 10 |
| **A4** | **Story jumps problem → UI** | **P1** | ✅ | Two-link narrative deck |

---

## 5. Metric definitions (canonical — use everywhere)

### 5.1 Why these metrics? (Arindam: metric choice)

| Metric | Why we track it | Why not something else |
|--------|-----------------|---------------------------|
| **MAC cross-category %** (north star) | Directly measures habit expansion | GMV alone rewards urgency grocery |
| **Category Trust Score** | Captures “is Blinkit safe for this aisle?” | Star rating ≠ QC-specific friction |
| **Keep rate proxy** | Best public-data stand-in for repeat intent | No repurchase data in MVP |
| **See how tap rate** (deck) | Measures trust transparency engagement | ATC alone confounded by price/promo |
| **Product delta** | Differentiates SKUs within same aisle risk | SKU orders not available |

### 5.2 Category Trust Score (0–100)

Pre-purchase confidence for **shopping this category on Blinkit**.

```
raw = 50 + (0.6 × favorable_B × 35) − (0.4 × risk_A × 55)
clamped to [12, 92]
```

- **CORPUS A** (n≈1,504): friction themes  
- **CORPUS B** (n≈210): favorable supplement (66 scraped + 144 friction supplement)  

**UI label:** **Category Trust Score**

### 5.3 Product Confidence Adjustment

Delta ∈ [−12, +12] from brand mentions, positive B, price band, known brand.  
**Product Trust Score** = category score + delta.  
Label: *“Product signals (brand + price band)”* — not SKU repurchase.

### 5.4 Keep Rate Proxy

Review-sentiment proxy — **not** Blinkit repurchase. See Layer 2 policy (§3).

### 5.5 Confidence Tier

| Tier | Rule |
|------|------|
| High | ≥ 10 brand mentions |
| Medium | 3–9 |
| Low | 0–2 / category fallback → hide or dim metrics |

### 5.6 Badge rules (Option A — recommended)

“Safe to repeat” if: known brand + price ≤ ₹2k + product trust ≥ 55 + keep proxy ≥ 70 + confidence ≠ Low.

---

## 6. See how = mini AI Analyser (Link B)

Arindam wants **workflow, data, analyser** — See how is Link B’s analyser surface:

1. Category + Product Trust Score (analyser output)  
2. Confidence + real n  
3. Theme breakdown (what the classifier found)  
4. 2 review snippets (evidence)  
5. Tips with “because [theme] (n mentions)”  
6. Footnote: corpus sizes, last updated, link to methodology  

**Not in MVP:** live LLM per click, live API fetch, fake n.

---

## 7. Link A — Discovery / AI Analyser (primary analysis showcase)

Link A carries **most of Arindam’s “analysis depth” expectation.** Link B proves operationalization.

| Tab | Arindam job |
|-----|-------------|
| **Insights** | Industry + consumer pain from 1,504 reviews |
| **Workflow — How It Works** | Pipeline visible (ingest → embed → theme) |
| **AI Analyser** (2.0 — Phase 8H) | Split view: Data stats \| Run analysis \| Output themes + quotes |
| **AI Chatbot** | Optional — disclose Groq failure modes |

**“Fetch latest data” (evaluator click):**  
Re-analyse **bundled** `blinkit_clean_data.csv` (refresh theme summary + counts) — simulates live pull without network scrape on eval day. Label: *“Re-run analyser on committed corpus (MVP).”*

---

## 8. LLM & AI failure modes (deck + methodology)

| Failure mode | Example | Mitigation in MVP |
|--------------|---------|-------------------|
| Hallucination | Fake review quote | Snippets **only** from CSV rows by ID |
| Overconfidence | “81% keep” on 2 mentions | Confidence tier + hide low n |
| Theme drift | Wrong Primary Theme | Show theme + confidence; human audit sample in deck |
| Stale data | Old reviews | `corpus_meta.last_updated` in API |
| LLM outage (Link A chat) | Groq 429 | Offline keyword + FAISS fallback already built |
| Prompt injection (chat) | User jailbreak | Link B has **no chat** |
| Competitor comparison bias | “Use Amazon” | Banned badge phrases in code |

---

## 9. Competitive moat (Arindam: creativity & durability)

**Problem we solve:** Cautious Dabblers won’t **repeat** non-grocery on Blinkit (trust / re-decision tax).

**Why novel:** Trust layer **before** purchase, inside QC UX — not a chatbot bolt-on, not price comparison.

**Why hard to copy:**

| Competitor | Gap |
|------------|-----|
| Amazon | No Blinkit 10-min + dark-store context |
| Nykaa | Beauty-only; no cross-category MAC story |
| Other QC apps | Lack classified **QC-specific** friction corpus + future **repurchase loop** |

**Production moat:** Blinkit proprietary repurchase / return / CSAT wired to same Buy Smart UI — public reviews are MVP stand-in only.

---

## 10. Deck structure (Arindam-aligned)

| Slide | Content | Arindam criterion |
|-------|---------|-------------------|
| 1 | North star MAC | Metric rationale |
| 2 | Cautious Dabbler | Consumer depth |
| 3 | **Link A screenshot — top 3 themes + quotes** | Analysis |
| 4 | Trust problem + urgency trap | Problem depth |
| 5 | Link B flow (3 screens, callouts) | Delivery |
| 6 | **Pipeline: corpus → classifier → score → UI** | Workflow |
| 7 | **Metrics table + experiment design** | Which metric to track |
| 8 | Wedge + guardrails | Edge cases |
| 9 | Limitations + LLM failure mitigations | Honesty |
| 10 | Moat + production path | Stands test of time |

**Visual rule:** One message per slide; annotate screenshots — don’t make evaluator interpret.

---

## 11. UI copy standards (unchanged core + analyser labels)

| Location | 2.0 label |
|----------|-----------|
| See how header | Product Trust Score + Category baseline |
| PDP | Keep proxy* with footnote |
| Low n | “Insufficient brand data” / “Low sample” |
| Link A Analyser | “Re-run on committed corpus” |
| API fail | “Demo mode — API unavailable” |

---

## 12. AI-native claim (honest)

| Claim | Valid? |
|-------|--------|
| Embeddings classify 1,504 reviews into themes | ✅ Link A |
| Deterministic trust scoring from dual corpus | ✅ Link B API |
| Evaluator can run full flow | ✅ Three URLs |
| Real-time LLM analyses each PDP | ❌ Don’t claim |
| Blinkit internal repurchase data | ❌ Production |

**One-liner:** *AI-native = visible classification pipeline + auditable scoring — not a black-box score.*

---

## 13. 2.0 success criteria (evaluator-ready)

**Arindam test (5 min demo):**

1. Open Link A → see themes + quotes + workflow  
2. Click “Re-run analyser” → output updates from bundled data  
3. Open Link B → boAt See how → snippets + theme breakdown  
4. Ask “why this metric?” → answer from §5.1 without hesitation  
5. Ask “what if LLM wrong?” → answer from §8  

**Technical test:** Same as before (E1–E12) in §4.

---

## 14. Related docs

| Doc | Purpose |
|-----|---------|
| [`implementation2.md`](./implementation2.md) | Phased build incl. Phase 8H Analyser |
| [`Arindam-feedback.txt`](./Arindam-feedback.txt) | Source feedback |
| [`context.md`](./context.md) | Original product context |
| [`deck-outline.md`](./deck-outline.md) | 12-slide map + URLs (8D) |
| [`deck-slides.md`](./deck-slides.md) | Full slide copy + speaker notes (8D) |
| [`demo-script.md`](./demo-script.md) | 5-min demo + evaluator checklist (8D) |

---

*Last updated: Aug 2026 — post deploy + Arindam feedback integration*
