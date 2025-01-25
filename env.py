from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
from dotenv import load_dotenv
from models import Base
from alembic import context

load_dotenv()

config = context.config
fileConfig(config.config_file_name)


def run_migrations_offline():
    """миграция в режиме "offline"""
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """миграция в режиме "online"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()
