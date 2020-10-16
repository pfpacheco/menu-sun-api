from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.mappers.base_order_notification_mapper import BaseOrderNotificationMapper


class PernodOrderNotificationMapper(BaseOrderNotificationMapper):
    def __init__(self, base_mapper: BaseOrderNotificationMapper = BaseOrderNotificationMapper()):
        self._base_mapper = base_mapper

    def visit(self, entity):

        if isinstance(entity, Order):
            general_message = self._base_mapper.visit(entity)
            pernod_message = {
                "order_id": entity.order_id,
                "seller_id": entity.seller_id,
            }

            return {**general_message, **pernod_message}

        return None
