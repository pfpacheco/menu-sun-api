
import datetime as datetime
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_integration.application.clients.interfaces.abstract_customer_client import AbstractCustomerClient
from menu_sun_integration.application.clients.interfaces.abstract_customer_pricing import AbstractCustomerPricingClient
from menu_sun_integration.application.clients.interfaces.abstract_inventories_client import AbstractInventoriesClient
from menu_sun_integration.application.clients.interfaces.abstract_post_order_client import AbstractPostOrderClient
from menu_sun_integration.application.clients.interfaces.abstract_product_client import AbstractProductClient
from menu_sun_integration.application.clients.interfaces.abstract_product_default_pricing_client import \
    AbstractProductDefaultPricingClient
from menu_sun_integration.application.repositories.interfaces.abstract_customer_repository import \
    AbstractCustomerRepository
from menu_sun_integration.application.repositories.interfaces.abstract_order_repository import AbstractOrderRepository
from menu_sun_integration.application.repositories.interfaces.abstract_pricing_repository import \
    AbstractPricingRepository
from menu_sun_integration.application.repositories.interfaces.abstract_product_repository import \
    AbstractProductRepository
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_detail_get_request import \
    BRFCustomerDetailGetRequest
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_detail_get_response import \
    BRFCustomerDetailGetResponse
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_post_request import \
    BRFCustomerPostRequest
from menu_sun_integration.infrastructure.brf.presentations.inventory.brf_inventory_get_request import \
    BRFInventoryGetRequest
from menu_sun_integration.infrastructure.brf.presentations.inventory.brf_inventory_get_response import \
    BRFInventoryGetResponse
from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_post_request import \
    BRFOrderPostRequest

from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_post_response import \
    BRFOrderPostResponse
from menu_sun_integration.infrastructure.brf.presentations.pricing.brf_pricing_detail_get_response import \
    BRFPricingDetailGetResponse
from menu_sun_integration.infrastructure.brf.presentations.pricing.customer.brf_customer_pricing_detail_get_request import \
    BRFCustomerPricingDetailGetRequest
from menu_sun_integration.infrastructure.brf.presentations.pricing.product.\
    brf_product_default_pricing_detail_get_request import BRFProductDefaultPricingDetailGetRequest
from menu_sun_integration.infrastructure.brf.presentations.product.brf_product_get_request import BRFProductGetRequest
from menu_sun_integration.infrastructure.brf.presentations.product.brf_product_get_response import BRFProductGetResponse
from datetime import datetime as datetime_str_pr_time
import dateutil.parser


class BRFClient(AbstractPostOrderClient, AbstractProductClient, AbstractCustomerClient, AbstractCustomerPricingClient,
                AbstractInventoriesClient, AbstractProductDefaultPricingClient):
    def __init__(self, customer_repository: AbstractCustomerRepository, product_repository: AbstractProductRepository,
                 pricing_repository: AbstractPricingRepository, order_repository: AbstractOrderRepository):
        super().__init__()
        self.customer_repository = customer_repository
        self.product_repository = product_repository
        self.pricing_repository = pricing_repository
        self.order_repository = order_repository

    @staticmethod
    def day_of_delivery_date_by_grade(grade, delivery_date):
        datetime_object = datetime_str_pr_time.strptime(delivery_date, '%Y-%m-%d  %H:%M:%S')
        date_list = [datetime_object + datetime.timedelta(days=x) for x in range(7)]
        weekday_name = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
        for date in date_list:
            for day in grade:
                if day.upper() == weekday_name[date.weekday()]:
                    return dateutil.parser.parse(str(date)).strftime('%Y-%m-%dT%H:%M:%S%Z')

    def post_order(self, request: BRFOrderPostRequest) -> BRFOrderPostResponse:
        request_customer = BRFCustomerDetailGetRequest(cnpj=request.customer.document,
                                                       postal_code=request.customer.postal_code)
        response_customer = self.get_customer(request_customer)

        customer = response_customer.get_customer() if response_customer.succeeded else None

        grade = customer.grade.split(",")
        delivery_date_sent = self.day_of_delivery_date_by_grade(grade=grade, delivery_date=request.delivery_date)

        if customer.active:
            payment_code = "0007"
            if customer.payment_code is not None:
                payment_code = customer.payment_code

            request_order = BRFOrderPostRequest(total=request.total,
                                                shipping=request.shipping,
                                                discount=request.discount,
                                                subtotal=request.subtotal,
                                                order_id=request.order_id,
                                                delivery_date=delivery_date_sent,
                                                order_date=request.order_date,
                                                unb=customer.cdd,
                                                payment_code=payment_code, items=request.items,
                                                shipping_address=request.shipping_address,
                                                billing_address=request.billing_address,
                                                customer=request.customer, status=request.status)

            data = self.order_repository.post(request_order)
            return BRFOrderPostResponse(customer=customer, payload=data)

    def get_customer(self, request: BRFCustomerDetailGetRequest) -> BRFCustomerDetailGetResponse:
        data = self.customer_repository.get(request)

        response = BRFCustomerDetailGetResponse(payload=data)
        if response.succeeded:
            customer_response = response.get_customer()
            if customer_response.is_new():
                customer_repository = CustomerRepository()
                customer = customer_repository.get_by_document_and_seller_integration(integration_type='BRF',
                                                                                      document=request.document)

                customer_request = BRFCustomerPostRequest(email=customer.email,
                                                          state_code=customer.uf,
                                                          postal_code=customer.cep,
                                                          document=request.document,
                                                          phone_number=customer.phone_number)
                self.post_customer(customer_request)
                data = self.customer_repository.post(customer_request)
                return BRFCustomerDetailGetResponse(payload=data)
            else:
                return response

    def post_customer(self, request: BRFCustomerPostRequest) -> BRFCustomerDetailGetResponse:
        data = self.customer_repository.post(request)
        return BRFCustomerDetailGetResponse(payload=data)

    def get_customer_pricing(self, request: BRFCustomerPricingDetailGetRequest) -> BRFPricingDetailGetResponse:
        data = self.pricing_repository.get_by_customer(request)
        return BRFPricingDetailGetResponse(payload=data)

    def get_products_default_pricing(self, request: BRFProductDefaultPricingDetailGetRequest) \
            -> BRFPricingDetailGetResponse:
        data = self.product_repository.get_prices(request)
        return BRFPricingDetailGetResponse(payload=data)

    def get_products(self, request: BRFProductGetRequest) -> BRFProductGetResponse:
        data = self.product_repository.get_all(request)
        return BRFProductGetResponse(payload=data)

    def get_inventories(self, request: BRFInventoryGetRequest) -> BRFInventoryGetResponse:
        data = self.product_repository.get_inventories(request)
        return BRFInventoryGetResponse(payload=data)
