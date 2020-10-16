from sqlalchemy import and_, or_
from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.order.order import (Order, OrderStatusType,
                                                   OrderStatus, OwnerType)
from menu_sun_api.shared.specification import Specification


class OrderStatusSpecificationCreditPreApproved(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        or_conditions = [
            OrderStatus.status == OrderStatusType.PENDING,
            OrderStatus.status == OrderStatusType.PENDING_INVOICE,
            OrderStatus.status == OrderStatusType.ORDER_INVOICED,
            OrderStatus.status == OrderStatusType.COMPLETE,
            OrderStatus.status == OrderStatusType.ENTREGUE,
            OrderStatus.status == OrderStatusType.CLOSED,
            OrderStatus.status == OrderStatusType.ORDER_REFUNDED,
            OrderStatus.status == OrderStatusType.CANCELED
        ]

        and_conditions = [
            Order.seller_id == seller_id,
            Order.order_queue_date.is_(None),
            OrderStatus.owner == OwnerType.MENU
        ]

        return and_(*and_conditions, Order.statuses.any(or_(*or_conditions)))
