import pytest

from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, \
    OrderItemDetailSQSPlatform, OrderAddressSQSPlatform, OrderCustomerSQSPlatform, OrderStatusSQSPlatform, \
    OrderSQSMessagePlatform


class TestOrderSQSPlatform:

    @pytest.fixture
    def order_raw_from_platform(self):
        payload = {
            "ReceiptHandle": "AAAAA",
            "Body": {
                "order_id": "99999999",
                "total": 73.60,
                "discount": 3.60,
                "shipping": 10.00,
                "subtotal": 63.6,
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
                        "name": "Cerveja Beck's",
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
                    "status": "APPROVED",
                    "comments": "",
                    "updated_date": "2020-04-13T14:41:25"
                }],
                "order_date": "2020-04-13T14:41:25",
                "delivery_date": "2020-04-14T14:41:25",
                "seller_code": "0810204",
                "payment_code": "2",
                "document": "00005234000121",
                "seller_id": 1,
                "integration_type": "NONE"
            }
        }
        return payload

    def test_mapping_order_from_platform_to_domain(self, order_raw_from_platform):
        receipt_handle = order_raw_from_platform.get("ReceiptHandle", {})
        body = order_raw_from_platform.get("Body", {})

        order_detail = OrderDetailSQSPlatform.from_dict(body)
        order_detail_items = [OrderItemDetailSQSPlatform.from_dict(item) for item in body.get('items', {})]
        order_detail.items = order_detail_items
        order_detail.shipping_address = OrderAddressSQSPlatform.from_dict(body.get("shipping_address", {}))
        order_detail.billing_address = OrderAddressSQSPlatform.from_dict(body.get("billing_address", {}))
        order_detail.customer = OrderCustomerSQSPlatform.from_dict(body.get("customer", {}))
        order_detail.statuses = [OrderStatusSQSPlatform.from_dict(item) for item in body.get('statuses', {})]

        order_platform = OrderSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)

        order = order_platform.body
        raw = order_raw_from_platform["Body"]

        assert order.order_id == raw["order_id"]
        assert order.total == raw["total"]
        assert order.discount == raw["discount"]
        assert order.shipping == raw["shipping"]
        assert order.subtotal == raw["subtotal"]
        assert order.shipping_address.name == raw["shipping_address"]["name"]
        assert order.shipping_address.number == raw["shipping_address"]["number"]
        assert order.shipping_address.city == raw["shipping_address"]["city"]
        assert order.billing_address.name == raw["billing_address"]["name"]
        assert order.billing_address.number == raw["billing_address"]["number"]
        assert order.billing_address.city == raw["billing_address"]["city"]
        assert order.seller_code == raw["seller_code"]
        assert order.payment_code == raw["payment_code"]
        assert order.document == raw["document"]
        assert order.seller_id == raw["seller_id"]
        assert order.integration_type == raw["integration_type"]
        assert order.customer.name == raw["customer"]["name"]
        assert order.customer.email == raw["customer"]["email"]
        assert order.customer.phone_number == raw["customer"]["phone_number"]
        assert order.customer.document == raw["customer"]["document"]

        assert order.statuses[0].status == raw["statuses"][0]["status"]
        assert order.statuses[0].comments == raw["statuses"][0]["comments"]
        assert order.statuses[0].updated_date == raw["statuses"][0]["updated_date"]

        assert order.items[0].sku == raw["items"][0]["sku"]
        assert order.items[0].name == raw["items"][0]["name"]
        assert order.items[0].price == raw["items"][0]["price"]
        assert order.items[0].original_price == raw["items"][0]["original_price"]
        assert order.items[0].quantity == raw["items"][0]["quantity"]
