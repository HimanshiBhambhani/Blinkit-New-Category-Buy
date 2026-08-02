import Link from "next/link";
import { Icon } from "@/components/Icon";
import { BLINKIT_LOGO } from "@/lib/stitchAssets";

export function BlinkitHeader() {
  return (
    <header className="sticky top-0 z-40 shrink-0 bg-primary-container px-container-padding pb-3 pt-3 text-on-primary-container">
      <div className="mb-3 flex items-center justify-between gap-2">
        <div className="flex min-w-0 flex-1 items-center gap-2">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img alt="Blinkit" className="h-8 shrink-0 object-contain" src={BLINKIT_LOGO} />
          <div className="min-w-0 flex-1">
            <p className="text-headline-sm font-bold leading-5">Blinkit</p>
            <div className="flex min-w-0 items-center">
              <span className="truncate text-trust">Home - 1234, Main St...</span>
              <Icon className="text-on-primary-container" name="keyboard_arrow_down" size={18} />
            </div>
          </div>
        </div>
        <Icon className="shrink-0 text-on-primary-container" filled name="account_circle" size={28} />
      </div>
      <div className="flex h-12 w-full items-center rounded-lg bg-surface-container-lowest px-3 shadow-[inset_0_1px_3px_rgba(0,0,0,0.1)]">
        <Icon className="mr-2 shrink-0 text-outline" name="search" size={22} />
        <input
          className="min-w-0 flex-1 border-none bg-transparent p-0 text-body text-on-surface placeholder:text-outline-variant focus:ring-0"
          placeholder="Search 'milk'"
          readOnly
          type="text"
        />
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
