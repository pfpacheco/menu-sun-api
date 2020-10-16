from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform


class AbstractMetafieldPlatform(AbstractPlatform):
    namespace: str = None
    key: str = None
    value: str = None

