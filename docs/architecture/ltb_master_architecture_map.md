============================================================
LTB MASTER ARCHITECTURE MAP
Author: System Design Spec
Purpose: Live Trading Bot (LTB) Core Runtime Architecture
============================================================


SYSTEM OVERVIEW
------------------------------------------------------------

LTB is an event-driven multi-worker trading engine.

The engine is composed of independent workers that communicate
through an asynchronous event bus (QueueBus).

Each worker subscribes to specific event topics, processes data,
and publishes new events that propagate through the trading pipeline.

This design allows:

- modular architecture
- fault tolerance
- asynchronous processing
- multi-strategy trading
- portfolio level decision making


------------------------------------------------------------
ENGINE RUNTIME PIPELINE
------------------------------------------------------------

Market Layer
↓
Market Regime Analysis
↓
Scanner and Alpha Selection
↓
Indicator Engine
↓
Strategy Engine
↓
Signal Processing Pipeline
↓
Portfolio Decision Layer
↓
Execution Engine
↓
Portfolio Management
↓
Risk Management
↓
Analytics and Monitoring


------------------------------------------------------------
MARKET DATA LAYER
------------------------------------------------------------

MarketWorker

Purpose

Generate or receive market price data.

Responsibilities

- generate mock market ticks (backtest / paper)
- receive real market data (live mode)
- publish price events

Published Events

market.price
MARKET_TICK


------------------------------------------------------------
MARKET REGIME LAYER
------------------------------------------------------------

Workers

MarketCalendarWorker
MarketSessionWorker
MarketRegimeWorker
LiquidityRegimeWorker
ExposureWorker


Responsibilities

- detect market session state
- detect market regime
- detect liquidity regime
- adjust exposure model


Published Events

market.regime
market.liquidity_regime


------------------------------------------------------------
SCANNER AND ALPHA SELECTION
------------------------------------------------------------

Workers

RelativeTurnoverScannerWorker
ScannerWorker
AlphaRankingWorker
UniverseScannerWorker
RankingWorker


Responsibilities

Detect high activity trading candidates.

Alpha selection pipeline:

RelativeTurnoverScannerWorker

Detects abnormal turnover relative to average.


ScannerWorker

Detects symbols that satisfy scanner rules.


AlphaRankingWorker

Ranks symbols using liquidity and volatility signals.


UniverseScannerWorker

Maintains dynamic trading universe.


RankingWorker

Ranks top symbols based on momentum, volume,
turnover pressure, and VWAP positioning.


------------------------------------------------------------
INDICATOR ENGINE
------------------------------------------------------------

IndicatorWorker

Responsibilities

Calculate technical indicators.


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


------------------------------------------------------------
STRATEGY ENGINE
------------------------------------------------------------

StrategyWorker


Strategies Implemented

SimpleMomentumStrategy
VWAPReclaimBandStrategy
VWAPBandBounceStrategy


Responsibilities

Evaluate trading opportunities based on indicators.

Generate strategy signals.


Published Events

strategy.signal


------------------------------------------------------------
SIGNAL PROCESSING PIPELINE
------------------------------------------------------------

SignalDedupWorker

Purpose

Prevent duplicated signals.


SignalPersistenceWorker

Purpose

Buffer signals and stabilize event stream.


SignalRankingWorker

Purpose

Rank signals using alpha scoring model.


LiquidityFilterWorker

Purpose

Remove signals with insufficient liquidity.


StrategyAllocationWorker

Purpose

Allocate capital weights to strategies.


Published Event

allocation.signal


------------------------------------------------------------
PORTFOLIO DECISION LAYER
------------------------------------------------------------

Workers

PositionIntentWorker
CorrelationFilterWorker
PortfolioOptimizerWorker


Responsibilities

Resolve conflicts between strategies and optimize portfolio.


PositionIntentWorker

Select best signal candidate per symbol.


CorrelationFilterWorker

Prevent correlated exposure.


PortfolioOptimizerWorker

Select final signals based on optimizer score.


Optimizer Model

optimizer_score =
alpha
+ allocation_weight
+ liquidity factor
+ momentum factor
- volatility penalty


Published Event

optimized.signal


------------------------------------------------------------
EXECUTION ENGINE
------------------------------------------------------------

ExecutionWorker

Responsibilities

- validate risk conditions
- calculate position size
- enforce trading limits


Execution Constraints

max portfolio positions
max strategy positions
portfolio heat control
order rate control


OrderExecutorWorker

Responsibilities

Send orders to broker or exchange execution backend.


ExecutorRouter

Routes order requests to specific execution systems.

Possible executors

KIS executor
crypto exchange executor
future exchange executor


Published Events

ORDER_FILLED


------------------------------------------------------------
PORTFOLIO MANAGEMENT
------------------------------------------------------------

PortfolioWorker

Responsibilities

Track open positions and calculate PnL.


Published Events

portfolio.update
POSITION_OPENED
POSITION_CLOSED


TradeLedgerWorker

Responsibilities

Persist trade records and trade metrics.


------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

Workers

TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker
RiskWorker
StrategyKillSwitchWorker


Responsibilities

Manage portfolio risk and enforce exit conditions.


TrailingStopWorker

Dynamic trailing stop.


SignalDecayExitWorker

Exit when signal strength weakens.


PositionTimeStopWorker

Exit positions after maximum holding time.


RiskWorker

Monitor global risk constraints.


StrategyKillSwitchWorker

Disable underperforming strategies.


------------------------------------------------------------
SYSTEM MONITORING
------------------------------------------------------------

Workers

AnalyticsWorker
AlertWorker
KillSwitchWorker
HeartbeatWorker


AnalyticsWorker

Compute system statistics.


AlertWorker

Detect anomalies and notify system alerts.


KillSwitchWorker

Emergency trading shutdown.


HeartbeatWorker

Monitor system health and engine state.


------------------------------------------------------------
EVENT BUS
------------------------------------------------------------

QueueBus


Purpose

Asynchronous communication between workers.


Characteristics

multi-threaded event dispatch
queue based processing
worker decoupling
fault tolerant execution


------------------------------------------------------------
SYSTEM SCALE
------------------------------------------------------------

Workers                : 30+
Source files           : 120+
Event topics           : 50+


Architecture Type

event-driven trading engine
multi-strategy portfolio system
modular worker architecture


============================================================
END OF DOCUMENT
============================================================
