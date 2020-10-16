from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from menu_sun_api.domain.model.product.product_repository import ProductRepository
import pytest


class TestProductRepository(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABC')
        session.commit()
        return seller

    def test_should_retrieve_product(self, session, seller):
        repository = ProductRepository(session)
        ProductFactory.create(seller_id=seller.id, sku='A')
        ProductFactory.create(seller_id=seller.id, sku='B')
        session.commit()

        ls = list(repository.search_products(seller_id=seller.id))
        assert len(ls) == 2

    def test_should_load_product_with_sku_filter(self, session, seller):
        ProductFactory.create(seller_id=seller.id, sku='A')
        ProductFactory.create(seller_id=seller.id, sku='B')
        ProductFactory.create(seller_id=seller.id, sku='C')
        session.commit()
        repository = ProductRepository(session)
        ls = list(repository.search_products(seller_id=seller.id,
                                             skus=['A', 'C']))
        assert len(ls) == 2
        assert ls[0].sku == 'A'
        assert ls[1].sku == 'C'
