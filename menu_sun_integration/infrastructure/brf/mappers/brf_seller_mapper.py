from typing import Optional, Dict

from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BRFSellerMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Seller):
            metafield_document = next(
                (field for field in entity.metafields if field.namespace == "INTEGRATION_API_FIELD"
                 and field.key == "CDD_DOCUMENT"), None)

            metafield_postal_code = next(
                (field for field in entity.metafields if field.namespace == "INTEGRATION_API_FIELD"
                 and field.key == "CDD_POSTAL_CODE"), None)

            cnpj_default_cdd = metafield_document.value if metafield_document else ""
            postal_code_default_cdd = metafield_postal_code.value if metafield_postal_code else ""

            return {"seller_id": entity.id, "seller_code": entity.seller_code, "cdd_document": cnpj_default_cdd,
                    "integration_type": entity.get_integration_type().name, "cdd_postal_code": postal_code_default_cdd}

        return None
