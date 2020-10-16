from menu_sun_api.domain.model.response.failure_response import FailureResponse, FailureResponseCategory
from menu_sun_api.domain.model.response.success_response import SuccessResponse


class ProductService:

    def __init__(self, repository):
        self.repository = repository

    def update_product(self, seller_id, sku, product):
        product_db = self.repository.get_by_sku(sku=sku, seller_id=seller_id)

        if not product_db:
            rs = FailureResponse(FailureResponseCategory.ERROR,
                                 key='product_not_found',
                                 args=[sku]
                                 )
            return rs
        product_db.update(product)
        product_db.update_metafields(product.metafields)
        return SuccessResponse(product_db)

    def load_all(self, seller_id):
        products_db = self.repository.load_all(seller_id=seller_id)
        return SuccessResponse(products_db)

    def create_product(self, product_domain):
        self.repository.add(product_domain)
        # should check if the customer exists
        return SuccessResponse(product_domain)
