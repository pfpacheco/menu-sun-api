from menu_sun_integration.application.adapters.product_adapter import ProductAdapter
from menu_sun_integration.infrastructure.serbom.builders.benjamin_base_builder import BenjaminBaseBuilder
from menu_sun_integration.infrastructure.serbom.translators.serbom_product_default_translator import \
    SerbomProductDefaultTranslator


class BenjaminProductBuilder(BenjaminBaseBuilder):
    def define_translator(self) -> None:
        self._translator = SerbomProductDefaultTranslator()

    def build_adapter(self) -> None:
        self._adapter = ProductAdapter(client=self._client, translator=self._translator)
