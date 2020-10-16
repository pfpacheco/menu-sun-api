from typing import Dict

from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_notification_response import \
    PernodOrderStatusNotificationResponse
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse


class PernodOrderDetailGetResponse(AbstractOrderDetailGetResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            result = self.payload['reference']['id'] is not None
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

    def get_order(self) -> PernodOrderStatusNotificationResponse:
        return PernodOrderStatusNotificationResponse(payload=self.payload)
