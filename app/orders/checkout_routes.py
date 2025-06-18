# app/orders/checkout_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth.utils import require_user
from app.auth.models import User
from app.cart.models import CartItem
from app.products.models import Product
from app.orders import models, schemas
from app.core.logger import logger


router = APIRouter(prefix="/checkout", tags=["Checkout"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.OrderOut)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    cart_items = db.query(CartItem).filter_by(user_id=current_user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter_by(id=item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        subtotal = product.price * item.quantity
        total += subtotal

        order_item = models.OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        order_items.append(order_item)

    order = models.Order(
        user_id=current_user.id,
        total_amount=total,
        status="paid",
        items=order_items
    )

    db.add(order)
    db.query(CartItem).filter_by(user_id=current_user.id).delete()
    db.commit()
    logger.info(f"User {current_user.email} placed an order. Total: ₹{total}")
    db.refresh(order)
    return order
