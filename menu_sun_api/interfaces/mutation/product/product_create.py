import graphene

from menu_sun_api.interfaces.definition.product import Product as ProductDefinition
from menu_sun_api.interfaces.mutation.product.product_input import ProductInput
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.application.product_service import ProductService


class ProductCreate(graphene.Mutation):
    class Arguments:
        product = ProductInput(required=True)

    product = graphene.Field(ProductDefinition)

    def mutate(parent, info, product, **args):
        repository = ProductRepository()
        seller = info.context.get('seller')
        service = ProductService(repository)
        product_db = product.map(additional={"seller_id": seller.id})
        res = service.create_product(product_db)
        Session().commit()
        return ProductCreate(product=res.value)


class ProductCreateMutation(graphene.ObjectType):
    product_create = ProductCreate.Field()
