import logging

import graphene
from menu_sun_api.interfaces.mutations import Mutations
from menu_sun_api.interfaces.queries import Query

log = logging.getLogger()
log.setLevel(logging.WARN)


class GraphqlEntryPoint(object):
    def __init__(self):
        self.schema = graphene.Schema(query=Query,
                                      #        ProductCatalogItem,
                                      #        Category,
                                      #        POS,
                                      #        ControlType,
                                      #        ControlIdentifier,
                                      #        InventoryPosting,
                                      #        ControlMethod,
                                      #        PaymentMethod,
                                      #        BrandPaymentMethod,
                                      #        CompanyAddress
                                      #        ],
                                      mutation=Mutations
                                      )

    def execute(self, query, seller, variables=None):
        # try:
        context = {
            'seller': seller
            # 'data_loaders': DataLoaders()
        }
        #

        # TableVersionNotification.bind_tables()

        result = self.schema.execute(query,
                                     variables=variables,
                                     context=context)
        #
        # if environment == 'TEST':
        #     return result
        return result

    def print_schema(self):
        print(self.schema)

    def schema(self):
        return self.schema


if __name__ == "__main__":
    entry_point = GraphqlEntryPoint()
    entry_point.print_schema()
