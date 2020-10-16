from menu_sun_api.domain.model.product.product import Product
from factory import BUILD_STRATEGY, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from menu_sun_api.infrastructure.connection_factory import Session


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = Product
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    sku = Sequence(lambda n: "SKU_%d" % n)
