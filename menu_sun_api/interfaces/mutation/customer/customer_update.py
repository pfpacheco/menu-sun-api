import graphene

from menu_sun_api.interfaces.definition.customer import Customer as CustomerDefinition
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.customer.customer_service import CustomerService


class CustomerUpdate(graphene.Mutation):
    class Arguments:
        customer = CustomerInput(required=True)

    customer = graphene.Field(CustomerDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, customer, **args):
        repository = CustomerRepository()
        seller = info.context.get('seller')
        service = CustomerService(repository)
        customer_domain = customer.map()
        res = service.update_customer(
            seller_id=seller.id,
            document=customer.document,
            customer=customer_domain)

        if (res):
            Session.commit()
            return CustomerUpdate(failure_message=None, customer=res.value)
        else:
            failure_message = FailureMessage.to_definition(res.value)
            return CustomerUpdate(
                failure_message=failure_message, customer=None)


class CustomerUpdateMutation(graphene.ObjectType):
    customer_update = CustomerUpdate.Field()
