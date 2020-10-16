from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder


class NotImplementedBuilder(AbstractBuilder):
    def create_session(self, session) -> None:
        pass

    def create_client(self) -> None:
        pass

    def get_adapter(self) -> AbstractAdapter:
        pass

    def define_translator(self) -> None:
        pass

    def build_adapter(self) -> None:
        pass
