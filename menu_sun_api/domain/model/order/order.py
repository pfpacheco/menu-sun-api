import enum
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Float, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from menu_sun_api.domain import Base, Default
from sqlalchemy import UniqueConstraint
from menu_sun_api.domain.model.metafield.metafield import Metafield
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.domain.model.customer.customer import Customer


class OrderPaymentType(enum.Enum):
    BOLETO = 1
    CARTAO_CREDITO = 2
    DINHEIRO = 3


class Address(Default):
    street = Column(String(512))
    number = Column(Integer)
    complement = Column(String(64))
    reference = Column(String(512))
    neighborhood = Column(String(128))
    region = Column(String(128))
    state_code = Column(String(2))
    city = Column(String(128))
    country_code = Column(String(2))
    phone = Column(String(16))
    secondary_phone = Column(String(16))
    postcode = Column(String(16))
    name = Column(String(128))


class OrderBillingAddress(Address, Base):
    serialize_rules = ('-id', '-created_date', '-updated_date')
    __tablename__ = 'order_billing_address'


class OrderShippingAddress(Address, Base):
    serialize_rules = ('-id', '-created_date', '-updated_date')
    __tablename__ = 'order_shipping_address'


class OrderMetafield(Metafield, Base):
    __tablename__ = 'order_metafield'
    serialize_rules = ('-order_id', '-id', '-created_date', '-updated_date')
    order_id = Column(
        Integer,
        ForeignKey(
            'order.id',
            ondelete='CASCADE'),
        nullable=False)


class OrderItem(Default, Base):
    __tablename__ = "order_item"
    serialize_rules = ('-id', '-order_id', '-created_date', '-updated_date')
    order_id = Column(
        Integer,
        ForeignKey(
            'order.id',
            ondelete='CASCADE'),
        nullable=False)
    sku = Column(String(32), nullable=False)
    name = Column(String(256))
    ean = Column(String(16))
    ncm = Column(String(16))
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    quantity = Column(Integer)
    __table_args__ = (
        UniqueConstraint(
            'order_id',
            'sku',
            'quantity',
            name='_order_id_sku_quantity'),
    )


class OwnerType(enum.Enum):
    MENU = 1
    SELLER = 2

    @classmethod
    def get_value(cls, member):
        return cls.__get_values().get(member)

    @classmethod
    def __get_values(cls):
        return {
            'MENU': OwnerType.MENU,
            'SELLER': OwnerType.SELLER
        }


class OrderStatusType(enum.Enum):
    NEW = 1
    APPROVED = 2
    INVOICED = 3
    SHIPPED = 4
    DELIVERED = 5
    CANCELED = 6
    SHIPMENT_EXCEPTION = 7
    PAYMENT_OVERDUE = 8
    NEW_ORDER = 9
    SELLER_REVIEW = 10
    PROCESSING = 11
    ORDER_INVOICED = 12
    PENDING = 13
    CREDIT_MENU = 14
    CLOSED = 15
    PENDING_REVIEW = 16
    PENDING_INVOICE = 17
    ENTREGUE = 18
    COMPLETE = 19
    ORDER_REFUNDED = 20

    @classmethod
    def get_value(cls, member):
        return cls.__get_values().get(member)

    @classmethod
    def __get_values(cls):
        return {
            'NEW': OrderStatusType.NEW,
            'APPROVED': OrderStatusType.APPROVED,
            'INVOICED': OrderStatusType.INVOICED,
            'SHIPPED': OrderStatusType.SHIPPED,
            'DELIVERED': OrderStatusType.DELIVERED,
            'CANCELED': OrderStatusType.CANCELED,
            'SHIPMENT_EXCEPTION': OrderStatusType.SHIPMENT_EXCEPTION,
            'PAYMENT_OVERDUE': OrderStatusType.PAYMENT_OVERDUE,
            'NEW_ORDER': OrderStatusType.NEW_ORDER,
            'SELLER_REVIEW': OrderStatusType.SELLER_REVIEW,
            'PROCESSING': OrderStatusType.PROCESSING,
            'ORDER_INVOICED': OrderStatusType.ORDER_INVOICED,
            'PENDING': OrderStatusType.PENDING,
            'CREDIT_MENU': OrderStatusType.CREDIT_MENU,
            'CLOSED': OrderStatusType.CLOSED,
            'PENDING_REVIEW': OrderStatusType.PENDING_REVIEW,
            'PENDING_INVOICE': OrderStatusType.PENDING_INVOICE,
            'ENTREGUE': OrderStatusType.ENTREGUE,
            'COMPLETE': OrderStatusType.COMPLETE,
            'ORDER_REFUNDED': OrderStatusType.ORDER_REFUNDED
        }


class OrderStatus(Default, Base):
    __tablename__ = "order_status"
    serialize_rules = ('-id', '-order_id', '-created_date', '-updated_date')
    order_id = Column(
        Integer,
        ForeignKey(
            'order.id',
            ondelete='CASCADE'),
        nullable=False)
    status = Column(Enum(OrderStatusType), nullable=False)
    owner = Column(Enum(OwnerType), default=OwnerType.SELLER)
    comments = Column(String(512))
    published_date = Column(DateTime)

    def set_as_published(self):
        from datetime import datetime
        self.published_date = datetime.utcnow()


class OrderPayment(Default, Base):
    __tablename__ = "order_payment"
    serialize_rules = ('-id', '-order_id', '-created_date', '-updated_date')
    deadline = Column(Integer)
    payment_type = Column(Enum(OrderPaymentType))
    order_id = Column(
        Integer,
        ForeignKey(
            'order.id',
            ondelete='CASCADE'),
        nullable=False)


class Order(Default, Base):
    __tablename__ = 'order'
    serialize_rules = ('-seller_id', '-seller', '-customer_id', '-shipping_address_id', '-billing_address_id', '-id',
                       '-uuid')

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship(Customer, lazy='joined', uselist=False)
    shipping_address_id = Column(Integer, ForeignKey(
        'order_shipping_address.id'), nullable=False)
    shipping_address = relationship(
        "OrderShippingAddress",
        lazy='joined',
        uselist=False)
    billing_address_id = Column(
        Integer, ForeignKey('order_billing_address.id'))
    billing_address = relationship(
        "OrderBillingAddress",
        lazy='joined',
        uselist=False)

    payments = relationship(OrderPayment, lazy='joined', passive_deletes=True)
    items = relationship(OrderItem, lazy='joined', passive_deletes=True)
    statuses = relationship(
        "OrderStatus",
        order_by="asc(OrderStatus.created_date)",
        passive_deletes=True)
    seller_id = Column(Integer, ForeignKey('seller.id'), nullable=False)
    seller = relationship(Seller, lazy='joined', uselist=False)
    order_id = Column(String(32), nullable=False)
    seller_order_id = Column(String(32))
    integration_date = Column(DateTime)
    order_queue_date = Column(DateTime)
    order_date = Column(DateTime, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    subtotal = Column(Float, nullable=False)
    shipping = Column(Float, nullable=False)
    discount = Column(Float)
    commissioned = Column(Boolean, nullable=False, default=False)
    total = Column(Float, nullable=False)  # subtotal + shipping
    metafields = relationship(
        OrderMetafield,
        lazy='joined',
        passive_deletes=True)
    __table_args__ = (
        UniqueConstraint(
            'seller_id',
            'order_id',
            name='_seller_id_order_id'),
    )

    @property
    def status(self):
        index = len(self.statuses) - 1
        if index >= 0:
            return self.statuses[index]
        return None

    def on_wms(self):
        terminal_status = [OrderStatusType.DELIVERED, OrderStatusType.CANCELED]
        status = self.status.status
        return (self.integration_date is not None) and (status not in terminal_status)

    def delivery(self, owner=OwnerType.SELLER):
        if self.status.status != OrderStatusType.DELIVERED:
            order_status = OrderStatus(status=OrderStatusType.DELIVERED, owner=owner)
            self.statuses.append(order_status)

    def invoice(self, owner=OwnerType.SELLER):
        if self.status.status != OrderStatusType.INVOICED:
            order_status = OrderStatus(status=OrderStatusType.INVOICED, owner=owner)
            self.statuses.append(order_status)

    def approve(self, owner=OwnerType.SELLER):
        if (self.status.status != OrderStatusType.APPROVED) and (
                self.status.status == OrderStatusType.NEW):
            order_status = OrderStatus(status=OrderStatusType.APPROVED, owner=owner)
            self.statuses.append(order_status)

    def ship(self, owner=OwnerType.SELLER):
        if self.status.status != OrderStatusType.SHIPPED:
            order_status = OrderStatus(status=OrderStatusType.SHIPPED, owner=owner)
            self.statuses.append(order_status)

    def credit_menu(self):
        if self.status.status != OrderStatusType.CREDIT_MENU:
            order_status = OrderStatus(status=OrderStatusType.CREDIT_MENU, owner=OwnerType.MENU)
            self.statuses.append(order_status)

    def list_unpublished_statuses(self):
        ls = []
        for status in self.statuses:
            if status.published_date is None:
                ls.append(status)
        return ls

    def cancel(self, owner=OwnerType.SELLER, comments=""):
        if self.status != OrderStatusType.CANCELED:
            order_status = OrderStatus(status=OrderStatusType.CANCELED, owner=owner)
            if comments is not '':
                order_status_description = OrderStatus(
                    comments=comments, status=OrderStatusType.CANCELED, owner=owner)
                self.statuses.append(order_status_description)
            else:
                self.statuses.append(order_status)

    def link_seller_order_id(self, seller_order_id):
        self.seller_order_id = seller_order_id

    def change_metafield(self, input):
        self.updated_date = datetime.utcnow()
        for m in self.metafields:
            if (m.namespace == input.namespace) and (m.key == input.key):
                m.value = input.value
                return m

        self.metafields.append(input)
        return input

    def change_status(self, input):
        for m in self.statuses:
            if m.status == input.status:
                return

        self.statuses.append(input)
        return input

    def published_status(self, input):
        for m in self.statuses:
            if m.id == input.id:
                m.published_date = input.published_date
                m.comments = input.comments
                return m
        return input
