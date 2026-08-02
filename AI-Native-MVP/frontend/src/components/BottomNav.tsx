"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icon } from "@/components/Icon";

export function BottomNav() {
  const pathname = usePathname();
  const isHome = pathname === "/";
  const isCategory = pathname.startsWith("/category");

  return (
    <nav className="absolute bottom-0 left-0 z-50 flex w-full items-center justify-around border-t border-outline-variant bg-surface px-2 py-2 shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
      <Link
        className={`flex min-w-0 flex-1 flex-col items-center px-1 py-1 text-caps ${
          isHome ? "text-secondary" : "text-on-surface-variant"
        }`}
        href="/"
      >
        <Icon filled={isHome} name="home" size={24} />
        <span className="mt-0.5">Home</span>
      </Link>
      <Link
        className={`flex min-w-0 flex-1 flex-col items-center px-1 py-1 text-caps ${
          isCategory ? "font-bold text-secondary" : "text-on-surface-variant"
        }`}
        href="/category/electronics"
      >
        <Icon filled={isCategory} name="grid_view" size={24} />
        <span className="mt-0.5">Categories</span>
      </Link>
      <button
        className="relative flex min-w-0 flex-1 flex-col items-center px-1 py-1 text-caps text-on-surface-variant"
        type="button"
      >
        <Icon name="shopping_cart" size={24} />
        <span className="mt-0.5">Cart</span>
        <span className="absolute right-[calc(50%-28px)] top-0 flex h-4 min-w-4 items-center justify-center rounded-full bg-error px-1 text-[10px] font-bold leading-none text-white">
          2
        </span>
      </button>
    </nav>
  );
}
