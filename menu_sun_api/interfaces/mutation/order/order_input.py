from menu_sun_api.interfaces.mutation.sqlalchemy_input_object_type import SQLAlchemyInputObjectType
from menu_sun_api.domain.model.order.order import OrderShippingAddress, \
    OrderBillingAddress, Order, OrderItem, OrderPayment, OrderMetafield
import graphene


class OrderMetafieldInput(SQLAlchemyInputObjectType):
    class Meta:
        model = OrderMetafield
        exclude_fields = ('order_id',
                          'created_date',
                          'updated_date',
                          'id'
                          )


class OrderPaymentInput(SQLAlchemyInputObjectType):
    class Meta:
        model = OrderPayment
        exclude_fields = ('id',
                          'updated_date',
                          'created_date',
                          'order_id',
                          )


class OrderBillingAddressInput(SQLAlchemyInputObjectType):
    class Meta:
        model = OrderBillingAddress
        exclude_fields = ('id',
                          'uuid',
                          'updated_date',
                          'created_date')


class OrderShippingAddressInput(SQLAlchemyInputObjectType):
    class Meta:
        model = OrderShippingAddress
        exclude_fields = ('id',
                          'uuid',
                          'updated_date',
                          'created_date')


class OrderItemInput(SQLAlchemyInputObjectType):
    class Meta:
        model = OrderItem
        only_fields = ('sku', 'name', 'ean', 'ncm', 'price', 'original_price', 'quantity')


class OrderInput(SQLAlchemyInputObjectType):
    class Meta:
        model = Order
        only_fields = ('order_id',
                       'delivery_date',
                       'order_date',
                       'subtotal',
                       'total',
                       'shipping'
                       )
        # exclude_fields = ('id')

    billing_address = OrderBillingAddressInput()
    shipping_address = OrderShippingAddressInput(required=True)
    document = graphene.String(required=True)
    email = graphene.String(required=False)
    items = graphene.List(OrderItemInput)
    payments = graphene.List(OrderPaymentInput, required=True)
    meta_fields = graphene.List(OrderMetafieldInput, required=False)
