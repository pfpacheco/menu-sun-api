from sqlalchemy import and_

from menu_sun_api.domain.db_repository import DBRepository
from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.shared.specification import Specification


class PricingRepository(DBRepository):

    def __init__(self, session=None):
        super().__init__(Pricing, session)

    def get_pricing_by_customer_and_product(self, customer_id, product_id):
        condition = and_(Pricing.product_id == product_id,
                         Pricing.customer_id == customer_id)
        query = self.session.query(Pricing) \
            .outerjoin(Product) \
            .outerjoin(Customer)

        return query.filter(condition).one_or_none()

    def get_pricing(self, seller_id, sku, document):
        condition = and_(Product.sku == sku,
                         Customer.document == document,
                         Seller.id == seller_id)
        query = self.session.query(Pricing) \
            .outerjoin(Product) \
            .outerjoin(Customer) \
            .outerjoin(Seller)
        return query.filter(condition).one_or_none()

    def get_pricing_by_seller_code(self, seller_code, sku, document):
        condition = and_(Product.sku == sku,
                         Customer.document == document,
                         Seller.seller_code == seller_code)
        query = self.session.query(Pricing) \
            .outerjoin(Product) \
            .outerjoin(Customer) \
            .outerjoin(Seller)
        return query.filter(condition).one_or_none()

    def filter_by_specification(self, seller_id: int, specification: Specification):
        query = self.session.query(Pricing, Product, Customer)

        return query.filter(specification.is_satisfied_by(seller_id)).all()
