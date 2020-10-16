import graphene

from menu_sun_api.domain.model.order.order import OwnerType
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.order.order_cancel_command import OrderCancelCommandHandler, OrderCancelCommand
from menu_sun_api.application.order_service import OrderService


class OrderCanceled(graphene.Mutation):
    class Arguments:
        order_id = graphene.String(required=True)

    order_id = graphene.String(required=False)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, order_id, **args):
        session = Session()
        seller = info.context.get('seller')
        order_repository = OrderRepository()
        command = OrderCancelCommand(seller_id=seller.id, order_id=order_id)
        handler = OrderCancelCommandHandler(
            order_repository=order_repository, session=session, owner=OwnerType.MENU)
        rs = handler.execute(command)
        if rs:
            return OrderCanceled(order_id=order_id, failure_message=None)
        else:
            return OrderCanceled(order_id=order_id, failure_message=rs)


class OrderCanceledMutation(graphene.ObjectType):
    order_canceled = OrderCanceled.Field()
