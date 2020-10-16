from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.domain.model.customer.customer import PaymentTerms
from menu_sun_api.domain.model.customer.customer import PaymentType


class CustomerPaymentTermsBulkUpsertCommand(Command):

    def __init__(self, seller_id, payment_terms):
        self.seller_id = seller_id
        self.payment_terms = payment_terms

    def validate(self):
        return True


class CustomerPaymentTermsdBulkUpsertCommandHandler(TransactionCommandHandler):

    def __init__(self, customer_repository, session):
        super(
            CustomerPaymentTermsdBulkUpsertCommandHandler,
            self).__init__(session)
        self.customer_repository = customer_repository

    def process_request(self, command):
        seller_id = command.seller_id
        ls = []
        for payment_term in command.payment_terms:
            document = payment_term['document']

            customer_db = self.customer_repository.get_by_document(
                seller_id=seller_id, document=document)

            if (not customer_db):
                return FailureResponse(FailureResponseCategory.ERROR,
                                       key='customer_not_found',
                                       args=[document]
                                       )
            payment_terms_input = PaymentTerms.from_dict(payment_term)
            rs = customer_db.change_payment_terms(payment_terms_input)

            ls.append(rs)
        return SuccessResponse(ls)
