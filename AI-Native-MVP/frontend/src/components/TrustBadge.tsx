import Link from "next/link";
import { Icon } from "@/components/Icon";

interface TrustBadgeProps {
  productId: string;
  badge: string;
}

export function TrustBadge({ productId, badge }: TrustBadgeProps) {
  /** Product-specific insights: score, tips, verdict */
  const href = `/product/${productId}/see-how`;
  const isSafe = badge.toLowerCase().includes("safe to repeat");
  const label = isSafe
    ? "Safe to repeat"
    : badge.replace(/\s*·?\s*See how\s*→?/i, "").trim() || badge;

  return (
    <Link
      className="flex w-full items-center justify-between gap-2 rounded-card border border-blinkit-green bg-surface-container-lowest p-2.5 transition-colors hover:bg-surface-container-low"
      href={href}
    >
      <div className="flex min-w-0 items-center gap-1.5">
        <Icon className="shrink-0 text-blinkit-green" filled name="verified" size={20} />
        <span className="truncate text-body font-semibold text-blinkit-green">{label}</span>
      </div>
      <div className="flex shrink-0 items-center gap-0.5">
        <span className="text-trust text-on-surface-variant">See how</span>
        <Icon className="text-on-surface-variant" name="arrow_forward" size={16} />
      </div>
    </Link>
  );
}

export function SeeHowLink({ productId }: { productId: string }) {
  return (
    <Link
      className="text-trust text-primary underline decoration-primary/30 underline-offset-2"
      href={`/product/${productId}/how-calculated`}
    >
      See how trust is calculated →
    </Link>
  );
}
