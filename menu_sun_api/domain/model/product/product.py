import enum

from sqlalchemy import Column, Integer, ForeignKey, String, Float, Enum, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from menu_sun_api.domain import Base, Default
from menu_sun_api.shared.str_converters import hex_uuid
from menu_sun_api.domain.model.metafield.metafield import Metafield
from datetime import datetime


class ProductStatus(enum.Enum):
    ENABLED = 1
    DISABLED = 2


class MetaTags(Default, Base):
    __tablename__ = 'meta_tags'
    serialize_rules = ('-product_id', '-id', '-created_date', '-updated_date')
    description = Column(Text)
    title = Column(Text)
    keyword = Column(Text)
    product_id = Column(Integer, ForeignKey('product.id'))


class ProductMetafield(Metafield, Base):
    __tablename__ = 'product_metafield'
    serialize_rules = ('-product_id', '-id', '-created_date', '-updated_date')
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)


class Product(Default, Base):
    __tablename__ = 'product'
    serialize_rules = ('-seller_id', '-id', '-uuid', '-created_date', '-updated_date')

    uuid = Column(String(32), nullable=False, unique=True, default=hex_uuid)
    seller_id = Column(Integer, ForeignKey('seller.id'), nullable=False)
    sku = Column(String(32), nullable=False, index=True)
    name = Column(String(256))
    description = Column(Text)
    status = Column(Enum(ProductStatus))
    ean = Column(String(16))
    brand = Column(String(256))
    inventory = Column(Integer)
    ncm = Column(String(16))
    weight = Column(Float)
    height = Column(Float)
    width = Column(Float)
    length = Column(Float)
    cost = Column(Float)
    list_price = Column(Float)
    sale_price = Column(Float)
    promo_price = Column(Float)
    meta_tags = relationship("MetaTags", lazy='joined')
    metafields = relationship(ProductMetafield, lazy='joined')
    __table_args__ = (UniqueConstraint('seller_id', 'sku', name='_seller_id_sku'),
                      )

    def __search_metafield(self, key):
        for metafield in self.metafields:
            if metafield.key == key:
                return metafield
        return None

    def update_metafields(self, metafields_input):

        for metafield_input in metafields_input:
            rs = self.__search_metafield(metafield_input.key)
            if rs:
                rs.value = metafield_input.value
            else:
                self.metafields.append(metafield_input)

    def change_metafield(self, input):
        self.updated_date = datetime.utcnow()
        for m in self.metafields:
            if (m.namespace == input.namespace) and (m.key == input.key):
                m.value = input.value
                return m

        self.metafields.append(input)
        return input

    def change_meta_tags(self, input):
        self.updated_date = datetime.utcnow()
        for m in self.meta_tags:
            if m.keyword == input.keyword:
                m.description = input.description
                m.title = input.title
                return m

        self.meta_tags.append(input)

        return input

    def __hash__(self):
        return hash(self.sku)

    def __eq__(self, other):
        if not hasattr(other, 'sku'):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.sku == other.sku
