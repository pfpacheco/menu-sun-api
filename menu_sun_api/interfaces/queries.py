import graphene

from menu_sun_api.interfaces.query.customer_query import CustomerQuery
from menu_sun_api.interfaces.query.order_query import OrderQuery
from menu_sun_api.interfaces.query.product_query import ProductQuery
from menu_sun_api.interfaces.query.seller_metafield_query import SellerMetafieldQuery


class Query(ProductQuery,
            CustomerQuery,
            OrderQuery,
            SellerMetafieldQuery,
            graphene.ObjectType):
    pass
