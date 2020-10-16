from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.shared.specification import Specification


class ProductSpecificationBase(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        return Product.seller_id == seller_id
