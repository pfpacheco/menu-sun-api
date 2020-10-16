import requests
import logging
import json

logger = logging.getLogger()


def log_info(payload):
    logger.info(json.dumps(payload))


class HttpPromax():

    def __init__(self, domain=None, signed_hash=None):
        self.signed_hash = signed_hash
        self.domain = domain

    def authenticate(self, user_id, password, type='PDV'):

        if not self.signed_hash:
            url = 'https://{}/ambev/security/ldap/authenticateUser'.format(
                self.domain)
            payload = {"packageInfo":
                       {
                           "header": {
                               "bodyType": "application/json",
                               "credentials": {
                                   "userId": user_id,
                                   "password": password,
                                   "userType": type
                               }
                           }
                       }
                       }

            log_info(payload=payload)
            rs = requests.post(url=url, json=payload, verify=False)
            if (rs.status_code != 200):
                logger.error(rs.text)
                raise Exception(rs.text)
            data = rs.json()
            log_info(payload=data)
            self.signed_hash = data['packageInfo']['header']['token']['signedHash']

        return self.signed_hash

    def __post(self, url, user_id, password, request_object):
        service_name = request_object.payload
        signed_hash = self.authenticate(user_id=user_id, password=password)
        payload = {
            "packageInfo": {
                "header": {
                    "serviceName": service_name,
                    "credentials": {
                        "userId": request_object.cnpj,
                        "userDataAttr": {
                            "unb": request_object.unb
                        }
                    },
                    "token": {
                        "signedHash": signed_hash
                    }
                }
            }
        }
        log_info(payload=payload)
        rs = requests.post(url=url, json=payload, verify=False)
        if (rs.status_code != 200):
            logger.error(rs.text)
            raise Exception(rs.text)
        data = rs.json()
        log_info(payload=data)
        return data

    def send_order(self, order_request, auth={}):
        url = "https://{}/ambev/genericRestEndpoint".format(self.domain)
        user_id = auth.get('user_id')
        password = auth.get('password')
        data = self.__post(url=url,
                           user_id=user_id,
                           password=password,
                           request_object=order_request)
        return data

    def get_order_history(self, order_history_request, auth={}):
        url = "https://{}/ambev/genericRestEndpoint".format(self.domain)
        user_id = auth.get('user_id')
        password = auth.get('password')
        data = self.__post(url=url,
                           user_id=user_id,
                           password=password,
                           request_object=order_history_request)
        return data

    def get_order_history_by_order_id(
            self, order_history_by_order_id_request, auth={}):
        url = "https://{}/ambev/genericRestEndpoint".format(self.domain)
        user_id = auth.get('user_id')
        password = auth.get('password')
        data = self.__post(url=url,
                           user_id=user_id,
                           password=password,
                           request_object=order_history_by_order_id_request)
        return data

    def get_order_details(self, order_details_request, auth={}):
        url = "https://{}/ambev/genericRestEndpoint".format(self.domain)
        user_id = auth.get('user_id')
        password = auth.get('password')
        data = self.__post(url=url,
                           user_id=user_id,
                           password=password,
                           request_object=order_details_request)
        return data
