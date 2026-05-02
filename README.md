# Option Strategy Simulator with Kite Connect

A lightweight Python codebase to **model common options strategies** and optionally execute orders through **Zerodha Kite Connect**.

## What this provides

- Reusable option-leg model (`OptionLeg`) for CALL/PUT and BUY/SELL legs.
- Prebuilt multi-leg strategies:
  - Bull Call Spread
  - Bear Put Spread
  - Long Straddle
  - Short Strangle
  - Iron Condor
- Payoff engine to evaluate strategy P/L across spot prices.
- Kite Connect execution adapter with safe `dry_run` mode.

## Project structure

- `option_strategies_kite/models.py`: Leg data model and leg-level payoff math.
- `option_strategies_kite/strategies.py`: Strategy constructors.
- `option_strategies_kite/engine.py`: Strategy-level payoff simulation.
- `option_strategies_kite/kite_executor.py`: Kite Connect integration and order placement.
- `example.py`: End-to-end usage example.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Kite credentials

Export credentials before live execution:

```bash
export KITE_API_KEY="your_api_key"
export KITE_ACCESS_TOKEN="your_access_token"
```

## Run example

```bash
python example.py
```

This prints a payoff table and a dry-run order payload.

## Live execution caution

- Keep `dry_run=True` while testing.
- Validate instrument symbols and expiry format for your broker contract naming.
- This repo is an educational starter; harden risk controls before real trading.
