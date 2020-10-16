from datetime import datetime, timedelta

import pytest
import json
from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.order.order_get_by_status_handler import handle
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatusType


class TestOrderGetByStatusHandler(IntegrationTest):
    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABC')
        session.commit()
        return seller

    @pytest.fixture
    def customer(self, session, seller):
        customer = CustomerFactory.create(document='444129288788', seller_id=seller.id)
        session.commit()
        return customer

    @pytest.fixture
    def orders(self, session, seller, customer):

        statuses = [OrderStatusFactory(status=OrderStatusType.NEW,
                                       created_date=datetime.now() - timedelta(seconds=1)),
                    OrderStatusFactory(status=OrderStatusType.CREDIT_MENU,
                                       created_date=datetime.now())]
        order_0002 = OrderFactory.create(seller_id=seller.id, order_id='00002', customer_id=customer.id,
                                         statuses=statuses)
        statuses = [OrderStatusFactory(status=OrderStatusType.NEW,
                                       created_date=datetime.now() - timedelta(seconds=2)),
                    OrderStatusFactory(status=OrderStatusType.PROCESSING,
                                       created_date=datetime.now() - timedelta(seconds=1)),
                    OrderStatusFactory(status=OrderStatusType.CREDIT_MENU,
                                       created_date=datetime.now())]
        order_0003 = OrderFactory.create(seller_id=seller.id, order_id='00003', customer_id=customer.id,
                                         statuses=statuses)
        statuses = [OrderStatusFactory(status=OrderStatusType.CREDIT_MENU,
                                       created_date=datetime.now() - timedelta(seconds=1)),
                    OrderStatusFactory(status=OrderStatusType.APPROVED,
                                       created_date=datetime.now())]
        order_0001 = OrderFactory.create(seller_id=seller.id, order_id='00001', customer_id=customer.id,
                                         statuses=statuses)
        session.commit()
        return [order_0001, order_0002, order_0003]

    def test_order_get_by_status(self, seller, customer, orders):
        event = {"queryStringParameters": {'status': "CREDIT_MENU"},
                 "headers": {'Authorization': seller.token}}

        rs = handle(event, None)

        assert rs['statusCode'] == 200
        body = json.loads(rs['body'])
        assert len(body) == 2
        assert body[0]['order_id'] == '00002'
        assert body[1]['order_id'] == '00003'
