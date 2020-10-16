import graphene

from menu_sun_api.interfaces.definition.customer import Customer as CustomerDefinition
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.command.customer.customer_create_command import CustomerCreateCommand, CustomerCreateCommandHandler
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository


class CustomerCreate(graphene.Mutation):
    class Arguments:
        customer = CustomerInput(required=True)

    customer = graphene.Field(CustomerDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, customer, **args):
        session = Session()
        seller = info.context.get('seller')

        from_input = MapInputToCommand()
        customer = customer.accept(from_input)
        command = CustomerCreateCommand(customer=customer, seller_id=seller.id)
        handler = CustomerCreateCommandHandler(
            CustomerRepository(session), session)
        rs = handler.execute(command)
        if (rs):
            return CustomerCreate(customer=rs.value, failure_message=None)
        else:
            return CustomerCreate(customer=None, failure_message=rs)


class CustomerCreateMutation(graphene.ObjectType):
    customer_create = CustomerCreate.Field()
