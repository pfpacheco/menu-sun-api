from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.pricing.pricing import Pricing


class PricingCreateCommand(Command):

    def __init__(self, pricing, seller_id):
        self.pricing = pricing
        self.seller_id = seller_id

    def validate(self):
        return True


class PricingCreateCommandHandler(TransactionCommandHandler):

    def __init__(self, pricing_repository, customer_repository,
                 product_repository, session):
        super(PricingCreateCommandHandler, self).__init__(session)
        self.pricing_repository = pricing_repository
        self.customer_repository = customer_repository
        self.product_repository = product_repository

    def process_request(self, command):
        seller_id = command.seller_id
        pricing = command.pricing
        document = pricing['document']
        sku = pricing['sku']
        pricing = Pricing.from_dict(pricing)
        customer = self.customer_repository.get_by_document(
            seller_id=seller_id, document=document)
        if not customer:
            rs = FailureResponse(FailureResponseCategory.ERROR,
                                 key='customer_not_found',
                                 args=[document]
                                 )
            return rs

        product = self.product_repository.get_by_sku(
            sku=sku, seller_id=seller_id)
        if not product:
            rs = FailureResponse(category=FailureResponseCategory.ERROR,
                                 key='product_not_found',
                                 args=[sku]
                                 )
            return rs

        pricing.customer_id = customer.id
        pricing.product_id = product.id
        rs = self.pricing_repository.add(pricing)
        return SuccessResponse(rs)
