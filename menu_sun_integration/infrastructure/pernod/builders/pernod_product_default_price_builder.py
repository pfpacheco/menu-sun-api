from menu_sun_integration.application.adapters.product_default_pricing_by_sku_adapter import \
    ProductDefaultPricingBySkuAdapter
from menu_sun_integration.infrastructure.pernod.builders.pernod_base_builder import PernodBaseBuilder
from menu_sun_integration.infrastructure.pernod.translators.pernod_product_default_princing_by_sku_translator import \
    PernodProductDefaultPricingBySkuTranslator


class PernodProductDefaultPricingBuilder(PernodBaseBuilder):
    def define_translator(self) -> None:
        self._translator = PernodProductDefaultPricingBySkuTranslator()

    def build_adapter(self) -> None:
        self._adapter = ProductDefaultPricingBySkuAdapter(client=self._client, translator=self._translator)
