from graphene_sqlalchemy import SQLAlchemyObjectType

from menu_sun_api.domain.model.pricing.pricing import Pricing as PricingDomain


class Pricing(SQLAlchemyObjectType):
    class Meta:
        model = PricingDomain
        description = "Pricing Domain"
        exclude_fields = ('uuid',)

    def resolve_id(parent, info):
        return parent.uuid
