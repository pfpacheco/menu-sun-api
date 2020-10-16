from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse
from menu_sun_integration.shared.specification.base_specification import Specification


class AlwaysComissionedSpecification(Specification):
    description = 'Commission always true'

    def is_satisfied_by(self, order: AbstractOrderResponse):
        return True
