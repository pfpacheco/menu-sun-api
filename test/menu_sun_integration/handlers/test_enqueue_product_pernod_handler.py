from mock import patch

from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.product_sqs_queue import ProductSQSQueue
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.product_pernod_queue_mock import mock_queue_make_api_call


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueueProductService(IntegrationTest):

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_brf_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)

        session.commit()

        queue = ProductSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/product-queue")
        repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='product', session=session, seller_repository=repository,
                                                 platform_service=queue)

        result = platform_service.enqueue(seller)

        assert (len(result.value) == 1)
