import { notFound } from "next/navigation";
import { Icon } from "@/components/Icon";
import { PdpHeader } from "@/components/BlinkitHeader";
import { PageFrame } from "@/components/PageFrame";
import { ProductImage } from "@/components/ProductImage";
import { SeeHowLink, TrustBadge } from "@/components/TrustBadge";
import { TrustRow } from "@/components/TrustRow";
import { formatPrice, getProduct } from "@/lib/api";
import { ALL_PRODUCT_IDS } from "@/lib/mockTrust";
import { discountPct, getProductVisual } from "@/lib/stitchAssets";

interface ProductPageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return ALL_PRODUCT_IDS.map((id) => ({ id }));
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;
  const product = await getProduct(id);
  if (!product) notFound();

  const visual = getProductVisual(id);
  const mrp = visual?.mrp ?? Math.round(product.price * 1.4);
  const off = discountPct(product.price, mrp);

  return (
    <PageFrame>
      <PdpHeader href={`/category/${product.category}`} />
      <main className="no-scrollbar min-h-0 flex-1 overflow-y-auto pb-20">
        <div className="relative aspect-square w-full bg-surface-container">
          <ProductImage
            alt={product.name}
            emoji={product.emoji}
            productId={id}
            variant="pdp"
          />
          <div className="absolute left-3 top-3 flex items-center gap-0.5 rounded-md bg-surface-container-lowest px-1.5 py-0.5 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
            <Icon name="timer" size={14} />
            <span className="text-caps text-on-surface">10 MINS</span>
          </div>
        </div>

        <div className="space-y-3 bg-surface-container-lowest px-container-padding py-4">
          <h1 className="line-clamp-3 text-headline-sm leading-snug text-on-surface">
            {product.name}
          </h1>
          <p className="text-trust text-on-surface-variant">{visual?.subtitle ?? "1 unit"}</p>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-price text-on-surface">{formatPrice(product.price)}</span>
            {off > 0 ? (
              <>
                <span className="text-body text-on-surface-variant line-through">
                  {formatPrice(mrp)}
                </span>
                <span className="rounded-sm bg-secondary-container px-1.5 py-0.5 text-caps text-on-secondary-container">
                  {off}% OFF
                </span>
              </>
            ) : null}
          </div>

          <TrustBadge badge={product.badge} productId={product.product_id} />
          <TrustRow product={product} />
          <SeeHowLink productId={product.product_id} />
        </div>

        {visual?.description ? (
          <>
            <div className="h-2 bg-surface-container" />
            <div className="space-y-3 bg-surface-container-lowest px-container-padding py-4">
              <h2 className="text-headline-sm text-on-surface">Product Details</h2>
              <div>
                <h3 className="text-trust font-semibold text-on-surface">Description</h3>
                <p className="mt-1 text-trust leading-relaxed text-on-surface-variant">
                  {visual.description}
                </p>
              </div>
              {visual.features?.length ? (
                <div>
                  <h3 className="text-trust font-semibold text-on-surface">Key Features</h3>
                  <ul className="mt-1 list-inside list-disc space-y-0.5 text-trust text-on-surface-variant">
                    {visual.features.map((feature) => (
                      <li key={feature}>{feature}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          </>
        ) : null}
      </main>

      <div className="absolute bottom-0 left-0 z-30 w-full border-t border-surface-variant bg-surface-container-lowest px-container-padding py-2.5 shadow-[0_-2px_10px_rgba(0,0,0,0.05)]">
        <button
          className="w-full rounded-lg bg-blinkit-green py-2.5 text-headline-sm font-semibold text-white shadow-md active:scale-[0.98]"
          type="button"
        >
          ADD TO CART
        </button>
      </div>
    </PageFrame>
  );
}
