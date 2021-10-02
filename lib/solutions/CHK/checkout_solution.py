# noinspection PyUnusedLocal
# skus = unicode string
from dataclasses import dataclass
from enum import IntEnum
from typing import Generator, List, Dict

from abc import ABC, abstractmethod


class Product(IntEnum):
    A = 50
    B = 30
    C = 20
    D = 15
    E = 40


class UnknownProductException(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown product found: {name}")


class Condition(ABC):

    @abstractmethod
    def is_applicable(self, items: Dict[Product, int]) -> bool:
        pass


@dataclass
class MultiBuy(Condition):
    product: Product
    count: int

    def is_applicable(self, items: Dict[Product, int]) -> bool:
        return self.product in items and items[self.product] >= self.count


class Discount(ABC):

    @abstractmethod
    def apply(self, items: Dict[Product, int]) -> int:
        pass


@dataclass
class FixPrice(Discount):
    product: Product
    count: int
    price: int

    def apply(self, items: Dict[Product, int]) -> int:
        discount = 0
        if self.product in items and items[self.product] >= self.count:
            items[self.product] -= self.count
            discount = self.product.value * self.count - self.price
        return discount


@dataclass
class GetFree(Discount):
    product: Product
    count: int

    def apply(self, items: Dict[Product, int]) -> int:
        discount = 0
        if self.product in items and items[self.product] >= self.count:
            items[self.product] -= self.count
            discount = self.product.value * self.count
        return discount


@dataclass
class Offer:
    condition: Condition
    discount: Discount


class Basket:

    def __init__(self) -> None:
        self.items: Dict[Product, int] = {}

    def add_item(self, product: Product):
        count = self.items.get(product)
        if count is None:
            count = 0
        count += 1
        self.items[product] = count

    def checkout(self):
        total = self._calculate_total()

    def _calculate_total(self):
        total = 0
        for product, count in self.items.items():
            total += product.value * count
        return total

    def _calculate_discount(self):
        pass

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


def get_offers() -> List[Offer]:
    return [
        Offer(MultiBuy(Product.A, 3), FixPrice(Product.A, 3, 130)),
        Offer(MultiBuy(Product.A, 5), FixPrice(Product.A, 5, 200)),
        Offer(MultiBuy(Product.B, 2), FixPrice(Product.B, 2, 45)),
        Offer(MultiBuy(Product.E, 2), GetFree(Product.B, 1)),
    ]


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




