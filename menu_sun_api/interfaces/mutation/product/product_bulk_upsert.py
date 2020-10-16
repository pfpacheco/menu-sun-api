import graphene

from menu_sun_api.interfaces.definition.product import Product as ProductDefinition
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.mutation.product.product_input import ProductInput

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.command.product.product_bulk_upsert_command import ProductBulkUpsertCommand, \
    ProductBulkUpsertCommandHandler
from menu_sun_api.domain.model.product.product_repository import ProductRepository


class ProductBulkUpsert(graphene.Mutation):
    class Arguments:
        products = graphene.List(ProductInput, required=True)

    products = graphene.List(ProductDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, products, **args):
        session = Session()
        seller = info.context.get('seller')
        product_repository = ProductRepository(session)
        from_input = MapInputToCommand()
        product_list = [i.accept(from_input) for i in products]

        command = ProductBulkUpsertCommand(product_list=product_list,
                                           seller_id=seller.id)

        handler = ProductBulkUpsertCommandHandler(
            product_repository=product_repository,
            session=session)
        rs = handler.execute(command)
        if (rs):
            return ProductBulkUpsert(products=rs.value,
                                     failure_message=None)
        else:
            return ProductBulkUpsert(products=[],
                                     failure_message=rs)


class ProductBulkUpsertMutation(graphene.ObjectType):
    product_bulk_upsert = ProductBulkUpsert.Field()
