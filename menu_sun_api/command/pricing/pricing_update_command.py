from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.pricing.pricing import Pricing


class PricingUpdateCommand(Command):

    def __init__(self, pricing, seller_id):
        self.pricing = pricing
        self.seller_id = seller_id

    def validate(self):
        return True


class PricingUpdateCommandHandler(TransactionCommandHandler):

    def __init__(self, pricing_repository, session):
        super(PricingUpdateCommandHandler, self).__init__(session)
        self.pricing_repository = pricing_repository

    def process_request(self, command):
        seller_id = command.seller_id
        pricing = command.pricing
        document = pricing['document']
        sku = pricing['sku']
        pricing_db = self.pricing_repository.get_pricing(
            seller_id=seller_id, document=document, sku=sku)
        if not pricing_db:
            return FailureResponse(
                category=FailureResponseCategory.ERROR,
                key='pricing_not_found',
                args=[document, sku]
            )
        pricing_db.update_from_dict(pricing)
        return SuccessResponse(pricing_db)
