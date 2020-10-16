from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.serbom.builders.benjamin_base_builder import BenjaminBaseBuilder
from menu_sun_integration.infrastructure.serbom.translators.benjamin_order_translator import BenjaminOrderTranslator


class BenjaminOrderBuilder(BenjaminBaseBuilder):
    def create_session(self, session) -> None:
        pass

    def define_translator(self) -> None:
        self._translator = BenjaminOrderTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderAdapter(client=self._client, translator=self._translator)
