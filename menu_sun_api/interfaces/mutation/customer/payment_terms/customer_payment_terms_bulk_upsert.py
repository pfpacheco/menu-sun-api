import graphene

from menu_sun_api.interfaces.definition.customer import PaymentTerms as PaymentTermsDefinition
from menu_sun_api.interfaces.definition.failure_message import FailureMessage
from menu_sun_api.interfaces.mutation.customer.customer_input import CustomerInput

from menu_sun_api.interfaces.mutation.customer.customer_input import PaymentTermsInput
from menu_sun_api.interfaces.mapper import MapInputToCommand
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.customer.payment_terms.customer_payment_terms_bulk_upsert_command import CustomerPaymentTermsBulkUpsertCommand, \
    CustomerPaymentTermsdBulkUpsertCommandHandler


class CustomerPaymentTermsBulkUpsert(graphene.Mutation):
    class Arguments:
        payment_terms = graphene.List(PaymentTermsInput, required=True)

    payment_terms = graphene.List(PaymentTermsDefinition)
    failure_message = graphene.Field(FailureMessage)

    def mutate(parent, info, payment_terms, **args):
        session = Session()
        seller = info.context.get('seller')
        customer_repository = CustomerRepository(session)
        from_input = MapInputToCommand()
        payment_terms_list = [i.accept(from_input) for i in payment_terms]

        command = CustomerPaymentTermsBulkUpsertCommand(payment_terms=payment_terms_list,
                                                        seller_id=seller.id)

        handler = CustomerPaymentTermsdBulkUpsertCommandHandler(
            customer_repository=customer_repository,
            session=session)
        rs = handler.execute(command)
        if (rs):
            return CustomerPaymentTermsBulkUpsert(payment_terms=rs.value,
                                                  failure_message=None)
        else:
            return CustomerPaymentTermsBulkUpsert(payment_terms=[],
                                                  failure_message=rs)


class CustomerPaymentTermsBulkUpsertMutation(graphene.ObjectType):
    customer_payment_terms_bulk_upsert = CustomerPaymentTermsBulkUpsert.Field()
