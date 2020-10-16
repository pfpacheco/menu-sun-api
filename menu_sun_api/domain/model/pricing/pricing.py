from sqlalchemy import Column, Integer, ForeignKey, String, Float, UniqueConstraint

from menu_sun_api.domain import Base, Default
from menu_sun_api.shared.str_converters import hex_uuid


class Pricing(Default, Base):
    __tablename__ = 'pricing'
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    list_price = Column(Float)
    sale_price = Column(Float)
    uuid = Column(String(32), nullable=False, unique=True, default=hex_uuid)
    __table_args__ = (UniqueConstraint('customer_id', 'product_id', name='_customer_id_product_id'),
                      )


class PricingBulkLoad(Base):
    __tablename__ = 'pricing_bulkload'
    sku = Column(String(32), nullable=False, primary_key=True)
    document = Column(String(16), nullable=False, primary_key=True)
    list_price = Column(Float)
    sale_price = Column(Float)
