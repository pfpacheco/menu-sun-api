from datetime import datetime

from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class BRFOrderResponse(AbstractOrderResponse):
    def __init__(self, customer_status: str, last_ordered_date: datetime):
        self.customer_status = customer_status
        self.last_ordered_date = last_ordered_date
