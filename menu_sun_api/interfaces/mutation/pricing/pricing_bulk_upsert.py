import graphene

from menu_sun_api.command.pricing.pricing_bulk_upsert_command import PricingBulkUpsertCommand, \
    PricingBulkUpsertCommandHandler
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.definition.pricing import Pricing as PricingDefinition
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.interfaces.mutation.pricing.pricing_input import PricingInput


class PricingBulkUpsert(graphene.Mutation):
    class Arguments:
        pricings = graphene.List(PricingInput, required=True)

    pricings = graphene.List(PricingDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, pricings, **args):
        session = Session()
        seller = info.context.get('seller')
        pricing_repository = PricingRepository(session)
        customer_repository = CustomerRepository(session)
        product_repository = ProductRepository(session)

        from_input = MapInputToCommand()
        pricing_list = [i.accept(from_input) for i in pricings]

        command = PricingBulkUpsertCommand(pricing_list=pricing_list,
                                           seller_id=seller.id)

        handler = PricingBulkUpsertCommandHandler(
            pricing_repository=pricing_repository,
            customer_repository=customer_repository,
            product_repository=product_repository,
            session=session)
        rs = handler.execute(command)

        if rs:
            return PricingBulkUpsert(pricings=rs.value, failure_message=None)
        else:
            return PricingBulkUpsert(pricings=[], failure_message=rs)


class PricingBulkUpsertMutation(graphene.ObjectType):
    pricing_bulk_upsert = PricingBulkUpsert.Field()
