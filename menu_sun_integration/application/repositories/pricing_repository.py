from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_context import AbstractGetContext
from menu_sun_integration.application.repositories.interfaces.abstract_pricing_repository import \
    AbstractPricingRepository
from menu_sun_integration.presentations.pricing.customer.abstract_customer_pricing_detail_get_request import \
    AbstractCustomerPricingDetailGetRequest


class PricingRepository(AbstractPricingRepository):
    def __init__(self, context: AbstractGetContext):
        self.context = context

    def get_by_customer(self, request: AbstractCustomerPricingDetailGetRequest) -> Dict:
        return self.context.get(request)


