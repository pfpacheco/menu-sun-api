from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.customer.customer import Customer


class CustomerCreateCommand(Command):

    def __init__(self, customer, seller_id):
        self.customer = customer
        self.seller_id = seller_id

    def validate(self):
        return True


class CustomerCreateCommandHandler(TransactionCommandHandler):

    def __init__(self, customer_repository, session):
        super(CustomerCreateCommandHandler, self).__init__(session)
        self.customer_repository = customer_repository

    def process_request(self, command):
        customer = command.customer
        seller_id = command.seller_id
        document = customer['document']
        rs = self.customer_repository.get_by_document(
            document=document, seller_id=seller_id)
        if rs:
            rs = FailureResponse(category=FailureResponseCategory.ERROR,
                                 key='customer_exists',
                                 args=[document]
                                 )
            return rs

        customer_domain = Customer.from_dict(customer)
        customer_domain.seller_id = seller_id
        rs = self.customer_repository.add(customer_domain)
        return SuccessResponse(rs)
