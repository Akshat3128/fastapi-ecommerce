from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    product = relationship("Product")  # JOIN to product table
