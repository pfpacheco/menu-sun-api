from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.domain.model.customer.customer import CustomerMetafield


class CustomerMetafieldBulkUpsertCommand(Command):

    def __init__(self, seller_id, metafields):
        self.seller_id = seller_id
        self.metafields = metafields

    def validate(self):
        return True


class CustomerMetafieldBulkUpsertCommandHandler(TransactionCommandHandler):

    def __init__(self, customer_repository, session):
        super(CustomerMetafieldBulkUpsertCommandHandler, self).__init__(session)
        self.customer_repository = customer_repository

    def process_request(self, command):
        seller_id = command.seller_id
        ls = []
        for metafield in command.metafields:
            document = metafield['document']
            customer_db = self.customer_repository.get_by_document(seller_id=seller_id,
                                                                   document=document)

            if not customer_db:
                return FailureResponse(FailureResponseCategory.ERROR,
                                       key='customer_not_found',
                                       args=[document]
                                       )

            input = CustomerMetafield.from_dict(metafield)
            rs = customer_db.change_metafield(input)
            ls.append(rs)
        return SuccessResponse(ls)
