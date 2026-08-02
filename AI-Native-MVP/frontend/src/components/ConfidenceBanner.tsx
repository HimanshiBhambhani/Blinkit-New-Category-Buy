import { Icon } from "@/components/Icon";

interface ConfidenceBannerProps {
  message?: string;
}

export function ConfidenceBanner({
  message = "Not enough brand mentions — showing category-level analysis",
}: ConfidenceBannerProps) {
  return (
    <div
      className="flex items-start gap-2 rounded-xl border border-[#ffe082] bg-[#fff8e1] p-3"
      role="status"
    >
      <Icon className="mt-px shrink-0 text-[#f57c00]" name="info" size={18} />
      <p className="text-trust text-on-surface">{message}</p>
    </div>
  );
}

interface DemoModeBannerProps {
  show: boolean;
}

export function DemoModeBanner({ show }: DemoModeBannerProps) {
  if (!show) return null;
  return (
    <div className="flex items-start gap-2 rounded-xl border border-outline-variant bg-surface-container-low p-3">
      <Icon className="mt-px shrink-0 text-on-surface-variant" name="warning" size={18} />
      <p className="text-trust text-on-surface-variant">
        Demo mode — API unavailable, showing offline sample data.
      </p>
    </div>
  );
}
