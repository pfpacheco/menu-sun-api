from menu_sun_api.domain.model.product.product import Product as ProductDomain


class TestMapper():

    def test_mapping_domain_to_domain(self):
        target = ProductDomain(description="DESC", name="P1")
        target.update(ProductDomain(description="DESC2"))
        assert (target.description == "DESC2")
        assert (target.name == "P1")

    def test_mapping_domain_to_domain_with_null_value(self):
        target = ProductDomain(description="DESC", name="P1")
        source = ProductDomain(description="DESC2", name=None)
        target.update(source)
        assert (target.description == "DESC2")
        assert (target.name is None)
