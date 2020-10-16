import graphene

from menu_sun_api.interfaces.definition.customer import CustomerMetafield as CustomerMetafieldDefinition
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerMetafieldInput


class CustomerMetafieldBulkDelete(graphene.Mutation):
    class Arguments:
        document = graphene.String(required=True)
        key = graphene.String(required=True)
        namespace = graphene.String(required=True)

    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, customers, **args):
        pass


class CustomerMetafieldBulkDeleteMutation(graphene.ObjectType):
    customer_metafield_bulk_delete = CustomerMetafieldBulkDelete.Field()
