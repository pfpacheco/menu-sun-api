import datetime as datetime_sent_order

from menu_sun_api.domain.model.customer.customer import Customer, PaymentType, CustomerMetafield
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.order_status_notification_sqs_queue import \
    OrderStatusNotificationSQSQueue
from menu_sun_api.domain.model.order.order import OrderStatusType
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
    def test_should_enqueue_promax_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)
        customer = Customer(document="10851803792", seller_id=seller.id)
        session.commit()

        OrderFactory.create(seller_id=seller.id,
                            order_id='PR2',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW,
                                                         published_date=datetime_sent_order.datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.APPROVED,
                                                         published_date=datetime_sent_order.datetime.now())]
                            )

        queue = OrderStatusNotificationSQSQueue()
        seller_repository = SellerRepository()
        platform_service = SellerPlatformService(entity='order_status_notification', session=session,
                                                 seller_repository=seller_repository, platform_service=queue)

        result = platform_service.enqueue(seller_dummy=seller)

        assert (len(result.value) == 1)
