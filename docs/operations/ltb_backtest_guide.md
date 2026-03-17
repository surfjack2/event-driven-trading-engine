# LTB Backtest Guide

The engine supports backtesting using historical replay.

--------------------------------------------------

Backtest Mode

ReplayMarketWorker simulates market events using historical data.

--------------------------------------------------

Execution Flow

Load historical dataset
↓
Replay market events
↓
Indicators update
↓
Strategy evaluation
↓
Signal pipeline
↓
Simulated execution

--------------------------------------------------

Purpose

Backtesting allows

- strategy validation
- pipeline verification
- architecture testing
