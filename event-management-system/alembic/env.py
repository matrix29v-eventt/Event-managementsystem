# alembic/env.py

import os
from dotenv import load_dotenv
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ----------------------------------------------------
# START OF CUSTOM PROJECT IMPORTS AND CONFIGURATION
# ----------------------------------------------------

# IMPORT YOUR PROJECT'S BASE AND MODELS HERE
import sys
from pathlib import Path

# Add project root to sys.path so 'app' modules can be imported
sys.path.append(str(Path(__file__).resolve().parents[1])) 

load_dotenv() # Load environment variables from .env

# Import your project's database connection and models
from app.db import Base, engine 
from app.models import models # Ensure your models are imported so Alembic can see them

# This is the Base class that contains all your SQLAlchemy model metadata
target_metadata = Base.metadata

# ----------------------------------------------------
# END OF CUSTOM PROJECT IMPORTS AND CONFIGURATION
# ----------------------------------------------------


# this is the Alembic Config object, which provides access to
# various values specified in .ini file.
config = context.config

# Interpret the config file for Python's standard logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an active connection.
    """
    # 💡 CHANGE: Use the DATABASE_URL from environment variables
    url = os.getenv("DATABASE_URL") 
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    
    # 💡 CHANGE: Use the project's 'engine' directly instead of recreating it from config
    connectable = engine 

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Uncomment if you need to use the transactional approach for migration
            # transaction_per_migration=True, 
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()