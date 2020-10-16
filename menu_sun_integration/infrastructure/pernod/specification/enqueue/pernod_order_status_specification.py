from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.order.order import Order, OrderStatusType, OrderStatus
from menu_sun_api.shared.specification import Specification
from sqlalchemy import and_, or_


class PernodOrderStatusSpecification(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        return and_(Order.seller_id == seller_id,
                    Order.statuses.any(and_(OrderStatus.published_date.is_(None),
                                            or_(OrderStatus.status == OrderStatusType.PENDING_INVOICE,
                                                OrderStatus.status == OrderStatusType.CANCELED))))
