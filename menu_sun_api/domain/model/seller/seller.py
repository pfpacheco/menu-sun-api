import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Enum

from menu_sun_api.domain import Base, Default
from menu_sun_api.shared.str_converters import hex_uuid
from menu_sun_api.domain.model.metafield.metafield import Metafield
from sqlalchemy.orm import relationship


class IntegrationType(enum.Enum):
    NOT_IMPLEMENTED = 0
    PROMAX = 1
    PERNOD = 2
    BRF = 3
    ARYZTA = 4
    BENJAMIN = 5


class SellerMetafield(Metafield, Base):
    __tablename__ = 'seller_metafield'
    seller_id = Column(Integer, ForeignKey('seller.id'), nullable=False)


class Seller(Default, Base):
    __tablename__ = 'seller'
    seller_code = Column(String(16), nullable=False, index=True)
    token = Column(String(32))
    uuid = Column(String(32), nullable=False, unique=True, default=hex_uuid)
    integration_type = Column(
        Enum(IntegrationType),
        nullable=False,
        server_default=IntegrationType.NOT_IMPLEMENTED.name)
    metafields = relationship(SellerMetafield)

    def change_metafield(self, input):
        self.updated_date = datetime.utcnow()
        for m in self.metafields:
            if (m.namespace == input.namespace) and (m.key == input.key):
                m.value = input.value
                return m

        self.metafields.append(input)
        return input

    def get_integration_type(self):
        return IntegrationType.NOT_IMPLEMENTED if self.integration_type is None else self.integration_type
