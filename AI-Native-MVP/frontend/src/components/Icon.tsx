import type { CSSProperties } from "react";

export type IconName =
  | "arrow_back"
  | "arrow_forward"
  | "search"
  | "share"
  | "home"
  | "grid_view"
  | "shopping_cart"
  | "account_circle"
  | "keyboard_arrow_down"
  | "timer"
  | "verified"
  | "verified_user"
  | "thumb_up"
  | "replay"
  | "info"
  | "lightbulb"
  | "warning"
  | "check_circle"
  | "remove"
  | "add";

interface IconProps {
  name: IconName;
  size?: number;
  filled?: boolean;
  className?: string;
}

export function Icon({ name, size = 24, filled = false, className = "" }: IconProps) {
  const style: CSSProperties = {
    fontSize: size,
    width: size,
    height: size,
  };

  return (
    <span
      aria-hidden
      className={`material-symbols-outlined inline-flex shrink-0 items-center justify-center leading-none ${filled ? "filled" : ""} ${className}`}
      style={style}
    >
      {name}
    </span>
  );
}
