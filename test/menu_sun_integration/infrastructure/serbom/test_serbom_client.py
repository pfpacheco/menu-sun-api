import pytest
import responses
import os

from mock import patch

from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.infrastructure.serbom.contexts.serbom_context_api import SerbomContextAPI
from menu_sun_integration.infrastructure.serbom.contexts.serbom_price_context_s3 import SerbomPriceS3Context
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderPostOrderRequest, SerbomOrderItemPostRequest, SerbomOrderCustomerPostRequest, \
    SerbomOrderAddressPostRequest
from menu_sun_integration.infrastructure.serbom.presentations.pricing.product. \
    serbom_product_default_pricing_detail_get_request import SerbomProductDefaultPricingDetailGetRequest
from menu_sun_integration.infrastructure.serbom.serbom_client import SerbomClient
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_aryzta_mock import mock_aws_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestSerbomClient:

    @pytest.fixture
    def serbom_context_api(self):
        return SerbomContextAPI()

    @pytest.fixture
    def order_repository(self, serbom_context_api):
        return OrderRepository(context=serbom_context_api)

    @pytest.fixture
    def serbom_context_s3(self):
        return SerbomPriceS3Context(bucket="ARYZTA_BUCKET")

    @pytest.fixture
    def product_repository(self, serbom_context_s3):
        return ProductRepository(context=serbom_context_s3)

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_aws_make_api_call)
    def test_request_client(self, order_repository, product_repository):
        items = [SerbomOrderItemPostRequest(sku="1013548", name="pao",
                                            quantity=12, price=13.00, weight=5.00, index=0),
                 SerbomOrderItemPostRequest(sku="1013549", name="torta",
                                            quantity=11, price=15.00, weight=10.00, index=1)
                 ]

        customer = SerbomOrderCustomerPostRequest(document="11762789110", name="jooj", telephone="9362864157")

        billing_address = SerbomOrderAddressPostRequest(street="Street", number=124, complement="complement",
                                                        neighborhood="the neighborhood", state_code="SP",
                                                        city="The_City", name="Duff", postcode="06555010")

        request = SerbomOrderPostOrderRequest(document_supplier="26230519000150", order_increment="2123791",
                                              order_id="2123791", document="11762789110", unb="UNB", items=items,
                                              customer=customer, shipping_address=billing_address)
        xml_file = open(
            os.path.join(
                here,
                'serbom_response/serbom_order_response.xml'))

        payload = xml_file.read()
        responses.add(responses.POST, os.getenv('URL_SEPARATION_SERBOM'), body=payload, status=200)
        client = SerbomClient(order_repository=order_repository, product_repository=product_repository)
        result = client.post_order(request)
        assert result

    @patch('botocore.client.BaseClient._make_api_call', new=mock_aws_make_api_call)
    def test_item_pricing(self, order_repository, product_repository):
        request_product = SerbomProductDefaultPricingDetailGetRequest()
        client = SerbomClient(order_repository=order_repository, product_repository=product_repository)
        result_product = client.get_products_default_pricing(request_product)
        assert result_product
