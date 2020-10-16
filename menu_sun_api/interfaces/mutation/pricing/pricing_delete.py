import graphene

from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.pricing.pricing_delete_command import PricingDeleteCommand, \
    PricingDeleteCommandHandler


class PricingDelete(graphene.Mutation):
    class Arguments:
        sku = graphene.String(required=True)
        document = graphene.String(required=True)

    id = graphene.ID(required=True)

    def mutate(parent, info, sku, document, **args):
        seller = info.context.get('seller')
        session = Session()

        command = PricingDeleteCommand(sku=sku, document=document,
                                       seller_id=seller.id)
        handler = PricingDeleteCommandHandler(
            PricingRepository(session), session)

        rs = handler.execute(command)
        if (rs):
            return PricingDelete(pricing=rs.value.uuid, failure_message=None)
        else:
            return PricingDelete(pricing=[], failure_message=rs)


class PricingDeleteMutation(graphene.ObjectType):
    pricing_delete = PricingDelete.Field()
