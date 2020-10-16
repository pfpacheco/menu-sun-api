from datetime import datetime

from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_response import BRFOrderResponse
from menu_sun_integration.shared.specification.base_specification import Specification


class LastOrderedDateSpecification(Specification):
    description = 'The given date must be lesser than 12 months'

    def is_satisfied_by(self, order: BRFOrderResponse):
        now = datetime.utcnow()
        num_months = (now.year - order.last_ordered_date.year) * 12 + (now.month - order.last_ordered_date.month)
        return num_months >= 12
