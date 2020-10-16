import os

from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_by_sku_post_request import \
    AbstractProductDefaultPricingBySkuPostRequest


class PernodProductDefaultPricingBySkuPostRequest(AbstractProductDefaultPricingBySkuPostRequest):
    def __init__(self, sku: str):
        super().__init__(sku)
        self.sku = sku
        self.id_tenant = os.getenv("PERNOD_ID_TENANT")

    @property
    def payload(self) -> str:
        payload = '{"products": [{"destinationSku": "%s"}]}' % self.sku

        self._logger.info(
            key="inventory_get_request",
            description="payload",
            payload=payload)

        return payload

    @property
    def resource(self) -> str:
        return f'freight/menu/{self.id_tenant}'
