import { Icon } from "@/components/Icon";
import type { CategoryTrust } from "@/lib/types";

interface BuySmartStripProps {
  category: CategoryTrust;
}

export function BuySmartStrip({ category }: BuySmartStripProps) {
  return (
    <section className="shrink-0 bg-blinkit-trust-bg px-container-padding py-4">
      <div className="mb-2 flex items-center gap-2">
        <span className="text-caps uppercase tracking-widest text-secondary">BUY SMART</span>
        <span className="rounded-sm bg-secondary px-1.5 py-0.5 text-caps leading-none text-white">
          {category.trust_score}
        </span>
      </div>
      <p className="mb-1 text-headline-sm leading-snug text-on-surface">{category.guidance}</p>
      <p className="flex items-start gap-1 text-trust text-on-surface-variant">
        <Icon className="mt-px shrink-0" name="verified_user" size={14} />
        <span>Top concern: {category.top_concern}</span>
      </p>
    </section>
  );
}
