import graphene

from menu_sun_api.interfaces.definition.customer import Customer as CustomerDefinition
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.command.customer.customer_bulk_upsert_command import CustomerBulkUpsertCommand, \
    CustomerBulkUpsertCommandHandler
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository


class CustomerBulkUpsert(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, customers, **args):
        session = Session()
        seller = info.context.get('seller')
        customer_repository = CustomerRepository(session)
        from_input = MapInputToCommand()
        customer_list = [i.accept(from_input) for i in customers]

        command = CustomerBulkUpsertCommand(customers=customer_list,
                                            seller_id=seller.id)

        handler = CustomerBulkUpsertCommandHandler(
            customer_repository=customer_repository,
            session=session)
        rs = handler.execute(command)
        if (rs):
            return CustomerBulkUpsert(customers=rs.value,
                                      failure_message=None)
        else:
            return CustomerBulkUpsert(customers=[],
                                      failure_message=rs)


class CustomerBulkCreateMutation(graphene.ObjectType):
    customer_bulk_upsert = CustomerBulkUpsert.Field()
