import Link from "next/link";
import { Icon } from "@/components/Icon";
import { ProductImage } from "@/components/ProductImage";
import { formatPrice } from "@/lib/api";
import { discountPct, getProductVisual } from "@/lib/stitchAssets";
import type { ProductCard } from "@/lib/types";

interface ProductCardProps {
  product: ProductCard;
}

function cardKeepLabel(product: ProductCard): string {
  const est = product.confidence === "low" ? " (est.)" : "";
  return `${product.keep_rate}% keep*${est}`;
}

export function ProductCardItem({ product }: ProductCardProps) {
  const visual = getProductVisual(product.product_id);
  const mrp = visual?.mrp ?? Math.round(product.price * 1.4);
  const off = discountPct(product.price, mrp);

  return (
    <Link
      className="flex min-w-0 flex-col rounded-lg bg-surface-container-lowest p-2.5 shadow-[0_1px_4px_rgba(0,0,0,0.08)]"
      href={`/product/${product.product_id}`}
    >
      <div className="relative mb-2 flex aspect-square w-full items-center justify-center overflow-hidden rounded-md bg-surface-container-low">
        <ProductImage
          alt={product.name}
          emoji={product.emoji}
          productId={product.product_id}
          variant="card"
        />
      </div>
      <div className="flex min-w-0 flex-1 flex-col justify-between gap-2">
        <div className="min-w-0">
          <h3 className="line-clamp-2 text-body leading-tight text-on-surface">
            {product.name}
          </h3>
          <p className="mt-0.5 text-caps text-on-surface-variant">
            {visual?.subtitle ?? "1 Unit"}
          </p>
        </div>
        <div>
          <div className="mb-1 flex items-center gap-0.5 text-caps text-secondary">
            <Icon filled name="thumb_up" size={12} />
            <span>{cardKeepLabel(product)}</span>
          </div>
          <div className="flex items-end justify-between gap-1">
            <div className="min-w-0">
              <p className="text-price text-on-surface">{formatPrice(product.price)}</p>
              {off > 0 ? (
                <p className="text-caps text-on-surface-variant line-through">
                  {formatPrice(mrp)}
                </p>
              ) : null}
            </div>
            <span className="shrink-0 rounded-full border border-secondary bg-secondary px-3 py-1 text-headline-sm uppercase leading-none text-white">
              ADD
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
}
