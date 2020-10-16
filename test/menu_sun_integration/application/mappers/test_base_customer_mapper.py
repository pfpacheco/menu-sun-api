from menu_sun_api.domain.model.customer.customer import CustomerMetafield, PaymentTerms, PaymentType, Customer
from menu_sun_integration.application.mappers.base_customer_mapper import BaseCustomerMapper


def test_map_base_customer_to_message():
    customer_metafield = CustomerMetafield(
        namespace="ADF", key="has_adf", value="true")
    payment_terms = [PaymentTerms(deadline=5, payment_type=PaymentType.BOLETO, description="BOLETO DESC"),
                     PaymentTerms(deadline=15, payment_type=PaymentType.CHEQUE, description="CHEQUE DESC")]
    customer = Customer(document="10851803792", metafields=[customer_metafield])
    payment_term_1 = payment_terms[0]
    payment_term_2 = payment_terms[1]
    customer.payment_terms.append(payment_term_1)
    customer.payment_terms.append(payment_term_2)

    visit = BaseCustomerMapper()
    customer_dict = customer.accept(visit)

    assert (customer_dict['document'] == customer.document)
    assert (customer_dict['customer_metafields'][0]['namespace'] == customer_metafield.namespace)
    assert (customer_dict['customer_metafields'][0]['key'] == customer_metafield.key)
    assert (customer_dict['customer_metafields'][0]['value'] == customer_metafield.value)
    assert (customer_dict['payment_terms'][0]['deadline'] == payment_term_1.deadline)
    assert (customer_dict['payment_terms'][0]['payment_type'] == payment_term_1.payment_type.name)
    assert (customer_dict['payment_terms'][0]['description'] == payment_term_1.description)
    assert (customer_dict['payment_terms'][1]['deadline'] == payment_term_2.deadline)
    assert (customer_dict['payment_terms'][1]['payment_type'] == payment_term_2.payment_type.name)
    assert (customer_dict['payment_terms'][1]['description'] == payment_term_2.description)
