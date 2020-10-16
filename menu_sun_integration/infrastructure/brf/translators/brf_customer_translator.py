from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.translators.interfaces.abstract_customer_translator import \
    AbstractCustomerTranslator
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_detail_get_request import \
    BRFCustomerDetailGetRequest
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_response import BRFCustomerResponse

from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest


class BRFCustomerTranslator(AbstractCustomerTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, customer: Customer) -> BRFCustomerDetailGetRequest:
        return BRFCustomerDetailGetRequest(cnpj=customer.document, postal_code=customer.cep)

    def to_domain_format(self, response: BRFCustomerResponse) -> Customer:
        metafields = []
        metafield_grade = CustomerMetafield(namespace='GRADE',
                                            key="GRADE",
                                            value=response.grade)

        seller_repository = SellerRepository(session=Session)
        seller = seller_repository.get_seller_by_seller_code(seller_code=response.cdd)
        metafields.append(metafield_grade)
        payment_terms = list(map(self.bind_payment_type, response.payment_terms))
        if response.active:

            return Customer(active=response.active, credit_limit=response.credit_limit,
                            payment_terms=payment_terms, metafields=metafields, seller_id=seller.id)

        else:
            return Customer(active=response.active, credit_limit=response.credit_limit)
