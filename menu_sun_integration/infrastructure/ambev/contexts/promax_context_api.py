import os
from typing import Optional

import requests

from menu_sun_integration.infrastructure.context.context_api import ContextAPI


class PromaxContextAPI(ContextAPI):
    def __init__(self):
        super().__init__(base_url=os.getenv("PROMAX_IP"))
        self.signed_hash: Optional[str] = None
        self.promax_password = os.getenv('PROMAX_PASSWORD')
        self.promax_user_id = os.getenv('PROMAX_USER_ID')
        self.url = f'https://{self.base_url}/ambev/genericRestEndpoint'

    def authentication(self) -> str:
        if self.signed_hash is None:
            url = f'https://{self.base_url}/ambev/security/ldap/authenticateUser'

            payload = {"packageInfo": {
                "header": {
                    "bodyType": "application/json",
                    "credentials": {
                        "userId": self.promax_user_id,
                        "password": self.promax_password,
                        "userType": 'PDV'
                    }
                }
            }
            }

            self._logger.info(key="promax_context_api", description=f'request_payload(url="{url}")',
                              payload=self._logger.dumps(payload))

            rs = requests.post(url=url, json=payload, verify=False)

            if rs.status_code != 200:
                self._logger.error(key="promax_context_api", description=f'response_payload_failed(url="{url}")',
                                   payload=rs.text)
                raise Exception(rs.text)

            data = rs.json()

            self._logger.info(key="promax_context_api", description=f'response_payload_succeeded(url="{url}")',
                              payload=self._logger.dumps(data))

            self.signed_hash = data['packageInfo']['header']['token']['signedHash']
        return self.signed_hash

    def __post(self, request):
        service_name = request.payload
        signed_hash = self.authentication()
        payload = {
            "packageInfo": {
                "header": {
                    "serviceName": service_name,
                    "credentials": {
                        "userId": request.document,
                        "userDataAttr": {
                            "unb": request.seller_code
                        }
                    },
                    "token": {
                        "signedHash": signed_hash
                    }
                }
            }
        }

        self._logger.info(key="promax_context_api", description=f'request_payload(url="{self.url}")',
                          payload=self._logger.dumps(payload))

        return requests.post(url=self.url, json=payload, verify=False, timeout=30)

    def do_post(self, request):
        return self.__post(request)

    def do_get(self, request):
        return self.__post(request)
