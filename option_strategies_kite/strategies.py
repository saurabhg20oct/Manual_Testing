from __future__ import annotations

from .models import OptionLeg, OptionType, TransactionType


def bull_call_spread(symbol: str, lower_strike: float, higher_strike: float, qty: int, lower_premium: float, higher_premium: float) -> list[OptionLeg]:
    return [
        OptionLeg(symbol, lower_strike, OptionType.CALL, TransactionType.BUY, qty, lower_premium),
        OptionLeg(symbol, higher_strike, OptionType.CALL, TransactionType.SELL, qty, higher_premium),
    ]


def bear_put_spread(symbol: str, higher_strike: float, lower_strike: float, qty: int, higher_premium: float, lower_premium: float) -> list[OptionLeg]:
    return [
        OptionLeg(symbol, higher_strike, OptionType.PUT, TransactionType.BUY, qty, higher_premium),
        OptionLeg(symbol, lower_strike, OptionType.PUT, TransactionType.SELL, qty, lower_premium),
    ]


def long_straddle(symbol: str, strike: float, qty: int, call_premium: float, put_premium: float) -> list[OptionLeg]:
    return [
        OptionLeg(symbol, strike, OptionType.CALL, TransactionType.BUY, qty, call_premium),
        OptionLeg(symbol, strike, OptionType.PUT, TransactionType.BUY, qty, put_premium),
    ]


def short_strangle(symbol: str, put_strike: float, call_strike: float, qty: int, put_premium: float, call_premium: float) -> list[OptionLeg]:
    return [
        OptionLeg(symbol, put_strike, OptionType.PUT, TransactionType.SELL, qty, put_premium),
        OptionLeg(symbol, call_strike, OptionType.CALL, TransactionType.SELL, qty, call_premium),
    ]


def iron_condor(symbol: str, lower_put_buy: float, lower_put_sell: float, upper_call_sell: float, upper_call_buy: float, qty: int, p_buy: float, p_sell: float, c_sell: float, c_buy: float) -> list[OptionLeg]:
    return [
        OptionLeg(symbol, lower_put_buy, OptionType.PUT, TransactionType.BUY, qty, p_buy),
        OptionLeg(symbol, lower_put_sell, OptionType.PUT, TransactionType.SELL, qty, p_sell),
        OptionLeg(symbol, upper_call_sell, OptionType.CALL, TransactionType.SELL, qty, c_sell),
        OptionLeg(symbol, upper_call_buy, OptionType.CALL, TransactionType.BUY, qty, c_buy),
    ]
