from typing import Dict, Optional

from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_status_response import \
    PromaxOrderStatusNotificationResponse
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse


class PromaxOrderDetailGetResponse(AbstractOrderDetailGetResponse):
    def __init__(self, order_id: str, payload: Dict):
        super().__init__(payload)
        self.order_id = order_id
        self.orders = self.payload['packageInfo']['body']['data']['response']['historico']

    @property
    def succeeded(self) -> bool:
        result = False

        try:
            result = (len(self.orders) > 0)
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

    def get_order(self) -> Optional[PromaxOrderStatusNotificationResponse]:
        for order in self.orders:
            order_id = self.order_id.replace('M', '7')
            if str(order['idPedidoFacil']) == order_id:
                return PromaxOrderStatusNotificationResponse(payload=order)

        self._logger.warn(
            key="order_detail_get_response",
            description="order_not_found",
            payload=self._logger.dumps(self.orders))


