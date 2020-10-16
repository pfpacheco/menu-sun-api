from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
from menu_sun_api.domain.model.customer.customer_service import CustomerService
import pytest


class TestGetCustomer(IntegrationTest):

    @pytest.fixture
    def customer(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABC')
        session.commit()
        customer = CustomerFactory.create(seller_id=seller.id, document='A')
        session.commit()
        return customer

    def test_should_get_customer(self, customer):
        repository = CustomerRepository()
        uc = CustomerService(repository)
        customer_db = uc.load_by_uuid(uuid=customer.uuid).value
        assert (customer.uuid == customer_db.uuid)
