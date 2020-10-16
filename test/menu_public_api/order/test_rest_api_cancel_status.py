from menu_sun_api.domain.model.order.order import OwnerType
from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.order.cancel_status_handler import handle
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory
import pytest
import json


class TestRestApiCancelOrderStatus(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_cancel_order_status(self, seller, session):
        customer = CustomerFactory.create(document='10851803792', seller_id=seller.id)
        order = OrderFactory.create(seller_id=seller.id, order_id='123456', customer_id=customer.id)
        session.commit()

        data = {'order_id': order.order_id}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = handle(event, None)
        assert order.status.owner == OwnerType.SELLER
        assert rs
