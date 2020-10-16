from typing import Dict

from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class PernodOrderResponse(AbstractOrderResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    def seller_order_id(self) -> str:
        return self.payload['reference']['id']

