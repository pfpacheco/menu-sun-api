from menu_sun_api import settings
import json
import pytest
from mock import patch
from menu_sun_integration.infrastructure.aws.sqs.order_sqs_queue import OrderSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_mock import mock_queue_make_api_call


class TestOrderQueue:

    @pytest.fixture
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def order_queue(self):
        return OrderSQSQueue()

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_send_message(self, order_queue):
        payload = {'order_id': "12345"}
        message_id = order_queue.enqueue(body=json.dumps(payload))
        assert message_id

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_receive_message(self, order_queue):
        mapped_orders = order_queue.dequeue()
        orders = list(mapped_orders)
        assert (len(orders) == 1)
        order = orders[0]
        assert (order.body.order_id == "12345")
        assert (order.body.shipping_address.name is None)
        assert (order.body.billing_address.name is not None)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_ack_message(self, order_queue):
        handle = 'AQEBWvhuG9mMCVO0LE7k+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL/e1ZchKlZ0DTF6rc9Q' \
                 '+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10' \
                 '+w3fU6l63NRFnmNeDjuDw/uq86s0puouRFHQmoeNlLg' \
                 '/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT' \
                 '+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO' \
                 '+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA== '
        rs = order_queue.processed(handle)
        assert rs
