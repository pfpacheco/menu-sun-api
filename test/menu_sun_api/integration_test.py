import pytest

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain import Base


class IntegrationTest(object):

    @pytest.yield_fixture(autouse=True)
    def session(self):
        Session.remove()
        session = Session()

        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
            session.commit()

        yield session
