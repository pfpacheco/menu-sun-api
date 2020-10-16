from menu_sun_api.domain.model.customer.customer import PaymentTerms, PaymentType, Customer
from menu_sun_integration.infrastructure.brf.mappers.brf_customer_mapper import BRFCustomerMapper


def test_map_brf_customer_to_message():
    payment_terms_1 = PaymentTerms(deadline=5, payment_type=PaymentType.BOLETO, description="BOLETO DESC")
    payment_terms_2 = PaymentTerms(deadline=10, payment_type=PaymentType.CHEQUE, description="CHEQUE DESC")
    customer = Customer(document="10851803792", payment_terms=[payment_terms_1, payment_terms_2])
    visit = BRFCustomerMapper()
    customer_dict = customer.accept(visit)

    assert (customer_dict['document'] == customer.document)
    assert (customer_dict['payment_term']['deadline'] == payment_terms_1.deadline)
    assert (customer_dict['payment_term']['payment_type'] == payment_terms_1.payment_type.name)
    assert (customer_dict['payment_term']['description'] == payment_terms_1.description)


def test_map_brf_customer_without_payment_to_message():
    customer = Customer(document="10851803792")
    visit = BRFCustomerMapper()
    customer_dict = customer.accept(visit)

    assert (customer_dict['document'] == customer.document)
    assert (customer_dict['payment_term'] == {})
