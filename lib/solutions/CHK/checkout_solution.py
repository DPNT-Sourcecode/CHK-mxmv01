# noinspection PyUnusedLocal
# skus = unicode string
from enum import Enum, IntEnum

from typing import Generator


def checkout(skus: str):
    basket = Basket()
    for goods in parse_goods(skus):
        basket.add_item(goods)
    return basket.calculate_total()


class Goods(IntEnum):
    A = 50
    B = 30
    C = 20
    D = 15


def parse_goods(skus: str) -> Generator[Goods, None, None]:
    for sku in list(skus):
        yield Goods[sku]


class Basket:

    def __init__(self) -> None:
        self.items = {}

    def add_item(self, goods: Goods):
        count = self.items.get(goods)
        if count is None:
            count = 0
        count += 1
        self.items[goods] = count

    def calculate_total(self):
        total = 0
        for goods, count in self.items.items():
            total += goods.value * count
        return total




