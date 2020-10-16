import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from menu_sun_api.domain.model.seller.seller import SellerMetafield


class SellerMetafield(SQLAlchemyObjectType):
    class Meta:
        model = SellerMetafield
        description = "SellerMetafield"
        exclude_fields = ('seller_id', 'id',)
