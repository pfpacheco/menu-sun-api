from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
import pytest
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatusType


class TestOrderRepository(IntegrationTest):

    @pytest.fixture(autouse=True)
    def seller(self, session):
        seller = SellerFactory.create()
        session.commit()
        return seller

    def test_load_all_status(self, seller, session):
        customer = CustomerFactory(seller_id=seller.id)
        order = OrderFactory.create(
            seller_id=seller.id,
            order_id='12345',
            customer=customer)
        s1 = OrderStatusFactory(status=OrderStatusType.NEW)
        s2 = OrderStatusFactory(status=OrderStatusType.APPROVED)
        s3 = OrderStatusFactory(status=OrderStatusType.INVOICED)
        order.statuses.append(s1)
        order.statuses.append(s2)
        order.statuses.append(s3)
        session.commit()
        repository = OrderRepository(session)
        order_status = repository.load_order_status(
            order_id=order.order_id, seller_id=seller.id)
        assert (len(order_status) == 3)

    def test_should_load_pending_orders(self, seller, session):
        customer = CustomerFactory(seller_id=seller.id)
        statuses = [
            OrderStatusFactory(
                status=OrderStatusType.NEW), OrderStatusFactory(
                status=OrderStatusType.APPROVED)]
        OrderFactory.create(
            seller_id=seller.id,
            order_id='1',
            customer=customer,
            statuses=statuses)
        session.commit()

        customer = CustomerFactory(seller_id=seller.id)
        statuses = [
            OrderStatusFactory(
                status=OrderStatusType.NEW), OrderStatusFactory(
                status=OrderStatusType.APPROVED)]
        OrderFactory.create(
            seller_id=seller.id,
            order_id='2',
            customer=customer,
            statuses=statuses)
        session.commit()
        #
        repository = OrderRepository(session)
        ls = repository.load_pending_orders(seller_id=seller.id)
        assert (len(ls) == 2)

    def test_should_load_on_wms_orders(self, seller, session):
        from datetime import datetime
        customer = CustomerFactory(seller_id=seller.id)
        statuses = [
            OrderStatusFactory(
                status=OrderStatusType.NEW), OrderStatusFactory(
                status=OrderStatusType.APPROVED)]
        order = OrderFactory.create(seller_id=seller.id,
                                    order_id='1',
                                    customer=customer,
                                    integration_date=datetime.utcnow(),
                                    statuses=statuses)
        session.commit()
        repository = OrderRepository(session)
        ls = repository.load_orders_on_wms(seller_id=seller.id)
        assert (len(ls) == 1)

    def test_should_load_orders_with_unpublished_events(self, seller, session):
        from datetime import datetime
        customer = CustomerFactory(seller_id=seller.id)
        order = OrderFactory.create(seller_id=seller.id,
                                    customer=customer,
                                    statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                              OrderStatusFactory(status=OrderStatusType.APPROVED)])
        session.commit()

        repository = OrderRepository(session)
        ls = repository.list_orders_with_unpublished_status(
            seller_id=seller.id)
        assert (len(ls) == 0)
