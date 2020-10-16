from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield, IntegrationType
from menu_sun_integration.infrastructure.brf.mappers.brf_seller_mapper import BRFSellerMapper


def test_map_brf_seller_to_message():
    random = SellerMetafield(
        namespace="ADF", key="has_adf", value="true")

    document = SellerMetafield(
        namespace="INTEGRATION_API_FIELD", key="CDD_DOCUMENT", value="0000.0000.00000/0-00")

    postal_code = SellerMetafield(
        namespace="INTEGRATION_API_FIELD", key="CDD_POSTAL_CODE", value="00000-000")
    seller = Seller(id=1, seller_code="00001", metafields=[random, document, postal_code],
                    integration_type=IntegrationType.BRF)

    visit = BRFSellerMapper()
    seller_dict = seller.accept(visit)
    assert (seller_dict['integration_type'] == seller.get_integration_type().name)
    assert (seller_dict['cdd_document'] == document.value)
    assert (seller_dict['cdd_postal_code'] == postal_code.value)
