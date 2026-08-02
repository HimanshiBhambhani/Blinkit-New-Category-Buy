import {
  mockCategory,
  mockProduct,
  mockProducts,
  MOCK_CATEGORIES,
} from "./mockTrust";
import type { CategoryTrust, ProductCard, ProductTrust } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string): Promise<T | null> {
  try {
    const res = await fetch(`${API}${path}`, { cache: "no-store" });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export async function getCategories(): Promise<CategoryTrust[]> {
  const data = await fetchJson<CategoryTrust[]>("/api/trust/categories");
  return data ?? MOCK_CATEGORIES;
}

export async function getCategory(slug: string): Promise<CategoryTrust | null> {
  const data = await fetchJson<CategoryTrust>(`/api/trust/category/${slug}`);
  return data ?? mockCategory(slug) ?? null;
}

export async function getProducts(category: string): Promise<ProductCard[]> {
  const data = await fetchJson<ProductCard[]>(
    `/api/trust/products?category=${encodeURIComponent(category)}`,
  );
  return data ?? mockProducts(category);
}

export async function getProduct(id: string): Promise<ProductTrust | null> {
  const data = await fetchJson<ProductTrust>(`/api/trust/product/${id}`);
  if (data) return data;
  const mock = mockProduct(id);
  if (mock) return { ...mock, demo_mode: true };
  return null;
}

export function formatPrice(price: number): string {
  return `₹${price.toLocaleString("en-IN")}`;
}
