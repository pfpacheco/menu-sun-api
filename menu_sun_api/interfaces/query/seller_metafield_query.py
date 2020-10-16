import graphene
from graphene import ObjectType

from menu_sun_api.interfaces.definition.seller import SellerMetafield
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository


class SellerMetafieldQuery(ObjectType):
    metafields = graphene.List(SellerMetafield)
    metafield = graphene.Field(SellerMetafield,
                               namespace=graphene.String(required=True),
                               key=graphene.String(required=True))

    def resolve_metafields(parent, info, **kwargs):
        seller = info.context.get('seller')
        repository = SellerRepository()
        seller = repository.get_by_id(seller_id=seller.id)
        return seller.metafields

    def resolve_metafield(parent, info, namespace, key, **kwargs):
        seller = info.context.get('seller')
        repository = SellerRepository()
        return repository.get_metafield(
            seller_id=seller.id, key=key, namespace=namespace)
