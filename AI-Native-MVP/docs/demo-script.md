# Buy Smart — Demo & Evaluator Scripts (Phase 8D)

> Rehearse to **under 5 minutes**. Pre-warm Render API before eval (free tier cold start).

---

## Live URLs

| Component | URL |
|-----------|-----|
| Link A — Discovery Engine | https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/ |
| Link B — Buy Smart UI | https://ai-native-mvp.vercel.app |
| Link B — Trust API | https://buy-smart-api.onrender.com/api/health |

**Pre-demo check (2 min before):**
```bash
curl -s https://buy-smart-api.onrender.com/api/health
curl -s https://buy-smart-api.onrender.com/api/trust/product/boat-airdopes-141 | head -c 200
```

---

## 5-minute Arindam demo script

| Time | Screen | Say |
|------|--------|-----|
| **0:00–1:00** | Link A → **Insights** | “We analyzed **1,504** public reviews across 8 categories. Six interviews pivoted us from a discovery hypothesis to a **trust and repeat** problem — warranty anxiety and authenticity show up repeatedly.” |
| **1:00–2:00** | Link A → **AI Analyser** → click **Re-run** | “This is the runnable analyser: **workflow**, **data stats**, and **theme output** on our committed corpus — not a live scrape. Re-run reloads the CSV and recomputes summaries in seconds.” |
| **2:00–4:00** | Link B → **Electronics** → **boAt** → **See how** | “Link B operationalizes the analysis. Product score **59** vs category **51** — product delta from brand signals. Here are **theme breakdown**, **verbatim snippets**, and **confidence** from real mention counts.” |
| **4:00–4:30** | Link B → **JBL** → **See how** (optional) | “Low sample — only 2 mentions — we show a **category estimate** banner instead of fake precision.” |
| **4:30–5:00** | Link B → **How calculated** or deck Slide 6b | “Keep rate is a **review-sentiment proxy**, not Blinkit repurchase. Production swaps in internal repurchase data — same UI. Link B scoring is **deterministic** — no LLM at request time.” |

### If interrupted — short answers

**“Why this metric?”**  
→ Slide 6b: MAC cross-category for habit; trust score for aisle safety; keep proxy because we lack repurchase data in MVP.

**“What if the LLM is wrong?”**  
→ Slide 6c: Link B doesn’t use LLM for scores; snippets are CSV-only; low-n gets confidence banner.

**“Is this just a UI mock?”**  
→ Link A analyser + Link B API both run on real classified corpus; catalog SKUs are simulated but scores are computed.

---

## Evaluator test script (8/8)

| # | Test | Pass criteria | Link |
|---|------|---------------|------|
| 1 | Link A Analyser re-run | Click Re-run → success banner + themes appear | [Link A](https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/) |
| 2 | Workflow + data stats | Sections 1–2 visible before re-run | Link A → AI Analyser |
| 3 | boAt See how evidence | Theme breakdown + ≥1 snippet | [boAt See how](https://ai-native-mvp.vercel.app/product/boat-airdopes-141/see-how) |
| 4 | Product ≠ category score | boAt trust **59** ≠ strip **51** | Electronics category |
| 5 | Low n handling | JBL shows low-sample banner + Est. | [JBL See how](https://ai-native-mvp.vercel.app/product/jbl-go-3/see-how) |
| 6 | Deck metric rationale | Slide 6b present | `deck-slides.md` |
| 7 | Deck moat + LLM | Slides 6c + 10 present | `deck-slides.md` |
| 8 | Methodology = UI | “No LLM at request time” in See how footnote | See how bottom + How calculated |

---

## Methodology alignment (deck ↔ product)

| Claim in deck | Where in product |
|---------------|------------------|
| Keep rate = proxy | PDP / See how “keep-rate proxy*” |
| Category vs product score | See how “Category baseline … product signals ±N” |
| Low sample honesty | Yellow banner + “Est.” on metrics |
| No LLM on Link B scores | See how + How calculated footnote |
| Simulated catalog | `analysis_meta.is_simulated_catalog` in API |
| Link A classifies themes | Discovery Engine + cross-link in See how |

---

## Screenshots needed for PDF deck

Capture before export:

1. **Slide 3** — Link A Insights (top themes)
2. **Slide 5** — boAt PDP + See how
3. **Slide 6** — Pipeline diagram (draw in slides tool OR Link A Workflow)
4. **Appendix A** — Link A AI Analyser after Re-run (annotate 4 callouts)
5. **Appendix B** (optional) — Electronics grid showing different scores

Save as PNG, compress if PDF >40MB.

---

## Q&A cheat sheet

| Question | Answer |
|----------|--------|
| Why not use Blinkit data? | MVP uses public reviews; production moat is repurchase/return wiring |
| Why is CORPUS B small? | Favorable supplement only; disclosed in deck + API note |
| Why boAt “Safe to repeat” but low trust category? | Badge uses product-level signals + keep proxy + confidence rules |
| Can evaluator run everything? | Yes — three URLs, no login |
| What’s AI-native? | Embeddings classify reviews; deterministic scoring; auditable evidence in UI |
