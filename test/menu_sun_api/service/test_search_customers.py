from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
from menu_sun_api.domain.model.customer.customer_service import CustomerService

import pytest


class TestSearchCustomers(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABC')
        session.commit()
        return seller

    def test_should_search_customers_by_document(self, seller, session):
        CustomerFactory.create(seller_id=seller.id, document='A')
        CustomerFactory.create(seller_id=seller.id, document='B')
        session.commit()
        repository = CustomerRepository()
        uc = CustomerService(repository)
        customer_list = list(
            uc.search_by_documents(
                seller_id=seller.id,
                documents=['A']).value)
        assert (len(customer_list) == 1)
        assert (customer_list[0].document == 'A')
