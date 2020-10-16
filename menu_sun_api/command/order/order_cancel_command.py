from menu_sun_api.command.command_handler import Command
from menu_sun_api.command.order.order_change_status_command import OrdeChangeStatusCommandHandler
from menu_sun_api.domain.model.order.order import OwnerType


class OrderCancelCommand(Command):

    def __init__(self, order_id, seller_id):
        self.order_id = order_id
        self.seller_id = seller_id

    def validate(self):
        return True


class OrderCancelCommandHandler(OrdeChangeStatusCommandHandler):

    def __init__(self, order_repository, session, owner):
        super(
            OrderCancelCommandHandler,
            self).__init__(
            order_repository,
            session, owner)

    def change_status(self, order):
        order.cancel(owner=self.owner)
