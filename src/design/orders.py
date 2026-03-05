from dataclasses import dataclass


@dataclass
class Order:
    """There is no need to describe anything here."""


class Discount:
    def apply(self, order: Order):
        raise NotImplementedError()


class FixedDiscount(Discount):
    def apply(self, order: Order):
        print("Applied fixed discount")


class PercentageDiscount(Discount):
    def apply(self, order: Order):
        print("Applied percentage discount")


class LoyaltyDiscount(Discount):
    def apply(self, order: Order):
        print("Applied loyalty discount")


class DiscountGetter:
    def get_discounts_list(self, order: Order) -> list[Discount]:
        raise NotImplementedError()


class DiscountGetterImpl(DiscountGetter):
    def get_discounts_list(self, order: Order) -> list[Discount]:
        return [LoyaltyDiscount(), PercentageDiscount()]


class DiscontApplier:
    def __init__(self, order: Order, discount_getter: DiscountGetter):
        self.__order = order
        self.__discount_getter = discount_getter

    def apply_discounts(self):
        for discount in self.__discount_getter.get_discounts_list(self.__order):
            discount.apply(self.__order)


applier = DiscontApplier(Order(), DiscountGetterImpl())
applier.apply_discounts()
