from sqlalchemy import and_

from menu_sun_api.domain.db_repository import DBRepository
from menu_sun_api.domain.model.order.order import Order, OrderStatus, OrderStatusType
import logging

from menu_sun_api.shared.specification import Specification

logger = logging.getLogger()


class OrderRepository(DBRepository):

    def __init__(self, session=None):
        super().__init__(Order, session)

    def get_order(self, seller_id, order_id):
        query = self.session.query(Order). \
            filter(
            and_(
                Order.seller_id == seller_id,
                Order.order_id == order_id))
        order = query.one_or_none()
        return order

    def get_order_not_seller_id(self, order_id):
        query = self.session.query(Order). \
            filter(
            and_(
                Order.order_id == order_id))
        order = query.one_or_none()
        return order

    def load_order_status(self, seller_id, order_id):
        query = self.session.query(OrderStatus). \
            outerjoin(Order). \
            filter(and_(Order.seller_id == seller_id, Order.order_id == order_id)). \
            order_by(OrderStatus.id)
        statuses = query.all()
        return statuses

    def append_status(self, status):
        self.session.add(status)

    def load_pending_orders(self, seller_id):
        orders = self.session.query(Order). \
            filter(
            and_(
                Order.order_queue_date.is_(None),
                Order.seller_id == seller_id)).all()
        ls = []
        for order in orders:
            logger.info('Filtering order: [{}]'.format(order.order_id))
            status = order.status

            if status:
                logger.info('Order status: [{}]'.format(status.status))
                if status.status == OrderStatusType.APPROVED:
                    ls.append(order)
        return ls

    def mark_as_integrated(self, seller_id, order_id):
        from datetime import datetime
        order = self.get_order(seller_id=seller_id, order_id=order_id)
        order.integration_date = datetime.utcnow()

    def load_orders_on_wms(self, seller_id):
        orders = self.session.query(Order). \
            filter(and_(Order.integration_date is not None, Order.seller_id == seller_id)). \
            filter(and_(Order.created_date >= '2020-02-01')). \
            all()

        ls = []
        for order in orders:
            if order.on_wms():
                logger.info('Filtering order: [{}]'.format(order.order_id))
                ls.append(order)
        return ls

    def load_order_by_order_id(self, seller_id, order_id):
        orders = self.session.query(Order). \
            filter(and_(Order.integration_date is not None, Order.seller_id == seller_id)). \
            filter(and_(Order.order_id == order_id)). \
            limit(1)

        ls = []
        for order in orders:
            if order.on_wms():
                logger.info('Filtering order: [{}]'.format(order.order_id))
                ls.append(order)

        return ls

    def list_orders_with_unpublished_status(self, seller_id):
        stmt = self.session.query(OrderStatus.order_id). \
            join(Order). \
            filter(and_(OrderStatus.published_date is None,
                        Order.seller_id == seller_id)).distinct()
        statuses = self.session.query(Order). \
            filter(Order.id.in_(stmt)).all()
        return statuses

    def filter_by_specification(self, seller_id: int, specification: Specification):
        query = self.session.query(Order)
        return query.filter(specification.is_satisfied_by(seller_id)).all()

    def list_orders_by_status(self, seller_id, status_filter):
        orders = self.session.query(Order). \
            filter(Order.seller_id == seller_id).all()

        logger.info('Filtering order by status: [{}]'.format(status_filter))
        logger.info('Filtering all orders: {}'.format(list(map(lambda x: str(x), orders))))
        result = [order for order in orders if order.status.status == status_filter]
        logger.info('Filtered orders: {}'.format(list(map(lambda x: str(x), result))))

        return result
