import os
from datetime import datetime, timedelta

import json
from typing import Optional

import requests

from menu_sun_api.domain.model.seller.seller import SellerMetafield
from menu_sun_integration.infrastructure.context.context_api import ContextAPI


def get_value_or_default(value, default_value):
    if value is None:
        return default_value
    else:
        return value


def _filter_or_default(collection, filter) -> Optional[str]:
    for item in collection:
        if filter(item):
            return item.value
    return None


class PernodContextAPI(ContextAPI):
    date_format = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, seller_repository):
        super().__init__(base_url=os.getenv("PERNOD_API_URL"))
        self._client_id = os.getenv("PERNOD_CLIENT_ID")
        self._client_secret = os.getenv("PERNOD_CLIENT_SECRET")
        self._username = os.getenv("PERNOD_MENU_USERNAME")
        self._password = os.getenv("PERNOD_MENU_PASSWORD")
        self._seller_repository = seller_repository
        self._token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._expired_date_token: Optional[str] = None
        self._oauth_namespace = "OAUTH_TOKEN_AUTHENTICATION"

    def __bind_seller(self, seller_id):
        self._seller = self._seller_repository.get_by_id(seller_id)

    def __save_oauth_token(self, key: str, value: str):
        metafield = {"key": key, "value": value, "namespace": self._oauth_namespace}
        self._seller.change_metafield(SellerMetafield.from_dict(metafield))

    def __updated_oauth(self):
        self.__save_oauth_token(key="OAUTH_TOKEN", value=self._token)
        self.__save_oauth_token(key="OAUTH_REFRESH_TOKEN", value=self._refresh_token)
        self.__save_oauth_token(key="OAUTH_TOKEN_EXPIRATION_DATE", value=self._expired_date_token)
        self._seller_repository.session.commit()

    def __bind_oauth_token(self):

        self._token = _filter_or_default(
            self._seller.metafields,
            lambda metafield:
            metafield.namespace == self._oauth_namespace and metafield.key == "OAUTH_TOKEN")

        self._refresh_token = _filter_or_default(
            self._seller.metafields, lambda metafield:
            metafield.namespace == self._oauth_namespace and metafield.key == "OAUTH_REFRESH_TOKEN")

        self._expired_date_token = _filter_or_default(
            self._seller.metafields,
            lambda metafield:
            metafield.namespace == self._oauth_namespace and metafield.key == "OAUTH_TOKEN_EXPIRATION_DATE")

    def __generate_payload_for_authentication(self):
        payload_default = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "scope": "inventory orders catalog",
            "username": self._username,
            "password": self._password,
        }

        if self._token is None:
            payload_authentication = {
                "grant_type": "password",
            }
            return {**payload_default, **payload_authentication}
        else:
            payload_refresh_token = {
                "grant_type": "refresh_token",
                "refresh_token": get_value_or_default(self._refresh_token, "")
            }

            return {**payload_default, **payload_refresh_token}

    def __has_valid_token(self):
        if self._token is not None:
            now = datetime.now()
            expiration_date = datetime.strptime(get_value_or_default(self._expired_date_token,
                                                                     now.strftime(self.date_format)),
                                                self.date_format)

            return True if expiration_date > now else False
        else:
            return False

    def __bind_url(self, resource: str):
        token = self.authentication()
        self.url = f'https://{self.base_url}/{resource}?access_token={token}'

    def authentication(self) -> str:
        if not self.__has_valid_token():
            url = f'https://{self.base_url}/oauth2/login'
            payload = self.__generate_payload_for_authentication()

            self._logger.info(key="pernod_context_api", description=f'request_payload(url="{url}")',
                              payload=self._logger.dumps(payload))

            rs = requests.post(url=url, json=payload, verify=False)

            if rs.status_code != 200:
                self._logger.error(key="pernod_context_api", description=f'response_payload_failed(url="{url}")',
                                   payload=rs.text)
                raise Exception(rs.text)

            data = rs.json()

            self._logger.info(key="pernod_context_api", description=f'response_payload_succeeded(url="{url}")',
                              payload=self._logger.dumps(data))

            self._token = data['access_token']
            self._refresh_token = data['refresh_token']
            expires_in = data['expires_in']
            self._expired_date_token = \
                (datetime.now() + timedelta(seconds=expires_in)).strftime(self.date_format)

        return self._token

    def do_post(self, request):
        self.__bind_seller(request.seller_id)
        self.__bind_oauth_token()
        self.__bind_url(resource=request.resource)
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.loads(request.payload)
        self._logger.info(key="pernod_context_api_post", description=f'request_payload(url="{request.resource}")',
                          payload=payload)
        response = requests.post(url=self.url, json=payload, verify=False, headers=headers)
        self.__updated_oauth()
        return response

    def do_get(self, request):
        self.__bind_seller(request.seller_id)
        self.__bind_oauth_token()
        self.__bind_url(resource=request.resource)
        response = requests.get(url=self.url, verify=False)
        self.__updated_oauth()
        return response

    def do_put(self, request):
        self.__bind_seller(request.seller_id)
        self.__bind_oauth_token()
        self.__bind_url(resource=request.resource)
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.loads(request.payload)
        self._logger.info(key="pernod_context_api_post", description=f'request_payload(url="{request.resource}")',
                          payload=payload)
        response = requests.put(url=self.url, json=payload, verify=False, headers=headers)
        self.__updated_oauth()
        return response
