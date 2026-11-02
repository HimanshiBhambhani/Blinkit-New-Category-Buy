/**
 * Visual assets extracted from stitch_blinkit_buy_smart_prototype/
 * Only include `image` when the Stitch export matches this exact product.
 */

export const STITCH_REF = {
  home: "/stitch/01-home.png",
  categoryElectronics: "/stitch/02-category-electronics.png",
  pdpBoat: "/stitch/03-pdp-boat.png",
  seeHow: "/stitch/04-see-how.png",
} as const;

/**
 * Prefix for raw asset URLs used outside next/image (e.g. CSS background-image),
 * which do NOT get Next.js basePath applied automatically. Empty in dev.
 */
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

/** Prepend the deploy basePath to a public asset path (for CSS/background usage). */
export function assetUrl(path: string): string {
  return `${BASE_PATH}${path}`;
}

export const BLINKIT_LOGO = "/brand/blinkit-logo.png";

export const BANNER_HERO = "/brand/banner-hero.png";

/** boAt Airdopes 141 — verified from stitch electronics grid + PDP exports */
const BOAT_LIST_IMAGE = "/products/boat-airdopes-141.png";

const BOAT_PDP_IMAGE = "/products/boat-airdopes-141-pdp.png";

export const HOME_CATEGORIES = [
  {
    slug: "electronics",
    label: "Electronics & Accessories",
    image: "/categories/electronics.png",
    href: "/category/electronics",
  },
  {
    slug: "personal_care_beauty",
    label: "Beauty & Personal Care",
    image: "/categories/personal_care_beauty.png",
    href: "/category/personal_care_beauty",
  },
  {
    slug: "pharmacy",
    label: "Pharmacy",
    image: "/categories/pharmacy.png",
    href: null,
  },
  {
    slug: "toys",
    label: "Toys & Games",
    image: "/categories/toys.png",
    href: null,
  },
] as const;

export interface StitchProductVisual {
  /** Grid / card thumbnail */
  listImage?: string;
  /** PDP hero — only when different from list */
  pdpImage?: string;
  mrp: number;
  subtitle: string;
  description?: string;
  features?: string[];
}

export const PRODUCT_VISUALS: Record<string, StitchProductVisual> = {
  "boat-airdopes-141": {
    listImage: BOAT_LIST_IMAGE,
    pdpImage: BOAT_PDP_IMAGE,
    mrp: 4490,
    subtitle: "Black, 1 unit",
    description:
      "boAt Airdopes 141 true wireless earbuds with 42H playtime, beast mode (low latency up to 80ms) for gaming, ENx tech, ASAP charge...",
    features: [
      "Playback — Up to 42 Hours",
      "Clear Voice Calls — ENx Tech",
      "Low Latency — BEAST Mode",
    ],
  },
  "jbl-go-3": {
    listImage: "/products/jbl-go-3.png",
    pdpImage: "/products/jbl-go-3.png",
    mrp: 3999,
    subtitle: "Blue, 1 unit",
    description:
      "JBL Go 3 portable Bluetooth speaker with bold JBL Pro Sound, IP67 waterproof and dustproof rating, and integrated loop for easy carrying.",
  },
  "apple-earpods": {
    listImage: "/products/apple-earpods.png",
    pdpImage: "/products/apple-earpods.png",
    mrp: 2000,
    subtitle: "USB-C, 1 unit",
    description:
      "Apple EarPods with USB-C connector. In-ear design with built-in remote and microphone for calls and music control.",
  },
  "realme-buds": {
    listImage: "/products/realme-buds.png",
    pdpImage: "/products/realme-buds.png",
    mrp: 3999,
    subtitle: "Black, 1 unit",
    description:
      "realme Buds T310 true wireless earbuds with active noise cancellation, long battery life, and low-latency gaming mode.",
  },
  "cerave-moisturizer": {
    listImage: "/products/cerave-moisturizer.png",
    pdpImage: "/products/cerave-moisturizer.png",
    mrp: 469,
    subtitle: "50 ml",
    description:
      "CeraVe Moisturizing Cream with ceramides and hyaluronic acid for dry to very dry skin. Moisturises and helps restore the protective skin barrier. Fragrance free.",
  },
  "minimalist-serum": {
    listImage: "/products/minimalist-serum.png",
    pdpImage: "/products/minimalist-serum.png",
    mrp: 599,
    subtitle: "30 ml",
    description:
      "Minimalist Niacinamide 10% Face Serum with matmarine, zinc and acetyl glucosamine. Regulates sebum and evens skin tone. For all skin types.",
  },
};

export function discountPct(price: number, mrp: number): number {
  if (mrp <= price) return 0;
  return Math.round(((mrp - price) / mrp) * 100);
}

export function getProductVisual(productId: string): StitchProductVisual | undefined {
  return PRODUCT_VISUALS[productId];
}

export function getListImage(productId: string): string | undefined {
  return PRODUCT_VISUALS[productId]?.listImage;
}

export function getPdpImage(productId: string): string | undefined {
  const visual = PRODUCT_VISUALS[productId];
  return visual?.pdpImage ?? visual?.listImage;
}

/** Blinkit screenshots — crop to the left product panel only */
const SCREENSHOT_IMAGES = new Set([
  "/products/jbl-go-3.png",
  "/products/realme-buds.png",
  "/products/cerave-moisturizer.png",
  "/products/minimalist-serum.png",
]);

export function isProductScreenshot(src: string): boolean {
  return SCREENSHOT_IMAGES.has(src);
}
