import json
import os

import requests

from menu_sun_integration.infrastructure.context.context_api import ContextAPI


class BRFContextAPI(ContextAPI):
    def __init__(self):
        super().__init__(base_url=os.getenv("BRF_API_URL"))

    def __bind_url(self, resource: str):
        self.url = f'https://{self.base_url}/{resource}'

    def authentication(self) -> str:
        return os.getenv("BRF_API_KEY")

    def do_post(self, request):
        api_key = self.authentication()
        payload = json.dumps(json.loads(request.payload))
        self.__bind_url(resource=request.resource)

        headers = {
            'Content-Type': 'application/json',
            'ApiKey': api_key,
        }

        self._logger.info(key="brf_context_api_post", description=f'request_payload(url="{request.resource}")',
                          payload=payload)

        return requests.request("POST", self.url, headers=headers, data=payload)

    def do_get(self, request):
        api_key = self.authentication()
        self.__bind_url(resource=request.payload)
        return requests.get(url=self.url, verify=False, headers={'ApiKey': api_key})
