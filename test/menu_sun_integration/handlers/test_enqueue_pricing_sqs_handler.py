from mock import patch

from menu_sun_api.domain.model.customer.customer import CustomerMetafield
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.customer_platform_service import CustomerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.pricing_sqs_queue import PricingSQSQueue
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_brf_mock import mock_queue_make_api_call


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueuePricingService(IntegrationTest):

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_brf_message(self, session):
        another_seller = build_seller(session, IntegrationType.BRF)
        seller = build_seller(session, IntegrationType.BRF)

        ProductFactory.create(seller_id=seller.id, name="Product One")
        ProductFactory.create(seller_id=seller.id, name="Product Two")
        ProductFactory.create(seller_id=another_seller.id, name="Product Three")

        session.commit()

        CustomerFactory.create(document="10851803792", seller_id=seller.id,
                               metafields=[CustomerMetafield(namespace="NAMESPACE_1", key="KEY_1",
                                                             value="VALUE_1")])
        CustomerFactory.create(document="10851803793", seller_id=seller.id,
                               metafields=[CustomerMetafield(namespace="NAMESPACE_2", key="KEY_2",
                                                             value="VALUE_2"),
                                           CustomerMetafield(namespace="NAMESPACE_3", key="KEY_3",
                                                             value="VALUE_3")])
        CustomerFactory.create(document="10851803793", seller_id=another_seller.id)

        session.commit()

        queue = PricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/pricing-queue")
        repository = CustomerRepository(session)
        platform_service = CustomerPlatformService(entity='customer_pricing', session=session,
                                                   customer_repository=repository, platform_service=queue)

        result = platform_service.enqueue(seller=seller)

        assert (len(result.value) == 2)
