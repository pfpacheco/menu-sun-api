from menu_sun_integration.application.adapters.product_default_pricing_adapter import ProductDefaultPricingAdapter

from menu_sun_integration.infrastructure.serbom.builders.benjamin_base_builder import BenjaminBaseBuilder
from menu_sun_integration.infrastructure.serbom.translators.serbom_product_default_pricing_translator import \
    SerbomProductDefaultPricingTranslator


class BenjaminProductDefaultPricingBuilder(BenjaminBaseBuilder):
    def define_translator(self) -> None:
        self._translator = SerbomProductDefaultPricingTranslator()

    def build_adapter(self) -> None:
        self._adapter = ProductDefaultPricingAdapter(client=self._client, translator=self._translator)
