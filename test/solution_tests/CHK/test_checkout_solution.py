from solutions.CHK.checkout_solution import checkout


class TestCheckout:

    def test_empty_basket(self):
        assert checkout("") == 0

    def test_one_goods(self):
        assert checkout("A") == 50

    def test_invalid_input(self):
        assert checkout("-") == -1

    def test_calculates_sum_correctly(self):
        assert checkout("ABCDACD") == 200

    def test_applies_discount(self):
        assert checkout("AAABB") == 175

    def test_applies_discount_to_correct_number_of_product(self):
        assert checkout("AAAAABBB") == 275

    def test_applies_bigger_discounts_before_smaller(self):
        assert checkout("AAAAAAAAA") == 380

    def test_without_discounted_items(self):
        assert checkout("EE") == 80

    def test_with_discounted_items(self):
        assert checkout("EEB") == 80

    def test_applies_cross_product_discount_first(self):
        assert checkout("EEBBBB") == 155

    def test_applies_group_discount_to_different_products(self):
        assert checkout("STXY") == 62

    def test_applies_group_discount_to_pricier_products_first(self):
        assert checkout("XYZZ") == 62

