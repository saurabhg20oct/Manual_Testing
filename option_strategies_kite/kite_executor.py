from __future__ import annotations

import os
from typing import Any

from .models import OptionLeg

try:
    from kiteconnect import KiteConnect
except ImportError:  # optional dependency at runtime
    KiteConnect = None  # type: ignore


class KiteExecutor:
    def __init__(self, api_key: str | None = None, access_token: str | None = None) -> None:
        if KiteConnect is None:
            raise RuntimeError("kiteconnect package is not installed. Run: pip install kiteconnect")
        api_key = api_key or os.getenv("KITE_API_KEY")
        access_token = access_token or os.getenv("KITE_ACCESS_TOKEN")
        if not api_key or not access_token:
            raise ValueError("KITE_API_KEY and KITE_ACCESS_TOKEN are required")
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    def place_option_leg(self, leg: OptionLeg, exchange: str = "NFO", product: str = "NRML") -> Any:
        tradingsymbol = f"{leg.symbol}{int(leg.strike)}{leg.option_type.value}"
        return self.kite.place_order(
            variety=self.kite.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=leg.transaction_type.value,
            quantity=leg.quantity,
            product=product,
            order_type=self.kite.ORDER_TYPE_MARKET,
            validity=self.kite.VALIDITY_DAY,
        )

    def execute_strategy(self, legs: list[OptionLeg], dry_run: bool = True) -> list[Any]:
        if dry_run:
            return [
                {
                    "tradingsymbol": f"{leg.symbol}{int(leg.strike)}{leg.option_type.value}",
                    "transaction_type": leg.transaction_type.value,
                    "quantity": leg.quantity,
                }
                for leg in legs
            ]
        return [self.place_option_leg(leg) for leg in legs]
