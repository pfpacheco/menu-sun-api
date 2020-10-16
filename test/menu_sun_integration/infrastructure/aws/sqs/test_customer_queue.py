from menu_sun_api import settings
import json
import pytest
from mock import patch

from menu_sun_integration.infrastructure.aws.sqs.customer_sqs_queue import CustomerSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.customer_mock import mock_queue_make_api_call


class TestCustomerQueue:

    @pytest.fixture
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def customer_queue(self):
        return CustomerSQSQueue()

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_send_message(self, customer_queue):
        payload = {"document": "00005234000121"}
        message_id = customer_queue.enqueue(body=json.dumps(payload))
        assert message_id

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_receive_message(self, customer_queue):
        mapped_customers = customer_queue.dequeue()
        customers = list(mapped_customers)
        assert (len(customers) == 1)
        customer = customers[0].body

        assert customer.document == "00005234000121"
        assert customer.customer_metafields[0].namespace == "Customer Namespace 1"
        assert customer.customer_metafields[0].key == "Customer Key 1"
        assert customer.customer_metafields[0].value == "Customer VALUE 1"
        assert customer.customer_metafields[1].namespace == "Customer Namespace 2"
        assert customer.customer_metafields[1].key == "Customer Key 2"
        assert customer.customer_metafields[1].value == "Customer VALUE 2"
        assert customer.payment_terms[0].deadline == 5
        assert customer.payment_terms[0].description == "Payment 5"
        assert customer.payment_terms[0].payment_type == "BOLETO"
        assert customer.payment_terms[1].deadline == 10
        assert customer.payment_terms[1].description == "Payment 10"
        assert customer.payment_terms[1].payment_type == "CHEQUE"
        assert customer.integration_type == "BRF"
        assert customer.seller_id == 1
        assert customer.seller_code == "ABC"
        assert customer.seller_metafields[0].namespace == "CODIGO_PAGAMENTO"
        assert customer.seller_metafields[0].key == "BOLETO_7"
        assert customer.seller_metafields[0].value == "007"
        assert customer.seller_metafields[1].namespace == "CODIGO_PAGAMENTO"
        assert customer.seller_metafields[1].key == "BOLETO_14"
        assert customer.seller_metafields[1].value == "014"

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_ack_message(self, customer_queue):
        handle = 'AQEBWvhuG9mMCVO0LE7k+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL/e1ZchKlZ0DTF6rc9Q' \
                 '+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10' \
                 '+w3fU6l63NRFnmNeDjuDw/uq86s0puouRFHQmoeNlLg' \
                 '/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT' \
                 '+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO' \
                 '+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA== '
        rs = customer_queue.processed(handle)
        assert rs
