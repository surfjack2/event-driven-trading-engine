LTB Full Data Flow Map
Version: 2.0
Status: Architecture Reference


Purpose
-------

This document describes the complete end-to-end data flow of the
LTB trading system.

The goal is to provide a clear architectural overview of how market
data moves through the system, how trading signals are generated,
and how orders are executed.


High Level Data Flow
--------------------

Market Data
    │
    ▼
Market Worker
    │
    ▼
Indicator Engine
    │
    ▼
Strategy Worker
    │
    ▼
Signal Pipeline
    │
    ▼
Portfolio Optimizer
    │
    ▼
Execution Engine
    │
    ▼
Broker / Exchange


Detailed Event Pipeline
-----------------------

Market Data Ingestion

market.price
market.indicator


Strategy Signal Generation

strategy.signal


Signal Validation Pipeline

strategy.signal
    │
    ▼
signal_dedup_worker
    │
    ▼
signal_persistence_worker
    │
    ▼
signal_ranking_worker


Strategy Allocation

ranked.signal
    │
    ▼
strategy_allocation_worker
    │
    ▼
allocation.signal


Position Intent Resolution

allocation.signal
    │
    ▼
position_intent_worker
    │
    ▼
intent.signal


Portfolio Risk Filters

intent.signal
    │
    ▼
correlation_filter_worker
    │
    ▼
filtered.intent


Portfolio Optimization

filtered.intent
    │
    ▼
portfolio_optimizer_worker
    │
    ▼
optimized.signal


Execution Pipeline

optimized.signal
    │
    ▼
execution_worker
    │
    ▼
order.request
    │
    ▼
order_executor
    │
    ▼
ORDER_FILLED


Portfolio Update

ORDER_FILLED
    │
    ▼
portfolio_worker
    │
    ▼
POSITION_OPENED
POSITION_CLOSED


Trade Recording

POSITION_CLOSED
    │
    ▼
trade_ledger_worker
    │
    ▼
account.snapshot


Risk Management

POSITION_CLOSED
    │
    ▼
risk_worker
    │
    ▼
system.halt


Runtime Monitoring

All events
    │
    ▼
validation_monitor_worker


System Components
-----------------

The system consists of several functional layers.


Market Layer

Handles market data ingestion.

market_worker
indicator_engine
scanner_worker


Strategy Layer

Generates trading signals.

strategy_worker
strategy_engine
strategy modules


Signal Processing Layer

Validates and ranks signals.

signal_dedup_worker
signal_persistence_worker
signal_ranking_worker
strategy_allocation_worker


Portfolio Layer

Selects positions to execute.

position_intent_worker
correlation_filter_worker
portfolio_optimizer_worker


Execution Layer

Handles order routing and execution.

execution_worker
order_executor
kis_executor


Risk Layer

Protects the system from excessive losses.

risk_worker
killswitch_worker


Monitoring Layer

Provides runtime visibility.

validation_monitor_worker
account_stats_worker


Operational Characteristics
---------------------------

The LTB engine is designed as an event-driven system.

Workers communicate through the event bus.

Key properties:

• asynchronous processing
• modular workers
• pipeline based signal processing
• risk-first architecture


Future Expansion
----------------

The architecture supports future expansion including:

• multi-strategy portfolio research
• replay-based backtesting engine
• automated strategy evaluation
• meta strategy allocation


Implementation Status
---------------------

This data flow map represents the current architecture
of the LTB live trading engine.

Future research extensions are documented separately
in the Research Engine architecture documents.
