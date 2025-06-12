from pydantic import BaseModel, field_validator

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str

    @field_validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("stock")
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v

    @field_validator("name", "description", "category", "image_url")
    def validate_non_empty(cls, v, field):
        if not v.strip():
            raise ValueError(f"{field.name} must not be empty")
        return v

class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True
