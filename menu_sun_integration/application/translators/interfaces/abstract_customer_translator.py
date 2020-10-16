import abc
from menu_sun_api.domain.model.customer.customer import Customer, PaymentTerms, PaymentType
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.customer.abstract_customer_detail_get_request import \
    AbstractCustomerDetailGetRequest
from menu_sun_integration.presentations.customer.abstract_customer_response import AbstractCustomerResponse, \
    AbstractCustomerPaymentTermsResponse
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest


class AbstractCustomerTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_seller_get_format(self, entity: Customer) -> AbstractCustomerDetailGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractCustomerResponse) -> Customer:
        raise NotImplementedError

    @staticmethod
    def bind_payment_type(payment_term: AbstractCustomerPaymentTermsResponse) -> PaymentTerms:
        return PaymentTerms(
            deadline=payment_term.deadline,
            description=payment_term.description,
            payment_type=PaymentType.get_value(payment_term.payment_type))
