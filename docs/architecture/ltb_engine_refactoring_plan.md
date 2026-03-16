============================================================
LTB ENGINE REFACTORING PLAN
Author: System Architecture
Purpose: Engine Stabilization and Architecture Cleanup
============================================================


1. DOCUMENT PURPOSE

This document defines the refactoring plan for the LTB trading engine.

The LTB system has reached a stage where the core architecture is largely implemented,
but structural cleanup and stabilization are required before moving into real
market integration and operational deployment.

The primary objective of this document is to define the steps required to stabilize
the engine architecture and prepare the system for live market integration.


------------------------------------------------------------
2. CURRENT ENGINE STATE
------------------------------------------------------------

Current development phase

Core Engine Implementation


System characteristics

workers            : 30+
source files       : 120+
event topics       : 40+


Core architecture

Event-driven worker architecture
Queue based event bus
Multi-layer signal pipeline
Portfolio optimizer
Multi-layer risk control
Modular strategy engine


Current system mode

BACKTEST only

Market data

Mock generator
Replay dataset

Execution

Mock execution


------------------------------------------------------------
3. ARCHITECTURE ISSUES IDENTIFIED
------------------------------------------------------------

During code inspection several structural inconsistencies were identified.


Issue 1

Duplicate Engine Entry Points

Files

runtime/engine.py
runtime/engine_process.py

These two files represent different engine initialization patterns.


Issue 2

Multiple Event Bus Implementations

Files

runtime/event_bus.py
runtime/queue_bus.py

QueueBus is currently the active system component.


Issue 3

MarketWorker Responsibility Mixing

Current MarketWorker contains both

mock market generator
live market placeholder

This violates separation of responsibility.


------------------------------------------------------------
4. REFACTORING OBJECTIVES
------------------------------------------------------------

The refactoring process will pursue the following goals.


Architecture Simplification

Remove duplicate engine components.


Event Bus Standardization

QueueBus will become the single event bus implementation.


Market Source Separation

Separate mock, replay and live market sources.


Execution Adapter Expansion

Prepare execution layer for broker integrations.


Mode Architecture Stabilization

BACKTEST
PAPER
LIVE

must be fully isolated in engine runtime logic.


------------------------------------------------------------
5. TARGET ENGINE ARCHITECTURE
------------------------------------------------------------

Final runtime structure


SystemContext

mode

BACKTEST
PAPER
LIVE


Market Source

MockMarketWorker
ReplayMarketWorker
LiveMarketWorker


Execution Adapter

MockExecutionAdapter
PaperExecutionAdapter
BrokerExecutionAdapter


Broker Adapters

KISExecutor
UpbitExecutor


Core Runtime Pipeline


Market
↓
Indicator
↓
Strategy
↓
Signal Processing
↓
Portfolio Optimization
↓
Execution
↓
Portfolio Tracking
↓
Risk Control
↓
Analytics


------------------------------------------------------------
6. REFACTORING PHASES
------------------------------------------------------------


PHASE 1
Engine Stabilization


Tasks

Remove obsolete engine entry point

runtime/engine.py


Standardize event bus

QueueBus only


Refactor MarketWorker


MockMarketWorker
ReplayMarketWorker
LiveMarketWorker


Verify worker initialization order


------------------------------------------------------------


PHASE 2
Execution Layer Preparation


Expand ExecutorRouter

BACKTEST → MockExecutor
PAPER → PaperExecutor
LIVE → BrokerExecutor


Prepare broker adapters

KIS API
Upbit API


------------------------------------------------------------


PHASE 3
Market Integration


Add real market workers


KISMarketWorker
UpbitMarketWorker


WebSocket market ingestion


orderbook stream
trade stream
ticker stream


------------------------------------------------------------


PHASE 4
Backtest Infrastructure


Add CLI backtest interface


ltb backtest run
ltb backtest strategy
ltb backtest range


Add historical dataset loader


------------------------------------------------------------


PHASE 5
Monitoring Infrastructure


CLI monitoring dashboard


Web dashboard


Trading report system


------------------------------------------------------------
7. ENGINE STABILIZATION CHECKLIST
------------------------------------------------------------

The following items must be verified after refactoring.


Engine startup works in all modes


BACKTEST mode

ReplayMarketWorker operates correctly


PAPER mode

Mock market data works correctly


LIVE mode

Live market worker initialization works


Event bus stability

No queue overflow
Worker isolation verified


Execution pipeline stability

Order request
Order execution
Order filled events verified


Portfolio lifecycle validation

POSITION_OPENED
POSITION_CLOSED
portfolio.update


Risk control validation

portfolio heat
position sizing
strategy kill switch


------------------------------------------------------------
8. POST REFACTORING GOAL
------------------------------------------------------------

After refactoring the engine will be prepared for the next stage.


Market Integration


KIS API
Upbit API


Operational Tooling


CLI backtest system
CLI monitoring dashboard
Web dashboard


Analytics


Auto trading reports
Strategy performance analytics


------------------------------------------------------------
9. LONG TERM SYSTEM TARGET
------------------------------------------------------------

The final LTB system will operate as a fully autonomous trading engine.


Core system components


Market ingestion
Strategy engine
Portfolio optimizer
Execution engine
Risk control system
Analytics system
Monitoring system


Supported markets


US equities
KR equities
Crypto markets


Deployment

local trading node
cloud distributed execution


============================================================
END OF DOCUMENT
============================================================
