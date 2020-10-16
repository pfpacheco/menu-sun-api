from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform


class AbstractOrderItemPlatform(AbstractPlatform):
    name: str = None
    sku: str = None
    quantity: int = None
    price: float = None
    original_price: float = None


class AbstractOrderAddressPlatform(AbstractPlatform):
    name: str = None
    street: str = None
    number: int = None
    complement: str = None
    reference: str = None
    neighborhood: str = None
    state_code: str = None
    city: str = None
    country_code: str = None
    postcode: str = None
    shipping_provider: str = None
    shipping_service: str = None


class AbstractOrderCustomerPlatform(AbstractPlatform):
    name: str = None
    document: str = None
    phone_number: str = None
    email: str = None
    cep: str = None


class AbstractOrderStatusPlatform(AbstractPlatform):
    id: str = None
    status: str = None
    comments: str = None
    updated_date: str = None
    published_date: str = None


class AbstractOrderPlatform(AbstractPlatform):
    id: str = None
    integration_type: str = None
    order_id: str = None
    seller_order_id: str = None
    seller_id: str = None
    seller_code: str = None
    document: str = None
    order_date: str = None
    delivery_date: str = None
    payment_code: str = None
    total: float = None
    shipping: float = None
    discount: float = None
    subtotal: float = None
    items: [AbstractOrderItemPlatform] = None
    shipping_address: [AbstractOrderAddressPlatform] = None
    billing_address: [AbstractOrderAddressPlatform] = None
    customer: AbstractOrderCustomerPlatform = None
    statuses: [AbstractOrderStatusPlatform] = None
