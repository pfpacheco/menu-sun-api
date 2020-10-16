from typing import Optional, Dict

from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_put_response import \
    PernodOrderStatusPutResponse
from menu_sun_integration.presentations.order.abstract_order_status_detail_put_response import \
    AbstractOrderStatusDetailPutResponse


class PernodOrderStatusDetailPutResponse(AbstractOrderStatusDetailPutResponse):
    def __init__(self, payload: Dict, order_id: str, status_id: int):
        super().__init__(payload)
        self.order_id = order_id
        self.status_id = status_id

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            result = self.payload['status'] is not None
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="order_detail_get_response",
                    description="order_found",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="order_detail_get_response",
                    description="order_not_found",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_order(self) -> PernodOrderStatusPutResponse:
        return PernodOrderStatusPutResponse(payload=self.payload, order_id=self.order_id, status_id=self.status_id)
