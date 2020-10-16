import datetime
from typing import Optional, Dict

from menu_sun_integration.presentations.order.abstract_order_status_put_response import AbstractOrderStatusPutResponse


class PernodOrderStatusPutResponse(AbstractOrderStatusPutResponse):
    def __init__(self, payload: Dict, order_id: str, status_id: int):
        super().__init__(payload)
        self.order_id = order_id
        self.status_id = status_id

    def published_date(self):
        return datetime.datetime.now()
