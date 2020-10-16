from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
import os
import sys
import sqlalchemy_utils
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
from menu_sun_api.domain import Base
from menu_sun_api.domain.model.pricing.pricing import Pricing, PricingBulkLoad
from menu_sun_api.domain.model.product.product import Product, ProductStatus, MetaTags
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.order.order import OrderItem, \
    Order, OrderBillingAddress, OrderPayment, OrderShippingAddress, OrderStatus
from menu_sun_api.domain.model.metafield.metafield import Metafield
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == 'type' and isinstance(obj, sqlalchemy_utils.types.uuid.UUIDType):
        # add import for this type
        autogen_context.imports.add("import sqlalchemy_utils")
        autogen_context.imports.add("import uuid")
        return "sqlalchemy_utils.types.uuid.UUIDType(binary=False, native=False), default=uuid.uuid4, unique=True"


    # default rendering for other objects
    return False

def get_conn_string():
    try:
        db_host = context.get_x_argument(as_dictionary=True).get('DB_HOST')
        db_port = context.get_x_argument(as_dictionary=True).get('DB_PORT')
        db_user = context.get_x_argument(as_dictionary=True).get('DB_USER')
        db_password = context.get_x_argument(as_dictionary=True).get('DB_PASSWORD')
        db_name = context.get_x_argument(as_dictionary=True).get('DB_NAME')
        conn_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name)
        return conn_string
    except:
        return None


def try_to_create_database(db_host, db_port, db_user, db_password, db_name):
    connectable = get_connectable(db_host, db_port, db_user, db_password)
    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_item=render_item
        )
        print('Creating database...')
        context.execute("CREATE DATABASE IF NOT EXISTS {};".format(db_name))
        context.execute("USE {};".format(db_name))

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_conn_string()

    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)

    with context.begin_transaction():
        try_to_create_database()
        context.run_migrations()

def get_connectable(db_host, db_port, db_user, db_password, db_name = None):
    ini_section = config.get_section(config.config_ini_section)

    if (db_name):
        conn_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name)
    else:
        conn_string = "mysql+pymysql://{}:{}@{}:{}".format(db_user, db_password, db_host, db_port)

    if conn_string:
       ini_section['sqlalchemy.url'] = conn_string


    connectable = engine_from_config(
        ini_section,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)
    return connectable


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    db_host = context.get_x_argument(as_dictionary=True).get('DB_HOST')
    db_port = context.get_x_argument(as_dictionary=True).get('DB_PORT')
    db_user = context.get_x_argument(as_dictionary=True).get('DB_USER')
    db_password = context.get_x_argument(as_dictionary=True).get('DB_PASSWORD')
    db_name = context.get_x_argument(as_dictionary=True).get('DB_NAME')

    try_to_create_database(db_host, db_port, db_user, db_password, db_name)

    connectable = get_connectable(db_host, db_port, db_user, db_password, db_name)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_item=render_item
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
