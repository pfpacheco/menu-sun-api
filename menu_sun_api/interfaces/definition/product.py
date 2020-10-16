import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from menu_sun_api.interfaces.definition.pricing import Pricing
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.domain.model.product.product import Product as ProductDomain
from menu_sun_api.domain.model.product.product import ProductMetafield as ProductMetafieldDomain


class ProductMetafield(SQLAlchemyObjectType):
    class Meta:
        model = ProductMetafieldDomain
        description = "ProductMetafieldDomain"
        exclude_fields = ('product_id', 'id',)


class Product(SQLAlchemyObjectType):
    pricing = graphene.Field(Pricing)

    class Meta:
        model = ProductDomain
        description = "Product Domain"
        exclude_fields = ('uuid', 'product_metadata', 'seller_id')

    def resolve_id(parent, info):
        return parent.uuid

    def resolve_pricing(parent, info, **kwargs):
        repository = PricingRepository()
        customer_id = info.context.get('customer_id')
        pricing = repository.get_pricing_by_customer_and_product(product_id=parent.id,
                                                                 customer_id=customer_id)
        return pricing

    @classmethod
    def from_domain(cls, value):
        pass
