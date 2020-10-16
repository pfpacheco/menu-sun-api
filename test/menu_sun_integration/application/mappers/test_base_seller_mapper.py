from menu_sun_api.domain.model.seller.seller import SellerMetafield, Seller
from menu_sun_integration.application.mappers.base_seller_mapper import BaseSellerMapper


def test_map_base_seller_to_message():
    seller_metafield = SellerMetafield(
        namespace="ADF", key="has_adf", value="true")
    seller = Seller(id=1, seller_code="00001", metafields=[seller_metafield])

    visit = BaseSellerMapper()
    seller_dict = seller.accept(visit)

    assert (seller_dict['seller_id'] == seller.id)
    assert (seller_dict['seller_code'] == seller.seller_code)
    assert (seller_dict['integration_type'] == seller.get_integration_type().name)
    assert (seller_dict['seller_metafields'][0]['namespace'] == seller_metafield.namespace)
    assert (seller_dict['seller_metafields'][0]['key'] == seller_metafield.key)
    assert (seller_dict['seller_metafields'][0]['value'] == seller_metafield.value)
