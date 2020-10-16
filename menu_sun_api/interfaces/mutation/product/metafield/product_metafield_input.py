import graphene

from menu_sun_api.interfaces.mutation.sqlalchemy_input_object_type import SQLAlchemyInputObjectType
from menu_sun_api.domain.model.product.product import ProductMetafield


class ProductMetafieldInput(SQLAlchemyInputObjectType):
    class Meta:
        model = ProductMetafield
        exclude_fields = ('product_id',
                          )
    sku = graphene.String(required=True)
