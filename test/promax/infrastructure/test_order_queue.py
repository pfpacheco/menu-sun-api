from promax.infrastructure.sqs.order_queue import OrderQueue
import json
import pytest
from test.promax.infrastructure.order_queue_mock import mock_make_api_call
from mock import patch
from menu_sun_api import settings


class TestOrderQueue():

    @pytest.fixture
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    def order_queue(self):
        return OrderQueue(
            queue_url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")

    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    def test_send_message(self, order_queue):
        payload = {'order_id': "12345"}
        message_id = order_queue.send_message(body=json.dumps(payload))
        assert(message_id)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    def test_receive_message(self, order_queue):
        rs = order_queue.receive_messages()
        assert (len(rs) == 1)
        data = rs[0]
        order = json.loads(data['Body'])
        assert (order['order_id'] == "12345")

    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    def test_ack_message(self, order_queue):
        handle = 'AQEBWvhuG9mMCVO0LE7k+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL/e1ZchKlZ0DTF6rc9Q+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10+w3fU6l63NRFnmNeDjuDw/uq86s0puouRFHQmoeNlLg/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA=='
        rs = order_queue.ack_message(handle)
        assert(rs)
