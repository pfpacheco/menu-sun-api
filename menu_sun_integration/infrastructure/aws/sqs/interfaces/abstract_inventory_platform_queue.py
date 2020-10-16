import abc

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.presentations.product.abstract_product_message_platform import AbstractProductMessagePlatform


class AbstractInventoryPlatformQueue(AbstractPlatformQueue):
    def __init__(self, url: str):
        super().__init__(url=url)

    @abc.abstractmethod
    def map_payload(self, payload) -> AbstractProductMessagePlatform:
        pass



