# noinspection PyUnusedLocal
# skus = unicode string
from enum import Enum


def checkout(skus: str):
    basket = {}
    for sku in list(skus):
        count = basket.get(sku)

    print(skus)
    return 0


class Good(str):
    pass

class Basket:

    def __init__(self) -> None:
        self.items = {}

    def add_item(self, good: Good):
        count = self.items.get(good)
        if count is None:
            count = 0
        count += 1
        self.items[good] = count

