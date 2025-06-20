# app/orders/order_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.database import SessionLocal
from app.auth.utils import require_user
from app.auth.models import User
from app.orders import models, schemas
from typing import List
from app.core.logger import logger


router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.OrderOut])
def get_order_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    orders = db.query(models.Order)\
        .options(joinedload(models.Order.items))\
        .filter_by(user_id=current_user.id).all()
    logger.info(f"Order list viewed by: {current_user.email}")
    return orders

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    order = db.query(models.Order)\
        .options(joinedload(models.Order.items))\
        .filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        logger.info(f"Order not found {order_id} viewed by: {current_user.email}")
        raise HTTPException(status_code=404, detail="Order not found")
    logger.info(f"Order {order_id} viewed by: {current_user.email}")
    return order
