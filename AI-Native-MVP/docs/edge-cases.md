# Buy Smart — Edge Cases & Failure Modes

> Scenarios to handle, test, or disclose during build and QA.  
> Derived from [`implementation.md`](./implementation.md), [`architecture.md`](./architecture.md), [`context.md`](./context.md), and [`problemstatement.txt`](./problemstatement.txt).

**Use this doc for:** system boundaries, API contract violations, UI→backend mapping, pipeline stages, deployment topology, and pre-submission testing.

---

## How to read this doc

| Column | Meaning |
|--------|---------|
| **ID** | Reference for checklists |
| **Severity** | `P0` break MVP · `P1` wrong UX/data · `P2` polish · `INFO` disclose in deck only |
| **Expected** | What the system should do |
| **Test** | How to verify |

### System map (from architecture)

```
Link A (Streamlit)     CORPUS A only  →  Discovery / friction story
Link B (Next.js+API)   CORPUS A + B   →  Buy Smart trust layer
                       PRODUCT_CATALOG →  Simulated SKUs
```

---

## 1. Architecture & System Boundaries

Cross-cutting failures from [`architecture.md`](./architecture.md) §1–4, §10.

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| AR-01 | Buy Smart scores powered only by CORPUS A | P0 | Must load **A + B** in `trust_engine`; A alone ≈33 electronics | Inspect backend data load |
| AR-02 | Discovery Engine fed CORPUS B | P1 | Link A reads **A only** — B would weaken friction narrative | Streamlit data source path |
| AR-03 | FAISS / RAG chatbot treated as Link B | P2 | RAG is Link A optional tab — Link B has **no chat input** | Compare URLs |
| AR-04 | Frontend calls Streamlit instead of FastAPI | P0 | Link B fetches `NEXT_PUBLIC_API_URL` only | Network tab |
| AR-05 | FastAPI serves Discovery dashboard | P2 | Separate deployables — API is JSON only | Hit Render root |
| AR-06 | `trust_engine.py` imported from Data-Extraction at runtime on Render | P1 | **Port/copy** into `backend/engine/` — relative imports break | Deploy without parent repo |
| AR-07 | CORPUS A path points to live `blinkit_clean_data.csv` outside repo | P1 | Use bundled `data/friction_corpus.csv` on Render | Render file tree |
| AR-08 | Single monorepo deploy for both links | P2 | Two URLs: Streamlit (A) + Vercel/Render (B) | Deck links |
| AR-09 | LLM invoked on every product API request | P1 | **No** — scores from pre-classified CSV; Groq is Link A only | API latency + code review |
| AR-10 | Production evolution breaks API contract | INFO | `keep_rate`, `trust_score`, `badge`, `tips` fields stable — swap data sources only | architecture §11 |

---

## 2. Pipeline Stages (Data Ingestion)

From architecture §1 mermaid — Stage 2/3/4 edge cases.

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| PL-01 | Positive scrape runs Stage 2 friction filter | P0 | B path must **skip Stage 2** | Inspect export script |
| PL-02 | Stage 3 drops all non-grocery | P1 | B empty for intended categories — widen scrape or check filter | Category counts in B |
| PL-03 | Stage 4 relevance too aggressive | P1 | B row count very low — tune embedding threshold | Row count vs raw scrape |
| PL-04 | Friction path accidentally includes 5★ praise | P2 | Stage 2 should drop generic praise in A | Theme audit on A |
| PL-05 | Theme classify offline vs `ai` mode mismatch | P2 | MVP uses **offline/embedding** consistently for A and B | Compare `Primary Theme` columns |
| PL-06 | Export writes B into `Output/blinkit_clean_data.csv` | P0 | **Separate file** `mvp_trust_corpus.csv` only | File diff after pipeline |
| PL-07 | Reddit / live scrape mixed into B without label | P2 | Acceptable if classified — document sources in deck | `Source` column |

---

## 3. Data & Corpus (Phase 1)

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| D-01 | CORPUS B scrape returns 0 rows | P0 | Block deploy; log clear error at API startup | Delete B file, start API |
| D-02 | Positive scrape accidentally merged into CORPUS A | P0 | Discovery friction signals diluted — **never merge** | Diff `blinkit_clean_data.csv` row count vs backup |
| D-03 | CORPUS B has no `Primary Theme` column | P0 | Fail startup or run offline classify before deploy | Inspect CSV headers |
| D-04 | Category has 0 rows in CORPUS B | P1 | Trust score falls back to A-only risk leg or category default; label in sheet | Query empty category slug |
| D-05 | Category has 0 rows in CORPUS A | P1 | Tips/top concern generic; trust score uses B favorable leg only | Synthetic empty A filter |
| D-06 | CORPUS B very small (<50 rows total) | P1 | Scores noisy — disclose in deck; re-scrape with higher `--max-positive` | Row count check |
| D-07 | Generic 5★ reviews ("fast delivery only") in B | P2 | Stage 4 relevance filter should drop; if leaked, neutral theme not positive | Manual theme audit |
| D-08 | Same review text in A and B | INFO | OK if from separate pipeline runs — do not dedupe across corpora for MVP | — |
| D-09 | CSV path wrong on Render | P0 | Startup fails with readable error listing `CORPUS_A_PATH` / `CORPUS_B_PATH` | Deploy without env vars |
| D-10 | Symlink to CORPUS A breaks on Windows/Render | P1 | Use **copy** in repo, not symlink | Fresh clone on Render |

---

## 4. Theme Classification & AI

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| AI-01 | Embedding model fails to load | P1 | Fallback to regex in `themes.py` if ported; log warning | Block model download offline |
| AI-02 | Review below `MIN_THEME_SIMILARITY` | P2 | `Neutral / No Signal` — excluded from favorable/negative counts where appropriate | Sample low-sim review |
| AI-03 | Mixed 4★ review (praise + complaint) | P1 | Single `Primary Theme` wins — may misclassify; acceptable for MVP if disclosed | Read sample 4★ rows |
| AI-04 | Brand mentioned in grocery context | P2 | Category filter should exclude; if not, brand match may pollute electronics keep rate | Search "boat" in grocery rows |
| AI-05 | Re-classify at runtime on Render | P2 | **Avoid** — slow cold start + large deps; classify offline in pipeline | — |
| AI-06 | FAISS evidence optional and missing | P2 | Trust sheet works without snippets; tips still from themes | Disable FAISS |

| AI-07 | Link A Groq key missing | P2 | Discovery dashboard degrades LLM tab; **Link B unaffected** | Streamlit without `GROQ_API_KEY` |
| AI-08 | 384-dim FAISS vs MiniLM mismatch | P1 | Rebuild index after retheme — dimension must match | `retheme_reviews.py` |

---

## 5. Trust Engine & Scoring (Phase 2)

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| S-01 | Merged A+B rows for score (volume bias) | P0 | **Never concat** — use weighted legs separately | Code review |
| S-02 | Trust score only from CORPUS B | P1 | Too optimistic — must use 60/40 blend | Compare A-only vs blend |
| S-03 | Trust score only from CORPUS A | P1 | Too harsh (~33 electronics) — wrong for sheet display | — |
| S-04 | **0 brand mentions** for product | P1 | Keep rate = category estimate from B; `evidence_label` = "Category estimate (no brand-specific mentions)" | Unknown brand in catalog |
| S-05 | **1–2 brand mentions** | P1 | Category-level proxy; label mentions count | Rare brand |
| S-06 | **≥3 brand mentions** | P2 | Brand-level keep rate; full evidence label | boAt |
| S-07 | `keep_rate` computes to 90% raw | P2 | Clamped to **85%** max | Inflate favorable subset |
| S-08 | `keep_rate` computes to 20% raw | P2 | Clamped to **35%** min — still show on PDP with supportive badge tier | Heavy friction brand |
| S-09 | `keep_rate` is `null` / no data | P1 | Do not render `null%` — use category fallback or hide % with "See how" only | Empty corpora for brand |
| S-10 | Known brand + ₹1,999 but trust_score = 58 | P2 | **No** "Safe to repeat" — badge = verify tier if > threshold logic; price ≤2k but score gate fails | Lower trust_score product |
| S-11 | Unknown brand + ₹999 | P2 | No "Safe to repeat" (known brand required); mid/default badge | Add unknown SKU |
| S-12 | Price exactly ₹2,000 | P2 | Treat as repeat-safe tier (≤2000) | Boundary test |
| S-13 | Price exactly ₹2,001 | P2 | Mid tier: "Verify warranty · See how →" | realme Buds |
| S-14 | Price ₹5,001 | P2 | High tier: "Check return policy · See how →" | Hypothetical HDD |
| S-15 | Legacy urgency copy in engine | P0 | Must not appear in API `badge`, `tips`, `verdict` | Grep `urgent` in responses |
| S-16 | Hardcoded keep_rate in API | P0 | All products must compute from corpus | Change CSV, scores should shift |
| S-17 | Tips empty after theme pass | P2 | Default tips: unboxing video, check seal | Product with no A matches |
| S-18 | `top_concern` = "Mixed signals" | P2 | Acceptable when no dominant friction theme | Small category subset |
| S-19 | Product in catalog but category mismatch | P1 | 404 or correct category from catalog lookup | Wrong URL category param |
| S-20 | Shrishti-type high ticket + high friction | INFO | Supportive high-tier badge + strong tips in sheet — **not** "don't buy"; deck says CS out of scope | — |

| S-21 | Signal shown on wrong UI surface (arch §6) | P0 | `trust_score` / `positive_pct` → **See how only**; `keep_rate` → PDP | UI + API field audit |
| S-22 | `top_concern` missing on category strip | P2 | Category endpoint must return `top_concern` from CORPUS A | `GET /category/electronics` |
| S-23 | Keep rate computed from B but tips from A — user confusion | INFO | Valid split; footnote in sheet | See how copy |
| S-24 | Badge uses `buy_smart_score` boost from legacy engine | P2 | Use price-tier + known brand + trust threshold per architecture §5 | JBL badge logic |

---

## 6. Product Catalog (Simulated)

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| C-01 | Product ID not in `PRODUCT_CATALOG` | P0 | HTTP **404** | `GET .../product/unknown-id` |
| C-02 | Category slug typo (`electronic`) | P0 | HTTP **404** | Wrong slug |
| C-03 | Catalog product with no reviews for brand | P1 | Category fallback keep rate + generic tips | New catalog entry |
| C-04 | Duplicate brand across categories | P2 | Scope reviews by **brand + category** | JBL in electronics only |
| C-05 | Emoji / special chars in product name | P2 | JSON UTF-8 safe | API response encoding |
| C-06 | Evaluator asks "is this live Blinkit?" | INFO | Deck + footnote: simulated catalog | — |

---

## 7. API Contract & JSON Schema

From architecture §5 — field-level edge cases.

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| J-01 | Category response missing `guidance` | P1 | Include habit copy: e.g. "Start repeat habits with known brands under ₹2k" | JSON schema check |
| J-02 | Category response missing `review_count` | P2 | Sum or count from CORPUS A+B for category | — |
| J-03 | Product missing `replacement_days` or `warranty` | P1 | Always from catalog — static per SKU | boAt response |
| J-04 | `badge` includes emoji in API vs UI adds emoji | P2 | Consistent — either API returns plain text or UI prepends ✅ once | Visual check |
| J-05 | `positive_pct` > 100 or < 0 | P0 | Clamp 0–100 in engine | Bad data injection |
| J-06 | `mention_count` negative | P0 | Never — minimum 0 | — |
| J-07 | `/products?category=` returns products without trust fields | P1 | List endpoint may return minimal cards; PDP fetch gets full trust | Category page flow |
| J-08 | `/api/health` OK but CSV not loaded | P0 | Health should reflect readiness or fail fast at startup | Kill CSV after boot |
| J-09 | Wrong HTTP method (POST to trust) | P2 | 405 — GET only per architecture | curl -X POST |
| J-10 | Extra unknown JSON fields from Lovable | P2 | Frontend ignores; API need not send | — |

### Contract reference — product endpoint

| Field | Required | PDP | Trust sheet |
|-------|----------|-----|-------------|
| `keep_rate` | Yes | ✅ | ✅ |
| `replacement_days`, `warranty` | Yes | ✅ | optional repeat |
| `badge` | Yes | ✅ | — |
| `trust_score` | Yes | ❌ | ✅ |
| `positive_pct` | Yes | ❌ | ✅ |
| `mention_count`, `evidence_label` | Yes | ❌ | ✅ |
| `tips`, `top_concern` | Yes | ❌ | ✅ |

---

## 8. FastAPI Backend (Phase 3)

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| API-01 | Cold start on Render (>30s) | P1 | Frontend loading skeleton; health eventually 200 | First request after sleep |
| API-02 | CSV load fails at startup | P0 | Process exits non-zero or `/api/health` returns degraded with message | Bad path |
| API-03 | CORS blocked from Vercel | P0 | Add Vercel preview + production origins | Browser console |
| API-04 | CORS blocked from localhost | P0 | Allow `http://localhost:3000` | Local dev |
| API-05 | Concurrent requests | P2 | Read-only CSV in memory — no race | Load test light |
| API-06 | Missing optional field in JSON | P1 | Pydantic defaults or always include null-safe fields | Schema validation |
| API-07 | `tips` array empty | P2 | Return `[]` — frontend shows defaults or hides section | — |
| API-08 | Very long tip string | P2 | Truncate at 4 tips, ~200 chars each | — |
| API-09 | `/products?category=` missing param | P2 | 422 validation error | curl without query |
| API-10 | API up but frontend wrong `NEXT_PUBLIC_API_URL` | P0 | Network error in UI — show retry/friendly error | Wrong env on Vercel |

| API-11 | `trust_service` reloads CSV per request | P2 | Load once at startup (`lifespan` / module init) | Log load count |
| API-12 | Render `data/` path relative to wrong cwd | P1 | Resolve paths from env or `backend/` root | Print cwd on boot |

---

## 9. Frontend — Routes, Components & Lovable (Phase 4–5)

From architecture §9 — map components to API fields.

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| FE-01 | Lovable adds chatbot UI | P0 | Remove — out of scope (Link B ≠ Link A RAG) | Visual QA |
| FE-02 | Lovable adds Amazon compare link | P0 | Remove | Visual QA |
| FE-03 | `positive_pct` shown on PDP line | P0 | Move to trust sheet only | boAt PDP |
| FE-04 | Mock data not replaced after import | P0 | All scores from API | grep `81` hardcoded in frontend |
| FE-05 | Trust sheet navigates to new page | P1 | Bottom sheet / modal on same PDP | Tap "See how" |
| FE-06 | Badge not clickable | P1 | Opens trust sheet | Tap badge |
| FE-07 | API slow — trust row blank | P1 | Loading skeleton, not `undefined%` | Throttle network |
| FE-08 | API 404 for product | P1 | Friendly "Product not found" page | Bad product URL |
| FE-09 | `keep_rate` undefined in response | P1 | Hide % or show "See how for details" | Break backend field |
| FE-10 | Render cold start + client fetch | P1 | Retry once or show "Loading trust signals…" | First load after idle |
| FE-11 | Mobile viewport 320px | P2 | Trust row wraps cleanly | DevTools |
| FE-12 | Lovable exports wrong Next.js structure | P1 | Nest under `AI-Native-MVP/frontend/` per Phase 5 | `npm run build` |
| FE-13 | Urgency copy generated by Lovable | P0 | Remove "10 minutes", "urgent" CTAs | Grep frontend |
| FE-14 | Double fetch on strict mode | P2 | Acceptable for MVP; avoid duplicate sheet state bugs | React strict mode |
| FE-15 | Route `/category/[slug]` slug not in catalog | P1 | 404 or empty state — valid slugs: `electronics`, `personal_care_beauty` | Bad slug URL |
| FE-16 | `BuySmartStrip` shows `keep_rate` instead of category `trust_score` | P1 | Category strip → `trust_score` + `guidance` per architecture §4 | Category page |
| FE-17 | `TrustRow` missing warranty segment | P2 | Format: `{days}-day replacement \| {warranty} \| {keep}% keep this product*` | PDP |
| FE-18 | `TrustSheet` missing footnote | P2 | Review proxy + production swap note | See how |
| FE-19 | Home missing category for catalog entry | P2 | All `PRODUCT_CATALOG` keys reachable from `/` | Navigate beauty |
| FE-20 | Server Component fetch to localhost in prod | P0 | Use `NEXT_PUBLIC_API_URL` — client or edge-safe fetch | Vercel build |
| FE-21 | Component name drift (`ProductPDP` vs Lovable names) | P2 | Wire trust fields in whichever component renders PDP | Code review |

### Component → API mapping (must hold)

| Component | Endpoint | Key fields |
|-----------|----------|------------|
| `BuySmartStrip` | `/api/trust/category/{slug}` | `trust_score`, `guidance`, `top_concern` |
| `TrustRow` | `/api/trust/product/{id}` | `keep_rate`, `replacement_days`, `warranty` |
| `PriceTierBadge` | same | `badge` |
| `TrustSheet` | same | all sheet fields |

---

## 10. Deploy & Ops (Phase 6)

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| DEP-01 | CSV not committed — missing on Render | P0 | Bundle `data/*.csv` in repo or build step | Fresh deploy |
| DEP-02 | Render free tier spins down | P1 | First evaluator click slow — acceptable with skeleton | — |
| DEP-03 | Vercel env not set for production | P0 | Build succeeds but runtime fetch fails | Production URL |
| DEP-04 | HTTP API URL in Vercel env (not HTTPS) | P1 | Mixed content blocked — use `https://` Render URL | Browser console |
| DEP-05 | Link A and Link B same URL | P1 | Separate URLs in deck — Discovery ≠ Buy Smart | — |
| DEP-06 | Streamlit Buy Smart tab confused with Link B | P2 | Deck labels Link A / Link B clearly | — |
| DEP-07 | Vercel preview URL not in CORS allowlist | P1 | Add `*.vercel.app` or specific preview origin | PR preview |
| DEP-08 | Render API sleeps — Vercel SSR timeout | P2 | Client-side fetch with loading state | First visit |
| DEP-09 | `data/` CSV too large for git | P2 | Commit anyway for MVP or use Render disk — document size | `git ls-files data/` |
| DEP-10 | Backend root misconfigured on Render | P0 | Root = `AI-Native-MVP/backend`, not repo root | Render settings |

---

## 11. Link A — Discovery Engine (Streamlit)

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| LA-01 | FAISS index stale after CSV update | P1 | Run `retheme_reviews.py` after corpus change | Search wrong themes |
| LA-02 | Evaluator uses Discovery scores as Buy Smart scores | INFO | Deck: Link A = friction research; Link B = consumer trust | — |
| LA-03 | Buy Smart tab in `app.py` submitted as Link B | P2 | Link B = separate Vercel URL only | — |
| LA-04 | Groq rate limit on dashboard | P2 | Offline classify + cached insights OK for demo | — |
| LA-05 | Positive Experience theme count spikes in A | P1 | Retheme with embedding guards — friction corpus polluted | Theme counts |

---

## 12. Product & Copy Edge Cases

| ID | Scenario | Severity | Expected | Test |
|----|----------|----------|----------|------|
| P-01 | User sees high keep rate + high friction tips | INFO | **Valid** — B drives keep proxy, A drives tips; explain in See how | boAt sheet |
| P-02 | User expects real Blinkit repurchase data | INFO | Footnote on PDP + deck: review proxy in MVP | — |
| P-03 | User buys ₹11k item despite tips | INFO | MVP cannot fix post-purchase CS — out of scope | — |
| P-04 | "Safe to repeat" interpreted as guarantee | INFO | Deck: pre-purchase signal only, not warranty/CS promise | — |
| P-05 | Evaluator compares score to Play Store stars | INFO | Explain theme-based blend, not star average | — |
| P-06 | Habit message vs urgency in interviews | INFO | Research input only — not MVP CTA | — |

---

## 13. Evaluator / Deck Q&A (Prepare Answers)

| Question | Honest answer |
|----------|----------------|
| Why two corpora? | A = friction for discovery/risks; B = favorable signals; merging would bias one story |
| Is keep rate real? | Review proxy in MVP; production = Blinkit repurchase data, same UI |
| Why not one score? | Each signal has a job — keep rate on PDP, trust breakdown in sheet |
| What if no reviews for a SKU? | Category estimate + generic tips; evidence label says so |
| AI-native beyond one number? | Embedding theme classification powers scores, keep proxy, tips, concerns |
| Why not fix CS? | Pre-purchase trust layer only; Shrishti = post-purchase ops gap |
| Why separate deploy links? | Link A = research engine; Link B = product prototype — different stacks and corpora usage |
| Why FastAPI + Next.js not Streamlit for B? | Simulated in-app UX; Streamlit cannot ship as Blinkit mobile prototype |

---

## 14. Pre-Submission Edge-Case Test Script

Run after Phase 5–6. Mark pass/fail.

### Data & API

```bash
# Health
curl -s $API/api/health

# Happy path
curl -s $API/api/trust/product/boat-airdopes-141 | jq .keep_rate,.badge,.trust_score

# Mid tier
curl -s $API/api/trust/product/jbl-go-3 | jq .badge,.price

# 404
curl -s -o /dev/null -w "%{http_code}" $API/api/trust/product/not-real

# Category — architecture contract
curl -s $API/api/trust/category/electronics | jq .trust_score,.guidance,.top_concern,.review_count

# Products list (if implemented)
curl -s "$API/api/trust/products?category=electronics" | jq length
```

| # | Case | Pass? |
|---|------|-------|
| 1 | boat-airdopes-141: `keep_rate` 35–85, badge contains "Safe to repeat" | |
| 2 | jbl-go-3: badge contains "Verify warranty" | |
| 3 | not-real → 404 | |
| 4 | Response has no string "urgent" / "Amazon" | |
| 5 | `tips` length ≤ 4 | |
| 6 | `evidence_label` present when `mention_count` > 0 | |
| 7 | Category response has `guidance` + `top_concern` | |
| 8 | Product response has all contract fields (§7 table) | |

### UI (manual)

| # | Case | Pass? |
|---|------|-------|
| 9 | Category strip: trust score (not keep rate) | |
| 10 | PDP: keep rate visible, positive % **not** on trust row | |
| 11 | See how: trust_score + positive_pct + footnote | |
| 12 | API down: no crash, user-visible error | |
| 13 | No chatbot on any Link B screen | |
| 14 | Link A URL ≠ Link B URL | |

### Architecture sanity

| # | Case | Pass? |
|---|------|-------|
| 15 | Backend loads both CSVs (A + B) | |
| 16 | Discovery CSV row count unchanged after B scrape | |
| 17 | No POST/chat on Link B API | |

---

## 15. Known Acceptable Limitations (Do Not Fix Before Deadline)

Document in deck — not bugs.

- Brand matching is regex, not NER — may miss alternate spellings ("BOAT" vs "boAt" handled; "boat headphones" OK)
- Single primary theme per review — nuance loss on mixed reviews
- Public Play Store reviews ≠ Blinkit buyers only
- Simulated catalog — 6 SKUs, not full assortment
- No personalization (same scores for all users)
- No real-time scrape on API request
- Pet/protein categories in research but may be thin in corpus — strip copy may be generic

- Link B does not call FAISS at runtime unless explicitly added later (architecture §8 optional)
- `GET /products` may return catalog-only rows if not fully implemented — PDP must still work via `/product/{id}`

---

## 16. Priority Fix Order (If Time Is Short)

1. **P0 architecture:** Link B uses A+B; Link A uses A only; separate URLs  
2. **P0 data:** CORPUS B exists, A not contaminated, CSVs on Render  
2. **P0 scoring:** 60/40 blend, no hardcoded keep rates, no urgency copy  
3. **P0 API:** 404s, CORS, health check  
4. **P0 UI:** PDP vs sheet field split, no chatbot/Amazon  
5. **P1 fallbacks:** empty mentions, API loading/error states  
6. **P2 polish:** clamps, tip defaults, mobile wrap  

---

## Related Documents

| File | Role |
|------|------|
| [`implementation.md`](./implementation.md) | Build phases and checklists |
| [`context.md`](./context.md) | UX rules and scoring spec |
| [`architecture.md`](./architecture.md) | System boundaries, API contracts, component map |
| [`problemstatement.txt`](./problemstatement.txt) | Data honesty for deck |
