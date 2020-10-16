import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType, SellerMetafield
from menu_sun_integration.application.services.product_default_pricing_integration_service import \
    ProductDefaultPricingIntegrationService

from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.pricing_factory import PricingFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_integration.infrastructure.aws.sqs.default_pricing_sqs_queue import DefaultPricingSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.default_pricing_queue_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestBRFProductDefaultPricingIntegrationService(IntegrationTest):
    document = "01838723032592"
    sku = "000000000000044601"
    cep = "06803277"

    @pytest.fixture
    def seller(self, session):
        document = SellerMetafield(
            namespace="INTEGRATION_API_FIELD", key="CDD_DOCUMENT", value="01838723032592")

        postal_code = SellerMetafield(
            namespace="INTEGRATION_API_FIELD", key="CDD_POSTAL_CODE", value="06803277")
        seller = SellerFactory.create(seller_code='ABC', integration_type=IntegrationType.BRF)
        seller.change_metafield(document)
        seller.change_metafield(postal_code)
        session.commit()
        return seller

    @pytest.fixture
    def customer(self, seller, session):
        customer = CustomerFactory.create(seller_id=seller.id, document=self.document, cep=self.cep)
        session.commit()
        return customer

    @pytest.fixture
    def product(self, seller, session):
        product = ProductFactory.create(seller_id=seller.id, sku=self.sku)
        session.commit()

        return product

    @pytest.fixture
    def pricing(self, customer, product, session):
        pricing = PricingFactory.create(product_id=product.id, customer_id=customer.id, list_price=1, sale_price=0.99)
        session.commit()
        return pricing

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_updated_customer_pricing_with_valid_token(self, session, product, pricing, customer,
                                                               seller):
        metafield_postal_code = next((field for field in seller.metafields
                                      if field.namespace == "INTEGRATION_API_FIELD" and field.key == "CDD_POSTAL_CODE"),
                                     None)
        postal_code = metafield_postal_code.value if metafield_postal_code else ""

        metafield_document = next(
            (field for field in seller.metafields
             if field.namespace == "INTEGRATION_API_FIELD" and field.key == "CDD_DOCUMENT"), None)

        document = metafield_document.value if metafield_document else ""

        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_pricing_by_customer_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/prices/v1/Pricing?'
                                     f'Document={document}&PostalCode={postal_code}', json=response,
                      status=200)

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

        assert products[0].sku == response[0]["sku"]
