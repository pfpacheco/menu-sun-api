from typing import Optional, Dict

from menu_sun_api.domain.model.order.order import Order, OrderItem, OrderStatus
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BaseOrderMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Order):
            items = [i.accept(self) for i in entity.items]
            statuses = [i.accept(self) for i in entity.statuses]

            message = {
                "order_id": entity.order_id,
                "items": items,
                "statuses": statuses,
                "order_date": entity.order_date.isoformat(),
                "delivery_date": entity.delivery_date.isoformat(),
                "seller_code": entity.seller.seller_code,
                "seller_id": entity.seller.id,
                "integration_type": entity.seller.get_integration_type().name
            }
            return message

        if isinstance(entity, OrderItem):
            return {"sku": entity.sku,
                    "name": entity.name,
                    "price": entity.price,
                    "original_price": entity.original_price,
                    "quantity": entity.quantity
                    }

        if isinstance(entity, OrderStatus):

            published_date = None
            if entity.published_date is not None:
                published_date = entity.published_date.strftime("%Y-%m-%d %H:%M:%S")

            return {"status": entity.status.name,
                    "comments": entity.comments,
                    "published_date": published_date,
                    "updated_date": entity.created_date.strftime("%Y-%m-%d %H:%M:%S")
                    }

        return None
