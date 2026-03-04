class NegativeValueException(Exception):
    def __init__(self) -> None:
        super().__init__("Wallet's money cannot be negative")


class NotComparisonException(Exception):
    def __init__(self) -> None:
        super().__init__("Cannot compare different currencies")
