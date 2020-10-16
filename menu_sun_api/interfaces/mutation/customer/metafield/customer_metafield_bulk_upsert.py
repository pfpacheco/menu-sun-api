import graphene

from menu_sun_api.interfaces.definition.customer import CustomerMetafield as CustomerMetafieldDefinition
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput

from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerMetafieldInput
from menu_sun_api.command.customer.metafield.customer_metafield_bulk_upsert_command import CustomerMetafieldBulkUpsertCommand, \
    CustomerMetafieldBulkUpsertCommandHandler
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.infrastructure.connection_factory import Session


class CustomerMetafieldBulkUpsert(graphene.Mutation):
    class Arguments:
        metafields = graphene.List(CustomerMetafieldInput, required=True)

    metafields = graphene.List(CustomerMetafieldDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, metafields, **args):
        session = Session()
        seller = info.context.get('seller')
        customer_repository = CustomerRepository(session)
        from_input = MapInputToCommand()
        metafields_list = [i.accept(from_input) for i in metafields]

        command = CustomerMetafieldBulkUpsertCommand(metafields=metafields_list,
                                                     seller_id=seller.id)

        handler = CustomerMetafieldBulkUpsertCommandHandler(
            customer_repository=customer_repository,
            session=session)
        rs = handler.execute(command)
        if (rs):
            return CustomerMetafieldBulkUpsert(metafields=rs.value,
                                               failure_message=None)
        else:
            return CustomerMetafieldBulkUpsert(metafields=[],
                                               failure_message=rs)


class CustomerMetafieldBulkUpsertMutation(graphene.ObjectType):
    customer_metafield_bulk_upsert = CustomerMetafieldBulkUpsert.Field()
