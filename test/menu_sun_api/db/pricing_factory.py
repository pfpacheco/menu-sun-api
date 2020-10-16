from factory import BUILD_STRATEGY, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.pricing.pricing import Pricing


class PricingFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = Pricing
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    sale_price = 10
    list_price = 12
