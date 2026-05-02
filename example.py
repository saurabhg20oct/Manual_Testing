from option_strategies_kite.engine import payoff_table
from option_strategies_kite.kite_executor import KiteExecutor
from option_strategies_kite.strategies import bull_call_spread


if __name__ == "__main__":
    legs = bull_call_spread("NIFTY", 22500, 22700, qty=50, lower_premium=180, higher_premium=110)

    table = payoff_table(legs, start=22000, stop=23000, step=100)
    for row in table:
        print(f"Spot={row.spot:.0f} -> P/L={row.payoff:.2f}")

    # dry_run keeps it safe and only prints order payload equivalent
    try:
        executor = KiteExecutor()
        print(executor.execute_strategy(legs, dry_run=True))
    except Exception as exc:
        print(f"Skipping live integration setup: {exc}")
