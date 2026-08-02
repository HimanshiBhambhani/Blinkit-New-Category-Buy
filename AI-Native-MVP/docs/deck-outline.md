# Buy Smart — 10-Slide Deck Outline

> One-page map for submission deck (PDF, no name, ≤40MB).  
> Full narrative: [`problemstatement.txt`](./problemstatement.txt) · Demo: Link A + Link B

---

## Slide 1 — Title & north star

**Title:** Buy Smart — AI trust layer for cross-category habits on Blinkit  
**North star:** ↑ % MAC purchasing from ≥1 **new non-grocery category** per month  
**One line:** Help Cautious Dabblers **repeat** on Blinkit — not one-off urgent buys

---

## Slide 2 — Target user

**Cautious Dabblers:** 2–3×/week grocery, tried non-grocery 1–2×, **don’t repeat**  
Mental model: *Amazon for non-grocery, Blinkit for urgent groceries*  
**Quote:** Manushri — *"Default setting in your head moves to Amazon"*

---

## Slide 3 — Research pivot (Link A)

**Hypothesis:** Discovery problem → users don’t know Blinkit sells electronics/beauty  
**Finding:** They **know** — they don’t **trust** or **repeat**  
**Evidence:** 6 interviews + 1,505 AI-classified reviews (Discovery Engine screenshot)

---

## Slide 4 — Problem & root cause

Blinkit = *"kaam-chalau"* — convenience, not quality destination for non-grocery  
Pain: *"Should I risk buying this on Blinkit?"* → mental tax → no repeat → flat MAC  
**Constraint:** Urgency explains today’s use; **habit** is the growth lever

---

## Slide 5 — Solution — Buy Smart (Link B)

Pre-purchase **trust layer** in-app (simulated MVP):  
Category strip → PDP (keep rate + badge) → **See how** sheet (full breakdown)  
**NOT:** chatbot · Amazon compare · urgency-first CTA

**Screenshot:** boAt PDP + bottom sheet

---

## Slide 6 — AI-native layer

| Signal | Source | UI |
|--------|--------|-----|
| Theme classification | MiniLM embeddings | All scores |
| Trust score | 60% CORPUS B + 40% CORPUS A | See how |
| Keep rate | Review proxy (brand mentions) | PDP |
| Tips / top concern | CORPUS A friction themes | See how |

Link A finds trust problem → Link B operationalizes it

---

## Slide 7 — Success metrics

| Layer | Metric | MVP / production |
|-------|--------|------------------|
| **North star** | % MAC with ≥1 new non-grocery category / month | Production (Growth dashboard) |
| **Leading** | Buy Smart strip CTR on category page | A/B exposure |
| **Leading** | "See how" tap rate on badged PDPs | Event tracking |
| **Proxy** | Conversion on "Safe to repeat" SKUs vs control | Experiment |
| **Habit** | 30-day repeat in same category | Blinkit repurchase data |

**Hypothesis:** Reducing re-decision tax → ↑ repeat non-grocery orders → ↑ MAC cross-category

---

## Slide 8 — Wedge & rollout

**Phase 1 wedge:** Known brand + ≤₹2k electronics (Sarthak pattern — low regret)  
**Phase 2:** Beauty sealed SKUs, pet/protein (Sayra repeat categories)  
**Guardrails:** No strong badge on grocery; emphasize return policy >₹5k (Shrishti lesson)

**Entry point:** Category browse strip + PDP (exploration without forcing search)

---

## Slide 9 — Limitations & production path

| MVP today | Production swap |
|-----------|-----------------|
| Keep rate = review proxy | Blinkit repurchase / return rate |
| Trust score from public reviews | + internal CSAT, return rate by category |
| CORPUS B thin on category positives | Internal post-purchase surveys |
| Simulated product catalog | Live catalog + inventory API |
| Pre-purchase only | + post-purchase CS loop (Shrishti) |

**Openly dual corpus:** Discovery = friction (A); Buy Smart = 60/40 blend (A+B)

---

## Slide 10 — Roadmap & ask

**Now (MVP):** Trust signals at PDP → habit-first copy → See how transparency  
**Next:** Re-order nudge · category habit streak · ops fixes for high-AOV  
**Ask (evaluators):** Does this reduce re-decision tax enough to trial cross-category repeat?

**Links:** Link A (Discovery) · Link B (Buy Smart live demo)

---

## Appendix (backup slides if Q&A)

- Signal divergence: keep rate (brand) vs trust score (category blend) — explain in sheet  
- CORPUS B build: 4–5★ scrape + favorable supplement — not merged into Discovery CSV  
- Data honesty footnote on every See how sheet
