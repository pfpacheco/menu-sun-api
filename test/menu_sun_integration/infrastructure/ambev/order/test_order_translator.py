import pytest
import dateutil.parser
import pytz
from mock import MagicMock

from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_request import \
    PromaxOrderItemPostRequest, PromaxOrderPostRequest
from menu_sun_integration.infrastructure.ambev.translators.promax_order_translator import PromaxOrderTranslator
from menu_sun_integration.presentations.order.order_sqs_platform import OrderSQSMessagePlatform, OrderDetailSQSPlatform, \
    OrderItemDetailSQSPlatform
from test.menu_sun_integration.infrastructure.stubs.FakeClient import FakeClient


class TestOrderTranslator:
    @pytest.fixture
    def order_raw_from_platform(self):
        payload = {
            "ReceiptHandle": "AAAAA",
            "Body": {
                "order_id": "99999999",
                "items": [
                    {
                        "sku": "13201",
                        "name": "Cerveja Beck's",
                        "ean": "42040613",
                        "ncm": "2203.00.00",
                        "price": 31.80,
                        "quantity": 1
                    },
                    {
                        "sku": "13202",
                        "name": "Cerveja Beck's",
                        "ean": "42040613",
                        "ncm": "2203.00.00",
                        "price": 31.80,
                        "quantity": 1
                    }
                ],
                "order_date": "13-04-2020T02:41:25",
                "delivery_date": "14-04-2020T02:41:25",
                "seller_code": "0810204",
                "payment_code": "2",
                "document": "00005234000121",
                "seller_id": 1,
                "integration_type": "NONE"
            }
        }
        return payload

    @pytest.fixture
    def order_from_platform(self, order_raw_from_platform):
        receipt_handle = order_raw_from_platform["ReceiptHandle"]
        order_detail = OrderDetailSQSPlatform.from_dict(order_raw_from_platform["Body"])
        order_detail_items = [OrderItemDetailSQSPlatform.from_dict(item) for item in
                              order_raw_from_platform["Body"]["items"]]
        order_detail.items = order_detail_items
        return OrderSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)

    @pytest.fixture
    def request_to_promax(self, order_from_platform: OrderSQSMessagePlatform):
        promax_order_items = (PromaxOrderItemPostRequest(item.sku, item.quantity, item.price)
                              for item in order_from_platform.body.items)
        tz = pytz.timezone('America/Sao_Paulo')

        order_date_parse = dateutil.parser.parse(order_from_platform.body.order_date)
        order_date = pytz.utc.localize(order_date_parse).astimezone(tz).strftime('%d/%m/%Y')

        delivery_date_parse = dateutil.parser.parse(order_from_platform.body.delivery_date)
        delivery_date = pytz.utc.localize(delivery_date_parse).astimezone(tz).strftime('%d/%m/%Y')

        promax_order_request = PromaxOrderPostRequest(order_from_platform.body.order_id,
                                                      order_from_platform.body.document,
                                                      order_date, delivery_date, order_from_platform.body.seller_code,
                                                      order_from_platform.body.payment_code, promax_order_items)
        return promax_order_request

    def test_translation_of_orders_to_promax(self, order_from_platform: OrderSQSMessagePlatform,
                                             request_to_promax: PromaxOrderPostRequest):
        fake_client = FakeClient()
        fake_client.post_order = MagicMock(return_value=True)
        translator = PromaxOrderTranslator()
        adapter = OrderAdapter(client=fake_client, translator=translator)
        adapter.send_to_seller(order_from_platform.body)

        requested: PromaxOrderPostRequest = fake_client.post_order.call_args_list[0][0][0]
        assert fake_client.post_order.called
        assert fake_client.post_order.call_count == 1
        assert request_to_promax.order_id == requested.order_id
        assert request_to_promax.document == requested.document
        assert request_to_promax.payment_code == requested.payment_code
        assert request_to_promax.order_date == requested.order_date
        assert request_to_promax.delivery_date == requested.delivery_date

        for promax_item_request, promax_item_requested in zip(request_to_promax.items, requested.items):
            assert promax_item_request.sku == promax_item_requested.sku
            assert promax_item_request.quantity == promax_item_requested.quantity
            assert promax_item_request.price == promax_item_requested.price
