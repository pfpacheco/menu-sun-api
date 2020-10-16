from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield


class CustomerBulkUpsertCommand(Command):

    def __init__(self, customers, seller_id):
        self.customers = customers
        self.seller_id = seller_id

    def validate(self):
        return True


class CustomerBulkUpsertCommandHandler(TransactionCommandHandler):

    def __init__(self, customer_repository, session):
        super(CustomerBulkUpsertCommandHandler, self).__init__(session)
        self.customer_repository = customer_repository

    def process_request(self, command):
        seller_id = command.seller_id
        ls = []
        for customer in command.customers:
            document = customer['document']
            customer_input = Customer.from_dict(customer)
            customer_domain = self.customer_repository.get_by_document(
                document=document, seller_id=seller_id)
            if customer_domain:
                customer_domain.update(customer_input)
            else:
                customer_input.seller_id = seller_id
                customer_domain = self.customer_repository.add(customer_input)
            ls.append(customer_domain)
        return SuccessResponse(ls)
