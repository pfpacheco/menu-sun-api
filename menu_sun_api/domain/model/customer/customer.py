import enum

from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, Float, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from menu_sun_api.domain import Base, Default
from menu_sun_api.shared.str_converters import hex_uuid
from menu_sun_api.domain.model.metafield.metafield import Metafield
from datetime import datetime


class PaymentType(enum.Enum):
    BOLETO = 1
    CARTAO_CREDITO = 2
    DINHEIRO = 3
    CHEQUE = 4

    @classmethod
    def get_value(cls, member):
        return cls.__get_values().get(member)

    @classmethod
    def __get_values(cls):
        return {
            'BOLETO': PaymentType.BOLETO,
            'CARTAO_CREDITO': PaymentType.CARTAO_CREDITO,
            'DINHEIRO': PaymentType.DINHEIRO,
            'CHEQUE': PaymentType.CHEQUE
        }


class PaymentTerms(Default, Base):
    __tablename__ = 'payment_terms'
    serialize_rules = ('-id', '-customer_id', '-created_date', '-updated_date')
    deadline = Column(Integer)
    payment_type = Column(Enum(PaymentType))
    description = Column(String(512))
    customer_id = Column(Integer, ForeignKey('customer.id'))

    @classmethod
    def from_dict(cls, source):
        obj = cls()
        for key, value in source.items():
            if hasattr(obj, key):
                if key == 'payment_type':
                    obj.payment_type = PaymentType(value)
                else:
                    setattr(obj, key, value)
        return obj


class CustomerMetafield(Metafield, Base):
    __tablename__ = 'customer_metafield'
    serialize_rules = ('-seller_id', '-created_date', '-updated_date')
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)


class Customer(Default, Base):
    __tablename__ = 'customer'
    serialize_rules = ('-id', '-customer_id', '-created_date', '-updated_date')
    seller_id = Column(Integer, ForeignKey('seller.id'), nullable=False)
    document = Column(String(16), nullable=False, index=True)
    uuid = Column(String(32), nullable=False, unique=True, default=hex_uuid)
    payment_terms = relationship("PaymentTerms", lazy='joined')
    metafields = relationship(CustomerMetafield)
    name = Column(String(512))
    credit_limit = Column(Float)
    email = Column(String(256))
    phone_number = Column(String(32))
    uf = Column(String(2))
    cep = Column(String(9))
    active = Column(Boolean, default=True, nullable=True)

    __table_args__ = (UniqueConstraint('seller_id', 'document', name='_seller_id_document'),)

    def __search_metafield(self, key):
        for metafield in self.metafields:
            if metafield.key == key:
                return metafield
        return None

    def update_metafields(self, metafields_input):

        for metafield_input in metafields_input:
            rs = self.__search_metafield(metafield_input.key)
            if rs:
                rs.value = metafield_input.value
            else:
                self.metafields.append(metafield_input)

    def change_metafield(self, input):
        self.updated_date = datetime.utcnow()
        for m in self.metafields:
            if (m.namespace == input.namespace) and (m.key == input.key):
                m.value = input.value
                return m

        self.metafields.append(input)
        return input

    def change_payment_terms(self, input):
        self.updated_date = datetime.utcnow()
        for p in self.payment_terms:
            if p.payment_type == input.payment_type:
                p.deadline = input.deadline
                p.description = input.description
                return p

        self.payment_terms.append(input)

        return input
