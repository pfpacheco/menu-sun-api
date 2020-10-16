from menu_sun_api.domain.model.order.order import OrderStatus, OrderStatusType, OwnerType
from menu_sun_api.domain.model.response.success_response import SuccessResponse
import logging

logger = logging.getLogger()


class OrderService:

    def __init__(self, repository):
        self.repository = repository

    def create_order(self, order):
        status = OrderStatus(status=OrderStatusType.NEW, owner=OwnerType.MENU)
        order.statuses.append(status)
        rs = self.repository.add(order)
        return SuccessResponse(rs)

    def get_order(self, seller_id, order_id):
        order = self.repository.get_order(seller_id=seller_id,
                                          order_id=order_id)
        return SuccessResponse(order)

    def load_all(self, seller_id, limit, offset):
        orders = self.repository.load_all(
            seller_id=seller_id, limit=limit, offset=offset)
        return SuccessResponse(orders)

    def load_statuses(self, seller_id, order_id):
        statuses = self.repository.load_order_status(seller_id, order_id)
        return SuccessResponse(statuses)

    def load_pending_orders(self, seller_id):
        rs = self.repository.load_pending_orders(seller_id=seller_id)
        return SuccessResponse(rs)

    def load_orders_by_start_end_date(self, start_date, end_date, seller_id):
        rs = self.repository.load_orders_by_start_end_date(
            start_date, end_date, seller_id)
        return SuccessResponse(rs)

    def mark_order_as_integrated(self, order_id, seller_id):
        rs = self.repository.mark_as_integrated(seller_id, order_id)
        return SuccessResponse(rs)

    def list_orders_by_status(self, status, seller_id):
        status_filter = OrderStatusType.get_value(status.upper())
        rs = self.repository.list_orders_by_status(seller_id=seller_id, status_filter=status_filter)
        return SuccessResponse(rs)
