import Link from "next/link";
import { Icon } from "@/components/Icon";

/** Real Blinkit home address from app reference */
export const BLINKIT_HOME_ADDRESS = "home - 608 Sector 21B, NIT, Faridabad...";

function BlinkitWordmark() {
  return (
    <span
      aria-label="Blinkit"
      className="select-none text-[26px] font-extrabold lowercase leading-none tracking-[-0.5px] text-[#318616]"
    >
      blinkit
    </span>
  );
}

function BannerScallop() {
  return (
    <svg
      aria-hidden
      className="absolute bottom-0 left-0 w-full translate-y-[99%] text-white"
      height="8"
      preserveAspectRatio="none"
      viewBox="0 0 100 8"
      width="100%"
    >
      <path
        d="M0,0 H100 V8 Q87.5,0 75,8 Q62.5,0 50,8 Q37.5,0 25,8 Q12.5,0 0,8 Z"
        fill="currentColor"
      />
    </svg>
  );
}

export function BlinkitHeader() {
  return (
    <header className="sticky top-0 z-40 shrink-0 bg-white shadow-[0_1px_0_rgba(0,0,0,0.06)]">
      {/* Yellow brand banner */}
      <div className="relative bg-[#F8CB46] px-container-padding pb-5 pt-3">
        <div className="flex justify-center py-1">
          <BlinkitWordmark />
        </div>
        <BannerScallop />
      </div>

      {/* Delivery + address */}
      <div className="px-container-padding pb-2 pt-3">
        <p className="text-[15px] font-bold leading-tight text-on-surface">
          delivery in 10 minutes
        </p>
        <div className="mt-1.5 flex items-center gap-2">
          <p className="min-w-0 flex-1 truncate text-[13px] leading-snug text-on-surface">
            {BLINKIT_HOME_ADDRESS}
          </p>
          <button
            aria-label="Change delivery address"
            className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#F8CB46] text-on-surface"
            type="button"
          >
            <Icon name="arrow_forward" size={16} />
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="px-container-padding pb-3">
        <div className="flex h-12 items-center rounded-full border border-[#e8e8e8] bg-white px-4 shadow-[0_1px_4px_rgba(0,0,0,0.06)]">
          <Icon className="mr-2.5 shrink-0 text-[#9e9e9e]" name="search" size={22} />
          <input
            className="min-w-0 flex-1 border-none bg-transparent p-0 text-[14px] text-on-surface placeholder:text-[#9e9e9e] focus:ring-0"
            placeholder="search for atta dal and coke and more"
            readOnly
            type="text"
          />
        </div>
      </div>
    </header>
  );
}

interface BackHeaderProps {
  title: string;
  href: string;
  showSearch?: boolean;
}

export function BackHeader({ title, href, showSearch = false }: BackHeaderProps) {
  return (
    <header className="sticky top-0 z-40 shrink-0 border-b border-surface-container-highest bg-surface-container-lowest">
      <div className="flex h-14 min-w-0 items-center gap-2 px-container-padding">
        <Link
          aria-label="Go back"
          className="shrink-0 rounded-full p-1.5 text-on-surface hover:bg-surface-container-low"
          href={href}
        >
          <Icon name="arrow_back" size={22} />
        </Link>
        <h1 className="min-w-0 flex-1 truncate text-headline-sm text-on-surface">{title}</h1>
        {showSearch ? (
          <button
            aria-label="Search"
            className="shrink-0 rounded-full p-1.5 text-on-surface hover:bg-surface-container-low"
            type="button"
          >
            <Icon name="search" size={22} />
          </button>
        ) : (
          <span className="w-9 shrink-0" />
        )}
      </div>
    </header>
  );
}

export function PdpHeader({ href }: { href: string }) {
  return (
    <header className="sticky top-0 z-40 flex h-14 shrink-0 items-center justify-between border-b border-surface-variant bg-surface-container-lowest px-container-padding">
      <Link
        aria-label="Go back"
        className="rounded-full p-1.5 hover:bg-surface-container-low"
        href={href}
      >
        <Icon name="arrow_back" size={22} />
      </Link>
      <button
        aria-label="Share"
        className="rounded-full p-1.5 hover:bg-surface-container-low"
        type="button"
      >
        <Icon name="share" size={22} />
      </button>
    </header>
  );
}

export function SeeHowHeader({ productId }: { productId: string }) {
  return (
    <header className="shrink-0 bg-primary-container px-container-padding py-2 text-on-primary-container">
      <Link
        aria-label="Back to product"
        className="inline-flex rounded-full p-1.5 hover:bg-black/10"
        href={`/product/${productId}`}
      >
        <Icon name="arrow_back" size={22} />
      </Link>
    </header>
  );
}
