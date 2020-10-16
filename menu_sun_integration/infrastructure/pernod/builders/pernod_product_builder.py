from menu_sun_integration.application.adapters.product_adapter import ProductAdapter
from menu_sun_integration.infrastructure.pernod.builders.pernod_base_builder import PernodBaseBuilder
from menu_sun_integration.infrastructure.pernod.translators.pernod_product_translator import PernodProductTranslator


class PernodProductBuilder(PernodBaseBuilder):
    def define_translator(self) -> None:
        self._translator = PernodProductTranslator()

    def build_adapter(self) -> None:
        self._adapter = ProductAdapter(client=self._client, translator=self._translator)
