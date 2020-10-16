from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse


class CustomerUpdateCommand(Command):

    def __init__(self, customer, seller_id):
        self.customer = customer
        self.seller_id = seller_id

    def validate(self):
        return True


class CustomerUpdateCommandHandler(TransactionCommandHandler):

    def __init__(self, customer_repository, session):
        super(CustomerUpdateCommandHandler, self).__init__(session)
        self.customer_repository = customer_repository

    def process_request(self, command):
        seller_id = command.seller_id
        customer = command.customer
        document = customer['document']
        customer_db = self.customer_repository.get_by_document(seller_id=seller_id, document=document)
        if not customer_db:
            return FailureResponse(
                category=FailureResponseCategory.ERROR,
                key='customer_not_found',
                args=[document]
            )
        customer_db.update_from_dict(customer)
        return SuccessResponse(customer_db)
