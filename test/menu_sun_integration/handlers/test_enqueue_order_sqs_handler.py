import datetime as datetime_sent_order
from datetime import datetime, timedelta
from menu_sun_api.domain.model.customer.customer import Customer, PaymentType, CustomerMetafield
from test.menu_sun_api.db.customer_factory import CustomerFactory
from menu_sun_api.domain.model.order.order import OrderStatusType, OrderMetafield, OrderPayment, OrderPaymentType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.order_platform_service import OrderPlatformService
from menu_sun_integration.infrastructure.aws.sqs.order_sqs_queue import OrderSQSQueue
from test.menu_sun_api.db.order_factory import OrderStatusFactory, OrderFactory, OrderPaymentFactory
from test.menu_sun_api.db.seller_factory import SellerFactory, SellerMetafieldFactory
from test.menu_sun_api.integration_test import IntegrationTest
from mock import patch
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_pernod_mock import mock_queue_make_api_call


def build_seller(session, integration_type: IntegrationType):
    seller = SellerFactory.create(integration_type=integration_type.name)
    session.commit()
    return seller


class TestEnqueueOrderService(IntegrationTest):

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_promax_message(self, session):
        seller = build_seller(session, IntegrationType.PROMAX)

        customer = Customer(document="10851803792", seller_id=seller.id)
        session.commit()

        OrderFactory.create(seller_id=seller.id,
                            order_id='PR2',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW,
                                                         published_date=datetime_sent_order.datetime.now(),
                                                         created_date=datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.APPROVED,
                                                         published_date=datetime_sent_order.datetime.now(),
                                                         created_date=datetime.now() + timedelta(seconds=3))]
                            )

        OrderFactory.create(seller_id=seller.id,
                            order_id='PR3',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                      OrderStatusFactory(status=OrderStatusType.APPROVED)],
                            order_queue_date=datetime_sent_order.datetime.now()
                            )

        session.commit()

        order_queue = OrderSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")
        order_repository = OrderRepository(session)
        order_platform_service = OrderPlatformService(session=session, order_repository=order_repository,
                                                      platform_service=order_queue)

        result = order_platform_service.enqueue(seller=seller)

        assert (len(result.value) == 1)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_pernod_message(self, session):
        seller = build_seller(session, IntegrationType.PERNOD)

        customer = Customer(document="10851803792", seller_id=seller.id)
        session.commit()

        OrderFactory.create(seller_id=seller.id,
                            order_id='P2',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW, created_date=datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.PENDING,
                                                         created_date=datetime.now() + timedelta(seconds=3))]
                            )

        order = OrderFactory.create(seller_id=seller.id,
                                    order_id='P3',
                                    customer=customer,
                                    statuses=[OrderStatusFactory(status=OrderStatusType.APPROVED)],
                                    order_queue_date=datetime_sent_order.datetime.now(),
                                    metafields=[OrderMetafield(key="DELIVERY_PROVIDER",
                                                               value="CORREIOS",
                                                               namespace="INTEGRATION_API_FIELD"),
                                                OrderMetafield(key="DELIVERY_SERVICE",
                                                               value="PAC",
                                                               namespace="INTEGRATION_API_FIELD")
                                                ]
                                    )
        order.payments.append(OrderPayment(payment_type=OrderPaymentType.BOLETO, deadline=12))
        session.commit()

        queue = OrderSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")
        platform_service = OrderPlatformService(session=session, order_repository=OrderRepository(session),
                                                platform_service=queue)

        result = platform_service.enqueue(seller=seller)

        assert (len(result.value) == 1)

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_should_enqueue_brf_message(self, session):
        seller = build_seller(session, IntegrationType.BRF)

        customer_metafield = CustomerMetafield(
            namespace="GRADE", key="GRADE", value="TER;QUA;SAB")

        SellerMetafieldFactory.create(
            seller_id=seller.id,
            key="BOLETO_7",
            value="7",
            namespace="CODIGO_PAGAMENTO")

        customer = CustomerFactory.create(seller_id=seller.id,
                                          document='10851803792',
                                          cep='0000000',
                                          payment_terms__deadline=7,
                                          payment_terms__payment_type=PaymentType.BOLETO,
                                          metafields=[customer_metafield])

        session.commit()

        OrderFactory.create(seller_id=seller.id,
                            order_id='BRF2',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW,
                                                         published_date=datetime_sent_order.datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.SELLER_REVIEW)]
                            )

        OrderFactory.create(seller_id=seller.id,
                            order_id='BRF3',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW, created_date=datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.SELLER_REVIEW,
                                                         created_date=datetime.now() + timedelta(seconds=3)),
                                      OrderStatusFactory(status=OrderStatusType.CREDIT_MENU,
                                                         created_date=datetime.now() + timedelta(seconds=6)
                                                         )]
                            )

        OrderFactory.create(seller_id=seller.id,
                            order_id='BRF4',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW, created_date=datetime.now())]
                            )

        OrderFactory.create(seller_id=seller.id,
                            order_id='BRF5',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW, created_date=datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.SELLER_REVIEW,
                                                         created_date=datetime.now() + timedelta(seconds=3))],
                            order_queue_date=datetime_sent_order.datetime.now()
                            )

        OrderFactory.create(seller_id=seller.id,
                            order_id='BRF6',
                            customer=customer,
                            statuses=[OrderStatusFactory(status=OrderStatusType.NEW, created_date=datetime.now()),
                                      OrderStatusFactory(status=OrderStatusType.SELLER_REVIEW,
                                                         created_date=datetime.now() + timedelta(seconds=3)),
                                      OrderStatusFactory(status=OrderStatusType.CREDIT_MENU,
                                                         created_date=datetime.now() + timedelta(seconds=6))],
                            order_queue_date=datetime_sent_order.datetime.now()
                            )

        session.commit()

        queue = OrderSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")
        platform_service = OrderPlatformService(session=session, order_repository=OrderRepository(session),
                                                platform_service=queue)

        result = platform_service.enqueue(seller=seller)

        assert (len(result.value) == 2)
