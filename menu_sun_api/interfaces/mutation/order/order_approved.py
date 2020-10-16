import graphene

from menu_sun_api.domain.model.order.order import OwnerType
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.order.order_approve_command import OrderApproveCommand, OrderApproveCommandHandler


class OrderApproved(graphene.Mutation):
    class Arguments:
        order_id = graphene.String(required=True)

    order_id = graphene.String(required=True)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, order_id, **args):
        session = Session()
        seller = info.context.get('seller')
        order_repository = OrderRepository()
        command = OrderApproveCommand(seller_id=seller.id, order_id=order_id)
        handler = OrderApproveCommandHandler(
            order_repository=order_repository, session=session, owner=OwnerType.MENU)
        rs = handler.execute(command)
        if rs:
            return OrderApproved(order_id=order_id, failure_message=None)
        else:
            return OrderApproved(order_id=order_id, failure_message=rs)


class OrderApprovedMutation(graphene.ObjectType):
    order_approved = OrderApproved.Field()
