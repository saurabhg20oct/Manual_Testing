# Indian Market Signal Engine (Milestone 1) — Implementation Plan

## Scope
Milestone 1 covers **analysis + signal generation + backtesting + reporting** for Indian equities, ETFs, indices, and option chains. No auto-execution.

## Recommended Repository Structure
```text
market_signal_engine/
  config/
    config.yaml
  data/
    raw/
    processed/
    cache/
  src/
    core/
      models.py
      enums.py
      settings.py
    data_pipeline/
      universe.py
      ohlcv_fetcher.py
      intraday_fetcher.py
      option_chain_fetcher.py
      corporate_actions_fetcher.py
      adjustments.py
      quality_checks.py
      storage.py
    fundamentals/
      screener_scraper.py
      governance_flags.py
      piotroski.py
      altman.py
      dupont.py
      dcf.py
      peer_ranker.py
    technical/
      indicators.py
      strategy_library.py
      regime.py
      signal_aggregator.py
      suppression_rules.py
    events/
      bse_events.py
      macro_calendar.py
      signal_modifiers.py
    options/
      iv.py
      pcr.py
      max_pain.py
      oi_classifier.py
      greeks.py
      payoff.py
      margin.py
      strategy_selector.py
    prediction/
      features.py
      arima_model.py
      prophet_model.py
      lgbm_model.py
      xgb_model.py
      lstm_model.py
      sentiment_finbert.py
      monte_carlo.py
      ensemble.py
    backtest/
      engine.py
      costs.py
      walk_forward.py
      metrics.py
    reports/
      templates/
      stock_report.py
      daily_digest.py
      pdf_export.py
    dashboard/
      live_console.py
      alerting.py
    cli/
      run.py
      analyze.py
      signals.py
      events.py
      options.py
      predict.py
      backtest.py
      report.py
  tests/
    unit/
    integration/
```

## Core Interface Contracts (for cross-module development)

```python
# src/data_pipeline/storage.py
from pandas import DataFrame

def store_ohlcv(symbol: str, timeframe: str, df: DataFrame) -> None: ...
def get_ohlcv(symbol: str, timeframe: str, start: str, end: str) -> DataFrame: ...
def store_option_chain(symbol: str, expiry: str, df: DataFrame) -> None: ...
def get_option_chain(symbol: str, expiry: str) -> DataFrame: ...
```

```python
# src/technical/signal_aggregator.py
from dataclasses import dataclass
from typing import Literal

SignalType = Literal["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL", "WAIT", "AVOID"]

@dataclass
class Signal:
    symbol: str
    strategy: str
    timeframe: str
    signal: SignalType
    entry: float
    stop_loss: float
    targets: list[float]
    rr_ratio: float
    confidence: int
    suppression_reasons: list[str]
```

```python
# src/prediction/ensemble.py
from dataclasses import dataclass
from typing import Literal

Direction = Literal["BULLISH", "BEARISH", "NEUTRAL"]

@dataclass
class PredictionRange:
    symbol: str
    direction: Direction
    range_5d_p25_p75: tuple[float, float]
    range_10d_p10_p90: tuple[float, float]
    confidence: int
    model_agreement: str
    key_driver: str
```

## Week-by-Week Execution (Milestone 1)

### Week 1 (Foundation)
- Project scaffold + dependency management.
- Universe loader (NSE stocks/ETFs/indices).
- OHLCV daily/weekly ingestion + 5m/15m intraday ingestion.
- Option chain fetcher for Nifty + BankNifty.
- BSE corporate actions fetcher.
- Local storage schema (SQLite or DuckDB).
- Price adjustment (bonus/split/dividend).
- Data quality checks and unit tests.

### Week 2 (Fundamentals)
- Scrapers/fetchers for financial statements and shareholding.
- Ratios and scoring models (Piotroski, Altman, DuPont, DCF).
- Governance flag engine + insider tracking parser.
- Sector peer percentile ranking.

### Week 3 (Technical)
- Indicator library and 24-strategy implementation.
- Multi-timeframe confluence scoring.
- Suppression rules (VIX > 20, earnings window, market open first 15 minutes).

### Week 4 (Corporate actions)
- BSE event ingestion + 30-day timeline.
- Macro calendar and event-driven confidence adjustments.

### Week 5 (Options)
- IV/IV Rank/PCR/Max pain/OI classification.
- 18 strategy evaluators + payoff + margin + PoP.

### Week 6–7 (Prediction)
- ARIMA/Prophet baseline.
- LGBM/XGBoost classifier.
- LSTM/GRU per sector.
- FinBERT sentiment + ensemble confidence.
- Monte Carlo fan-chart outputs.

### Week 8 (Backtesting)
- Walk-forward harness.
- Transaction costs/slippage.
- Strategy-level metrics and equity curves.

### Week 9 (Reporting)
- Stock HTML/PDF report engine.
- Daily digest with top buys/sells/options + event calendar.

### Week 10 (Dashboard + Integration)
- Live terminal dashboard refresh every 5 minutes.
- Telegram/email alerts.
- End-to-end integration, profiling, and README ops guide.

## Non-negotiable implementation checks
1. No signal without a stop loss.
2. Position risk capped at 1% by formula.
3. Walk-forward only for predictive/backtest validation.
4. Cost + slippage always applied in backtests.
5. Prediction outputs are ranges/probabilities, never fixed price targets.
6. RED governance => AVOID override.

## Suggested Next Task
Start **Week 1 sprint** by scaffolding `src/data_pipeline`, `src/core`, `src/cli`, and writing `python run.py --fetch-all` with stub implementations + tests for interface contracts.
