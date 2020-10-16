from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.shared.specification import Specification


class SellerSpecificationBase(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        return Seller.id == seller_id
