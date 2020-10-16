from typing import Dict

from menu_sun_integration.presentations.order.abstract_order_status_notification_response import AbstractOrderStatusNotificationResponse, \
    AbstractStatusInfo


class PromaxOrderStatusInfo(AbstractStatusInfo):
    def succeeded(self) -> bool:
        raise NotImplementedError


class PromaxOrderStatusNotificationResponse(AbstractOrderStatusNotificationResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

        self._logger.info(
            key="order_status_response",
            description="payload",
            payload=self._logger.dumps(payload))

    @property
    def status(self) -> PromaxOrderStatusInfo:
        status = self.payload['situacao']
        info = ''
        # faturado
        if status == "F":
            if self.payload['pedidos'][0]['dsMotivoNaoEntrega'] != '':
                status = "C"
                info = self.payload['pedidos'][0]['dsMotivoNaoEntrega']

        self._logger.info(
            key="order_status_response",
            description="order_status",
            payload=self)

        status = PromaxOrderStatusInfo(code=status, info=info)

        self._logger.info(
            key="order_status_response",
            description="status_info",
            payload=status)

        return status

    @property
    def id(self) -> str:
        return str(self.payload['idPedidoFacil'])

    @property
    def seller_order_id(self) -> str:
        return str(self.payload['cdPedido'])

