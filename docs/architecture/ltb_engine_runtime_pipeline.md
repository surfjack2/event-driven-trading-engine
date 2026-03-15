LTB ENGINE RUNTIME PIPELINE
Event Driven Worker Architecture
--------------------------------------------------


System Overview

LTB trading engine operates as a multi-worker event-driven system.

Each worker subscribes to event topics through the QueueBus.
Workers process events and publish new events that propagate through the pipeline.

This architecture enables modular trading logic, asynchronous processing,
and clear separation between market processing, strategy evaluation,
portfolio optimization, and execution.


Core Runtime Flow

Market Layer
↓
Indicator Layer
↓
Strategy Layer
↓
Signal Processing Layer
↓
Portfolio Decision Layer
↓
Execution Layer
↓
Portfolio Management
↓
Risk Management
↓
Analytics and Monitoring


--------------------------------------------------
MARKET LAYER
--------------------------------------------------

MarketWorker

Responsibilities

- generate or receive market price events
- publish raw market data

Published Events

market.price
MARKET_TICK


--------------------------------------------------
INDICATOR LAYER
--------------------------------------------------

IndicatorWorker

Responsibilities

- compute technical indicators
- attach derived metrics to market events

Indicators

RSI
EMA
VWAP
VWAP Bands
Volume Moving Average
Turnover Moving Average
ATR

Published Events

market.indicator


--------------------------------------------------
STRATEGY LAYER
--------------------------------------------------

StrategyWorker

Responsibilities

- evaluate trading strategies
- generate strategy signals

Strategies

SimpleMomentumStrategy
VWAPReclaimBandStrategy
VWAPBandBounceStrategy

Published Events

strategy.signal


--------------------------------------------------
SIGNAL PROCESSING PIPELINE
--------------------------------------------------

SignalDedupWorker

Purpose

- remove duplicated signals
- enforce signal cooldown


SignalPersistenceWorker

Purpose

- buffer and persist signals
- provide signal stream stability


SignalRankingWorker

Purpose

- compute alpha score
- normalize alpha values
- rank signals

Alpha Model

trend alignment
momentum
liquidity pressure
volatility penalty


LiquidityFilterWorker

Purpose

- remove low liquidity opportunities
- enforce volume constraints


StrategyAllocationWorker

Purpose

- assign capital weights to strategies
- adjust allocation based on performance
- apply market regime adjustments

Published Event

allocation.signal


--------------------------------------------------
PORTFOLIO DECISION LAYER
--------------------------------------------------

PositionIntentWorker

Purpose

- collect signals per symbol
- select best signal candidate


CorrelationFilterWorker

Purpose

- prevent correlated positions
- reduce portfolio concentration


PortfolioOptimizerWorker

Purpose

- compute optimizer score
- select signals for execution

Optimizer Model

optimizer_score =
alpha
+ allocation_weight
+ liquidity factor
+ momentum factor
- volatility penalty

Published Event

optimized.signal


--------------------------------------------------
EXECUTION LAYER
--------------------------------------------------

ExecutionWorker

Responsibilities

- validate risk conditions
- calculate position size
- enforce execution safeguards

Execution Constraints

max portfolio positions
max strategy positions
portfolio heat control
order rate control

Position sizing uses

PositionSizer
RiskEngine


OrderExecutorWorker

Responsibilities

- send orders to exchange executor
- publish filled orders


ExecutorRouter

Routes order requests to execution backend

Possible executors

KIS executor
exchange specific executors


Published Events

ORDER_FILLED


--------------------------------------------------
PORTFOLIO MANAGEMENT
--------------------------------------------------

PortfolioWorker

Responsibilities

- track open positions
- calculate PnL
- manage position lifecycle

Position Events

POSITION_OPENED
POSITION_CLOSED

Published Event

portfolio.update


TradeLedgerWorker

Responsibilities

- store trade history
- record trade metrics


--------------------------------------------------
RISK MANAGEMENT
--------------------------------------------------

TrailingStopWorker

Purpose

- dynamic stop adjustment


SignalDecayExitWorker

Purpose

- exit when signal weakens


PositionTimeStopWorker

Purpose

- exit after maximum holding time


RiskWorker

Purpose

- monitor portfolio risk
- enforce global risk limits


StrategyKillSwitchWorker

Purpose

- disable underperforming strategies


--------------------------------------------------
ANALYTICS AND SYSTEM MONITORING
--------------------------------------------------

AnalyticsWorker

Purpose

- compute trading statistics
- aggregate system metrics


AlertWorker

Purpose

- monitor anomalies
- notify system issues


KillSwitchWorker

Purpose

- emergency trading halt


HeartbeatWorker

Purpose

- verify system health
- confirm engine alive


--------------------------------------------------
EVENT BUS
--------------------------------------------------

QueueBus

Purpose

- asynchronous event distribution
- worker decoupling

Characteristics

multi-threaded workers
queue based dispatch
fault tolerant execution


--------------------------------------------------
SYSTEM CONTEXT
--------------------------------------------------

SystemContext

Defines runtime environment

mode

BACKTEST
PAPER
LIVE

market

US
KR
CRYPTO


--------------------------------------------------
ENGINE SCALE
--------------------------------------------------

Workers                : 30+
Source files           : 120+
Event topics           : 50+

Architecture type

event driven trading engine
multi strategy portfolio system
modular worker architecture


End of Document
