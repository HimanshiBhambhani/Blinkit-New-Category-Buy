import type { CategoryTrust, ProductCard, ProductTrust } from "./types";

export const MOCK_CATEGORIES: CategoryTrust[] = [
  {
    category: "electronics",
    label: "Electronics",
    trust_score: 51,
    category_trust_score: 51,
    review_count: 380,
    reviews_analysed: 380,
    corpus_a_count: 353,
    corpus_b_count: 27,
    analysis_note: "Category-level score from 353 friction (CORPUS A) + 27 favorable (CORPUS B) reviews",
    guidance: "Start repeat habits with known brands under ₹2k",
    top_concern: "Warranty & Return Anxiety",
  },
  {
    category: "personal_care_beauty",
    label: "Beauty & Personal Care",
    trust_score: 45,
    category_trust_score: 45,
    review_count: 177,
    reviews_analysed: 177,
    guidance: "Start repeat habits with known brands under ₹2k",
    top_concern: "Dark Store Storage Concerns",
  },
];

export const MOCK_PRODUCTS: Record<string, ProductCard[]> = {
  electronics: [
    {
      product_id: "boat-airdopes-141",
      name: "boAt Airdopes 141",
      brand: "boat",
      price: 1299,
      emoji: "🎧",
      category: "electronics",
      keep_rate: 81,
      badge: "Safe to repeat · See how →",
      trust_score: 59,
      confidence: "high",
    },
    {
      product_id: "jbl-go-3",
      name: "JBL Go 3 Portable Bluetooth Speaker",
      brand: "jbl",
      price: 2969,
      emoji: "🔊",
      category: "electronics",
      keep_rate: 75,
      badge: "Category estimate · See how →",
      trust_score: 51,
      confidence: "low",
    },
    {
      product_id: "apple-earpods",
      name: "Apple EarPods (USB-C)",
      brand: "apple",
      price: 1649,
      emoji: "🎵",
      category: "electronics",
      keep_rate: 88,
      badge: "Safe to repeat · See how →",
      trust_score: 59,
      confidence: "medium",
    },
    {
      product_id: "realme-buds",
      name: "realme Buds T310 TWS Earbuds",
      brand: "realme",
      price: 2199,
      emoji: "🎧",
      category: "electronics",
      keep_rate: 72,
      badge: "Verify warranty · See how →",
      trust_score: 55,
      confidence: "medium",
    },
  ],
  personal_care_beauty: [
    {
      product_id: "cerave-moisturizer",
      name: "CeraVe Moisturizing Cream (with Ceramides)",
      brand: "cerave",
      price: 422,
      emoji: "🧴",
      category: "personal_care_beauty",
      keep_rate: 78,
      badge: "Category estimate · See how →",
      trust_score: 47,
      confidence: "low",
    },
    {
      product_id: "minimalist-serum",
      name: "Minimalist Niacinamide 10% Face Serum",
      brand: "minimalist",
      price: 570,
      emoji: "💧",
      category: "personal_care_beauty",
      keep_rate: 70,
      badge: "Verify warranty · See how →",
      trust_score: 46,
      confidence: "medium",
    },
  ],
};

const BOAT_MOCK_DETAIL: ProductTrust = {
  product_id: "boat-airdopes-141",
  name: "boAt Airdopes 141",
  brand: "boat",
  price: 1299,
  category: "electronics",
  replacement_days: 7,
  warranty: "1 year manufacturer warranty",
  emoji: "🎧",
  keep_rate: 81,
  trust_score: 59,
  category_trust_score: 51,
  product_delta: 8,
  positive_pct: 50,
  mention_count: 16,
  display_n: 16,
  badge: "Safe to repeat · See how →",
  confidence: "high",
  tips: [
    "Known brand — lower counterfeit risk on Blinkit",
    "Record unboxing video — 12 mentions cite return/support friction",
  ],
  top_concern: "Warranty & Return Anxiety",
  verdict: "Okay with caution",
  evidence_label: "Keep-rate proxy from 16 public review mentions",
  keep_rate_label: "Review-sentiment proxy (not Blinkit repurchase)",
  analysis_meta: {
    signal_level: "brand",
    mentions: 16,
    confidence: "high",
    data_source: "public_reviews",
    is_simulated_catalog: true,
    category: "electronics",
    brand: "boat",
  },
  snippets: [],
  snippets_note:
    "No product-specific positive Blinkit reviews in our public corpus yet. Trust score uses category and brand signals instead.",
};

export const MOCK_PRODUCT_DETAIL: Record<string, ProductTrust> = {
  "boat-airdopes-141": BOAT_MOCK_DETAIL,
};

export function mockCategory(slug: string): CategoryTrust | undefined {
  return MOCK_CATEGORIES.find((c) => c.category === slug);
}

export function mockProducts(slug: string): ProductCard[] {
  return MOCK_PRODUCTS[slug] ?? [];
}

export function mockProduct(id: string): ProductTrust | undefined {
  if (MOCK_PRODUCT_DETAIL[id]) return MOCK_PRODUCT_DETAIL[id];
  for (const list of Object.values(MOCK_PRODUCTS)) {
    const card = list.find((p) => p.product_id === id);
    if (card) {
      const low = card.confidence === "low";
      return {
        ...card,
        replacement_days: 7,
        warranty: "1 year manufacturer warranty",
        positive_pct: 50,
        mention_count: low ? 2 : 12,
        category_trust_score: card.trust_score - (low ? 0 : 4),
        product_delta: low ? 0 : 4,
        tips: ["Check return policy before opening", "Keep packaging for warranty claims"],
        top_concern: "Warranty & Return Anxiety",
        verdict: "Buy with checks — see warranty",
        evidence_label: low
          ? "Category keep-rate proxy (no brand-specific mentions)"
          : "Based on public review mentions",
        keep_rate_label: "Review-sentiment proxy (not Blinkit repurchase)",
        analysis_meta: {
          signal_level: low ? "category" : "brand",
          mentions: low ? 2 : 12,
          confidence: card.confidence ?? "medium",
          data_source: "public_reviews",
          is_simulated_catalog: true,
        },
        snippets: [],
        snippets_note:
          "No product-specific positive Blinkit reviews in our public corpus yet. Trust score uses category and brand signals instead.",
      };
    }
  }
  return undefined;
}
