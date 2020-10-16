from menu_sun_api import settings
import json
import pytest
from mock import patch

from menu_sun_integration.infrastructure.aws.sqs.inventories_sqs_queue import InventoriesSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_queue_mock import mock_queue_make_api_call


class TestInventoryQueue:

    @pytest.fixture
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def inventory_queue(self):
        return InventoriesSQSQueue()

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_send_message(self, inventory_queue):
        payload = {'seller_id': "12345"}
        message_id = inventory_queue.enqueue(body=json.dumps(payload))
        assert message_id

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_receive_message(self, inventory_queue):
        mapped_inventories = inventory_queue.dequeue()
        inventories = list(mapped_inventories)
        assert (len(inventories) == 1)
        inventory = inventories[0].body

        assert inventory.integration_type == "BRF"
        assert inventory.seller_id == 1
        assert inventory.seller_code == "AAAA"
        assert inventory.seller_metafields[0].namespace == "INTEGRATION_API_FIELD"
        assert inventory.seller_metafields[0].key == "CDD_DOCUMENT"
        assert inventory.seller_metafields[0].value == "0000.0000.00000/0-00"
        assert inventory.seller_metafields[1].namespace == "INTEGRATION_API_FIELD"
        assert inventory.seller_metafields[1].key == "CDD_POSTAL_CODE"
        assert inventory.seller_metafields[1].value == "13213085"

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_ack_message(self, inventory_queue):
        handle = 'AQEBWvhuG9mMCVO0LE7k+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL/e1ZchKlZ0DTF6rc9Q' \
                 '+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10' \
                 '+w3fU6l63NRFnmNeDjuDw/uq86s0puouRFHQmoeNlLg' \
                 '/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT' \
                 '+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO' \
                 '+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA== '
        rs = inventory_queue.processed(handle)
        assert rs
