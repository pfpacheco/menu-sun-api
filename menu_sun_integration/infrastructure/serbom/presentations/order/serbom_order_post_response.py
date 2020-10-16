from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_response import SerbomOrderResponse
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse


class SerbomOrderPostResponse(AbstractOrderPostResponse):
    def __init__(self, payload: str):
        super().__init__(payload={})
        self.response = payload

    @property
    def succeeded(self):
        payload = self.response
        result = False
        try:
            result = payload.find('OK')
        except Exception:
            result = False
        finally:
            if result != -1:
                result = True
                self._logger.info(
                    key="order_post_response",
                    description="order_integrated",
                    payload=self._logger.dumps(self.payload))
            else:
                result = False
                self._logger.error(
                    key="order_post_response",
                    description="order_not_integrated",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_order(self) -> SerbomOrderResponse:
        return SerbomOrderResponse()

