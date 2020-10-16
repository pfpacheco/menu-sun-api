from mock import patch
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.pricing_by_sku_sqs_queue import PricingBySkuSQSQueue
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_pernod_queue_mock import mock_queue_make_api_call


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueueDefaultPricingBySkuService(IntegrationTest):

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_default_pricing_by_sku_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)

        ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="11080913010713", list_price=799,
                              sale_price=799)
        session.commit()

        queue = PricingBySkuSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/default-pricing-queue")
        repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='product_default_pricing_by_sku', session=session,
                                                 seller_repository=repository, platform_service=queue)

        result = platform_service.enqueue(seller_dummy=seller)

        assert (len(result.value) == 1)
