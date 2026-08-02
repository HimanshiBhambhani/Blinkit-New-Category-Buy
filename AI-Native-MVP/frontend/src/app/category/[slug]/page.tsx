export const dynamic = "force-dynamic";

import { notFound } from "next/navigation";
import { BackHeader } from "@/components/BlinkitHeader";
import { BottomNav } from "@/components/BottomNav";
import { BuySmartStrip } from "@/components/BuySmartStrip";
import { PageFrame } from "@/components/PageFrame";
import { ProductCardItem } from "@/components/ProductCard";
import { getCategory, getProducts } from "@/lib/api";
import { getCategoryFilters } from "@/lib/stitchAssets";

interface CategoryPageProps {
  params: Promise<{ slug: string }>;
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { slug } = await params;
  const [category, products] = await Promise.all([
    getCategory(slug),
    getProducts(slug),
  ]);

  if (!category) notFound();

  const filters = getCategoryFilters(slug);

  return (
    <PageFrame>
      <BackHeader href="/" showSearch title={category.label} />
      <div className="no-scrollbar min-h-0 flex-1 overflow-y-auto pb-[72px]">
        <BuySmartStrip category={category} />
        <main className="px-container-padding">
          <div className="mb-3 flex snap-x gap-2 overflow-x-auto pb-1">
            {filters.map((filter, index) => (
              <button
                className={`snap-start shrink-0 rounded-full border px-3 py-1 text-trust ${
                  index === 0
                    ? "border-secondary bg-blinkit-trust-bg text-secondary"
                    : "border-outline-variant text-on-surface-variant"
                }`}
                key={filter}
                type="button"
              >
                {filter}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-2 gap-grid-gap">
            {products.map((product) => (
              <ProductCardItem key={product.product_id} product={product} />
            ))}
          </div>
        </main>
      </div>
      <BottomNav />
    </PageFrame>
  );
}
