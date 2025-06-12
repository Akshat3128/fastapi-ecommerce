from fastapi import FastAPI
from app.auth import routes as auth_routes
from app.core.database import Base, engine
from app.auth import models as auth_models
from app.products.models import Product
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from app.products import routes as product_routes
from app.core.config import settings
from app.products import public_routes as public_products
from app.cart import routes as cart_routes
from app.cart.models import CartItem
from app.orders import checkout_routes, order_routes
from app.orders.models import Order, OrderItem

Base.metadata.create_all(bind=engine)  # Create tables

app = FastAPI()

print("DB URL:", settings.DATABASE_URL)

app.include_router(auth_routes.router)
app.include_router(product_routes.router)


app.include_router(product_routes.router)         # /admin/products
app.include_router(public_products.router)        # /products

app.include_router(cart_routes.router)

app.include_router(checkout_routes.router)
app.include_router(order_routes.router)



# Optional Swagger customization
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-Commerce API",
        version="1.0.0",
        description="Backend with FastAPI",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
