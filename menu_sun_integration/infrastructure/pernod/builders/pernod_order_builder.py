from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.pernod.builders.pernod_base_builder import PernodBaseBuilder
from menu_sun_integration.infrastructure.pernod.translators.pernod_order_translator import PernodOrderTranslator


class PernodOrderBuilder(PernodBaseBuilder):
    def create_session(self, session) -> None:
        pass

    def define_translator(self) -> None:
        self._translator = PernodOrderTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderAdapter(client=self._client, translator=self._translator)
