from factory import BUILD_STRATEGY, Sequence, SubFactory, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from menu_sun_api.domain.model.order.order import Order, \
    OrderShippingAddress, OrderBillingAddress, OrderStatus, OrderPayment, OrderPaymentType, OrderItem
from menu_sun_api.infrastructure.connection_factory import Session
from datetime import datetime


class OrderItemFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = OrderItem
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    sku = "988"
    quantity = 2
    price = 10.0


class OrderPaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = OrderPayment
        sqlalchemy_session = Session
    id = Sequence(lambda n: n + 1)
    payment_type = OrderPaymentType.BOLETO
    deadline = 10


class OrderStatusFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = OrderStatus
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)


class OrderShippingAddressFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = OrderShippingAddress
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)


class OrderBillingAddressFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = OrderBillingAddress
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)


class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = Order
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    shipping_address = SubFactory(OrderShippingAddressFactory)
    billing_address = SubFactory(OrderBillingAddressFactory)
    order_id = '12345'
    total = 10
    subtotal = 9
    shipping = 1
    order_date = datetime.utcnow().isoformat()
    delivery_date = datetime.utcnow().isoformat()
    integration_date = datetime.utcnow().isoformat()

    @post_generation
    def payments(self, create, extracted, **kwargs):

        if not create:
            # Build, not create related
            return

        if extracted:
            assert isinstance(extracted, int)
            OrderPaymentFactory.create_batch(
                size=extracted, order_id=self.id, **kwargs)
        else:
            OrderPaymentFactory.create(order_id=self.id,
                                       **kwargs)

    @post_generation
    def items(self, create, extracted, **kwargs):
        """
        If called like: TeamFactory(players=4) it generates a Team with 4
        players.  If called without `players` argument, it generates a
        random amount of players for this team
        """
        if not create:
            # Build, not create related
            return

        if extracted:
            assert isinstance(extracted, int)
            OrderItemFactory.create_batch(
                size=extracted, order_id=self.id, **kwargs)
        else:
            OrderItemFactory.create(order_id=self.id,
                                    **kwargs)
