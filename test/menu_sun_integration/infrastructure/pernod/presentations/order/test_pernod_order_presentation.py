import json
import os
import string

import responses
from mock import patch, mock
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_detail_get_request import \
    PernodOrderDetailGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_detail_get_response import \
    PernodOrderDetailGetResponse
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_request import \
    PernodOrderItemPostRequest, PernodOrderPostRequest, PernodOrderAddressPostRequest, PernodOrderCustomerPostRequest, \
    PernodOrderStatusPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_response import \
    PernodOrderPostResponse
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_notification_response import \
    PernodOrderStatusNotificationResponse

here = os.path.abspath(os.path.dirname(__file__))


def mock_os_func(parameter, default_value=None):
    if parameter == "PERNOD_ID_TENANT":
        return 2585
    if default_value:
        return os.getenv(parameter, default_value)
    return os.getenv(parameter)


class TestPernodOrderPresentation:
    def test_order_detail_get_request(self):
        unb = "UNB"
        seller_id = 1
        document = "000.000.000-00"
        order_id = "12345"
        expected = '{"seller_code" : "%s", "document": "%s", "order_id" : "%s"}' % (unb, document, order_id)
        request = PernodOrderDetailGetRequest(unb=unb, cnpj=document, order_id=order_id, seller_id=seller_id)

        assert request.payload == expected

    def test_order_detail_get_response(self):
        seller_order_id = "779628370"
        order_id = "12345"
        payload_succeed = {"reference": {"id": seller_order_id, "source": order_id},
                           "status": {"status": "canceled", "message": "Erro"}}

        payload_not_succeed = {}
        expected_status = PernodOrderStatusNotificationResponse(payload=payload_succeed)
        expected_succeeded = PernodOrderDetailGetResponse(payload=payload_succeed)
        expected_not_succeed = PernodOrderDetailGetResponse(payload=payload_not_succeed)

        assert expected_succeeded.succeeded is True
        assert expected_not_succeed.succeeded is False

        order = expected_succeeded.get_order()

        assert order.id == expected_status.id
        assert order.seller_order_id == expected_status.seller_order_id
        assert order.status.information == expected_status.status.information
        assert order.status.code == "CANCELED"

    @responses.activate
    @patch('menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_request.os')
    def test_order_post_request(self, mock_os):
        mock_os.getenv = mock.Mock(side_effect=mock_os_func)
        items = [PernodOrderItemPostRequest(name="Item 1", sku="00001", price=10.00, quantity=1,
                                            original_price=11.00)]

        shipping_address = PernodOrderAddressPostRequest(street="Shipping Street", number=1,
                                                         complement="Shipping Street", reference="Shipping Street",
                                                         neighborhood="Shipping Street", state_code="Shipping Street",
                                                         city="Shipping Street", country_code="Shipping Street",
                                                         postcode="Shipping Street", name="Shipping Street",
                                                         shipping_provider='Correios', shipping_service='SEDEX')

        billing_address = PernodOrderAddressPostRequest(street="Billing Street", number=1,
                                                        complement="Billing Street", reference="Billing Street",
                                                        neighborhood="Billing Street", state_code="Billing Street",
                                                        city="Billing Street", country_code="Billing Street",
                                                        postcode="Billing Street", name="Billing Street",
                                                        shipping_provider='Correios', shipping_service='SEDEX')

        order_customer = PernodOrderCustomerPostRequest(name="Luke Skywalker", document="00005234000121",
                                                        email="luke@starwars.com",
                                                        phone_number="5511999999999")

        order_status = PernodOrderStatusPostRequest(status="PENDING", updated_date="2020-04-30 15:32:00")

        request = PernodOrderPostRequest(order_id="12345", order_date="2020-04-30 15:32:00",
                                         delivery_date="2020-05-01 15:32:00", unb="UNB", payment_code="BOLETO",
                                         items=items, shipping_address=shipping_address,
                                         billing_address=billing_address, customer=order_customer, status=order_status,
                                         discount=1, shipping=10, subtotal=10, total=20, seller_id=1)

        json_file = open(
            os.path.join(
                here, '../../pernod_response/send_order.json'))
        expected = json.dumps(json.load(json_file))
        assert request.payload.translate({ord(c): None for c in string.whitespace}) == expected.translate(
            {ord(c): None for c in string.whitespace})

    def test_order_post_response(self):
        payload_succeed = {}
        payload_not_succeed = {"errors": [{}]}
        response_succeed = PernodOrderPostResponse(payload=payload_succeed)
        response_not_succeed = PernodOrderPostResponse(payload=payload_not_succeed)

        assert response_succeed.succeeded is True
        assert response_not_succeed.succeeded is False

    def test_order_status_response(self):
        order_id = "12345"
        seller_order_id = "779628370"
        situacao = "INVOICED"
        payload = {"reference": {"id": seller_order_id, "source": order_id},
                   "status": {"status": "invoiced", "message": ""}}
        expected = PernodOrderStatusNotificationResponse(payload=payload)

        assert expected.id == order_id
        assert expected.seller_order_id == seller_order_id
        assert expected.status.code == situacao
        assert expected.status.information == ''
