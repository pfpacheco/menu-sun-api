from factory import BUILD_STRATEGY, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield, IntegrationType


class SellerMetafieldFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = SellerMetafield
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)


class SellerFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = Seller
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    seller_code = 'ABC'
    token = 'ABC'
    integration_type = IntegrationType.PROMAX

    @post_generation
    def metafields(self, create, extracted, **kwargs):

        if not create:
            # Build, not create related
            return

        if extracted:
            assert isinstance(extracted, int)
            SellerMetafieldFactory.create_batch(
                size=extracted, seller_id=self.id, **kwargs)
        else:
            SellerMetafieldFactory.create(
                seller_id=self.id,
                key="BOLETO_10",
                value="91",
                namespace="CODIGO_PAGAMENTO")
            SellerMetafieldFactory.create(
                seller_id=self.id,
                key="DINHEIRO",
                value="2",
                namespace="CODIGO_PAGAMENTO")
