from mock import patch

from menu_sun_api.domain.model.customer.customer import CustomerMetafield
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.default_pricing_sqs_queue import DefaultPricingSQSQueue
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_brf_mock import mock_queue_make_api_call


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueueDefaultPricingService(IntegrationTest):

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_default_pricing_brf_message(self, session):
        another_seller = build_seller(session, IntegrationType.BRF)
        seller = build_seller(session, IntegrationType.BRF)

        ProductFactory.create(seller_id=seller.id, name="Product One", sale_price=5.00, list_price=7.00)
        ProductFactory.create(seller_id=seller.id, name="Product Two", sale_price=8.00, list_price=9.00)
        ProductFactory.create(seller_id=another_seller.id, name="Product Three", sale_price=10.00, list_price=11.00)

        session.commit()

        queue = DefaultPricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/default-pricing-queue")
        seller_repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='product_default_pricing', session=session,
                                                 seller_repository=seller_repository, platform_service=queue)

        result = platform_service.enqueue(seller_dummy=seller)

        assert (len(result.value) == 1)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_default_pricing_aryzta_message(self, session):
        another_seller = build_seller(session, IntegrationType.ARYZTA)
        seller = build_seller(session, IntegrationType.ARYZTA)

        ProductFactory.create(seller_id=seller.id, name="Product One", sale_price=5.00, list_price=7.00)
        ProductFactory.create(seller_id=seller.id, name="Product Two", sale_price=8.00, list_price=9.00)
        ProductFactory.create(seller_id=another_seller.id, name="Product Three", sale_price=10.00, list_price=11.00)

        session.commit()

        queue = DefaultPricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/default-pricing-queue")
        seller_repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='product_default_pricing', session=session,
                                                 seller_repository=seller_repository, platform_service=queue)

        result = platform_service.enqueue(seller_dummy=seller)

        assert (len(result.value) == 1)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_default_pricing_benjamin_message(self, session):
        another_seller = build_seller(session, IntegrationType.BENJAMIN)
        seller = build_seller(session, IntegrationType.BENJAMIN)

        ProductFactory.create(seller_id=seller.id, name="Product One", sale_price=5.00, list_price=7.00)
        ProductFactory.create(seller_id=seller.id, name="Product Two", sale_price=8.00, list_price=9.00)
        ProductFactory.create(seller_id=another_seller.id, name="Product Three", sale_price=10.00, list_price=11.00)

        session.commit()

        queue = DefaultPricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/default-pricing-queue")
        seller_repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='product_default_pricing', session=session,
                                                 seller_repository=seller_repository, platform_service=queue)

        result = platform_service.enqueue(seller_dummy=seller)

        assert (len(result.value) == 1)
