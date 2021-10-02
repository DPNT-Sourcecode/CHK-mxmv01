from solutions.CHK.checkout_solution import checkout


class TestCheckout:

    def test_empty_basket(self):
        assert checkout("") == 0

    def test_one_goods(self):
        assert checkout("A") == 50

    def test_unknown_goods(self):
        assert checkout("x") == -1


