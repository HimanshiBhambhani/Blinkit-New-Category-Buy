import Link from "next/link";
import { ConfidenceBanner, DemoModeBanner } from "@/components/ConfidenceBanner";
import { Icon } from "@/components/Icon";
import { LINK_A_DISCOVERY_URL } from "@/lib/trustFormat";
import {
  confidenceBadgeLabel,
  formatKeepRate,
  formatMentionCount,
  formatPositivePct,
  getConfidence,
  isLowConfidence,
} from "@/lib/trustFormat";
import type { ProductTrust } from "@/lib/types";

interface TrustDetailContentProps {
  product: ProductTrust;
}

export function TrustDetailContent({ product }: TrustDetailContentProps) {
  const confidence = getConfidence(product);
  const categoryScore = product.category_trust_score ?? product.trust_score;
  const delta = product.product_delta ?? 0;

  return (
    <div className="no-scrollbar flex flex-1 flex-col gap-4 overflow-y-auto bg-surface p-container-padding pb-24">
      <div>
        <h1 className="text-display text-on-surface">Buy Smart for this product</h1>
        <p className="mt-1 text-trust text-on-surface-variant">
          {product.name} · {product.brand}
        </p>
      </div>

      <DemoModeBanner show={Boolean(product.demo_mode)} />

      {isLowConfidence(product) ? <ConfidenceBanner /> : null}

      <div className="flex flex-col gap-3 rounded-xl border border-outline-variant bg-surface-container-lowest p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
        <div className="flex flex-wrap items-center gap-2">
          <span
            className={`rounded-sm px-1.5 py-0.5 text-caps ${
              confidence === "high"
                ? "bg-secondary-container text-on-secondary-container"
                : confidence === "medium"
                  ? "bg-surface-container-high text-on-surface-variant"
                  : "bg-error-container text-on-error-container"
            }`}
          >
            {confidenceBadgeLabel(confidence)}
          </span>
          <span className="text-caps text-on-surface-variant">{formatMentionCount(product)}</span>
        </div>

        <div>
          <div className="mb-1 flex items-end justify-between gap-2">
            <span className="text-headline-sm text-on-surface">Product Trust Score</span>
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
          <p className="mt-1.5 text-trust text-on-surface-variant">
            Category baseline {categoryScore}
            {delta !== 0 ? (
              <span>
                {" "}
                · product signals {delta > 0 ? "+" : ""}
                {delta}
              </span>
            ) : null}
          </p>
        </div>

        <hr className="border-outline-variant" />

        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-price text-on-surface">{formatKeepRate(product)}</p>
            <p className="text-trust text-on-surface-variant">Keep rate proxy*</p>
          </div>
          <div>
            <p className="text-price text-on-surface">{formatPositivePct(product)}</p>
            <p className="text-trust text-on-surface-variant">Positive mentions</p>
          </div>
        </div>

        <div className="flex items-start gap-1.5 rounded-lg bg-surface-container-low p-2">
          <Icon className="mt-px shrink-0 text-on-surface-variant" name="info" size={16} />
          <span className="text-trust text-on-surface-variant">
            {product.evidence_label}
            {product.keep_rate_label ? (
              <>
                <br />
                <span className="text-on-surface-variant/90">{product.keep_rate_label}</span>
              </>
            ) : null}
          </span>
        </div>
      </div>

      {product.theme_breakdown && product.theme_breakdown.length > 0 ? (
        <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
          <h2 className="mb-2 text-headline-sm text-on-surface">Theme breakdown</h2>
          <p className="mb-3 text-trust text-on-surface-variant">
            What our classifier found in review text for this brand / category.
          </p>
          <ul className="space-y-2">
            {product.theme_breakdown.map((item) => (
              <li
                className="flex items-center justify-between gap-2 text-body text-on-surface"
                key={item.theme}
              >
                <span className="min-w-0 flex-1 truncate">{item.theme}</span>
                <span className="shrink-0 rounded-sm bg-surface-container-high px-1.5 py-0.5 text-caps text-on-surface-variant">
                  {item.count}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {product.snippets && product.snippets.length > 0 ? (
        <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)]">
          <h2 className="mb-2 text-headline-sm text-on-surface">Review evidence</h2>
          <p className="mb-3 text-trust text-on-surface-variant">
            Verbatim excerpts from our public review corpus — not AI-generated.
          </p>
          <ul className="space-y-3">
            {product.snippets.map((snippet, index) => (
              <li
                className="border-l-2 border-primary pl-3 text-body italic text-on-surface-variant"
                key={`${snippet.theme}-${index}`}
              >
                &ldquo;{snippet.text}&rdquo;
                <p className="mt-1 not-italic text-caps text-on-surface-variant/80">
                  {snippet.theme} · {snippet.source}
                </p>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

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

      <p className="text-trust leading-relaxed text-on-surface-variant">
        Themes classified in the{" "}
        <Link
          className="text-primary underline decoration-primary/30 underline-offset-2"
          href={LINK_A_DISCOVERY_URL}
          rel="noopener noreferrer"
          target="_blank"
        >
          Discovery Engine (Link A)
        </Link>
        . Trust scores on this page are computed <strong>deterministically</strong> from the review
        corpus — no LLM at request time.
      </p>
    </div>
  );
}
