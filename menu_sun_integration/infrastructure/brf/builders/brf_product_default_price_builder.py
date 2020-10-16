
from menu_sun_integration.application.adapters.product_default_pricing_adapter import ProductDefaultPricingAdapter
from menu_sun_integration.infrastructure.brf.builders.brf_base_builder import BRFBaseBuilder
from menu_sun_integration.infrastructure.brf.translators.brf_product_default_pricing_translator import \
    BRFProductDefaultPricingTranslator


class BRFProductDefaultPricingBuilder(BRFBaseBuilder):
    def define_translator(self) -> None:
        self._translator = BRFProductDefaultPricingTranslator()

    def build_adapter(self) -> None:
        self._adapter = ProductDefaultPricingAdapter(client=self._client, translator=self._translator)
