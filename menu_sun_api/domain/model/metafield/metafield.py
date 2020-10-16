from sqlalchemy import Column, String
from menu_sun_api.domain import Default
from sqlalchemy.dialects.mysql import LONGTEXT


class Metafield(Default):
    namespace = Column(String(64), nullable=False)
    key = Column(String(64), nullable=False)
    value = Column(LONGTEXT)
