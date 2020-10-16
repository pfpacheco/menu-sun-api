import graphene

from menu_sun_api.interfaces.mutation.sqlalchemy_input_object_type import SQLAlchemyInputObjectType
from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput


class PricingInput(SQLAlchemyInputObjectType):
    class Meta:
        model = Pricing
        exclude_fields = ('id',
                          'updated_date',
                          'product_id',
                          'created_date',
                          'customer_id',
                          'uuid')

    sku = graphene.String(required=True)
    document = graphene.String(required=True)
