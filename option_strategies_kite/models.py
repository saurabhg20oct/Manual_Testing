from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OptionType(str, Enum):
    CALL = "CE"
    PUT = "PE"


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True)
class OptionLeg:
    symbol: str
    strike: float
    option_type: OptionType
    transaction_type: TransactionType
    quantity: int
    premium: float

    @property
    def signed_premium(self) -> float:
        """Cashflow for this leg: buy is debit(-), sell is credit(+)."""
        sign = -1 if self.transaction_type is TransactionType.BUY else 1
        return sign * self.premium * self.quantity

    def payoff(self, spot: float) -> float:
        intrinsic = (
            max(spot - self.strike, 0)
            if self.option_type is OptionType.CALL
            else max(self.strike - spot, 0)
        )
        direction = 1 if self.transaction_type is TransactionType.BUY else -1
        return (intrinsic - self.premium) * self.quantity * direction
