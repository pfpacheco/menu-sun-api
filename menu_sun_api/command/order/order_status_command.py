from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.order.order import Order, OrderStatus, OwnerType
from test.menu_sun_api.db.order_factory import OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatusType


class OrderStatusCommand(Command):

    def __init__(self, order_id, comments, status, seller_id, owner):
        self.order_id = order_id
        self.comments = comments
        self.status = status
        self.seller_id = seller_id
        self.owner = owner

    def validate(self):
        return True


class OrderStatusCommandHandler(TransactionCommandHandler):

    def __init__(self, order_repository, session):
        super(OrderStatusCommandHandler, self).__init__(session)
        self.order_repository = order_repository

    def process_request(self, command):
        order_id = command.order_id
        comments = command.comments
        status = command.status
        owner = command.owner
        order = self.order_repository.get_order_not_seller_id(order_id=order_id)
        if not order:
            rs = FailureResponse(category=FailureResponseCategory.ERROR,
                                 key='order_not_exists',
                                 args=[order_id]
                                 )
            return rs
        order_status = OrderStatus(status=status, comments=comments, owner=owner)
        order.statuses.append(order_status)
        if order_status.status in [OrderStatusType.CREDIT_MENU.name]:
            order.order_queue_date = None
        rs = self.order_repository.add(order)
        return SuccessResponse(rs)
