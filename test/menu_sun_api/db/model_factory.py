# from factory import BUILD_STRATEGY, Sequence
# from factory.alchemy import SQLAlchemyModelFactory
# from faker import Faker
# from menu_sun_api.domain.model.order.order import Order, OrderShippingAddress
#
# from menu_sun_api.domain.model.product.product import Product
# from menu_sun_api.domain.model.pricing.pricing import Pricing
# from menu_sun_api.domain.model.customer.customer import PaymentTerms, PaymentType
# from menu_sun_api.infrastructure.connection_factory import Session
# from menu_sun_api.domain.model.metafield.metafield import Metafield
#
# fake = Faker()
#
#
#
# class PaymentTermsFactory(SQLAlchemyModelFactory):
#     class Meta:
#         strategy = BUILD_STRATEGY
#         model = PaymentTerms
#         sqlalchemy_session = Session
#
#     id = Sequence(lambda n: n + 1)
#     payment_type = PaymentType.BOLETO
#
#
#
#
# class PricingFactory(SQLAlchemyModelFactory):
#     class Meta:
#         strategy = BUILD_STRATEGY
#         model = Pricing
#         sqlalchemy_session = Session
#
#     id = Sequence(lambda n: n + 1)
#     sale_price = 10
#     list_price = 12
#
