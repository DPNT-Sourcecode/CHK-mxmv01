# noinspection PyUnusedLocal
# skus = unicode string
from enum import IntEnum

from typing import Generator, List, Dict

from dataclasses import dataclass


class Product(IntEnum):
    A = 50
    B = 30
    C = 20
    D = 15


class UnknownProductException(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown product found: {name}")


@dataclass
class Offer:
    product: Product
    offer_count: int
    price: int

    def calculate_total(self, product_count) -> int:
        offers_count = product_count // self.offer_count
        full_price_count = product_count % self.offer_count
        return offers_count * self.price + full_price_count * self.product.value


class Basket:

    def __init__(self) -> None:
        self.items = {}

    def add_item(self, product: Product):
        count = self.items.get(product)
        if count is None:
            count = 0
        count += 1
        self.items[product] = count

    def calculate_total(self, offers: Dict[Product, Offer]):
        basket_total = 0
        for product, count in self.items.items():
            if product in offers:
                product_total = offers[product].calculate_total(count)
            else:
                product_total = product.value * count
            basket_total += product_total
        return basket_total


def get_offers() -> Dict[Product, Offer]:
    return {offer.product: offer for offer in [Offer(Product.A, 3, 130), Offer(Product.B, 2, 45)]}


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


