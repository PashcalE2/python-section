from typing import Self, Dict
from .currency import Currency
from .exceptions import NotComparisonException, NegativeValueException


class Money:
    __value: float
    __currency: Currency

    def __init__(self, value: float, currency: Currency) -> None:
        self.__value = value
        self.__currency = currency

    def __check_operand_type(self, other: object, operation: str) -> None:
        if not isinstance(other, Money):
            raise TypeError(
                f"Unsupported operand type for {operation} between 'Money' and {type(other).__name__}")

    def __check_currency_equals(self, other) -> None:
        if self.currency != other.currency:
            raise NotComparisonException()

    def __add__(self, other) -> "Money":
        self.__check_operand_type(other, "+")
        self.__check_currency_equals(other)
        return Money(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other) -> "Money":
        self.__check_operand_type(other, "-")
        self.__check_currency_equals(other)
        return Money(value=self.value - other.value, currency=self.currency)

    def __eq__(self, other) -> bool:
        self.__check_operand_type(other, "==")
        self.__check_currency_equals(other)
        return self.value == other.value

    @property
    def value(self):
        return self.__value

    @property
    def currency(self):
        return self.__currency


class Wallet:
    __currencies: Dict[Currency, Money] = {}

    def __init__(self, money: Money) -> None:
        self.__currencies[money.currency] = money

    def __contains__(self, key: Currency) -> bool:
        return key in self.__currencies

    def __getempty(self, key: Currency) -> Money:
        return Money(value=0, currency=key)

    def __getitem__(self, key: Currency) -> Money:
        return self.__currencies[key] if key in self else self.__getempty(key)

    def __delitem__(self, key: Currency) -> None:
        if key in self:
            del self.__currencies[key]

    def __len__(self) -> int:
        return len(self.__currencies)

    def add(self, money: Money) -> Self:
        if money.currency not in self:
            self.__currencies[money.currency] = money
        else:
            self.__currencies[money.currency] += money
        return self

    def sub(self, money: Money) -> Self:
        self_money = self.__currencies[money.currency] if money.currency in self else self.__getempty(
            money.currency)

        if self_money.value < money.value:
            raise NegativeValueException()

        self.__currencies[money.currency] -= money
        return self

    @property
    def currencies(self) -> Dict[Currency, Money]:
        return self.__currencies
