from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.product.product import Product


class ProductUpdateCommand(Command):

    def __init__(self, product, seller_id):
        self.product = product
        self.seller_id = seller_id

    def validate(self):
        return True


class ProductUpdateCommandHandler(TransactionCommandHandler):

    def __init__(self, product_repository, session):
        super(ProductUpdateCommandHandler, self).__init__(session)
        self.product_repository = product_repository

    def process_request(self, command):
        seller_id = command.seller_id
        product = command.product
        sku = product['sku']
        product_db = self.product_repository.get_by_sku(seller_id=seller_id, sku=sku)
        if not product_db:
            return FailureResponse(
                category=FailureResponseCategory.ERROR,
                key='product_not_found',
                args=[sku]
            )
        product_db.update_from_dict(product)
        return SuccessResponse(product_db)
