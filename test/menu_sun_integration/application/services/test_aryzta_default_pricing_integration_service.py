import os
import pytest
from mock import patch

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType

from menu_sun_integration.application.services.product_default_pricing_integration_service import \
    ProductDefaultPricingIntegrationService
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_integration.infrastructure.aws.sqs.default_pricing_sqs_queue import DefaultPricingSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_aryzta_mock import mock_aws_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestAryztaProductDefaultPricingIntegrationService(IntegrationTest):
    document = "01838723032592"
    sku = "525500018"

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(id=1, seller_code='ABC', integration_type=IntegrationType.ARYZTA)
        session.commit()
        return seller

    @pytest.fixture
    def product(self, seller, session):
        product = ProductFactory.create(seller_id=seller.id, sku=self.sku)
        session.commit()

        return product

    @patch('botocore.client.BaseClient._make_api_call', new=mock_aws_make_api_call)
    def test_success_updated_product_default_pricing_from_s3(self, session, product, seller):
        platform_service = \
            DefaultPricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/default-pricing-queue")
        product_repository = ProductRepository(session=session)
        product_service = ProductService(repository=product_repository)

        integration_service = ProductDefaultPricingIntegrationService(session=session,
                                                                      product_service=product_service,
                                                                      platform_service=platform_service)

        integration_service.update_product_default_pricing_from_seller()

        session.commit()

        db = product_service.load_all(seller_id=seller.id)

        assert db
        products = db.value

        assert products[0].sku == "525500018"
        assert products[0].list_price == 107.399
        assert products[0].sale_price == 107.399
