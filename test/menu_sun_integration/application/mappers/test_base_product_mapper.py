from menu_sun_api.domain.model.product.product import Product
from menu_sun_integration.application.mappers.base_product_mapper import BaseProductMapper


def test_map_base_product_to_message():
    product = Product(id=1, sku="00001")
    visit = BaseProductMapper()
    product_dict = product.accept(visit)
    assert (product_dict['sku'] == product.sku)
