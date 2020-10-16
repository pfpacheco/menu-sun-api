import pytest
import dateutil.parser

from mock import MagicMock

from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_request import \
    PernodOrderItemPostRequest, PernodOrderAddressPostRequest, PernodOrderPostRequest, PernodOrderCustomerPostRequest, \
    PernodOrderStatusPostRequest
from menu_sun_integration.infrastructure.pernod.translators.pernod_order_translator import PernodOrderTranslator
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, \
    OrderItemDetailSQSPlatform, OrderAddressSQSPlatform, OrderCustomerSQSPlatform, OrderStatusSQSPlatform, \
    OrderSQSMessagePlatform
from test.menu_sun_integration.infrastructure.stubs.FakeClient import FakeClient


class TestOrderTranslator:
    @pytest.fixture
    def order_raw_from_platform(self):
        payload = {
            "ReceiptHandle": "AAAAA",
            "Body": {
                "order_id": "99999999",
                "total": 31.80,
                "discount": 0.00,
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
                    "postcode": "Shipping Address Postcode",
                    "shipping_provider": "Correios",
                    "shipping_service": "Sedex"
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

    @pytest.fixture
    def order_from_platform(self, order_raw_from_platform):
        receipt_handle = order_raw_from_platform.get("ReceiptHandle", {})
        body = order_raw_from_platform.get("Body", {})

        order_detail = OrderDetailSQSPlatform.from_dict(body)
        order_detail_items = [OrderItemDetailSQSPlatform.from_dict(item) for item in body.get('items', {})]
        order_detail.items = order_detail_items
        order_detail.shipping_address = OrderAddressSQSPlatform.from_dict(body.get("shipping_address", {}))
        order_detail.billing_address = OrderAddressSQSPlatform.from_dict(body.get("billing_address", {}))
        order_detail.customer = OrderCustomerSQSPlatform.from_dict(body.get("customer", {}))
        order_detail.statuses = [OrderStatusSQSPlatform.from_dict(item) for item in body.get('statuses', {})]

        return OrderSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)

    @pytest.fixture
    def request_to_pernod(self, order_from_platform: OrderSQSMessagePlatform):
        order = order_from_platform.body

        order_date = dateutil.parser.parse(order.order_date).strftime('%Y-%m-%dT%H:%M:%S%Z')
        delivery_date = dateutil.parser.parse(order.delivery_date).strftime('%Y-%m-%dT%H:%M:%S%Z')

        status_sorted = sorted(order.statuses, key=lambda item: item.updated_date, reverse=True)
        status = (status_sorted[:1] or [OrderStatusSQSPlatform.from_dict(
            {"status": "", "updated_date": {order_date}})])[0]

        order_status = PernodOrderStatusPostRequest(status=status.status, updated_date=status.updated_date)

        order_items = [PernodOrderItemPostRequest(sku=item.sku, quantity=item.quantity, price=item.price,
                                                  name=item.name, original_price=item.original_price)
                       for item in order.items]

        shipping_address = PernodOrderAddressPostRequest(street=order.shipping_address.street,
                                                         number=order.shipping_address.number,
                                                         complement=order.shipping_address.complement,
                                                         reference=order.shipping_address.reference,
                                                         neighborhood=order.shipping_address.neighborhood,
                                                         state_code=order.shipping_address.state_code,
                                                         city=order.shipping_address.city,
                                                         country_code=order.shipping_address.country_code,
                                                         postcode=order.shipping_address.postcode,
                                                         name=order.shipping_address.name,
                                                         shipping_provider=order.shipping_address.shipping_provider,
                                                         shipping_service=order.shipping_address.shipping_service)

        billing_address = PernodOrderAddressPostRequest(street=order.billing_address.street,
                                                        number=order.billing_address.number,
                                                        complement=order.billing_address.complement,
                                                        reference=order.billing_address.reference,
                                                        neighborhood=order.billing_address.neighborhood,
                                                        state_code=order.billing_address.state_code,
                                                        city=order.billing_address.city,
                                                        country_code=order.billing_address.country_code,
                                                        postcode=order.billing_address.postcode,
                                                        name=order.billing_address.name,
                                                        shipping_provider=order.shipping_address.shipping_provider,
                                                        shipping_service=order.shipping_address.shipping_service)

        order_customer = PernodOrderCustomerPostRequest(name=order.customer.name, document=order.customer.document,
                                                        email=order.customer.email,
                                                        phone_number=order.customer.phone_number)

        order_request = PernodOrderPostRequest(order_id=order.order_id, order_date=order_date,
                                               delivery_date=delivery_date, unb=order.seller_code, items=order_items,
                                               total=order.total, subtotal=order.subtotal, shipping=order.shipping,
                                               discount=order.discount, shipping_address=shipping_address,
                                               billing_address=billing_address, payment_code=order.payment_code,
                                               status=order_status, customer=order_customer, seller_id=order.seller_id)
        return order_request

    def test_translation_of_orders_to_pernod(self, order_from_platform: OrderSQSMessagePlatform,
                                             request_to_pernod: PernodOrderPostRequest):
        fake_client = FakeClient()
        fake_client.post_order = MagicMock(return_value=True)
        translator = PernodOrderTranslator()
        adapter = OrderAdapter(client=fake_client, translator=translator)
        adapter.send_to_seller(order_from_platform.body)

        requested: PernodOrderPostRequest = fake_client.post_order.call_args_list[0][0][0]
        assert fake_client.post_order.called
        assert fake_client.post_order.call_count == 1
        assert request_to_pernod.order_id == requested.order_id
        assert request_to_pernod.payment_code == requested.payment_code
        assert request_to_pernod.order_date == requested.order_date
        assert request_to_pernod.delivery_date == requested.delivery_date
        assert request_to_pernod.total == requested.total
        assert request_to_pernod.subtotal == requested.subtotal
        assert request_to_pernod.shipping == requested.shipping
        assert request_to_pernod.discount == requested.discount
        assert request_to_pernod.shipping_address.name == requested.shipping_address.name
        assert request_to_pernod.shipping_address.city == requested.shipping_address.city
        assert request_to_pernod.shipping_address.shipping_provider == requested.shipping_address.shipping_provider
        assert request_to_pernod.shipping_address.shipping_service == requested.shipping_address.shipping_service
        assert request_to_pernod.billing_address.name == requested.billing_address.name
        assert request_to_pernod.billing_address.city == requested.billing_address.city

        assert request_to_pernod.status.real_status == requested.status.real_status
        assert request_to_pernod.status.order_status == requested.status.order_status
        assert request_to_pernod.status.updated_date == requested.status.updated_date

        for promax_item_request, promax_item_requested in zip(request_to_pernod.items, requested.items):
            assert promax_item_request.name == promax_item_requested.name
            assert promax_item_request.sku == promax_item_requested.sku
            assert promax_item_request.quantity == promax_item_requested.quantity
            assert promax_item_request.price == promax_item_requested.price
            assert promax_item_request.original_price == promax_item_requested.original_price
            assert promax_item_requested.discount == round(
                promax_item_request.original_price - promax_item_request.price, 2)
