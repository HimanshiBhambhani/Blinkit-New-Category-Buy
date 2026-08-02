import type { ReactNode } from "react";

interface PageFrameProps {
  children: ReactNode;
}

/** Centered mobile shell — matches Stitch 500px column, fits normal browser viewport. */
export function PageFrame({ children }: PageFrameProps) {
  return (
    <div className="flex min-h-[100dvh] justify-center bg-surface-container-low">
      <div className="relative flex h-[100dvh] w-full max-w-phone flex-col overflow-hidden bg-surface-container-lowest shadow-[0_8px_32px_rgba(0,0,0,0.12)]">
        {children}
      </div>
    </div>
  );
}
