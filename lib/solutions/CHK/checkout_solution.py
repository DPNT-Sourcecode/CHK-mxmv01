# noinspection PyUnusedLocal
# skus = unicode string
from enum import IntEnum

from typing import Generator


def checkout(skus: str):
    basket = Basket()
    try:
        for product in parse_products(skus):
            basket.add_item(product)
    except UnknownProductException:
        return -1
    return basket.calculate_total()


class Product(IntEnum):
    A = 50
    B = 30
    C = 20
    D = 15


class UnknownProductException(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown product found: {name}")


def parse_products(skus: str) -> Generator[Product, None, None]:
    for sku in list(skus):
        try:
            yield Product[sku]
        except KeyError:
            raise UnknownProductException(sku)


class Basket:

    def __init__(self) -> None:
        self.items = {}

    def add_item(self, product: Product):
        count = self.items.get(product)
        if count is None:
            count = 0
        count += 1
        self.items[product] = count

    def calculate_total(self):
        total = 0
        for product, count in self.items.items():
            total += product.value * count
        return total






