from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory, PaymentTermsFactory
import pytest
from menu_sun_api.domain.model.customer.customer import CustomerMetafield


class TestCustomerRepository(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create()
        session.commit()
        return seller

    def test_should_retrieve_customer(self, session, seller):
        repository = CustomerRepository(session)
        customer = CustomerFactory.create(seller_id=seller.id, document='A')
        session.commit()

        rs = repository.get_by_uuid(uuid=customer.uuid)
        assert(len(rs.payment_terms) == 1)
        assert(rs.uuid == customer.uuid)

    def test_should_retrieve_metadata_fields(self, session, seller):
        metafield = CustomerMetafield(key="baz", namespace="foo", value="bar")
        customer = CustomerFactory.create(
            seller_id=seller.id, document='A', metafields=[metafield])
        session.commit()
        repository = CustomerRepository(session)
        rs = repository.get_metafield(seller_id=seller.id, document=customer.document,
                                      namespace=metafield.namespace, key=metafield.key)
        assert(rs)
