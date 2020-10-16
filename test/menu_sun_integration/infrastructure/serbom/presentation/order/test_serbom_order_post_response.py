import os

from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_response import \
    SerbomOrderPostResponse

here = os.path.abspath(os.path.dirname(__file__))


class TestSerbomOrderResponse:
    def test_order_response_request(self):
        xml_file = open(
            os.path.join(
                here,
                '../../serbom_response/serbom_order_response.xml'))

        payload = xml_file.read()
        response = SerbomOrderPostResponse(payload)
        assert response.succeeded
