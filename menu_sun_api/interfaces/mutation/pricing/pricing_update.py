import graphene

from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.definition.pricing import Pricing as PricingDefinition
from menu_sun_api.interfaces.mutation.pricing.pricing_input import PricingInput
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.command.pricing.pricing_update_command import PricingUpdateCommand, \
    PricingUpdateCommandHandler


class PricingUpdate(graphene.Mutation):
    class Arguments:
        pricing = PricingInput(required=True)

    pricing = graphene.Field(PricingDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, pricing, **args):
        session = Session()
        seller = info.context.get('seller')
        pricing_repository = PricingRepository(session)

        from_input = MapInputToCommand()

        command = PricingUpdateCommand(pricing=pricing.accept(from_input),
                                       seller_id=seller.id)

        handler = PricingUpdateCommandHandler(
            pricing_repository=pricing_repository,
            session=session)
        rs = handler.execute(command)

        if (rs):
            return PricingUpdate(pricing=rs.value, failure_message=None)
        else:
            return PricingUpdate(pricing=[], failure_message=rs)


class PricingUpdateMutation(graphene.ObjectType):
    pricing_update = PricingUpdate.Field()
