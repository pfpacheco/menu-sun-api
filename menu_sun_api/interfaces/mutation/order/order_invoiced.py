import graphene

from menu_sun_api.domain.model.order.order import OwnerType
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.order.order_invoice_command import OrderInvoiceCommand, OrderInvoiceCommandHandler


class OrderInvoiced(graphene.Mutation):
    class Arguments:
        order_id = graphene.String(required=True)

    order_id = graphene.String(required=True)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, order_id, **args):
        session = Session()
        seller = info.context.get('seller')
        order_repository = OrderRepository()
        command = OrderInvoiceCommand(seller_id=seller.id, order_id=order_id)
        handler = OrderInvoiceCommandHandler(
            order_repository=order_repository, session=session, owner=OwnerType.MENU)
        rs = handler.execute(command)
        if rs:
            return OrderInvoiced(order_id=order_id, failure_message=None)
        else:
            return OrderInvoiced(order_id=order_id, failure_message=rs)


class OrderInvoicedMutation(graphene.ObjectType):
    order_invoiced = OrderInvoiced.Field()
