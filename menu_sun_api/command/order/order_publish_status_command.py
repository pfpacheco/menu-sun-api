from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse


class OrderPublishStatusCommand():

    def __init__(self, status):
        self.status = status


class OrderPublishStatusCommandHandler(TransactionCommandHandler):

    def __init__(self, order_repository, session):
        super(OrderPublishStatusCommandHandler, self).__init__(session)
        self.order_repository = order_repository

    def process_request(self, command):
        order_id = command.order_id
        seller_id = command.seller_id
        order = self.order_repository.get_order(
            order_id=order_id, seller_id=seller_id)
        if not order:
            rs = FailureResponse(category=FailureResponseCategory.ERROR,
                                 key='order_not_found',
                                 args=[order_id]
                                 )
            return rs
        self.change_status(order)
        return SuccessResponse(order)
