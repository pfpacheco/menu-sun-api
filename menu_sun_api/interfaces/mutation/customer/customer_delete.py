import graphene

from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.customer.customer_service import CustomerService


class CustomerDelete(graphene.Mutation):
    class Arguments:
        document = graphene.String(required=True)

    id = graphene.ID(required=True)

    def mutate(parent, info, document, **args):
        seller = info.context.get('seller')
        repository = CustomerRepository()
        service = CustomerService(repository)
        customer = service.delete_customer(
            seller_id=seller.id, document=document)
        Session().commit()
        return CustomerDelete(id=customer.value.uuid)


class CustomerDeleteMutation(graphene.ObjectType):
    customer_delete = CustomerDelete.Field()
