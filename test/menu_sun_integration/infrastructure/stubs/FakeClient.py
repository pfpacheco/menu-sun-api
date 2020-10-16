from menu_sun_integration.application.clients.interfaces.abstract_order_client import AbstractOrderClient
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse


class FakeClient(AbstractOrderClient):
    def __init__(self):
        super().__init__()

    def post_order(self, entity: AbstractRequest) -> bool:
        return True

    def get_order(self, entity_id: int) -> AbstractResponse:
        pass
