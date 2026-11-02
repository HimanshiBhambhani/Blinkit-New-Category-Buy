import { notFound } from "next/navigation";
import { BackHeader } from "@/components/BlinkitHeader";
import { BottomNav } from "@/components/BottomNav";
import { BuySmartStrip } from "@/components/BuySmartStrip";
import { PageFrame } from "@/components/PageFrame";
import { ProductCardItem } from "@/components/ProductCard";
import { getCategory, getProducts } from "@/lib/api";

interface CategoryPageProps {
  params: Promise<{ slug: string }>;
}

export function generateStaticParams() {
  return [{ slug: "electronics" }, { slug: "personal_care_beauty" }];
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { slug } = await params;
  const [category, products] = await Promise.all([
    getCategory(slug),
    getProducts(slug),
  ]);

  if (!category) notFound();

  return (
    <PageFrame>
      <BackHeader href="/" title={category.label} />
      <div className="no-scrollbar min-h-0 flex-1 overflow-y-auto pb-[72px]">
        <BuySmartStrip category={category} />
        <main className="px-container-padding pt-3">
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
