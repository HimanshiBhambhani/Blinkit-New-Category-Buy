import Image from "next/image";
import { getListImage, getPdpImage, isProductScreenshot } from "@/lib/stitchAssets";

interface ProductImageProps {
  productId: string;
  emoji: string;
  alt: string;
  variant: "card" | "pdp";
}

function ScreenshotImage({ alt, src, variant }: { alt: string; src: string; variant: "card" | "pdp" }) {
  return (
    <div className="relative h-full w-full overflow-hidden bg-white">
      <Image
        alt={alt}
        className={
          variant === "pdp"
            ? "absolute left-0 top-0 h-full w-[210%] max-w-none object-cover object-left"
            : "absolute left-0 top-0 h-full w-[210%] max-w-none object-cover object-left"
        }
        height={600}
        priority={variant === "pdp"}
        src={src}
        width={1200}
      />
    </div>
  );
}

export function ProductImage({ productId, emoji, alt, variant }: ProductImageProps) {
  const src = variant === "pdp" ? getPdpImage(productId) : getListImage(productId);

  if (src && isProductScreenshot(src)) {
    if (variant === "pdp") {
      return (
        <div className="absolute inset-0">
          <ScreenshotImage alt={alt} src={src} variant="pdp" />
        </div>
      );
    }
    return <ScreenshotImage alt={alt} src={src} variant="card" />;
  }

  if (src && variant === "pdp") {
    return (
      <Image
        alt={alt}
        className="object-contain p-4"
        fill
        priority
        sizes="430px"
        src={src}
      />
    );
  }

  if (src) {
    return (
      <Image
        alt={alt}
        className="h-[80%] w-[80%] object-contain"
        height={160}
        src={src}
        width={160}
      />
    );
  }

  return (
    <span
      aria-hidden
      className={variant === "pdp" ? "text-7xl leading-none" : "text-5xl leading-none"}
    >
      {emoji}
    </span>
  );
}
