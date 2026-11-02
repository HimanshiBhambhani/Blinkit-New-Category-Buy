import Link from "next/link";
import { notFound } from "next/navigation";
import { SeeHowHeader } from "@/components/BlinkitHeader";
import { PageFrame } from "@/components/PageFrame";
import { TrustDetailContent } from "@/components/TrustDetailContent";
import { getProduct } from "@/lib/api";
import { ALL_PRODUCT_IDS } from "@/lib/mockTrust";

interface SeeHowPageProps {
  params: Promise<{ id: string }>;
}

export function generateStaticParams() {
  return ALL_PRODUCT_IDS.map((id) => ({ id }));
}

export default async function SeeHowPage({ params }: SeeHowPageProps) {
  const { id } = await params;
  const product = await getProduct(id);
  if (!product) notFound();

  return (
    <PageFrame>
      <SeeHowHeader productId={id} />
      <TrustDetailContent product={product} />
      <div className="absolute bottom-0 left-0 z-30 w-full border-t border-outline-variant bg-surface-container-lowest px-container-padding py-2.5">
        <Link
          className="block w-full truncate rounded-lg border border-secondary py-2.5 text-center text-headline-sm font-semibold text-secondary"
          href={`/product/${id}`}
        >
          Back to {product.name}
        </Link>
      </div>
    </PageFrame>
  );
}
