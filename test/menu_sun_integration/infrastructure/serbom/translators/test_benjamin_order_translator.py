import pytest
from mock import MagicMock

from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderPostOrderRequest
from menu_sun_integration.infrastructure.serbom.translators.benjamin_order_translator import BenjaminOrderTranslator
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, \
    OrderItemDetailSQSPlatform, OrderAddressSQSPlatform, OrderCustomerSQSPlatform, OrderStatusSQSPlatform, \
    OrderSQSMessagePlatform
from test.menu_sun_integration.infrastructure.stubs.FakeClient import FakeClient


class TestSerbomOrderTranslator:
    @pytest.fixture
    def order_raw_from_platform(self):
        payload = {
            "ReceiptHandle": "AAAAA",
            "Body": {
                "order_id": "M299999999",
                "total": 31.80,
                "discount": 0.02,
                "shipping": 10.00,
                "subtotal": 21.80,
                "shipping_address": {
                    "name": "Shipping Address Name",
                    "street": "Shipping Address Street",
                    "number": 1000,
                    "complement": "Shipping Address Complement",
                    "reference": "Shipping Address Reference",
                    "neighborhood": "Shipping Address Neighborhood",
                    "state_code": "Shipping Address State Code",
                    "city": "Shipping Address City",
                    "country_code": "Shipping Address Country Code",
                    "postcode": "Shipping Address Postcode"
                },
                "billing_address": {
                    "name": "Billing Address Name",
                    "street": "Billing Address Street",
                    "number": 1111,
                    "complement": "Billing Address Complement",
                    "reference": "Billing Address Reference",
                    "neighborhood": "Billing Address Neighborhood",
                    "state_code": "Billing Address State Code",
                    "city": "Billing Address City",
                    "country_code": "Billing Address Country Code",
                    "postcode": "Billing Address Postcode"
                },
                "items": [
                    {
                        "sku": "13201",
                        "name": "Cerveja DUff's",
                        "ean": "42040613",
                        "ncm": "2203.00.00",
                        "price": 31.80,
                        "original_price": 32.00,
                        "quantity": 1
                    },
                    {
                        "sku": "13202",
                        "name": "Cerveja Beck's",
                        "ean": "42040613",
                        "ncm": "2203.00.00",
                        "price": 31.80,
                        "original_price": 32.00,
                        "quantity": 1
                    }
                ],
                "customer": {
                    "name": "Luke Skywalker",
                    "document": "00005234000121",
                    "email": "luke@starwars.com",
                    "phone_number": "5511999999999",
                },
                "statuses": [{
                    "status": "NEW",
                    "comments": "",
                    "updated_date": "2020-05-13T14:41:25"
                }, {
                    "status": "APPROVED",
                    "comments": "",
                    "updated_date": "2020-04-13T14:41:25"
                }],
                "order_date": "2020-04-13T14:41:25",
                "delivery_date": "2020-04-14T14:41:25",
                "seller_code": "0810204",
                "payment_code": "2",
                "seller_id": 1,
                "integration_type": "NONE"
            }
        }
        return payload

    def test_benjamin_order_translator(self, order_raw_from_platform):
        receipt_handle = order_raw_from_platform["ReceiptHandle"]
        body = order_raw_from_platform.get("Body", {})

        order_detail = OrderDetailSQSPlatform.from_dict(body)
        order_detail_items = [OrderItemDetailSQSPlatform.from_dict(item) for item in body.get('items', {})]
        order_detail.items = order_detail_items
        order_detail.shipping_address = OrderAddressSQSPlatform.from_dict(body.get("shipping_address", {}))
        order_detail.billing_address = OrderAddressSQSPlatform.from_dict(body.get("billing_address", {}))
        order_detail.customer = OrderCustomerSQSPlatform.from_dict(body.get("customer", {}))
        order_detail.statuses = [OrderStatusSQSPlatform.from_dict(item) for item in body.get('statuses', {})]

        queue_message = OrderSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)

        fake_client = FakeClient()
        fake_client.post_order = MagicMock(return_value=True)
        translator = BenjaminOrderTranslator()
        adapter = OrderAdapter(client=fake_client, translator=translator)
        adapter.send_to_seller(queue_message.body)

        request_to_serbom = translator.to_seller_send_format(order_detail)

        requested: SerbomOrderPostOrderRequest = fake_client.post_order.call_args_list[0][0][0]

        assert fake_client.post_order.called
        assert fake_client.post_order.call_count == 1
        assert request_to_serbom.order_id == requested.order_id
        assert request_to_serbom.document == requested.document
        assert request_to_serbom.payment_code == requested.payment_code
        assert request_to_serbom.order_date == requested.order_date
        assert request_to_serbom.delivery_date == requested.delivery_date
        assert request_to_serbom.document_supplier == requested.document_supplier
        for serbom_item_request, serbom_item_requested in zip(request_to_serbom.items, requested.items):
            assert serbom_item_request.name == serbom_item_requested.name
            assert serbom_item_request.sku == serbom_item_requested.sku
            assert serbom_item_request.quantity == serbom_item_requested.quantity
