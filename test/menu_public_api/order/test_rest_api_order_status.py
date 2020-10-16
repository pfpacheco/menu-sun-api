from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.order.create_order_status_handler import handle
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatusType, OwnerType
from datetime import datetime
import pytest
import json


class TestRestApiApprovedOrderStatus(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_order_status(self, seller, session):
        customer = CustomerFactory.create(document='10851803792', seller_id=seller.id)
        statuses = [OrderStatusFactory(status=OrderStatusType.NEW), OrderStatusFactory(status=OrderStatusType.APPROVED)]
        order = OrderFactory.create(seller_id=seller.id, order_id='M22345', customer_id=customer.id, statuses=statuses,
                                    order_queue_date=datetime.utcnow().isoformat())
        session.commit()

        data = {'order_id': order.order_id, 'comments': 'teste comentario', 'status': 'CREDIT_MENU'}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': '{}'.format(seller.token)}
                 }

        rs = handle(event, None)
        assert order.status.owner == OwnerType.SELLER
        assert rs
