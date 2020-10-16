from graphene_sqlalchemy import SQLAlchemyObjectType

from menu_sun_api.domain.model.order.order import Order as OrderDomain
from menu_sun_api.domain.model.order.order import OrderBillingAddress as OrderBillingAddressDomain
from menu_sun_api.domain.model.order.order import OrderShippingAddress as ShippingAddressDomain
from menu_sun_api.domain.model.order.order import OrderStatus as OrderStatusDomain
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order import OrderMetafield as OrderMetafieldDomain
from menu_sun_api.domain.model.customer.customer import Customer as CustomerDomain


class OrderMetafield(SQLAlchemyObjectType):
    class Meta:
        model = OrderMetafieldDomain
        description = "OrderMetafieldDomain"
        exclude_fields = ('order_id',)


class OrderStatus(SQLAlchemyObjectType):
    class Meta:
        model = OrderStatusDomain
        description = "Order Status"
        exclude_fields = ('id',
                          'order_queue_date',
                          'integration_date',
                          'seller_order_id',
                          'seller_id',)


class OrderShippingAddress(SQLAlchemyObjectType):
    class Meta:
        model = ShippingAddressDomain
        description = "Shipping Address"
        exclude_fields = ('id',)


class OrderCustomer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerDomain
        description = "Customer"
        exclude_fields = ('id',)


class OrderBillingAddress(SQLAlchemyObjectType):
    class Meta:
        model = OrderBillingAddressDomain
        description = "Billing Address"
        exclude_fields = ('id',)


class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderDomain
        description = "Order Domain"
        exclude_fields = ('id',)

    def resolve_statuses(parent, info, **kwargs):
        order_id = parent.order_id
        seller = info.context.get('seller')
        repository = OrderRepository()
        order_service = OrderService(repository)
        statuses = order_service.load_statuses(
            seller_id=seller.id, order_id=order_id)
        return statuses.value
