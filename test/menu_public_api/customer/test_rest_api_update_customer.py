from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
from menu_public_api.customer.update_customer_handler import handle

import pytest
import json


class TestRestApiUpdateCustomer(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    @pytest.fixture
    def customer(self, session, seller):
        customer = CustomerFactory.create(document='444429288788', seller_id=seller.id)
        session.commit()
        return customer

    def test_rest_api_update_customer(self, seller, customer, session):
        data = {'document': customer.document, 'name': 'Menu Lead', 'credit_limit': '2000'}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = handle(event, None)
        body = json.loads(rs['body'])
        assert (rs['statusCode'] == 200)
        assert (body['document'] == customer.document)
        assert (body['name'] == 'Menu Lead')
        assert (body['credit_limit'] == 2000.0)
        assert rs
