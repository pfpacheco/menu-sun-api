from menu_sun_api import settings
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
_database_url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_user,
                                                        db_password,
                                                        db_host,
                                                        db_port,
                                                        db_name)
_engine = create_engine(_database_url, pool_size=1)
_factory = sessionmaker(bind=_engine)
Session = scoped_session(sessionmaker(bind=_engine))
