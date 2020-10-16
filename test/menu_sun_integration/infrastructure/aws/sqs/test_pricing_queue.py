from menu_sun_api import settings
import json
import pytest
from mock import patch

from menu_sun_integration.infrastructure.aws.sqs.pricing_sqs_queue import PricingSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.pricing_mock import mock_queue_make_api_call


class TestPricingQueue:

    @pytest.fixture
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def pricing_queue(self):
        return PricingSQSQueue()

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_send_message(self, pricing_queue):
        payload = {"document": "00005234000121"}
        message_id = pricing_queue.enqueue(body=json.dumps(payload))
        assert message_id

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_receive_message(self, pricing_queue):
        mapped_pricing = pricing_queue.dequeue()
        pricing_list = list(mapped_pricing)
        assert (len(pricing_list) == 1)
        pricing = pricing_list[0].body

        assert pricing.document == "00005234000121"
        assert pricing.customer_metafields[0].namespace == "Customer Namespace 1"
        assert pricing.customer_metafields[0].key == "Customer Key 1"
        assert pricing.customer_metafields[0].value == "Customer VALUE 1"
        assert pricing.customer_metafields[1].namespace == "Customer Namespace 2"
        assert pricing.customer_metafields[1].key == "Customer Key 2"
        assert pricing.customer_metafields[1].value == "Customer VALUE 2"
        assert pricing.payment_terms[0].deadline == 5
        assert pricing.payment_terms[0].description == "Payment 5"
        assert pricing.payment_terms[0].payment_type == "BOLETO"
        assert pricing.payment_terms[1].deadline == 10
        assert pricing.payment_terms[1].description == "Payment 10"
        assert pricing.payment_terms[1].payment_type == "CHEQUE"
        assert pricing.integration_type == "BRF"
        assert pricing.seller_id == 1
        assert pricing.seller_code == "ABC"
        assert pricing.seller_metafields[0].namespace == "Seller Namespace 1"
        assert pricing.seller_metafields[0].key == "Seller Key 1"
        assert pricing.seller_metafields[0].value == "Seller VALUE 1"
        assert pricing.seller_metafields[1].namespace == "Seller Namespace 2"
        assert pricing.seller_metafields[1].key == "Seller Key 2"
        assert pricing.seller_metafields[1].value == "Seller VALUE 2"

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_ack_message(self, pricing_queue):
        handle = 'AQEBWvhuG9mMCVO0LE7k+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL/e1ZchKlZ0DTF6rc9Q' \
                 '+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10' \
                 '+w3fU6l63NRFnmNeDjuDw/uq86s0puouRFHQmoeNlLg' \
                 '/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT' \
                 '+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO' \
                 '+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA== '
        rs = pricing_queue.processed(handle)
        assert rs
