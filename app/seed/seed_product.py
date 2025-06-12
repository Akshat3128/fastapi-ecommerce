# seed/seed_products.py
from app.core.database import SessionLocal
from app.products.models import Product

# Sample product data
product_data = [
    {
        "name": "Red Hoodie",
        "description": "Warm and cozy hoodie for winter",
        "price": 799.99,
        "stock": 25,
        "category": "clothing",
        "image_url": "https://example.com/images/red-hoodie.png"
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Loud and clear portable speaker",
        "price": 1499.00,
        "stock": 15,
        "category": "electronics",
        "image_url": "https://example.com/images/speaker.png"
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight running shoes for daily jogs",
        "price": 2199.50,
        "stock": 40,
        "category": "footwear",
        "image_url": "https://example.com/images/shoes.png"
    },
    {
        "name": "Notebook Set",
        "description": "Set of 5 ruled notebooks",
        "price": 299.00,
        "stock": 100,
        "category": "stationery",
        "image_url": "https://example.com/images/notebooks.png"
    },
    {
        "name": "LED Desk Lamp",
        "description": "Adjustable lamp with touch control",
        "price": 899.75,
        "stock": 30,
        "category": "home",
        "image_url": "https://example.com/images/lamp.png"
    }
]

def seed_products():
    db = SessionLocal()
    for data in product_data:
        existing = db.query(Product).filter_by(name=data["name"]).first()
        if not existing:
            db.add(Product(**data))
    db.commit()
    db.close()
    print("Seeded default products into the database.")

if __name__ == "__main__":
    seed_products()
