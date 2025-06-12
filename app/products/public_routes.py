from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.products.models import Product
from app.products.schemas import ProductOut
from app.core.database import SessionLocal

router = APIRouter(prefix="/products", tags=["Public Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query(default="id"),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort_by in ["price", "name", "stock"]:
        query = query.order_by(getattr(Product, sort_by))

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    return query.all()

# //search prod by keyword
@router.get("/search", response_model=List[ProductOut])
def search_products(keyword: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.name.ilike(f"%{keyword}%")).all()

# search prod by id
@router.get("/{product_id}", response_model=ProductOut)
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


