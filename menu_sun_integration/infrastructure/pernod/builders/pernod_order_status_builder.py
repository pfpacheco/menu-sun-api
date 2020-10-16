from menu_sun_integration.application.adapters.order_status_adapter import OrderStatusAdapter
from menu_sun_integration.infrastructure.pernod.builders.pernod_base_builder import PernodBaseBuilder
from menu_sun_integration.infrastructure.pernod.translators.pernod_order_status_translator import \
    PernodOrderStatusTranslator


class PernodOrderStatusBuilder(PernodBaseBuilder):
    def define_translator(self) -> None:
        self._translator = PernodOrderStatusTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderStatusAdapter(client=self._client, translator=self._translator)
