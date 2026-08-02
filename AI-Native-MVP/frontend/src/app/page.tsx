export const dynamic = "force-dynamic";

import Link from "next/link";
import { BlinkitHeader } from "@/components/BlinkitHeader";
import { BottomNav } from "@/components/BottomNav";
import { Icon } from "@/components/Icon";
import { PageFrame } from "@/components/PageFrame";
import { BANNER_HERO, HOME_CATEGORIES } from "@/lib/stitchAssets";

export default function HomePage() {
  return (
    <PageFrame>
      <BlinkitHeader />
      <main className="no-scrollbar min-h-0 flex-1 overflow-y-auto pb-[72px]">
        <div className="mt-4 px-container-padding">
          <div
            className="relative flex h-32 items-center overflow-hidden rounded-xl p-4"
            style={{
              background: "linear-gradient(135deg, #FFD1D1 0%, #FF9B9B 100%)",
            }}
          >
            <div className="z-10 max-w-[65%]">
              <h2 className="mb-1 text-headline font-bold leading-snug text-on-surface">
                Shop beyond groceries
              </h2>
              <p className="text-trust text-on-surface-variant">
                Electronics, beauty &amp; more delivered in 10 mins.
              </p>
            </div>
            <div
              className="absolute right-0 top-0 h-full w-[38%] bg-cover bg-center"
              style={{ backgroundImage: `url('${BANNER_HERO}')` }}
            />
          </div>
        </div>

        <div className="mt-4 px-container-padding">
          <h3 className="mb-3 text-headline-sm font-bold text-on-surface">Categories</h3>
          <div className="grid grid-cols-2 gap-grid-gap">
            {HOME_CATEGORIES.map((cat) => {
              const tile = (
                <>
                  <div
                    className="mb-2 h-20 w-20 bg-contain bg-center bg-no-repeat"
                    style={{ backgroundImage: `url('${cat.image}')` }}
                  />
                  <span className="line-clamp-2 text-center text-trust font-semibold leading-tight text-on-surface">
                    {cat.label}
                  </span>
                </>
              );

              if (!cat.href) {
                return (
                  <div
                    className="flex aspect-square flex-col items-center justify-center rounded-xl bg-surface-bright p-3 opacity-60 shadow-[0_1px_4px_rgba(0,0,0,0.08)]"
                    key={cat.slug}
                  >
                    {tile}
                  </div>
                );
              }

              return (
                <Link
                  className="flex aspect-square flex-col items-center justify-center rounded-xl bg-surface-bright p-3 shadow-[0_1px_4px_rgba(0,0,0,0.08)] transition-colors hover:bg-surface-container-low"
                  href={cat.href}
                  key={cat.slug}
                >
                  {tile}
                </Link>
              );
            })}
          </div>
        </div>

        <div className="mt-4 flex w-full items-center justify-between bg-blinkit-trust-bg px-container-padding py-3">
          <div className="flex items-center gap-1.5 text-secondary">
            <Icon name="timer" size={18} />
            <span className="text-trust font-semibold">10 min delivery</span>
          </div>
          <div className="flex items-center gap-1.5 text-secondary">
            <Icon name="verified" size={18} />
            <span className="text-trust font-semibold">100% Genuine</span>
          </div>
        </div>
      </main>
      <BottomNav />
    </PageFrame>
  );
}
