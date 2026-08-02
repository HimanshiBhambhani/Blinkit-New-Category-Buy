# Buy Smart — Deck Slide Copy (Phase 8D)

> Copy-paste into Google Slides / PowerPoint / Canva.  
> One headline + one visual per slide. Speaker notes below each slide.

---

## Slide 1 — Title & north star

**Headline:** Buy Smart — AI trust layer for cross-category habits on Blinkit

**Bullets:**
- **North star:** ↑ % MAC buying from ≥1 new non-grocery category / month
- **User:** Cautious Dabblers — grocery-regular, non-grocery one-off
- **One line:** Reduce re-decision tax so Blinkit becomes a **repeat** destination

**Footer links:**
- Link A: https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/
- Link B: https://ai-native-mvp.vercel.app
- API: https://buy-smart-api.onrender.com

**Speaker notes:** Open with north star, not UI. Mention three live links evaluators can run.

---

## Slide 2 — Target user

**Headline:** Cautious Dabblers don’t lack discovery — they lack repeat confidence

**Bullets:**
- 2–3×/week on Blinkit for groceries
- Tried electronics or beauty 1–2×, **did not form habit**
- Mental model: *Blinkit = urgent groceries · Amazon = considered non-grocery*

**Quote (large):** *"Default setting in your head moves to Amazon"* — Manushri

**Speaker notes:** Arindam cares about consumer depth — this slide is the “why.”

---

## Slide 3 — Research pivot (Link A)

**Headline:** Analysis pivot: trust & repeat, not catalog awareness

**Bullets:**
- **Hypothesis:** Users don’t know Blinkit sells non-grocery
- **Finding:** They know — friction is **trust, warranty, authenticity**
- **Evidence:** 6 user interviews + **1,504** classified public reviews

**Visual:** Screenshot — Link A **Insights** tab  
Annotate: top 3 themes (Warranty anxiety, Price concerns, Category unawareness) + 1 quote each

**Speaker notes:** This is the analysis slide. Spend 30–45 seconds here.

---

## Slide 4 — Problem & root cause

**Headline:** Re-decision tax blocks MAC cross-category growth

**Bullets:**
- Blinkit wins **urgency** (“kaam-chalau”) — not **quality destination** for non-grocery
- Every non-grocery buy repeats the question: *“Should I risk this on Blinkit?”*
- Result: flat MAC in new categories despite assortment existing

**Speaker notes:** Tie to business — habit expansion, not GMV from one-off urgent carts.

---

## Slide 5 — Solution — Buy Smart (Link B)

**Headline:** Buy Smart — pre-purchase trust layer inside Blinkit

**Flow (3 steps):**
1. **Category page** — Buy Smart strip (category trust score + guidance)
2. **PDP** — keep-rate proxy*, badge, warranty row
3. **See how** — themes, snippets, confidence, tips

**NOT building:** chatbot · Amazon price compare · “don’t buy” verdicts

**Visual:** boAt PDP + See how sheet (side by side or stacked)

**Speaker notes:** Delivery slide — show you operationalized Link A findings.

---

## Slide 6 — AI-native pipeline

**Headline:** AI-native = visible workflow, auditable analyser output

**Diagram text:**
```
Sources → 3-stage filter → Theme labels (MiniLM)
       → CORPUS A (friction) + CORPUS B (favorable)
       → Deterministic trust score + product delta
       → Link B See how (evidence surfaced to user)
```

**Bullets:**
- Link A: discovery + analyser on **1,504** committed reviews
- Link B: **no LLM at request time** on scoring path
- Same theme taxonomy powers both links

**Speaker notes:** Answer “where is the AI?” — classification pipeline + deterministic scoring.

---

## Slide 6b — Why these metrics?

**Headline:** Metric rationale — why these, not others

| Metric | Why track | Why not alternative |
|--------|-----------|---------------------|
| MAC cross-category % | Habit expansion | GMV favors grocery urgency |
| Category Trust Score | Aisle-level QC safety | Star ratings miss friction themes |
| Keep rate proxy | Repeat intent (public data) | No repurchase API in MVP |
| See how tap rate | Transparency engagement | Add-to-cart mixes price/promo |
| Product delta ±12 | SKU differentiation | No order-level SKU data |

**Speaker notes:** If evaluator asks “why keep rate?” — say proxy until repurchase data; labeled honestly in UI.

---

## Slide 6c — LLM failure modes & mitigations

**Headline:** What can go wrong — and how we mitigated it

| Risk | Example | MVP mitigation |
|------|---------|----------------|
| Hallucinated evidence | Fake quote | Snippets from CSV only |
| Overconfidence | High % on n=2 | Confidence tier + “Est.” |
| Theme mislabel | Wrong pillar | Show breakdown + audit sample |
| Stale corpus | Old reviews | Corpus date + committed bundle |
| Groq outage | Chat fails | FAISS/keyword fallback (Link A) |
| Prompt injection | Jailbreak chat | No chat on Link B scores |
| Bad UX copy | “Use Amazon” | Banned phrases in code |

**Callout box:** **Link B trust API = deterministic. LLM only optional on Link A chatbot tab.**

**Speaker notes:** Rehearse this slide for Arindam Q&A.

---

## Slide 7 — Success metrics & experiments

**Headline:** How we’d measure success in production

| Layer | Metric | Notes |
|-------|--------|-------|
| North star | MAC cross-category % | Growth dashboard |
| Leading | Buy Smart strip CTR | Category exposure |
| Leading | See how tap rate | Trust engagement |
| Proxy | “Safe to repeat” SKU conversion | vs control |
| Habit | 30-day category repeat | Repurchase data |

**Hypothesis:** Less re-decision tax → more repeat non-grocery → higher MAC cross-category

---

## Slide 8 — Wedge & guardrails

**Headline:** Wedge: low-regret electronics → expand categories

**Phase 1:** Known brand + ≤₹2k (e.g. boAt earbuds)  
**Phase 2:** Sealed beauty, pet, protein  
**Guardrails:**
- Low brand mentions → category estimate (show banner, not fake precision)
- High AOV → emphasize return policy, not “safe to repeat”
- Grocery excluded from strong badges

---

## Slide 9 — Limitations & production path

**Headline:** Honest MVP limits — and what production replaces

| Today (MVP) | Production |
|-------------|------------|
| Keep rate = sentiment proxy | Blinkit repurchase rate |
| Public review corpora | + CSAT, returns by category |
| CORPUS B ~108 rows | Surveys + internal signals |
| 6-SKU simulated catalog | Live catalog |
| Pre-purchase trust only | + post-purchase CS |

**Footnote:** Dual corpus — A = friction research; B = favorable supplement for trust blend

---

## Slide 10 — Moat & ask

**Headline:** Why this is hard to copy — and durable

**Novelty:** Trust layer **before** purchase, native to QC UX

| Competitor | Gap |
|------------|-----|
| Amazon | No 10-min QC + dark-store context |
| Nykaa | Single-category; no MAC story |
| Other QC apps | No QC-friction corpus + repurchase flywheel |

**Production moat:** Wire **Blinkit repurchase + return + CSAT** into same Buy Smart UI.

**Ask evaluators:** Does reducing re-decision tax justify a cross-category repeat trial?

**Footer:** Link A · Link B · API (URLs on slide 1)

---

## Appendix A — Link A AI Analyser

**Headline:** Runnable analyser — workflow · data · output

**Screenshot:** Link A → AI Analyser → after Re-run

**Callouts to draw:**
1. Workflow cards (6 steps)
2. Data stats — 1,504 reviews, theme chart
3. Re-run button + “What ran (offline steps)”
4. Top themes + verbatim quotes

**Caption:** *Re-run aggregates pre-classified CSV — committed corpus MVP*

---

## Appendix B — Score divergence demo (live)

**Headline:** Same category, different products — boAt 59 vs JBL 51

| Product | Category score | Product score | Confidence | Why |
|---------|----------------|---------------|------------|-----|
| boAt Airdopes | 51 | 59 | High (16 mentions) | +delta, known brand |
| JBL Go 3 | 51 | 51 | Low (2 mentions) | Category estimate |

**Live URL:** https://ai-native-mvp.vercel.app/category/electronics

**Speaker notes:** Use if evaluator challenges “are scores real?”
