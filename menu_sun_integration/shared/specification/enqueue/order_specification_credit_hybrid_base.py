from sqlalchemy.sql.elements import BinaryExpression

from menu_sun_api.domain.model.order.order import Order, OrderStatusType, OrderStatus
from menu_sun_api.shared.specification import Specification
from sqlalchemy import and_, or_


class OrderSpecificationCreditHybridBase(Specification):
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        return and_(Order.seller_id == seller_id, Order.order_queue_date.is_(None),
                    Order.statuses.any(or_(OrderStatus.status == OrderStatusType.SELLER_REVIEW,
                                           OrderStatus.status == OrderStatusType.CREDIT_MENU)))
