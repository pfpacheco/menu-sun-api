from menu_sun_api.domain.model.response.failure_response import FailureResponse
from menu_sun_api.domain.model.response.success_response import SuccessResponse


class ProductService:

    def __init__(self, repository):
        self.repository = repository

    def get_by_sku(self, seller_id, sku):
        product = self.repository.get_by_sku(seller_id, sku)
        return SuccessResponse(value=product)

    def get_by_id(self, product_id):
        product = self.repository.get_by_uuid(product_id)
        return SuccessResponse(value=product)

    def get_products_by_created_date_or_update(self, created_date, seller_id):
        product = self.repository.get_products_by_created_date_or_update(
            created_date, seller_id)
        return SuccessResponse(value=product)

    def search_by_skus(self, seller_id, skus):
        products = self.repository.search_products(seller_id,
                                                   skus)
        return SuccessResponse(products)

    def search_by_seller(self, seller_id):
        products = self.repository.search_products(seller_id)
        return SuccessResponse(products)

    def get_products_by_seller(self, seller_id):
        products = self.repository.search_products(seller_id)
        return SuccessResponse(products)

    def create_product(self, product):
        rs = self.repository.add(product)
        return SuccessResponse(rs)

    def update_product_by_sku(self, seller_id, sku, product):
        product_db = self.get_by_sku(sku=sku, seller_id=seller_id)
        value = product_db.value
        value.update(product)
        # product_db = Mapper.domain_to_domain(source=product, target=value)
        return SuccessResponse(value)

    def delete_product_by_sku(self, seller_id, sku):
        product = self.repository.delete_by_sku(seller_id, sku)
        if product:
            return SuccessResponse(value=product)
        return FailureResponse()
