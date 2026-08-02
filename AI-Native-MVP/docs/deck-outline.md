# Buy Smart — Deck Outline (Submission)

> **Phase 8D** — Arindam-aligned deck map. Full slide copy: [`deck-slides.md`](./deck-slides.md)  
> Demo script: [`demo-script.md`](./demo-script.md)  
> PDF rules: no name on file · ≤40MB · one message per slide

**Live links (put on Slide 1 footer + Slide 10):**

| Link | URL |
|------|-----|
| **Link A** — Discovery Engine | https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/ |
| **Link B** — Buy Smart UI | https://ai-native-mvp.vercel.app |
| **Link B** — Trust API | https://buy-smart-api.onrender.com |

---

## Slide map (12 slides + appendix)

| # | Title | Arindam criterion | Visual |
|---|-------|-------------------|--------|
| 1 | Title & north star | Metric rationale | Title + 3 URLs |
| 2 | Target user — Cautious Dabbler | Consumer depth | Persona card |
| 3 | Research pivot (Link A) | **Analysis** | Insights screenshot — top themes + quotes |
| 4 | Problem & root cause | Problem depth | Quote + urgency trap |
| 5 | Solution — Buy Smart (Link B) | Delivery | PDP + See how flow (3 screens) |
| 6 | AI-native pipeline | **Workflow** | Corpus → classify → score → UI diagram |
| **6b** | **Why these metrics?** | **Which metric / why** | Metric rationale table |
| **6c** | **LLM & AI failure modes** | **Risk mitigation** | Failure → mitigation table |
| 7 | Success metrics & experiments | Measurement | North star + leading + proxy table |
| 8 | Wedge & rollout | Edge cases | Phase 1/2 + guardrails |
| 9 | Limitations & production path | Honesty | MVP vs production swap table |
| **10** | **Moat & roadmap** | **Stands test of time** | Competitor gap + repurchase moat |
| Appx | Link A Analyser | Runnable flow | Screenshot with callouts |

---

## Slide 1 — Title & north star

**Title:** Buy Smart — AI trust layer for cross-category habits on Blinkit  
**North star:** ↑ % MAC purchasing from ≥1 **new non-grocery category** per month  
**One line:** Help Cautious Dabblers **repeat** on Blinkit — not one-off urgent buys  
**Footer:** Link A · Link B UI · API (URLs above)

---

## Slide 2 — Target user

**Cautious Dabblers:** 2–3×/week grocery, tried non-grocery 1–2×, **don’t repeat**  
Mental model: *Amazon for non-grocery, Blinkit for urgent groceries*  
**Quote:** Manushri — *"Default setting in your head moves to Amazon"*

---

## Slide 3 — Research pivot (Link A)

**Hypothesis:** Discovery problem → users don’t know Blinkit sells electronics/beauty  
**Finding:** They **know** — they don’t **trust** or **repeat**  
**Evidence:** 6 interviews + **1,504** AI-classified reviews (Discovery Engine)  
**Screenshot:** Insights tab — top 3 friction themes + verbatim quotes

---

## Slide 4 — Problem & root cause

Blinkit = *"kaam-chalau"* — convenience, not quality destination for non-grocery  
Pain: *"Should I risk buying this on Blinkit?"* → re-decision tax → no repeat → flat MAC  
**Constraint:** Urgency explains today’s use; **habit** is the growth lever

---

## Slide 5 — Solution — Buy Smart (Link B)

Pre-purchase **trust layer** in-app:  
Category strip → PDP (keep proxy* + badge) → **See how** (themes + snippets + confidence)  
**NOT:** chatbot · Amazon compare · urgency-first CTA  
**Screenshot:** boAt PDP + See how sheet (annotate: score, snippets, confidence badge)

---

## Slide 6 — AI-native pipeline

```
CORPUS A (1,504 friction) + CORPUS B (~210 favorable)
        ↓ theme classification (MiniLM embeddings — offline)
        ↓ deterministic trust score (60/40 blend + product delta)
        ↓ Link B UI (See how = mini analyser)
```

Link A **finds** trust problem → Link B **operationalizes** it  
**Key claim:** AI-native = visible pipeline + auditable scores — **not** black-box LLM at checkout

---

## Slide 6b — Why these metrics? *(Arindam)*

| Metric | Why we track it | Why not something else |
|--------|-----------------|------------------------|
| **MAC cross-category %** (north star) | Measures habit expansion | GMV rewards urgency grocery |
| **Category Trust Score** | “Is this aisle safe on Blinkit?” | App star rating ≠ QC friction |
| **Keep rate proxy** | Best public stand-in for repeat intent | No repurchase data in MVP |
| **See how tap rate** | Trust transparency engagement | ATC confounded by price/promo |
| **Product delta (±12)** | Differentiates SKUs in same aisle | No SKU order data in MVP |

**Say in Q&A:** *“We chose metrics that measure habit, not one-off urgency.”*

---

## Slide 6c — LLM & AI failure modes *(Arindam)*

| Failure mode | Example | Mitigation in MVP |
|--------------|---------|-------------------|
| Hallucination | Fake review quote | Snippets **only** from CSV rows |
| Overconfidence | “81% keep” on 2 mentions | Confidence tier + “Est.” / low-sample banner |
| Theme drift | Wrong Primary Theme | Theme breakdown + human audit sample |
| Stale data | Old reviews | Corpus date in Link A; committed CSV |
| LLM outage (Link A chat) | Groq 429 | FAISS + keyword fallback |
| Prompt injection | Chat jailbreak | **Link B scoring: no LLM at request time** |
| Competitor bias | “Use Amazon” | Banned badge phrases in code |

**One-liner:** Link B trust scores are **deterministic** from classified corpus — LLM optional on Link A chat only.

---

## Slide 7 — Success metrics & experiments

| Layer | Metric | MVP / production |
|-------|--------|------------------|
| **North star** | % MAC with ≥1 new non-grocery category / month | Production dashboard |
| **Leading** | Buy Smart strip CTR | A/B on category page |
| **Leading** | See how tap rate on badged PDPs | Event tracking |
| **Proxy** | Conversion on “Safe to repeat” SKUs vs control | Experiment |
| **Habit** | 30-day repeat in same category | Blinkit repurchase data |

**Hypothesis:** Reducing re-decision tax → ↑ repeat non-grocery → ↑ MAC cross-category

---

## Slide 8 — Wedge & rollout

**Phase 1:** Known brand + ≤₹2k electronics (low regret wedge)  
**Phase 2:** Beauty sealed SKUs, pet/protein  
**Guardrails:** No strong badge on grocery; return-policy emphasis >₹5k  
**Edge case:** Low brand n → category estimate (JBL demo), never fake precision

---

## Slide 9 — Limitations & production path

| MVP today | Production swap |
|-----------|-----------------|
| Keep rate = review proxy | Blinkit repurchase / return rate |
| Trust from public reviews | + CSAT, return rate by category |
| CORPUS B supplement (~210 rows) | Play Store 4–5★ scrape + friction favorable rows |
| Simulated 6-SKU catalog | Live catalog API |
| Pre-purchase only | + post-purchase CS loop |

**Dual corpus:** Discovery = friction (A); Buy Smart = 60/40 blend (A+B)

---

## Slide 10 — Moat & ask *(Arindam: durability)*

**Why novel:** Pre-purchase trust **inside** QC app — not chatbot, not price compare

| Competitor | Why they can’t copy quickly |
|------------|----------------------------|
| Amazon | No 10-min dark-store + QC habit context |
| Nykaa | Beauty-only; no cross-category MAC |
| Other QC | No QC-specific friction corpus + repurchase loop |

**Production moat:** Blinkit **repurchase + return + CSAT** wired to same Buy Smart UI — public reviews are MVP stand-in.

**Ask:** Does this reduce re-decision tax enough to trial cross-category repeat?

**Links:** Link A · Link B · API

---

## Appendix — Link A AI Analyser screenshot

**Capture:** Link A → **AI Analyser** tab → after Re-run

**Annotate callouts:**
1. **Workflow** — ingest → clean → classify pipeline  
2. **Data** — 1,504 rows, corpus path, theme chart  
3. **Analyser** — Re-run button + top themes + quotes  
4. Label: *“Committed corpus MVP — not live scrape”*

**Backup Q&A slides:**
- boAt vs JBL score divergence (59 vs 51) — product delta + confidence  
- CORPUS B build — favorable Play Store supplement, not merged into Discovery CSV
