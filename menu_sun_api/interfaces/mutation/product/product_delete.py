import graphene

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.application.product_service import ProductService


class ProductDelete(graphene.Mutation):
    class Arguments:
        sku = graphene.String(required=True)

    id = graphene.ID(required=True)

    def mutate(parent, info, sku, **args):
        repository = ProductRepository()
        service = ProductService(repository)
        seller = info.context.get('seller')
        product = service.delete_product_by_sku(seller_id=seller.id, sku=sku)
        Session().commit()
        return ProductDelete(id=product.value.uuid)


class ProductDeleteMutation(graphene.ObjectType):
    product_delete = ProductDelete.Field()
