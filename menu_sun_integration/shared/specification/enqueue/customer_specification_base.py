from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.shared.specification import Specification


class CustomerSpecificationBase(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        return Customer.seller_id == seller_id
