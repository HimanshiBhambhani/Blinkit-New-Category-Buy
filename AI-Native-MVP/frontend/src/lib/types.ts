export interface CategoryTrust {
  category: string;
  label: string;
  trust_score: number;
  review_count: number;
  guidance: string;
  top_concern: string;
}

export interface ProductCard {
  product_id: string;
  name: string;
  brand: string;
  price: number;
  emoji: string;
  category: string;
  keep_rate: number;
  badge: string;
  trust_score: number;
}

export interface ProductTrust extends ProductCard {
  replacement_days: number;
  warranty: string;
  trust_score: number;
  positive_pct: number;
  mention_count: number;
  tips: string[];
  top_concern: string;
  verdict: string;
  evidence_label: string;
}
