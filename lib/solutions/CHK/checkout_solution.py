

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str):
    basket = {}
    for sku in list(skus):
        count = basket.get(sku)

    print(skus)
    return 0


class Basket:

    def __init__(self) -> None:
        super().__init__()

