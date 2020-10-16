from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.brf.builders.brf_base_builder import BRFBaseBuilder
from menu_sun_integration.infrastructure.brf.translators.brf_order_translator import BRFOrderTranslator


class BRFOrderBuilder(BRFBaseBuilder):
    def define_translator(self) -> None:
        self._translator = BRFOrderTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderAdapter(client=self._client, translator=self._translator)

