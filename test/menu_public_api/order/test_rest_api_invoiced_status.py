from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.order.invoiced_status_handler import handle
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatusType, OwnerType
import pytest
import json


class TestRestApiInvoicedOrderStatus(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_invoiced_order_status(self, seller, session):
        customer = CustomerFactory.create(document='10851803792', seller_id=seller.id)
        session.commit()
        statuses = [OrderStatusFactory(status=OrderStatusType.NEW), OrderStatusFactory(status=OrderStatusType.APPROVED)]
        order = OrderFactory.create(seller_id=seller.id, order_id='12345', customer_id=customer.id, statuses=statuses)
        session.commit()

        data = {'order_id': order.order_id}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = handle(event, None)
        assert order.status.owner == OwnerType.SELLER
        assert rs
