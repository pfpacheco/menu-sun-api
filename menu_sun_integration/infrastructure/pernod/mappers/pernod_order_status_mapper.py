from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.mappers.base_order_notification_mapper import BaseOrderNotificationMapper


class PernodOrderStatusMapper(BaseOrderNotificationMapper):
    def __init__(self, base_mapper: BaseOrderNotificationMapper = BaseOrderNotificationMapper()):
        self._base_mapper = base_mapper

    def visit(self, entity):

        if isinstance(entity, Order):
            general_message = self._base_mapper.visit(entity)
            pernod_message = {
                "order_id": entity.order_id,
                "seller_id": entity.seller_id,
                "seller_order_id": entity.seller_order_id,
                "status_id": entity.status.id,
                "status": entity.status.status.name,
                "integration_type": entity.seller.integration_type.name,
                "created_at": str(entity.created_date),
                "comments": entity.status.comments or ""
            }

            return {**general_message, **pernod_message}

        return None
