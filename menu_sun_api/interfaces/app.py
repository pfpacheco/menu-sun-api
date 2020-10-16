from flask import Flask
from flask_graphql import GraphQLView

from menu_sun_api.interfaces.error_formatter import ErrorFormatter
from menu_sun_api.interfaces.graphql_entrypoint import GraphqlEntryPoint
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller import IntegrationType

print(__name__)
app = Flask(__name__)
app.debug = True


class SellerMock:
    def __init__(self, seller_id, seller_code, integration_type):
        self.id = seller_id
        self.seller_code = seller_code
        self.integration_type = integration_type


seller = SellerMock(1, 'ABC', IntegrationType.PROMAX)


class SafeGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        err = ErrorFormatter()
        return err.format_error(error)


app.add_url_rule(
    '/graphql',
    view_func=SafeGraphQLView.as_view(
        'graphql',
        schema=GraphqlEntryPoint().schema,
        get_context=lambda: {'seller': seller},
        graphiql=True  # for having the GraphiQL interface
    )
)

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

if __name__ == '__main__':
    session = Session()
    app.run()
