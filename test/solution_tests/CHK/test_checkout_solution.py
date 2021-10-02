from solutions.CHK.checkout_solution import checkout


class TestCheckout:

    def test_empty_basket(self):
        assert checkout("") == 0

    def test_one_goods(self):
        assert checkout("A") == 50

    def test_unknown_goods(self):
        assert checkout("X") == -1

    def test_invalid_input(self):
        assert checkout("-") == -1

    def test_calculates_sum_correctly(self):
        assert checkout("ABCDACD") == 200

    def test_applies_discount(self):
        assert checkout("AAABB") == 175

    def test_applies_discount_to_correct_number_of_product(self):
        assert checkout("AAAAABBB") == 305
