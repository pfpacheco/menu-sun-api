import abc

from menu_sun_integration.shared.loggers.logger import Logger


class AbstractContext(abc.ABC):
    _logger = Logger()

    def __init__(self, base_url: str):
        self.base_url = base_url



