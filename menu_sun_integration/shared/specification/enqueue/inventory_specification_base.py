from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.shared.specification import Specification
from sqlalchemy import and_


class InventorySpecificationBase(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        return and_(Customer.seller_id == seller_id, Pricing.customer_id == Customer.id,
                    Pricing.product_id == Product.id)
