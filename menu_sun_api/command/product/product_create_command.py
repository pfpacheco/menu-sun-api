from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.product.product import Product, ProductMetafield, MetaTags


class ProductCreateCommand(Command):

    def __init__(self, product, seller_id):
        self.product = product
        self.seller_id = seller_id

    def validate(self):
        return True


class ProductCreateCommandHandler(TransactionCommandHandler):

    def __init__(self, product_repository, session):
        super(ProductCreateCommandHandler, self).__init__(session)
        self.product_repository = product_repository

    def process_request(self, command):
        seller_id = command.seller_id
        product = command.product
        sku = product['sku']
        metafields = []
        metatags = []
        if 'metafields' in product:
            metafields = list(map(lambda metafield: ProductMetafield.from_dict(metafield), product['metafields']))
        if 'metatags' in product:
            metatags = list(map(lambda metatag: MetaTags.from_dict(metatag), product['metatags']))

        product = Product.from_dict(product)
        product_db = self.product_repository.get_by_sku(seller_id=seller_id, sku=sku)

        if not product_db:
            product.seller_id = seller_id
            product.metafields = metafields
            product.meta_tags = metatags
            rs = self.product_repository.add(product)
            return SuccessResponse(rs)
