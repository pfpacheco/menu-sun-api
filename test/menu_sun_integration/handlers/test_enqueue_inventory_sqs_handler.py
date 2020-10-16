from mock import patch

from menu_sun_api.application.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.inventory_sqs_queue import InventorySQSQueue
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_pernod_queue_mock import mock_queue_make_api_call
from menu_sun_api.domain.model.product.product_repository import ProductRepository


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueueInventoryBySku(IntegrationTest):

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_inventory_by_sku_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)
        ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="11080913010713", inventory=9)
        session.commit()

        queue = InventorySQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/inventory-queue")
        repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='inventory_by_sku', session=session,
                                                 seller_repository=repository,
                                                 platform_service=queue)

        result = platform_service.enqueue(seller_dummy=seller)

        assert (len(result.value) == 1)
