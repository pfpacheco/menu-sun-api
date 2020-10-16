import abc
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.presentations.interfaces.abstract_order_status_message_platform import \
    AbstractOrderStatusMessagePlatform


class AbstractOrderStatusPlatformQueue(AbstractPlatformQueue):
    def __init__(self, url: str):
        super().__init__(url=url)

    @abc.abstractmethod
    def map_payload(self, payload) -> AbstractOrderStatusMessagePlatform:
        pass
