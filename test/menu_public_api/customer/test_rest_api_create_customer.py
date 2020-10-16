from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.customer.create_customer_handler import handle

import pytest
import json


class TestRestApiCreateCustomer(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_rest_api_create_customer(self, seller, session):
        data = {'document': '34829266788'}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}}

        rs = handle(event, None)
        body = json.loads(rs['body'])
        assert (rs['statusCode'] == 200)
        assert (body['document'] == '34829266788')
        assert rs
