import graphene

from menu_sun_api.interfaces.mutation.customer.customer_create import CustomerCreateMutation
from menu_sun_api.interfaces.mutation.customer.customer_delete import CustomerDeleteMutation
from menu_sun_api.interfaces.mutation.customer.customer_update import CustomerUpdateMutation
from menu_sun_api.interfaces.mutation.order.change_order_status import ChangeOrderStatusMutation
from menu_sun_api.interfaces.mutation.order.order_create import OrderCreateMutation
from menu_sun_api.interfaces.mutation.order.order_approved import OrderApprovedMutation
from menu_sun_api.interfaces.mutation.order.order_canceled import OrderCanceledMutation
from menu_sun_api.interfaces.mutation.order.order_credit_menu import OrderCreditMenuMutation
from menu_sun_api.interfaces.mutation.order.order_delivered import OrderDeliveredMutation
from menu_sun_api.interfaces.mutation.order.order_invoiced import OrderInvoicedMutation
from menu_sun_api.interfaces.mutation.order.order_shipped import OrderShippedMutation
from menu_sun_api.interfaces.mutation.pricing.pricing_create import PricingCreateMutation
from menu_sun_api.interfaces.mutation.pricing.pricing_delete import PricingDeleteMutation
from menu_sun_api.interfaces.mutation.pricing.pricing_update import PricingUpdateMutation
from menu_sun_api.interfaces.mutation.product.product_create import ProductCreateMutation
from menu_sun_api.interfaces.mutation.product.product_delete import ProductDeleteMutation
from menu_sun_api.interfaces.mutation.product.product_update import ProductUpdateMutation
from menu_sun_api.interfaces.mutation.customer.customer_bulk_upsert import CustomerBulkCreateMutation
from menu_sun_api.interfaces.mutation.pricing.pricing_bulk_upsert import PricingBulkUpsertMutation
from menu_sun_api.interfaces.mutation.customer.metafield.customer_metafield_bulk_upsert import \
    CustomerMetafieldBulkUpsertMutation
from menu_sun_api.interfaces.mutation.customer.metafield.customer_metafield_bulk_delete import \
    CustomerMetafieldBulkDeleteMutation
from menu_sun_api.interfaces.mutation.customer.payment_terms.customer_payment_terms_bulk_upsert import \
    CustomerPaymentTermsBulkUpsertMutation
from menu_sun_api.interfaces.mutation.product.product_bulk_upsert import ProductBulkUpsertMutation


class Mutations(
        ProductCreateMutation,
        ProductUpdateMutation,
        ProductDeleteMutation,
        PricingUpdateMutation,
        PricingCreateMutation,
        PricingDeleteMutation,
        ProductBulkUpsertMutation,
        PricingBulkUpsertMutation,
        CustomerBulkCreateMutation,
        CustomerMetafieldBulkUpsertMutation,
        CustomerMetafieldBulkDeleteMutation,
        CustomerPaymentTermsBulkUpsertMutation,
        CustomerCreateMutation,
        CustomerUpdateMutation,
        CustomerDeleteMutation,
        OrderCreateMutation,
        OrderApprovedMutation,
        OrderCanceledMutation,
        OrderDeliveredMutation,
        OrderShippedMutation,
        OrderInvoicedMutation,
        OrderCreditMenuMutation,
        ChangeOrderStatusMutation,
        graphene.ObjectType):
    pass
