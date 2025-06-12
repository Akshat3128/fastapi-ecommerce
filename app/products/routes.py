from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from . import models, schemas
from app.auth.utils import require_admin

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

from typing import List
from app.auth.utils import require_admin
from .models import Product
from .schemas import ProductOut

@router.get("/", response_model=List[ProductOut])
def get_all_products(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return db.query(Product).all()

# update_product
@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_product.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# delete Product
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

