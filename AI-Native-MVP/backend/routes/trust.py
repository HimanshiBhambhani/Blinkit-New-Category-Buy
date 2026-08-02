"""Trust API routes — category, product, and product list."""

from fastapi import APIRouter, HTTPException, Query

from services import trust_service

router = APIRouter()


@router.get("/category/{slug}")
def category_trust(slug: str):
    result = trust_service.get_category(slug)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown category: {slug}")
    return result


@router.get("/product/{product_id}")
def product_trust(product_id: str):
    result = trust_service.get_product(product_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown product: {product_id}")
    return result


@router.get("/products")
def products(category: str = Query(..., description="Category slug, e.g. electronics")):
    result = trust_service.list_products_for_category(category)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown category: {category}")
    return result


@router.get("/categories")
def categories():
    """All categories with trust scores (home page)."""
    return trust_service.list_all_categories()
