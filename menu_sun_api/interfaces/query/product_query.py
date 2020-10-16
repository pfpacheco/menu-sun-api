import graphene
from graphene import ObjectType

from menu_sun_api.interfaces.definition.product import Product
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.application.product_service import ProductService


class ProductQuery(ObjectType):
    product_by_id = graphene.Field(Product, id=graphene.ID(required=True))
    # products = graphene.List(Product, skus=graphene.List(graphene.String, required=True))
    product = graphene.Field(Product, sku=graphene.String(required=True))
    search_products_by_date_created_or_updated = graphene.List(
        Product, date=graphene.Date(required=True))

    def resolve_product_by_id(parent, info, id, **kwargs):
        repository = ProductRepository()
        uc = ProductService(repository)
        res = uc.get_by_id(product_id=id)
        return Product.from_domain(res.value)

    def resolve_search_products_by_date_created_or_updated(
            parent, info, date, **kwargs):
        seller = info.context.get('seller')
        repository = ProductRepository()
        uc = ProductService(repository)
        res = uc.get_products_by_created_date_or_update(created_date=date, seller_id=seller.id)
        return res.value

    # def resolve_products(parent, info, skus, **kwargs):
    #     seller = info.context.get('seller')
    #     repository = ProductRepository()
    #     uc = ProductService(repository)
    #     res = uc.search_by_skus(seller_id=seller.id, skus=skus)
    #     return res.value

    def resolve_product(self, info, sku, **kwargs):
        seller = info.context.get('seller')
        repository = ProductRepository()
        uc = ProductService(repository)
        res = uc.get_by_sku(sku=sku, seller_id=seller.id)
        return res.value
