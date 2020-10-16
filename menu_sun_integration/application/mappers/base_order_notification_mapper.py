from typing import Optional, Dict

from menu_sun_api.domain.model.order.order import Order, OrderItem, OrderStatus
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BaseOrderNotificationMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Order):
            message = {
                "order_id": entity.order_id,
                "seller_id": entity.seller_id
            }
            return message

        return None
