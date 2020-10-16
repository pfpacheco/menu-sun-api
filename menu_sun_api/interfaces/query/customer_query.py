import graphene
from graphene import ObjectType

from menu_sun_api.interfaces.definition.customer import Customer
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.customer.customer import Customer as CustomerDomain
from menu_sun_api.domain.model.customer.customer_service import CustomerService


class CustomerFilter(graphene.InputObjectType):
    updated_date = graphene.DateTime()


class CustomerQuery(ObjectType):
    customer_by_id = graphene.Field(Customer, id=graphene.ID(required=True))
    customer = graphene.Field(
        Customer, document=graphene.String(
            required=True))
    customers = graphene.List(
        Customer,
        offset=graphene.Int(),
        limit=graphene.Int())

    customer_by_integration_type = graphene.Field(
        Customer, document=graphene.String(
            required=True))

    def resolve_customers(parent, info, **kwargs):
        seller = info.context.get('seller')
        offset = kwargs.get('offset')
        limit = kwargs.get('limit')
        repository = CustomerRepository()
        service = CustomerService(repository)
        customers = service.load_all_customers(
            seller_id=seller.id, offset=offset, limit=limit)

        return customers.value

    def resolve_customer_by_id(parent, info, id, **kwargs):
        repository = CustomerRepository()
        uc = CustomerService(repository)
        customer = uc.load_by_uuid(uuid=id)
        if customer.value:
            info.context['customer_id'] = customer.value.id
            return customer.value
        return None

    def resolve_customer(parent, info, document, **kwargs):
        seller = info.context.get('seller')
        repository = CustomerRepository()
        uc = CustomerService(repository)
        customer = uc.get_by_document(seller.id, document=document)
        if (customer.value):
            info.context['customer_id'] = customer.value.id
            return customer.value
        return CustomerDomain(document=document, uuid="")

    def resolve_customers_by_document(parent, info, **kwargs):
        pass
        # seller = info.context.get('seller')
        # repository = DBProductRepository()
        # list_product = ListProduct(repository)
        # request = ListProductRequest(seller_uuid=seller.uuid, skus=kwargs.get('skus'))
        # res = list_product.execute(request)
        # return [Product.from_domain(p) for p in res.value]

    def resolve_customer_by_integration_type(parent, info, document, **kwargs):
        seller = info.context.get('seller')
        repository = CustomerRepository()
        uc = CustomerService(repository)
        customer = uc.get_by_integration(seller.integration_type, document=document)
        if customer.value:
            info.context['customer_id'] = customer.value.id
            return customer.value
        return None
