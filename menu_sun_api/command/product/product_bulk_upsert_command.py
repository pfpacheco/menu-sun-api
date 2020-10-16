from menu_sun_api.command.command_handler import Command, TransactionCommandHandler
from menu_sun_api.command.command_response import FailureResponse, FailureResponseCategory, SuccessResponse
from menu_sun_api.domain.model.product.product import Product, ProductMetafield, MetaTags


class ProductBulkUpsertCommand(Command):

    def __init__(self, product_list, seller_id):
        self.product_list = product_list
        self.seller_id = seller_id

    def validate(self):
        return True


class ProductBulkUpsertCommandHandler(TransactionCommandHandler):

    def __init__(self, product_repository, session):
        super(ProductBulkUpsertCommandHandler, self).__init__(session)
        self.product_repository = product_repository

    def process_request(self, command):
        seller_id = command.seller_id
        ls = []
        for command in command.product_list:
            sku = command['sku']
            metafields = []
            metatags = []
            if 'metafields' in command:
                metafields = list(map(lambda metafield: ProductMetafield.from_dict(metafield), command['metafields']))
            if 'metatags' in command:
                metatags = list(map(lambda metatag: MetaTags.from_dict(metatag), command['metatags']))

            product_db = self.product_repository.get_by_sku(
                seller_id=seller_id, sku=sku)
            if product_db:
                product_db.update_from_dict(command)
                for metafield in metafields:
                    product_db.change_metafield(metafield)
                for metatag in metatags:
                    product_db.change_meta_tags(metatag)
                rs = product_db
            else:
                product = Product.from_dict(command)
                product.seller_id = seller_id
                product.metafields = metafields
                product.meta_tags = metatags
                rs = self.product_repository.add(product)
            ls.append(rs)
        return SuccessResponse(ls)
