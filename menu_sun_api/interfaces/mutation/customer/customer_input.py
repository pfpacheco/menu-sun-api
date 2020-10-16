import graphene

from menu_sun_api.interfaces.mutation.sqlalchemy_input_object_type import SQLAlchemyInputObjectType
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield, PaymentTerms, PaymentType
from menu_sun_api.interfaces.mutation.sqlalchemy_input_object_type import SQLAlchemyInputObjectType


class CustomerMetafieldInput(SQLAlchemyInputObjectType):
    class Meta:
        model = CustomerMetafield
        exclude_fields = ('customer_id',
                          'created_date',
                          'updated_date',
                          'id',
                          'value'
                          )

    document = graphene.String(required=True)
    value = graphene.String(required=True)


class PaymentTypeInput(graphene.Enum):
    BOLETO = 1
    CARTAO_CREDITO = 2
    DINHEIRO = 3
    CHEQUE = 4


class PaymentTermsInput(SQLAlchemyInputObjectType):
    class Meta:
        model = PaymentTerms
        exclude_fields = ('customer_id',
                          'id',
                          'created_date',
                          'payment_type',
                          'updated_date'
                          )

    document = graphene.String(required=True)
    payment_type = PaymentTypeInput(required=True)


class CustomerInput(SQLAlchemyInputObjectType):
    class Meta:
        model = Customer
        exclude_fields = ('id', 'metafields',
                          'created_date',
                          'seller_id',
                          'uuid',
                          'updated_date',
                          'payment_terms',
                          )

    # payment_terms = graphene.List(PaymentTermsInput)
