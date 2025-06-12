from pydantic import BaseModel
from app.products.schemas import ProductOut

class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(BaseModel):
    id: int
    quantity: int
    product: ProductOut  # nested product info

    class Config:
        orm_mode = True
