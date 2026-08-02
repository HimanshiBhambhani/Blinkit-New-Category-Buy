import { Icon } from "@/components/Icon";
import { formatKeepRate } from "@/lib/trustFormat";
import type { ProductTrust } from "@/lib/types";

interface TrustRowProps {
  product: ProductTrust;
}

export function TrustRow({ product }: TrustRowProps) {
  return (
    <div className="flex flex-wrap items-center gap-x-1.5 gap-y-1 text-trust text-on-surface-variant">
      <span className="inline-flex items-center gap-0.5">
        <Icon name="replay" size={14} />
        {product.replacement_days}-day replacement
      </span>
      <span className="text-surface-variant">|</span>
      <span className="inline-flex items-center gap-0.5">
        <Icon name="verified" size={14} />
        {product.warranty}
      </span>
      <span className="text-surface-variant">|</span>
      <span className="inline-flex items-center gap-0.5">
        <Icon name="thumb_up" size={14} />
        {formatKeepRate(product)} keep this*
      </span>
    </div>
  );
}
