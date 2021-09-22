"""Alembic Configuration file"""
import sys
import os
from logging.config import fileConfig
from typing import Optional

from sqlalchemy import BOOLEAN, Boolean, create_engine
from sqlalchemy.dialects.mysql import TINYINT
from alembic import context
sys.path.append(os.getcwd())

from built_draws_service.extensions import DB  # noqa pylint: disable=C0413
from built_draws_service.models.database_helpers import (  # noqa pylint: disable=C0413
    get_connection_string)
from built_draws_service.models import *  # noqa pylint: disable=W0401, W0614, C0413

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
CONFIG = context.config  # pylint: disable=E1101

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(CONFIG.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
TARGET_METADATA = DB.Model.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def mysql_compare_type(
    context,  # pylint: disable=W0621,W0613
    inspected_column,  # pylint: disable=W0613
    metadata_column,  # pylint: disable=W0613
    inspected_type,
    metadata_type,
) -> Optional[bool]:
    """SQLAlchemy converts a BOOLEAN column definition to MySQL's TINYINT. On inspection
    during autogeneration of alembic migrations, SQLAlchemy compares the column definition
    from the model (BOOLEAN or Boolean) against the actual db type (TINYINT) and thinks
    the column needs to be altered. This occurs on every new generation of a migration.

    This custom compare_type overrides the comparison behavior only for this scenario
    to prevent unnecessary column alteration statements.
    https://github.com/miguelgrinberg/Flask-Migrate/issues/143
    """
    if isinstance(metadata_type, (BOOLEAN, Boolean)) and isinstance(inspected_type, TINYINT):
        return False
    return None


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = CONFIG.get_main_option("sqlalchemy.url")
    context.configure(  # pylint: disable=E1101
        compare_type=mysql_compare_type,
        url=url,
        target_metadata=TARGET_METADATA,
        literal_binds=True)

    with context.begin_transaction():  # pylint: disable=E1101
        context.run_migrations()  # pylint: disable=E1101


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alchemy_engine = create_engine(get_connection_string())

    with alchemy_engine.connect() as connection:
        context.configure(  # pylint: disable=E1101
            compare_type=mysql_compare_type,
            connection=connection,
            target_metadata=TARGET_METADATA)

        with context.begin_transaction():  # pylint: disable=E1101
            context.run_migrations()  # pylint: disable=E1101


if context.is_offline_mode():  # pylint: disable=E1101
    run_migrations_offline()
else:
    run_migrations_online()
