import os

from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest


class PernodProductGetRequest(AbstractProductGetRequest):
    def __init__(self):
        self.id_tenant = os.getenv("PERNOD_ID_TENANT")

    @property
    def payload(self):
        payload = f'listskus/{self.id_tenant}?filter=SalesChannel:112'

        return payload
