from menu_sun_integration.application.clients.interfaces.abstract_inventory_by_sku_client import \
    AbstractInventoryBySkuClient
from menu_sun_integration.application.clients.interfaces.abstract_order_client import AbstractOrderClient
from menu_sun_integration.application.clients.interfaces.abstract_order_status_client import AbstractOrderStatusClient
from menu_sun_integration.application.clients.interfaces.abstract_product_client import AbstractProductClient
from menu_sun_integration.application.clients.interfaces.abstract_product_default_pricing_by_sku_client import \
    AbstractProductDefaultPricingBySkuClient
from menu_sun_integration.application.repositories.interfaces.abstract_order_repository import AbstractOrderRepository
from menu_sun_integration.application.repositories.interfaces.abstract_product_repository import \
    AbstractProductRepository
from menu_sun_integration.infrastructure.pernod.presentations.inventory.pernod_inventory_by_sku_post_request import \
    PernodInventoryBySkuPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.inventory.pernod_inventory_get_response import \
    PernodInventoryGetResponse
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_detail_get_request import \
    PernodOrderDetailGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_detail_get_response import \
    PernodOrderDetailGetResponse
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_request import \
    PernodOrderPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_response import \
    PernodOrderPostResponse
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_detail_put_response import \
    PernodOrderStatusDetailPutResponse
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_notification_get_request import \
    PernodOrderStatusNotificationGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_put_request import \
    PernodOrderStatusPutRequest
from menu_sun_integration.infrastructure.pernod.presentations.pricing.pernod_pricing_detail_get_response import \
    PernodPricingDetailGetResponse
from menu_sun_integration.infrastructure.pernod.presentations.pricing.product. \
    pernod_product_default_pricing_by_sku_post_request import PernodProductDefaultPricingBySkuPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.product.pernod_product_get_request import \
    PernodProductGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.product.pernod_product_get_response import \
    PernodProductGetResponse


class PernodClient(AbstractOrderClient, AbstractProductClient,
                   AbstractProductDefaultPricingBySkuClient,
                   AbstractInventoryBySkuClient, AbstractOrderStatusClient):

    def __init__(self, order_repository: AbstractOrderRepository, product_repository: AbstractProductRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def post_order(self, request: PernodOrderPostRequest) -> PernodOrderPostResponse:
        data = self.order_repository.post(request)
        return PernodOrderPostResponse(payload=data)

    def get_order(self, request: PernodOrderDetailGetRequest) -> PernodOrderDetailGetResponse:
        data = self.order_repository.get(request)
        return PernodOrderDetailGetResponse(payload=data)

    def get_products(self, request: PernodProductGetRequest) -> PernodProductGetResponse:
        data = self.product_repository.get_all(request)
        return PernodProductGetResponse(payload=data)

    def get_inventory(self, request: PernodInventoryBySkuPostRequest) -> PernodInventoryGetResponse:
        data = self.product_repository.get_inventory(request)
        return PernodInventoryGetResponse(payload=data)

    def get_price(self, request: PernodProductDefaultPricingBySkuPostRequest) -> PernodPricingDetailGetResponse:
        data = self.product_repository.get_price(request)
        return PernodPricingDetailGetResponse(payload=data)

    def get_order_status(self, request: PernodOrderStatusNotificationGetRequest) -> PernodOrderDetailGetResponse:
        data = self.order_repository.get_status(request)
        return PernodOrderDetailGetResponse(payload=data)

    def put_order_status(self, request: PernodOrderStatusPutRequest) -> PernodOrderStatusDetailPutResponse:
        data = self.order_repository.put_order_status(request)
        return PernodOrderStatusDetailPutResponse(payload=data, order_id=request.order_id, status_id=request.status_id)
