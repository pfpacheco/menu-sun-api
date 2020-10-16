from factory import BUILD_STRATEGY, Sequence, SubFactory, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.customer.customer import PaymentTerms, PaymentType


class PaymentTermsFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = PaymentTerms
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    payment_type = PaymentType.BOLETO


class CustomerMetafieldFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = CustomerMetafield
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)


class CustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        strategy = BUILD_STRATEGY
        model = Customer
        sqlalchemy_session = Session

    id = Sequence(lambda n: n + 1)
    document = Sequence(lambda n: "document_%d" % n)

    @post_generation
    def payment_terms(self, create, extracted, **kwargs):

        if not create:
            # Build, not create related
            return

        if extracted:
            assert isinstance(extracted, int)
            PaymentTermsFactory.create_batch(
                size=extracted, customer_id=self.id, **kwargs)
        else:
            PaymentTermsFactory.create(customer_id=self.id,
                                       **kwargs)
