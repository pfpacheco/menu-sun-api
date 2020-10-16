import json
import pytest
import os
import responses
import sys
import logging
from mock import patch

from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.infrastructure.aws.sqs.default_pricing_sqs_queue import DefaultPricingSQSQueue
from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_integration.application.services.product_default_pricing_integration_service import \
    ProductDefaultPricingIntegrationService
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_aryzta_mock import mock_queue_make_api_call, S3Object

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

here = os.path.dirname(os.path.realpath(__file__))


def generated_payload():
    lines = open(
        os.path.join(
            here,
            '../infrastructure/aws/sqs/mocks/pricing/prices.csv'))

    items = []
    for line in lines:
        line = line.rsplit(";")
        items.append(
            {
                "destinationSku": line[0],
                "priceSale": round(float(line[1].replace("\n", "").replace(",", "."))),
                "priceBase": round(float(line[1].replace("\n", "").replace(",", ".")))
            }
        )

    payload = {"items": items}
    return payload


class TestDequeueProductDefaultPricingAryztaHandler(IntegrationTest):

    @pytest.fixture(name="generated_payload")
    def active_payload(self):
        return generated_payload()

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_dequeue_product_default_pricing_benjamin(self, session, payload=None):

        if payload is None:
            payload = generated_payload()

        seller = SellerFactory.create(id=1, integration_type=IntegrationType.BENJAMIN)
        session.commit()

        ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="525200073", list_price=30, sale_price=20)
        session.commit()

        default_pricing_sqs_queue = DefaultPricingSQSQueue()
        domain_repository = ProductRepository()
        domain_service = ProductService(repository=domain_repository)
        integration_service = ProductDefaultPricingIntegrationService(
            session,
            platform_service=default_pricing_sqs_queue,
            product_service=domain_service
        )
        integration_service.update_product_default_pricing_from_seller()

        session.commit()

        db = domain_service.load_all(seller_id=seller.id)

        assert db
        products = db.value

        assert products[0].sku == payload["items"][0]["destinationSku"]
        assert products[0].list_price == int(round(payload["items"][0]["priceSale"]))
        assert products[0].sale_price == int(round(payload["items"][0]["priceBase"]))
