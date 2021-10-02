# noinspection PyUnusedLocal
# skus = unicode string
from dataclasses import dataclass
from enum import IntEnum
from typing import Generator, Dict


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

    def calculate_discounted_total(self, offer: Offer, count: int) -> int:
        offers_count = count // offer.count
        full_price_count = count % offer.count
        return offers_count * offer.price + self.calculate_full_price_total(offer.product, full_price_count)

    def calculate_full_price_total(self, product: Product, count: int) -> int:
        return product.value * count

    def calculate_total(self, offers: Dict[Product, Offer]):
        total = 0
        for product, count in self.items.items():
            if product in offers:
                product_total = self.calculate_discounted_total(offers[product], count)
            else:
                product_total = self.calculate_full_price_total(product, count)
            total += product_total
        return total


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



