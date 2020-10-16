from typing import Dict

from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_response import PernodOrderResponse
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse
from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class PernodOrderPostResponse(AbstractOrderPostResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            has_succeeded = self.payload.get('errors', [])
            result = not (len(has_succeeded) >= 1)
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="order_post_response",
                    description="order_integrated",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="order_post_response",
                    description="order_not_integrated",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_order(self) -> [AbstractOrderResponse]:
        return PernodOrderResponse(payload=self.payload)
