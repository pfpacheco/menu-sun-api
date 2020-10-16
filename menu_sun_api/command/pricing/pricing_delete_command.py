from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository


class PricingDeleteCommand(Command):

    def __init__(self, seller_id, sku, document):
        self.sku = sku
        self.document = document
        self.seller_id = seller_id

    def validate(self):
        return True


class PricingDeleteCommandHandler(TransactionCommandHandler):

    def __init__(self, pricing_repository, session):
        super(PricingDeleteCommandHandler, self).__init__(session)
        self.pricing_repository = pricing_repository

    def process_request(self, command):
        self.pricing_repository.delete()
        pricing = self.repository.get_pricing(seller_id=command.seller_id,
                                              sku=command.sku,
                                              document=command.document)
        if (pricing):
            self.session.delete(pricing)
        else:
            return FailureResponse(
                category=FailureResponseCategory.ERROR,
                key='pricing_not_found',
                args=[command.document, command.sku]
            )
        return SuccessResponse(pricing)
