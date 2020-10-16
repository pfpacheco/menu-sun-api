import graphene

from menu_sun_api.interfaces.mutation.sqlalchemy_input_object_type import SQLAlchemyInputObjectType
from menu_sun_api.domain.model.product.product import Product


class ProductInput(SQLAlchemyInputObjectType):
    class Meta:
        model = Product
        exclude_fields = ('id',
                          'updated_date',
                          'product_id',
                          'created_date',
                          'customer_id',
                          'uuid',
                          'status',
                          'meta_tags',
                          'seller_id',
                          'product_metadata',
                          'metafields')

    sale_price = graphene.Float()
    list_price = graphene.Float()
    promo_price = graphene.Float()
    # metafields = graphene.List(MetafieldInput)
    sku = graphene.String(required=True)
    # document = graphene.String(required=True)
