from menu_sun_integration.application.adapters.product_adapter import ProductAdapter
from menu_sun_integration.infrastructure.brf.builders.brf_base_builder import BRFBaseBuilder
from menu_sun_integration.infrastructure.brf.translators.brf_product_translator import BRFProductTranslator


class BRFProductBuilder(BRFBaseBuilder):
    def define_translator(self) -> None:
        self._translator = BRFProductTranslator()

    def build_adapter(self) -> None:
        self._adapter = ProductAdapter(client=self._client, translator=self._translator)
