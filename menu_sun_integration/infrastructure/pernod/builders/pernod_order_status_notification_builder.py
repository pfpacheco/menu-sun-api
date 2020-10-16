from menu_sun_integration.application.adapters.order_status_notification_adapter import OrderStatusNotificationAdapter
from menu_sun_integration.infrastructure.pernod.builders.pernod_base_builder import PernodBaseBuilder
from menu_sun_integration.infrastructure.pernod.translators.pernod_order_status_notification_translator import \
    PernodOrderStatusNotificationTranslator


class PernodOrderStatusNotificationBuilder(PernodBaseBuilder):
    def define_translator(self) -> None:
        self._translator = PernodOrderStatusNotificationTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderStatusNotificationAdapter(client=self._client, translator=self._translator)