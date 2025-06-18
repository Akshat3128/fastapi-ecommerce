from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.cart import models, schemas
from app.auth.utils import require_user
from app.auth.models import User
from app.cart.schemas import CartItemOut
from typing import List
from app.core.logger import logger

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CartOut)
def add_to_cart(
    item: schemas.CartAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    cart_item = db.query(models.CartItem).filter_by(
        user_id=current_user.id, product_id=item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = models.CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        logger.info(f"Added to cart: product {item.product_id} x{item.quantity} by {current_user.email}")
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


# view_cart
@router.get("/", response_model=List[CartItemOut])
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    cart_items = db.query(models.CartItem).filter_by(user_id=current_user.id).all()
    logger.info(f"Cart viewed by: {current_user.email}")
    return cart_items

# update_quantity
@router.put("/{product_id}", response_model=schemas.CartItemOut)
def update_cart_item(
    product_id: int,
    item: schemas.CartAdd,  
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    cart_item = db.query(models.CartItem).filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = item.quantity
    db.commit()
    db.refresh(cart_item)
    logger.info(f"Cart item updated by: {current_user.email}")
    return cart_item

# delete_cart_product
@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    cart_item = db.query(models.CartItem).filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    logger.info(f"Removed product {product_id} from cart by {current_user.email}")
    return {"message": "Item removed from cart"}
