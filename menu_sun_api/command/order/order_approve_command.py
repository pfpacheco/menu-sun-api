from menu_sun_api.command.command_handler import Command
from menu_sun_api.command.order.order_change_status_command import OrdeChangeStatusCommandHandler


class OrderApproveCommand(Command):

    def __init__(self, order_id, seller_id):
        self.order_id = order_id
        self.seller_id = seller_id

    def validate(self):
        return True


class OrderApproveCommandHandler(OrdeChangeStatusCommandHandler):

    def __init__(self, order_repository, session, owner):
        super(
            OrderApproveCommandHandler,
            self).__init__(
            order_repository,
            session, owner)

    def change_status(self, order):
        order.approve(self.owner)
