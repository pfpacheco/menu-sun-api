import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from menu_sun_api.interfaces.definition.product import Product
from menu_sun_api.domain.model.customer.customer import Customer as CustomerDomain
from menu_sun_api.domain.model.customer.customer import CustomerMetafield as CustomerMetafieldDomain

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.application.product_service import ProductService
from menu_sun_api.domain.model.customer.customer import PaymentTerms as PaymentTermsDomain


class PaymentTerms(SQLAlchemyObjectType):
    class Meta:
        model = PaymentTermsDomain
        description = "Payment Terms"
        exclude_fields = ('id',)

    def resolve_id(parent, info):
        return parent.uuid


class CustomerMetafield(SQLAlchemyObjectType):
    class Meta:
        model = CustomerMetafieldDomain
        description = "CustomerMetafieldDomain"
        exclude_fields = ('customer_id', 'id',)


class Customer(SQLAlchemyObjectType):
    products = graphene.List(Product)

    class Meta:
        model = CustomerDomain
        description = "Customer"
        exclude_fields = ('uuid',)

    def resolve_id(parent, info):
        return parent.uuid

    def resolve_products(parent, info, **kwargs):
        seller = info.context.get('seller')
        repository = ProductRepository()
        uc = ProductService(repository)
        res = uc.get_products_by_seller(seller_id=seller.id)
        return res.value
