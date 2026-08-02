export const dynamic = "force-dynamic";

import Link from "next/link";
import { BlinkitHeader } from "@/components/BlinkitHeader";
import { BottomNav } from "@/components/BottomNav";
import { PageFrame } from "@/components/PageFrame";
import { BANNER_HERO, HOME_CATEGORIES } from "@/lib/stitchAssets";

export default function HomePage() {
  return (
    <PageFrame>
      <BlinkitHeader />
      <main className="no-scrollbar min-h-0 flex-1 overflow-y-auto bg-white pb-[72px]">
        <div className="mt-3 px-container-padding">
          <div
            className="relative h-[148px] overflow-hidden rounded-2xl"
            style={{
              background: "linear-gradient(135deg, #FFD1D1 0%, #FF9B9B 100%)",
            }}
          >
            <div className="relative z-10 flex h-full w-[56%] flex-col justify-center px-4 py-3">
              <h2 className="mb-1.5 text-[17px] font-bold leading-tight text-on-surface">
                Shop beyond groceries
              </h2>
              <p className="text-[12px] leading-[1.35] text-on-surface/85">
                Electronics, beauty
                <br />
                &amp; more delivered
                <br />
                in 10 mins.
              </p>
            </div>
            <div
              aria-hidden
              className="pointer-events-none absolute inset-y-0 right-0 w-[46%] bg-cover bg-center bg-no-repeat"
              style={{ backgroundImage: `url('${BANNER_HERO}')` }}
            />
            <div
              aria-hidden
              className="pointer-events-none absolute inset-y-0 left-[48%] z-[1] w-10"
              style={{
                background:
                  "linear-gradient(to right, rgba(255, 209, 209, 0.95) 0%, rgba(255, 209, 209, 0) 100%)",
              }}
            />
          </div>
        </div>

        <div className="mt-5 px-container-padding">
          <h3 className="mb-3 text-[16px] font-bold text-on-surface">Categories</h3>
          <div className="grid grid-cols-2 gap-3">
            {HOME_CATEGORIES.map((cat) => {
              const tile = (
                <>
                  <div
                    className="mb-2 h-[88px] w-[88px] bg-contain bg-center bg-no-repeat"
                    style={{ backgroundImage: `url('${cat.image}')` }}
                  />
                  <span className="line-clamp-2 px-1 text-center text-[12px] font-semibold leading-tight text-on-surface">
                    {cat.label}
                  </span>
                </>
              );

              if (!cat.href) {
                return (
                  <div
                    className="relative flex aspect-square flex-col items-center justify-center rounded-2xl border border-[#f0f0f0] bg-white p-3 opacity-55"
                    key={cat.slug}
                  >
                    <span className="absolute right-2 top-2 rounded-full bg-[#f3f3f4] px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-on-surface-variant">
                      Soon
                    </span>
                    {tile}
                  </div>
                );
              }

              return (
                <Link
                  className="flex aspect-square flex-col items-center justify-center rounded-2xl border border-[#f0f0f0] bg-white p-3 transition-colors active:bg-[#fafafa]"
                  href={cat.href}
                  key={cat.slug}
                >
                  {tile}
                </Link>
              );
            })}
          </div>
        </div>
      </main>
      <BottomNav />
    </PageFrame>
  );
}
