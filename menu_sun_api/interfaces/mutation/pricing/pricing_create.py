import graphene

from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.definition.pricing import Pricing as PricingDefinition
from menu_sun_api.interfaces.mutation.pricing.pricing_input import PricingInput
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.pricing.pricing_create_command import PricingCreateCommandHandler, \
    PricingCreateCommand
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository


class PricingCreate(graphene.Mutation):
    class Arguments:
        pricing = PricingInput(required=True)

    pricing = graphene.Field(PricingDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, pricing, **args):
        session = Session()
        seller = info.context.get('seller')
        pricing_repository = PricingRepository(session)
        product_repository = ProductRepository(session)
        customer_repository = CustomerRepository(session)

        from_input = MapInputToCommand()

        command = PricingCreateCommand(pricing=pricing.accept(from_input),
                                       seller_id=seller.id)

        handler = PricingCreateCommandHandler(
            pricing_repository=pricing_repository,
            customer_repository=customer_repository,
            product_repository=product_repository,
            session=session)
        rs = handler.execute(command)

        if rs:
            return PricingCreate(pricing=rs.value, failure_message=None)
        else:
            return PricingCreate(pricing=[], failure_message=rs)


class PricingCreateMutation(graphene.ObjectType):
    pricing_create = PricingCreate.Field()
