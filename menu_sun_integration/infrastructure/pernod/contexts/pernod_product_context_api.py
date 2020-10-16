import os
import requests
from typing import Dict

from menu_sun_integration.infrastructure.context.context_api import ContextAPI


class PernodProductContextAPI(ContextAPI):
    def __init__(self):
        super().__init__(base_url=os.getenv("PERNOD_PRODUCT_API_URL"))

    def __bind_url(self, resource: str, page: int = 1):
        limit = os.getenv("PERNOD_PRODUCT_API_PAGE_SIZE", 50)
        self.url = f'https://{self.base_url}/{resource}&offset={page}&limit={limit}'

    def __bind_url_post(self, resource: str):
        self.url = f'https://freight.hub2b.com.br/api/{resource}'

    def authentication(self) -> str:
        return os.getenv("PERNOD_PRODUCT_API_TOKEN")

    def do_post(self, request):
        headers = {'Content-Type': 'application/json'}
        self.__bind_url_post(resource=request.resource)
        payload = request.payload
        response = requests.post(url=self.url, headers=headers, data=payload, verify=False)
        return response

    def do_get(self, request):
        token = self.authentication()

        headers = {
            'Content-Type': 'application/json',
            'Auth': token,
        }
        result = {}
        products = []
        current_page = 1
        pages = 1

        while current_page <= pages:
            try:
                self.__bind_url(resource=request.payload, page=current_page)
                response = requests.get(url=self.url, headers=headers, verify=False)
                if response.status_code != 200:
                    raise Exception(response.text)

                response_in_json_format = response.json()

                self._logger.info(key='pernod_product_context_api',
                                  description="pernod_get_product_paging_response",
                                  payload=self._logger.dumps(response_in_json_format))

                products.extend(response_in_json_format['data']['list'])
                pages = response_in_json_format['data']['paging']['pages']
                current_page = response_in_json_format['data']['paging']['currentPage']
                current_page += 1

            except Exception as e:
                self._logger.error(key='pernod_product_context_api',
                                   description="pernod_get_product_error",
                                   payload=e)
                result.update({"error": str(e)})
                break

        result.update({"products": products})

        self._logger.info(key='pernod_product_context_api',
                          description="pernod_get_products_result_response",
                          payload=self._logger.dumps(products))

        return result

    def get(self, request) -> Dict:
        self._logger.info(key="pernod_product_context_api", description="request_payload", payload=request.payload)

        data = self.do_get(request)

        self._logger.info(key="pernod_product_context_api", description=f'response_payload_succeeded(url="{self.url}")',
                          payload=self._logger.dumps(data))

        return data
