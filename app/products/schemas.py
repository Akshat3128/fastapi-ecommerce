from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str

class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True
