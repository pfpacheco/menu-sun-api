import graphene

from menu_sun_api.interfaces.definition.product import Product as ProductDefinition
from menu_sun_api.interfaces.mutation.product.product_input import ProductInput
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.application.product_service import ProductService
from menu_sun_api.domain.model.product.product_service import ProductService


class ProductUpdate(graphene.Mutation):
    class Arguments:
        product = ProductInput(required=True)

    product = graphene.Field(ProductDefinition)
    ok = graphene.Boolean()

    def mutate(self, info, product):
        seller = info.context.get('seller')
        repository = ProductRepository()
        service = ProductService(repository)
        domain_product = product.map()
        res = service.update_product(seller.id, product.sku, domain_product)
        Session().commit()
        return ProductUpdate(product=res.value)


class ProductUpdateMutation(graphene.ObjectType):
    product_update = ProductUpdate.Field()
