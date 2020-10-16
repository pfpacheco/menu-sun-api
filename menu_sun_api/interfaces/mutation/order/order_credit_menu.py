import graphene

from menu_sun_api.command.order.order_credit_menu_command import OrderCreditMenuCommand, OrderCreditMenuCommandHandler
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session


class OrderCreditMenu(graphene.Mutation):
    class Arguments:
        order_id = graphene.String(required=True)

    order_id = graphene.String(required=True)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, order_id, **args):
        session = Session()
        seller = info.context.get('seller')
        order_repository = OrderRepository()
        command = OrderCreditMenuCommand(seller_id=seller.id, order_id=order_id)
        handler = OrderCreditMenuCommandHandler(
            order_repository=order_repository, session=session)
        rs = handler.execute(command)
        if rs:
            return OrderCreditMenu(order_id=order_id, failure_message=None)
        else:
            return OrderCreditMenu(order_id=order_id, failure_message=rs)


class OrderCreditMenuMutation(graphene.ObjectType):
    order_credit_menu = OrderCreditMenu.Field()
