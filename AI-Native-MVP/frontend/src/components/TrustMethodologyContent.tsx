import Link from "next/link";
import { Icon } from "@/components/Icon";
import type { ProductTrust } from "@/lib/types";

interface TrustMethodologyContentProps {
  product: ProductTrust;
}

export function TrustMethodologyContent({ product }: TrustMethodologyContentProps) {
  return (
    <div className="no-scrollbar flex flex-1 flex-col gap-4 overflow-y-auto bg-surface p-container-padding pb-24">
      <div>
        <h1 className="text-display text-on-surface">How trust is calculated</h1>
        <p className="mt-1 text-trust text-on-surface-variant">
          Methodology for {product.name}
        </p>
      </div>

      <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
        <div className="mb-2 flex items-center gap-1.5 text-on-surface-variant">
          <Icon name="info" size={18} />
          <span className="text-trust">{product.evidence_label}</span>
        </div>
        <p className="text-trust text-on-surface-variant">
          {product.mention_count} mentions · {product.category} · {product.brand}
        </p>
      </div>

      <section className="space-y-3">
        <div className="rounded-xl border border-outline-variant bg-surface-container-low p-3">
          <h2 className="mb-1 text-headline-sm text-on-surface">Keep rate</h2>
          <p className="mb-2 text-trust text-on-surface-variant">
            Share of buyers who keep the product instead of returning it.
          </p>
          <p className="text-body text-on-surface">
            <strong>MVP:</strong> Estimated from favorable sentiment in public review
            mentions.
          </p>
          <p className="mt-1 text-body text-on-surface">
            <strong>Production:</strong> Blinkit internal repurchase data — same UI,
            different source.
          </p>
          <p className="mt-2 text-trust text-secondary">
            This product: {product.keep_rate}% keep rate
          </p>
        </div>

        <div className="rounded-xl border border-outline-variant bg-surface-container-low p-3">
          <h2 className="mb-1 text-headline-sm text-on-surface">Trust score</h2>
          <p className="mb-2 text-trust text-on-surface-variant">
            Overall pre-purchase confidence score out of 100.
          </p>
          <p className="text-body text-on-surface">
            <strong>Formula:</strong> 60% favorable review signals + 40% friction risk
            themes from public reviews.
          </p>
          <p className="mt-2 text-trust text-secondary">
            This product: {product.trust_score}/100
          </p>
        </div>

        <div className="rounded-xl border border-outline-variant bg-surface-container-low p-3">
          <h2 className="mb-1 text-headline-sm text-on-surface">Positive mentions</h2>
          <p className="mb-2 text-trust text-on-surface-variant">
            Share of review text that praises this product or brand.
          </p>
          <p className="text-body text-on-surface">
            Pulled from our review corpus and theme classifier — not star ratings alone.
          </p>
          <p className="mt-2 text-trust text-secondary">
            This product: {product.positive_pct}% positive mentions
          </p>
        </div>
      </section>

      <div className="rounded-xl border border-[#c3e6c3] bg-blinkit-trust-bg p-3">
        <p className="text-trust text-on-surface">
          Buy Smart is a <strong>habit helper</strong>, not a buy/don&apos;t-buy verdict.
          Scores help you decide if this repeat purchase is worth the risk.
        </p>
      </div>

      <Link
        className="text-trust text-primary underline decoration-primary/30 underline-offset-2"
        href={`/product/${product.product_id}/see-how`}
      >
        ← View Buy Smart insights for this product
      </Link>
    </div>
  );
}
