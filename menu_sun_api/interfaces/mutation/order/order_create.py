import graphene

from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.interfaces.mutation.order.order_input import OrderInput
from menu_sun_api.domain.model.order.order import OrderPaymentType, OrderPayment
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.customer.customer import Customer


class OrderCreate(graphene.Mutation):
    class Arguments:
        order = OrderInput(required=True)

    order_id = graphene.String(required=True)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, order, **args):
        seller = info.context.get('seller')
        order_domain = order.map(additional={'seller_id': seller.id}, excludes=['payments',
                                                                                'items',
                                                                                'billing_address',
                                                                                'shipping_address',
                                                                                'meta_fields'])

        customer_repository = CustomerRepository()

        customer_domain = customer_repository.get_by_document(
            seller_id=seller.id, document=order['document'])

        if not customer_domain:
            customer_domain = customer_repository.add(Customer(document=order['document'],
                                                               email=order['email'],
                                                               seller_id=seller.id,
                                                               cep=order['billing_address']['postcode'],
                                                               uf=order['billing_address']['state_code'],
                                                               name=order['billing_address']['name'],
                                                               phone_number=order['billing_address']['phone']))
            order_domain.seller_id = customer_domain.seller_id
            Session().commit()

        order_domain.billing_address = order.billing_address.map(
        ) if order.billing_address is not None else None
        order_domain.customer_id = customer_domain.id

        order_domain.shipping_address = order.shipping_address.map(
        ) if order.shipping_address is not None else None

        if order.items:
            for item in order.items:
                order_domain.items.append(item.map())
        if order.payments:
            for payment in order.payments:
                payment_type = OrderPaymentType(payment.payment_type)
                payment_domain = OrderPayment(
                    deadline=payment.deadline, payment_type=payment_type)
                order_domain.payments.append(payment_domain)

        if order.meta_fields:
            for metafield in order.meta_fields:
                metafield_domain = metafield.map()
                if metafield_domain.value:
                    order_domain.change_metafield(metafield.map())

        repository = OrderRepository()
        order_service = OrderService(repository)
        rs = order_service.create_order(order_domain)

        if rs:
            Session().commit()
            return OrderCreate(order_id=order.order_id, failure_message=None)
        else:
            return OrderCreate(order_id=None, failure_message=None)


class OrderCreateMutation(graphene.ObjectType):
    order_create = OrderCreate.Field()
