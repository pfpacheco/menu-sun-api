import abc
import os

from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_post_context import AbstractGetPostContext


class ContextAPI(AbstractGetPostContext):
    url: str

    @abc.abstractmethod
    def authentication(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def do_post(self, request):
        raise NotImplemented

    @abc.abstractmethod
    def do_get(self, request):
        raise NotImplemented

    def do_put(self, request):
        raise NotImplemented

    def parser(self, response):
        return response.json()

    def post(self, request) -> Dict:
        payload = request.payload

        self._logger.info(key="context_api_post", description=f'request_payload(url="{request.resource}")',
                          payload=self._logger.dumps(payload))

        response = self.do_post(request)

        if response.status_code not in [200, 201]:
            self._logger.error(key="context_api_post", description=f'response_payload_failed(url="{self.url}")',
                               payload=f'{response.text} -- status_code: {response.status_code}')
            raise Exception(f'{response.text} -- {response.status_code}')

        data = self.parser(response)

        self._logger.info(key="context_api_post", description=f'response_payload_succeeded(url="{self.url}")',
                          payload=self._logger.dumps(data))

        return data

    def get(self, request) -> Dict:
        self._logger.info(key="context_api_get", description="request_payload", payload=request.payload)

        response = self.do_get(request)
        if response.status_code != 200:
            self._logger.error(key="context_api_get", description=f'response_payload_failed(url="{self.url}")',
                               payload=f'{response.text} -- status_code: {response.status_code}')
            raise Exception(f'{response.text} -- {response.status_code}')

        data = self.parser(response)

        self._logger.info(key="context_api_get", description=f'response_payload_succeeded(url="{self.url}")',
                          payload=self._logger.dumps(data))

        return data

    def put(self, request) -> Dict:
        self._logger.info(key="context_api_get", description="request_payload", payload=request.payload)

        response = self.do_put(request)
        if response.status_code != 200:
            self._logger.error(key="context_api_put", description=f'response_payload_failed(url="{self.url}")',
                               payload=f'{response.text} -- status_code: {response.status_code}')
            raise Exception(f'{response.text} -- {response.status_code}')

        data = self.parser(response)

        self._logger.info(key="context_api_get", description=f'response_payload_succeeded(url="{self.url}")',
                          payload=self._logger.dumps(data))
        return data
