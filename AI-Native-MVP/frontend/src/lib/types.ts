export type ConfidenceTier = "high" | "medium" | "low";

export interface AnalysisMeta {
  signal_level: "brand" | "category";
  mentions: number;
  confidence: ConfidenceTier;
  data_source: string;
  is_simulated_catalog: boolean;
  category?: string;
  brand?: string;
}

export interface ThemeBreakdownItem {
  theme: string;
  count: number;
}

export interface ReviewSnippet {
  text: string;
  theme: string;
  source: string;
}

export interface CategoryTrust {
  category: string;
  label: string;
  trust_score: number;
  category_trust_score?: number;
  review_count: number;
  reviews_analysed?: number;
  corpus_a_count?: number;
  corpus_b_count?: number;
  analysis_note?: string;
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
  confidence?: ConfidenceTier;
}

export interface ProductTrust extends ProductCard {
  replacement_days: number;
  warranty: string;
  trust_score: number;
  category_trust_score?: number;
  product_delta?: number;
  positive_pct: number;
  mention_count: number;
  display_n?: number;
  tips: string[];
  top_concern: string;
  verdict: string;
  evidence_label: string;
  keep_rate_label?: string;
  analysis_meta?: AnalysisMeta;
  theme_breakdown?: ThemeBreakdownItem[];
  snippets?: ReviewSnippet[];
  demo_mode?: boolean;
}
