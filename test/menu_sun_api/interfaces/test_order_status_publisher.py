from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
import pytest
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatusType
import responses
import os


class TestOrderStatusPublisher(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create()
        session.commit()
        return seller

    @responses.activate
    def test_should_publish_order_status(self, seller, session):
        from menu_sun_api.interfaces.order_status_publisher import handler
        customer = CustomerFactory(seller_id=seller.id)
        OrderFactory.create(seller_id=seller.id,
                            order_id='1',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                      OrderStatusFactory(status=OrderStatusType.APPROVED)])
        session.commit()

        order_status_webhook = 'https://ena0zvwf6vacc.x.pipedream.net/'
        bearer_token_callback = '111'
        header = {'Authorization': "Bearer " + bearer_token_callback}
        os.environ["ORDER_STATUS_WEBHOOK"] = order_status_webhook
        responses.add(responses.POST, order_status_webhook,
                      headers=header, status=200)
        handler({}, {})
