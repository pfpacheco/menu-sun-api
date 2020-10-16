import datetime as datetime_sent_order
from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_integration.application.services.order_status_platform_service import OrderStatusPlatformService
from menu_sun_integration.infrastructure.aws.sqs.order_status_sqs_queue import OrderStatusSQSQueue
from menu_sun_api.domain.model.order.order import OrderStatusType, OwnerType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from test.menu_sun_api.db.order_factory import OrderStatusFactory, OrderFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from mock import patch
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_promax_mock import mock_queue_make_api_call


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueueUpdateOrderStatusService(IntegrationTest):
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_status_pernod_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)
        session.commit()
        customer = Customer(document="10851803792", seller_id=seller.id)
        session.commit()

        OrderFactory.create(seller_id=seller.id,
                            order_id='PR2',
                            seller_order_id='779628370',
                            customer=customer,
                            statuses=[
                                OrderStatusFactory(status=OrderStatusType.NEW,
                                                   published_date=datetime_sent_order.datetime.now(),
                                                   owner=OwnerType.MENU),
                                OrderStatusFactory(status=OrderStatusType.PENDING_INVOICE, comments="teste",
                                                   owner=OwnerType.MENU)]
                            )
        queue = OrderStatusSQSQueue()
        order_repository = OrderRepository(session)
        platform_service = OrderStatusPlatformService(order_repository=order_repository, platform_service=queue)

        result = platform_service.enqueue(seller=seller)

        assert (len(result.value) == 1)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_not_enqueue_status_pernod_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)
        session.commit()
        customer = Customer(document="10851803792", seller_id=seller.id)
        session.commit()

        OrderFactory.create(seller_id=seller.id,
                            order_id='PR2',
                            seller_order_id='779628370',
                            customer=customer,
                            statuses=[
                                OrderStatusFactory(status=OrderStatusType.NEW,
                                                   published_date=datetime_sent_order.datetime.now(),
                                                   owner=OwnerType.SELLER),
                                OrderStatusFactory(status=OrderStatusType.PENDING_INVOICE, comments="teste",
                                                   owner=OwnerType.SELLER)]
                            )

        queue = OrderStatusSQSQueue()
        order_repository = OrderRepository(session)
        platform_service = OrderStatusPlatformService(order_repository=order_repository, platform_service=queue)

        result = platform_service.enqueue(seller=seller)

        assert (len(result.value) == 0)
