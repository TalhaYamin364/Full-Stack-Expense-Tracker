from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ─── PATH SETUP ────────────────────────────────────────────────────────────────
# Alembic runs from src/backend/, so we add it to sys.path so that
# "from api.xxx import ..." imports resolve correctly.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import our SQLAlchemy Base (which holds metadata about all tables) and the
# DATABASE_URL we defined in database.py — single source of truth for the URL.
from api.database import Base, DATABASE_URL  # noqa: E402

# Import all ORM models so SQLAlchemy's Base.metadata is aware of every table.
# Without these imports, autogenerate would see an empty schema and generate
# a migration that drops all your tables instead of creating them.
from api.db_models import User, Expense  # noqa: E402, F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with our DATABASE_URL from database.py.
# This keeps the URL in one place — database.py — instead of duplicating
# it in alembic.ini.
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata tells autogenerate what the schema *should* look like.
# Alembic compares this against the live DB to generate the diff.
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # Required for SQLite — ALTER TABLE is not natively supported.
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # Required for SQLite — ALTER TABLE is not natively supported.
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
