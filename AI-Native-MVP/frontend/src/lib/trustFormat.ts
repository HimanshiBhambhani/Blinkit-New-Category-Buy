import type { ConfidenceTier, ProductTrust } from "./types";

export const LINK_A_DISCOVERY_URL =
  "https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/";

export function getConfidence(product: ProductTrust): ConfidenceTier {
  return product.analysis_meta?.confidence ?? "medium";
}

export function isLowConfidence(product: ProductTrust): boolean {
  return getConfidence(product) === "low";
}

export function formatKeepRate(product: ProductTrust): string {
  const suffix = isLowConfidence(product) ? " (est.)" : "";
  return `${product.keep_rate}%${suffix}`;
}

export function formatPositivePct(product: ProductTrust): string {
  if (isLowConfidence(product)) return `Est. ${product.positive_pct}%`;
  return `${product.positive_pct}%`;
}

export function formatMentionCount(product: ProductTrust): string {
  if (isLowConfidence(product)) {
    return "Low sample — category estimate";
  }
  const n = product.display_n ?? product.mention_count;
  return `${n} brand mention${n === 1 ? "" : "s"} in corpus`;
}

export function confidenceBadgeLabel(tier: ConfidenceTier): string {
  switch (tier) {
    case "high":
      return "High confidence";
    case "medium":
      return "Medium confidence";
    case "low":
      return "Low sample";
  }
}
