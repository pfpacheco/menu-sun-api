from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.pricing.pricing import Pricing


class PricingBulkUpsertCommand(Command):

    def __init__(self, pricing_list, seller_id):
        self.pricing_list = pricing_list
        self.seller_id = seller_id

    def validate(self):
        return True


class PricingBulkUpsertCommandHandler(TransactionCommandHandler):

    def __init__(self, pricing_repository, customer_repository,
                 product_repository, session):
        super(PricingBulkUpsertCommandHandler, self).__init__(session)
        self.pricing_repository = pricing_repository
        self.customer_repository = customer_repository
        self.product_repository = product_repository

    def process_request(self, command):
        seller_id = command.seller_id
        ls = []
        for command in command.pricing_list:
            document = command['document']
            sku = command['sku']
            pricing_db = self.pricing_repository.get_pricing(
                seller_id=seller_id, document=document, sku=sku)
            if (pricing_db):
                pricing_db.update_from_dict(command)
                rs = pricing_db
            else:
                pricing = Pricing.from_dict(command)
                customer = self.customer_repository.get_by_document(
                    seller_id=seller_id, document=document)
                if not customer:
                    return FailureResponse(FailureResponseCategory.ERROR,
                                           key='customer_not_found',
                                           args=[document]
                                           )

                product = self.product_repository.get_by_sku(
                    sku=sku, seller_id=seller_id)
                if not product:
                    return FailureResponse(category=FailureResponseCategory.ERROR,
                                           key='product_not_found',
                                           args=[sku]
                                           )

                pricing.customer_id = customer.id
                pricing.product_id = product.id
                rs = self.pricing_repository.add(pricing)
            ls.append(rs)
        return SuccessResponse(ls)
