# Google Stitch Prompt — Buy Smart MVP (Blinkit Trust Layer)

> **How to use:** Attach your Blinkit mobile screenshot, then paste everything below into Stitch.  
> Replace `{API}` with `http://localhost:8000` (local) or your Render URL (deployed).

---

## ATTACHED REFERENCE (READ FIRST)

I have attached a **real Blinkit mobile app screenshot**. Use it for colors, header shape, card style, ADD button, and green/yellow brand accents.

**Do not invent a generic e-commerce UI.** Buy Smart sits inside the Blinkit shell.

---

## NON-NEGOTIABLE FRAME & TYPOGRAPHY (PROJECT RULE)

**Every screen must use the exact same canvas — no exceptions:**

| Rule | Value |
|------|--------|
| **Frame width** | **1920px** |
| **Frame height** | **1080px** |
| **Minimum font size** | **26px** — **no text anywhere may be below 26px** (labels, footnotes, badges, pipes, buttons, captions) |
| **Artboards** | Generate **4 separate frames**, each **1920×1080px** |

**Layout within 1920×1080:**  
Center the Blinkit app UI in a **vertical phone column** (~480–520px wide, full 1080px height) in the middle of the canvas, OR scale the mobile layout proportionally so it fills the frame — but **all four pages must use identical outer dimensions (1920×1080)** and the same column width/position so they align in Figma/Stitch side-by-side.

**Typography scale (all ≥ 26px):**
| Element | Size |
|---------|------|
| Page / section titles | **36–40px** semibold |
| Product name | **34px** semibold |
| Price | **36px** bold |
| Body / trust row / guidance | **26px** regular |
| Footnotes / evidence | **26px** regular (never smaller) |
| Badge / CTA | **28px** medium |
| Buy Smart score number | **48px** bold |

---

## PROJECT BRIEF

Build a **Blinkit quick-commerce prototype** with **4 full pages** (not 3 — the 4th is mandatory) for **“Buy Smart”** — a pre-purchase trust layer for **repeat non-grocery habits**.

This is **NOT**: chatbot, Amazon compare, urgency-first CTAs.  
This **IS**: 4 navigable pages, REST API data, habit/trust copy.

**Critical:** “See how” is a **full dedicated page (Screen 4)** — **NOT** a bottom sheet, modal, or overlay. Tapping the badge on PDP **navigates** to Screen 4.

---

## TECH STACK

- Next.js 14+ App Router, TypeScript, Tailwind CSS
- `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`)
- Each page root wrapper: `width: 1920px; height: 1080px; overflow: hidden;`

**Routes (exact — 4 pages):**

| # | Route | Screen |
|---|-------|--------|
| 1 | `/` | Home — category grid |
| 2 | `/category/[slug]` | Category + Buy Smart strip |
| 3 | `/product/[id]` | Product detail (PDP) |
| 4 | `/product/[id]/see-how` | **Trust breakdown (See how)** — **REQUIRED 4th page** |

Slugs: `electronics`, `personal_care_beauty`  
Product IDs: `boat-airdopes-141`, `jbl-go-3`, `apple-earpods`, `realme-buds`, `cerave-moisturizer`, `minimalist-serum`

---

## SHARED SHELL (ALL 4 PAGES — IDENTICAL)

Reuse the same components on every page so all frames look like one app:

1. **Outer canvas:** 1920×1080px, `#FFFFFF` or screenshot background
2. **Inner column:** centered, fixed width (e.g. 500px), 1080px tall, white background, subtle shadow optional
3. **BlinkitHeader** — location + search (match screenshot), **26px** min text
4. **Back button** on pages 2–4 (← **28px** touch target, min 44×44px)

**Do not change column width or header height between pages.**

---

## SCREEN 1 — HOME (`/`) — 1920×1080

### Content (inside centered column)
1. BlinkitHeader
2. Title: `Shop beyond groceries` — **36px** semibold
3. Subtitle: `Build repeat habits with Buy Smart` — **26px** secondary
4. **2 category tiles** (stacked or 2-col within column):
   - **Electronics** → `/category/electronics`
   - **Beauty & Personal Care** → `/category/personal_care_beauty`
5. Tile label: **28px** white on gradient overlay

### Optional API
`GET {API}/api/trust/categories` on mount.

---

## SCREEN 2 — CATEGORY (`/category/[slug]`) — 1920×1080

### Fetch
- `GET {API}/api/trust/category/{slug}`
- `GET {API}/api/trust/products?category={slug}`

### Content
1. Header: ← Back to Home + `{label}` — **34px**
2. **Buy Smart strip** (light green `#F0FAF0`, padding 24px):
   - `BUY SMART` — **26px** uppercase green
   - Score circle: **`{trust_score}`** — **48px** bold
   - `{guidance}` — **26px** — e.g. `Start repeat habits with known brands under ₹2k`
   - `Top concern: {top_concern}` — **26px** gray
3. **Product list** (scroll inside column if needed):
   - Card: image placeholder, name **26px**, price **28px** bold `₹1,299`
   - Mini line: `{keep_rate}% keep this product` — **26px** green
   - ADD button — **26px** white on green pill
   - Tap card → `/product/{product_id}`

---

## SCREEN 3 — PDP (`/product/[id]`) — 1920×1080

### Fetch
- `GET {API}/api/trust/product/{id}`

### Content
1. Header: ← Back to category
2. Hero image placeholder (square, emoji centered)
3. **Name** — **34px** | **Price** — **36px** bold `₹1,299`
4. Delivery: `Delivery in 10 minutes` — **26px** gray (not the trust headline)
5. **Trust row** — **26px**, pipes `|`:
   ```
   7-day replacement | 1 year manufacturer warranty | 81% keep this product*
   ```
   **Only keep_rate here — NO trust_score, NO positive_pct on this line.**
6. Footnote — **26px** gray:
   `*Keep rate estimated from public review signals. Production uses Blinkit repurchase data.`
7. **Badge button** (full width, tappable) — **28px**:
   - Display API `badge` text e.g. `Verify warranty · See how →`
   - ✅ prefix only if badge contains "Safe to repeat"
   - **onClick → navigate to `/product/{id}/see-how`** — **NOT a modal**
8. Link — **26px** green underline:
   `See how trust is calculated →` — **same navigation to Screen 4**
9. **ADD TO CART** — full width green, **28px** (inert)

---

## SCREEN 4 — SEE HOW / TRUST DETAIL (`/product/[id]/see-how`) — 1920×1080

**This is the missing page. Generate it as a full page identical in frame size to Screens 1–3.**

### Fetch
- Same as PDP: `GET {API}/api/trust/product/{id}`

### Navigation
- Entry: from Screen 3 badge OR “See how trust is calculated” link
- Back ← returns to `/product/{id}` (Screen 3)
- Forward deep-link URL must work: `/product/boat-airdopes-141/see-how`

### Content (scroll inside centered column if needed)

1. **Header**
   - ← Back to product — **26px**
   - Title: **`How Buy Smart works`** — **36px** semibold
   - Subtitle: `{name}` · `{brand}` — **26px** gray

2. **Score cards** (stack vertically, 16px gap, each card white with border):

   | Card title | Value | Style |
   |------------|-------|--------|
   | Trust score | `{trust_score}` / 100 | **48px** number + progress bar |
   | Keep rate | `{keep_rate}%` keep this product | **34px** |
   | Positive mentions | `{positive_pct}%` positive mentions in our data | **34px** |

3. **Evidence block** — **26px**:
   - `{evidence_label}` — e.g. `Based on 16 public review mentions`
   - `{mention_count} mentions · {category} · {brand}`

4. **Tips section**
   - Heading: `Tips before you buy` — **32px** semibold
   - Bullets from `tips[]` — **26px** each, green bullet

5. **Top concern section**
   - Heading: `Top concern from reviews` — **32px** semibold
   - `{top_concern}` — **26px** sentence case

6. **Verdict line** — **26px** italic gray:
   - `{verdict}` — e.g. `Buy with checks — see warranty`

7. **Footnote block** (top border, padding 24px) — **26px** gray, multi-line:
   ```
   Keep rate = review proxy in MVP (favorable sentiment in brand mentions).
   Production: Blinkit internal repurchase data — same UI, different source.
   Trust score = 60% favorable signals + 40% friction risk themes from public reviews.
   ```

8. **Sticky bottom (optional):** `Back to {product name}` button → Screen 3

### Screen 4 rules
- **Full page only** — no sheet, no dialog, no overlay
- Show `trust_score` and `positive_pct` **only on this page** (and not on PDP trust row)
- Same 1920×1080 frame and centered column as pages 1–3

---

## USER FLOW (MUST WORK IN STITCH PREVIEW)

```
Screen 1 Home
    → tap Electronics
Screen 2 Category
    → tap boAt card
Screen 3 PDP
    → tap badge OR "See how trust is calculated"
Screen 4 See how          ← YOU MUST GENERATE THIS PAGE
    → tap Back
Screen 3 PDP
```

Stitch must output **4 clickable frames/pages**, not 3.

---

## API — FULL PRODUCT PAYLOAD (Screens 3 & 4)

```json
{
  "product_id": "boat-airdopes-141",
  "name": "boAt Airdopes 141",
  "brand": "boat",
  "price": 1299,
  "category": "electronics",
  "replacement_days": 7,
  "warranty": "1 year manufacturer warranty",
  "emoji": "🎧",
  "keep_rate": 81,
  "trust_score": 51,
  "positive_pct": 50.0,
  "mention_count": 16,
  "badge": "Verify warranty · See how →",
  "tips": [
    "Known brand — lower counterfeit risk on Blinkit",
    "Record unboxing video — helps if you need a return"
  ],
  "top_concern": "Warranty & Return Anxiety",
  "verdict": "Buy with checks — see warranty",
  "evidence_label": "Based on 16 public review mentions"
}
```

```typescript
const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
// Screen 3 & 4
const product = await fetch(`${API}/api/trust/product/${id}`, { cache: "no-store" });
```

---

## MOCK DATA (if API down)

Use same JSON for `boat-airdopes-141`, `jbl-go-3`, `cerave-moisturizer` as in previous spec. Screens 3 and 4 share one fetch.

---

## COPY GUARDRAILS

**NEVER:** chat UI, urgency CTAs, “Don't buy” / “Skip” / “Use Amazon”, trust_score on PDP row, bottom sheet instead of page 4, font < 26px, frames not 1920×1080.

**ALWAYS:** 4 pages same size, navigate to `/product/[id]/see-how`, habit/repeat copy, keep_rate on PDP only.

---

## FILE STRUCTURE

```
app/
  page.tsx                         # Screen 1 — 1920×1080 wrapper
  category/[slug]/page.tsx         # Screen 2
  product/[id]/page.tsx            # Screen 3 — PDP
  product/[id]/see-how/page.tsx    # Screen 4 — REQUIRED
components/
  PageFrame.tsx                    # Enforces 1920×1080 + centered column
  BlinkitHeader.tsx
  BuySmartStrip.tsx
  ProductCard.tsx
  TrustRow.tsx
  TrustBadge.tsx                   # Links to see-how route (NOT modal)
  TrustDetailContent.tsx           # Screen 4 body
lib/
  api.ts
  mockTrust.ts
  types.ts
```

---

## INTERACTIONS CHECKLIST

- [ ] **4 frames**, each **1920×1080px**
- [ ] **No font below 26px** on any frame
- [ ] Home → Category → PDP → **See how page** → Back to PDP
- [ ] See how is a **route**, not a bottom sheet
- [ ] All pages share same column width and header
- [ ] PDP shows keep_rate only; trust_score + positive_pct on Screen 4 only
- [ ] Loading skeletons use 26px+ placeholder bars

---

## QUALITY BAR

1. **4 pages** exported, same **1920×1080** dimensions  
2. **26px minimum** typography strictly enforced  
3. **Screen 4 exists** and is reachable from Screen 3  
4. Blinkit visual match from screenshot  
5. Next.js export-ready for `frontend/` import  

**Generate all 4 complete pages now. Do not stop at 3 pages. Do not use a bottom sheet for See how — use Screen 4 at `/product/[id]/see-how`.**
