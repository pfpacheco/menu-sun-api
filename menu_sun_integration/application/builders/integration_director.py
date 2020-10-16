from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder


class IntegrationDirector:
    def __init__(self, builder: AbstractBuilder, session=None):
        self._builder = builder
        self._session = session

    def build_adapter(self) -> None:
        self._builder.create_session(self._session)
        self._builder.create_client()
        self._builder.define_translator()
        self._builder.build_adapter()

    def get_adapter(self) -> AbstractAdapter:
        return self._builder.get_adapter()
