from typing import Dict

from menu_sun_integration.presentations.order.abstract_order_status_notification_response import \
    AbstractOrderStatusNotificationResponse, \
    AbstractStatusInfo


class PernodStatusInfo(AbstractStatusInfo):
    pass


class PernodOrderStatusNotificationResponse(AbstractOrderStatusNotificationResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

        self._logger.info(
            key="order_status_response",
            description="payload",
            payload=self._logger.dumps(payload))

    @property
    def status(self) -> PernodStatusInfo:
        status = self.payload['status']['status'].upper()
        info = ''
        if 'message' in self.payload['status']:
            info = self.payload['status']['message']

        self._logger.info(
            key="order_status_response",
            description="order_status",
            payload=self)

        status = PernodStatusInfo(code=status, info=info)

        self._logger.info(
            key="order_status_response",
            description="status_info",
            payload=status)

        return status

    @property
    def id(self) -> str:
        return self.payload['reference']['source']

    @property
    def seller_order_id(self) -> str:
        return self.payload['reference']['id']
