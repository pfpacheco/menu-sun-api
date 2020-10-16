from promax.application.order_integration_service import OrderIntegrationService
from menu_sun_api.application.order_service import OrderService
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
import pytest
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory, OrderItemFactory
from menu_sun_api.domain.model.order.order import OrderPayment, OrderStatusType
from menu_sun_api.domain.model.customer.customer import Customer
from unittest.mock import MagicMock


class TestOrderIntegrationService(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create()
        session.commit()
        return seller

    def test_should_enqueue_message(self, seller, session):
        customer = Customer(document="10851803792", seller_id=seller.id)
        statuses = [OrderStatusFactory(status=OrderStatusType.NEW),
                    OrderStatusFactory(status=OrderStatusType.APPROVED)]
        OrderFactory.create(seller_id=seller.id,
                            order_id='2',
                            customer=customer,
                            statuses=statuses
                            )
        session.commit()
        order_queue = MagicMock()
        order_queue.send_message.return_value = '12345'
        order_repository = OrderRepository()
        order_service = OrderService(order_repository)
        order_integration_service = OrderIntegrationService(order_service=order_service,
                                                            order_queue=order_queue)
        rs = order_integration_service.enqueue_pending_orders(
            seller_id=seller.id)
        assert (len(rs.value) == 1)
