import type { CategoryTrust, ProductCard, ProductTrust } from "./types";

export const MOCK_CATEGORIES: CategoryTrust[] = [
  {
    category: "electronics",
    label: "Electronics",
    trust_score: 51,
    review_count: 380,
    guidance: "Start repeat habits with known brands under ₹2k",
    top_concern: "Warranty & Return Anxiety",
  },
  {
    category: "personal_care_beauty",
    label: "Beauty & Personal Care",
    trust_score: 45,
    review_count: 177,
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
      badge: "Verify warranty · See how →",
      trust_score: 51,
    },
    {
      product_id: "jbl-go-3",
      name: "JBL Go 3 Portable Bluetooth Speaker",
      brand: "jbl",
      price: 2969,
      emoji: "🔊",
      category: "electronics",
      keep_rate: 75,
      badge: "Verify warranty · See how →",
      trust_score: 51,
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
      trust_score: 55,
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
      trust_score: 48,
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
      badge: "Check seal · See how →",
      trust_score: 45,
    },
    {
      product_id: "minimalist-serum",
      name: "Minimalist Niacinamide 10% Face Serum",
      brand: "minimalist",
      price: 570,
      emoji: "💧",
      category: "personal_care_beauty",
      keep_rate: 70,
      badge: "Verify batch · See how →",
      trust_score: 42,
    },
  ],
};

export const MOCK_PRODUCT_DETAIL: Record<string, ProductTrust> = {
  "boat-airdopes-141": {
    product_id: "boat-airdopes-141",
    name: "boAt Airdopes 141",
    brand: "boat",
    price: 1299,
    category: "electronics",
    replacement_days: 7,
    warranty: "1 year manufacturer warranty",
    emoji: "🎧",
    keep_rate: 81,
    trust_score: 51,
    positive_pct: 50,
    mention_count: 16,
    badge: "Verify warranty · See how →",
    tips: [
      "Known brand — lower counterfeit risk on Blinkit",
      "Record unboxing video — helps if you need a return",
    ],
    top_concern: "Warranty & Return Anxiety",
    verdict: "Buy with checks — see warranty",
    evidence_label: "Based on 16 public review mentions",
  },
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
      return {
        ...card,
        replacement_days: 7,
        warranty: "1 year manufacturer warranty",
        positive_pct: 50,
        mention_count: 12,
        tips: ["Check return policy before opening", "Keep packaging for warranty claims"],
        top_concern: "Warranty & Return Anxiety",
        verdict: "Buy with checks — see warranty",
        evidence_label: "Based on public review mentions",
      };
    }
  }
  return undefined;
}
