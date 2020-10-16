from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_response import BRFOrderResponse
from menu_sun_integration.shared.specification.base_specification import Specification


class NewUserSpecification(Specification):
    description = 'The given user must be new'

    def is_satisfied_by(self, order: BRFOrderResponse):
        return order.customer_status == "NEW"
