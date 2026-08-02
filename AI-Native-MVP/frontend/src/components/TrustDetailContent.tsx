import { Icon } from "@/components/Icon";
import type { ProductTrust } from "@/lib/types";

interface TrustDetailContentProps {
  product: ProductTrust;
}

export function TrustDetailContent({ product }: TrustDetailContentProps) {
  return (
    <div className="no-scrollbar flex flex-1 flex-col gap-4 overflow-y-auto bg-surface p-container-padding pb-24">
      <div>
        <h1 className="text-display text-on-surface">Buy Smart for this product</h1>
        <p className="mt-1 text-trust text-on-surface-variant">
          {product.name} · {product.brand}
        </p>
      </div>

      <div className="flex flex-col gap-3 rounded-xl border border-outline-variant bg-surface-container-lowest p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
        <div>
          <div className="mb-1 flex items-end justify-between gap-2">
            <span className="text-headline-sm text-on-surface">Buy Smart Score</span>
            <span className="text-display text-primary">
              {product.trust_score}
              <span className="text-body font-normal text-on-surface-variant">/100</span>
            </span>
          </div>
          <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-variant">
            <div
              className="h-full bg-primary-container"
              style={{ width: `${product.trust_score}%` }}
            />
          </div>
        </div>
        <hr className="border-outline-variant" />
        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-price text-on-surface">{product.keep_rate}%</p>
            <p className="text-trust text-on-surface-variant">Keep Rate</p>
          </div>
          <div>
            <p className="text-price text-on-surface">{product.positive_pct}%</p>
            <p className="text-trust text-on-surface-variant">Positive Mentions</p>
          </div>
        </div>
        <div className="flex items-start gap-1.5 rounded-lg bg-surface-container-low p-2">
          <Icon className="mt-px shrink-0 text-on-surface-variant" name="info" size={16} />
          <span className="text-trust text-on-surface-variant">{product.evidence_label}</span>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <div className="rounded-xl border border-[#c3e6c3] bg-blinkit-trust-bg p-3">
          <div className="mb-2 flex items-center gap-1.5 text-secondary">
            <Icon filled name="lightbulb" size={18} />
            <h2 className="text-headline-sm">Buy Smart Tips</h2>
          </div>
          <ul className="list-disc space-y-1 pl-4 text-body text-on-surface">
            {product.tips.map((tip) => (
              <li key={tip}>{tip}</li>
            ))}
          </ul>
        </div>

        <div className="rounded-xl border border-[#ffb4ab] bg-error-container p-3">
          <div className="mb-1 flex items-center gap-1.5 text-on-error-container">
            <Icon filled name="warning" size={18} />
            <h2 className="text-headline-sm">Top Concern</h2>
          </div>
          <p className="text-body text-on-error-container">{product.top_concern}</p>
        </div>
      </div>

      <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
        <h2 className="mb-1 text-headline-sm text-on-surface">Verdict</h2>
        <p className="text-body text-on-surface-variant">{product.verdict}</p>
      </div>
    </div>
  );
}
