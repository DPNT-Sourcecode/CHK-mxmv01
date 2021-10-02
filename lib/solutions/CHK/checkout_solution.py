# noinspection PyUnusedLocal
# skus = unicode string
from dataclasses import dataclass
from enum import IntEnum
from typing import Generator, List, Dict


class Product(IntEnum):
    A = 50
    B = 30
    C = 20
    D = 15
    E = 40


class UnknownProductException(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown product found: {name}")


@dataclass
class Offer:
    product: Product
    count: int
    price: int


class Basket:

    def __init__(self) -> None:
        self.items = {}

    def add_item(self, product: Product):
        count = self.items.get(product)
        if count is None:
            count = 0
        count += 1
        self.items[product] = count

    def calculate_total(self, offers: Dict[Product, List[Offer]]):
        total = 0
        for product, count in self.items.items():
            if product in offers:
                product_total = self._calculate_discounted_total(product, offers[product], count)
            else:
                product_total = self._calculate_full_price_total(product, count)
            total += product_total
        return total

    def _calculate_discounted_total(self, product: Product, offers: List[Offer], count: int) -> int:
        product_total = 0
        for offer in offers:
            product_total += count // offer.count * offer.price
            count = count % offer.count
        product_total += self._calculate_full_price_total(product, count)
        return product_total

    def _calculate_full_price_total(self, product: Product, count: int) -> int:
        return product.value * count


def get_offers() -> Dict[Product, List[Offer]]:
    return {Product.A: [Offer(Product.A, 5, 200), Offer(Product.A, 3, 130)],
            Product.B: [Offer(Product.B, 2, 45)],
            Product.E: [Offer(Product.E, 2, 40)]}


def checkout(skus: str):
    basket = Basket()
    try:
        for product in parse_products(skus):
            basket.add_item(product)
    except UnknownProductException:
        return -1
    return basket.calculate_total(get_offers())


def parse_products(skus: str) -> Generator[Product, None, None]:
    for sku in list(skus):
        try:
            yield Product[sku]
        except KeyError:
            raise UnknownProductException(sku)
