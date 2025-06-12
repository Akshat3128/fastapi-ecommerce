from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Load environment variables and DB config
import os
from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings
from app.core.database import Base

# Import all models here
from app.auth.models import User
from app.products.models import Product
from app.cart.models import CartItem
from app.orders.models import Order, OrderItem

# Alembic Config
config = context.config

# Set DB URL from .env/config
# print("DB_URL", settings.DATABASE_URL)
# config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Assign metadata for autogeneration
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
