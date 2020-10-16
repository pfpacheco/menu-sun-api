from menu_sun_api.interfaces.mutation.pricing.pricing_input import PricingInput
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput
from menu_sun_api.interfaces.mutation.product.product_input import ProductInput
from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.interfaces.definition.pricing import Pricing as PricingOutput
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerMetafieldInput, \
    PaymentTermsInput, PaymentTypeInput


class Mapper:
    def __str__(self):
        return self.__class__.__name__


class MapInputToCommand(Mapper):

    def visit(self, entity):

        if (isinstance(entity, PricingInput)):
            return dict(entity)

        if isinstance(entity, CustomerInput):
            rs = dict(entity)
            metafields = entity.get("metafields", [])
            # rs['metafields'] = [metafield.accept(self) for metafield in metafields]
            return rs

        if isinstance(entity, CustomerMetafieldInput):
            return dict(entity)

        if isinstance(entity, PaymentTermsInput):
            return dict(entity)

        if isinstance(entity, ProductInput):
            return dict(entity)


class MapDomainToOutput(Mapper):

    def visit(self, entity):
        if isinstance(entity, Pricing):
            return PricingOutput(entity)
