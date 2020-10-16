from menu_sun_api import settings
import json
import pytest
from mock import patch

from menu_sun_integration.infrastructure.aws.sqs.product_sqs_queue import ProductSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.product_queue_mock import mock_queue_make_api_call


class TestProductQueue:

    @pytest.fixture
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def product_queue(self):
        return ProductSQSQueue()

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_send_message(self, product_queue):
        payload = {'seller_id': "12345"}
        message_id = product_queue.enqueue(body=json.dumps(payload))
        assert message_id

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_receive_message(self, product_queue):
        mapped_products = product_queue.dequeue()
        products = list(mapped_products)
        assert (len(products) == 1)
        product = products[0].body

        assert product.integration_type == "BRF"
        assert product.seller_id == 1
        assert product.seller_code == "AAAA"
        assert product.seller_metafields[0].namespace == "Seller Namespace 1"
        assert product.seller_metafields[0].key == "Seller Key 1"
        assert product.seller_metafields[0].value == "Seller VALUE 1"
        assert product.seller_metafields[1].namespace == "Seller Namespace 2"
        assert product.seller_metafields[1].key == "Seller Key 2"
        assert product.seller_metafields[1].value == "Seller VALUE 2"

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_ack_message(self, product_queue):
        handle = 'AQEBWvhuG9mMCVO0LE7k+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL/e1ZchKlZ0DTF6rc9Q' \
                 '+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10' \
                 '+w3fU6l63NRFnmNeDjuDw/uq86s0puouRFHQmoeNlLg' \
                 '/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT' \
                 '+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO' \
                 '+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA== '
        rs = product_queue.processed(handle)
        assert rs
