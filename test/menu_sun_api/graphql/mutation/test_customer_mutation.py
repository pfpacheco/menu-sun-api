from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory, CustomerMetafieldFactory
from menu_sun_api.domain.model.customer.customer import PaymentTerms, PaymentType
import pytest


class TestCustomerMutation(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC')
        session.commit()
        return seller

    def test_should_create_customer(self, seller):
        document = "10851803792"
        mutation = """
            mutation {
                customerCreate(customer:
                     {
                        document: "%s"
                    }) {
                    customer {
                        document
                    }
                }
            }
        """ % document

        rs = handle_graphql(mutation, seller)
        assert rs['data']['customerCreate']['customer']['document'] == document

    def test_should_update_customer(self, seller, session):
        customer = CustomerFactory.create(seller_id=seller.id,
                                          name='OLD NAME',
                                          document='10851803792')
        session.commit()
        new_name = "NEW NAME"
        mutation = """
            mutation {
                customerUpdate(customer: {document: "%s", name: "%s"}) {
                    customer {
                        document
                        name
                    }
                }
            }
        """ % (customer.document, new_name)

        rs = handle_graphql(mutation, seller)
        assert (rs['data']['customerUpdate']['customer']
                ['document'] == customer.document)
        assert (rs['data']['customerUpdate']['customer']['name'] == new_name)

    def test_should_delete_customer(self, seller, session):
        customer = CustomerFactory.create(
            seller_id=seller.id, document='10851803792')
        session.commit()

        mutation = """
            mutation {
                customerDelete(document: "%s") {
                    id
                }
            }
        """ % (customer.document)

        rs = handle_graphql(mutation, seller)
        assert (rs['data']['customerDelete']['id'] == customer.uuid)

    def test_should_bulk_upsert_customer(self, seller, session):
        customer = CustomerFactory.create(
            seller_id=seller.id,
            document='10851803792',
            name="Pedro")
        session.commit()

        mutation = """
            mutation($input: [CustomerInput]!) {
                customerBulkUpsert(customers: $input) {
                  customers{
                    id
                    active
                  }
                  failureMessage{
                    message
                  }
                }
            }
            """

        vars = {"input": [{"document": "10851803792", "name": "Pedro New", "active": False},
                          {"document": "10851803793", "name": "Pedro", "active": False}]}
        rs = handle_graphql(mutation, seller, vars)
        assert len(rs['data']['customerBulkUpsert']['customers']) == 2
        assert rs['data']['customerBulkUpsert']['customers'][0]['active'] is False

    def test_should_bulk_upsert_customer_metafield(self, seller, session):
        metafield = CustomerMetafieldFactory(
            key="baz", namespace="foo", value="bar")
        customer = CustomerFactory.create(
            seller_id=seller.id,
            document='10851803792',
            metafields=[metafield])
        session.commit()

        mutation = """
            mutation($input: [CustomerMetafieldInput]!) {
                customerMetafieldBulkUpsert(metafields: $input) {
                  metafields{
                    key
                    value
                    namespace
                  }
                  failureMessage{
                    message
                  }
                }
            }
            """

        vars = {"input": [{"document": customer.document,
                           "value": "foo",
                           "namespace": metafield.namespace,
                           "key": metafield.key},
                          {"document": customer.document,
                           "value": "foo_new",
                           "namespace": metafield.namespace,
                           "key": "foo_new"}
                          ]}
        rs = handle_graphql(mutation, seller, vars)
        assert rs['data']['customerMetafieldBulkUpsert']['metafields'][0]['value'] == "foo"
        assert rs['data']['customerMetafieldBulkUpsert']['metafields'][1]['value'] == "foo_new"
        assert rs['data']['customerMetafieldBulkUpsert']['metafields'][1]['key'] == "foo_new"

    def test_should_bulk_upsert_payment_terms(self, seller, session):
        customer = CustomerFactory.create(seller_id=seller.id,
                                          document='10851803792',
                                          payment_terms__deadline=20,
                                          payment_terms__payment_type=PaymentType.BOLETO
                                          )
        session.commit()

        mutation = """
            mutation($input: [PaymentTermsInput]!) {
                customerPaymentTermsBulkUpsert(paymentTerms: $input) {
                  paymentTerms{
                    deadline
                    paymentType
                  }
                  failureMessage{
                    message
                  }
                }
            }
            """

        vars = {"input": [{"paymentType": 'BOLETO',
                           "deadline": 10,
                           "document": customer.document},
                          {"paymentType": 'CARTAO_CREDITO',
                           "deadline": 0,
                           "document": customer.document}
                          ]}
        rs = handle_graphql(mutation, seller, vars)
        assert rs['data']['customerPaymentTermsBulkUpsert']['paymentTerms'][0]['deadline'] == 10
        assert rs['data']['customerPaymentTermsBulkUpsert']['paymentTerms'][0]['paymentType'] == 'BOLETO'
        assert rs['data']['customerPaymentTermsBulkUpsert']['paymentTerms'][1]['deadline'] == 0
        assert rs['data']['customerPaymentTermsBulkUpsert']['paymentTerms'][1]['paymentType'] == 'CARTAO_CREDITO'
