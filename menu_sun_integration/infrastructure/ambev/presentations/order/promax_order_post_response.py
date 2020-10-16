from typing import Dict

from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_response import PromaxOrderResponse
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse
from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class PromaxOrderPostResponse(AbstractOrderPostResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

    def __check_if_order_was_already_integrated(self) -> bool:
        result = False
        try:
            cd_erro = self.payload['packageInfo']['body']['data']['response']['status'][0]['cdErro']
            result = (cd_erro == "3")
        except Exception:
            result = False
        finally:
            if result:
                self._logger.warn(
                    key="order_post_response",
                    description="order_already_integrated",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="order_post_response",
                    description="order_already_integrated_error",
                    payload=self._logger.dumps(self.payload))

        return result

    def __check_success(self):
        result = False
        try:
            has_order = self.payload['packageInfo']['body']['data']['response']['pedidoRealizado']
            result = (len(has_order) == 1)
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="order_post_response",
                    description="order_integrated",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="order_post_response",
                    description="order_not_integrated",
                    payload=self._logger.dumps(self.payload))

        return result

    @property
    def succeeded(self) -> bool:
        result = self.__check_success()
        if result:
            return result

        return self.__check_if_order_was_already_integrated()

    def get_order(self) -> [AbstractOrderResponse]:
        return PromaxOrderResponse()
