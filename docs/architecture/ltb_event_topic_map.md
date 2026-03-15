LTB EVENT TOPIC MAP
Event Bus Communication Reference
--------------------------------------------------


Overview

LTB engine components communicate using an asynchronous event bus (QueueBus).

Workers subscribe to event topics and publish new events after processing.

This document lists the primary event topics used across the system.


--------------------------------------------------
MARKET EVENTS
--------------------------------------------------

market.price

published by
MarketWorker

consumed by
IndicatorWorker


MARKET_TICK

published by
MarketWorker

consumed by
ScannerWorker
AlphaRankingWorker
MarketRegimeWorker
LiquidityRegimeWorker


--------------------------------------------------
INDICATOR EVENTS
--------------------------------------------------

market.indicator

published by
IndicatorWorker

consumed by
StrategyWorker


--------------------------------------------------
STRATEGY EVENTS
--------------------------------------------------

strategy.signal

published by
StrategyWorker

consumed by
SignalDedupWorker


--------------------------------------------------
SIGNAL PIPELINE EVENTS
--------------------------------------------------

persistent.signal

published by
SignalPersistenceWorker

consumed by
SignalRankingWorker


ranked.signal

published by
SignalRankingWorker

consumed by
LiquidityFilterWorker


liquidity.signal

published by
LiquidityFilterWorker

consumed by
StrategyAllocationWorker


allocation.signal

published by
StrategyAllocationWorker

consumed by
PositionIntentWorker


intent.signal

published by
PositionIntentWorker

consumed by
CorrelationFilterWorker


filtered.intent

published by
CorrelationFilterWorker

consumed by
PortfolioOptimizerWorker


optimized.signal

published by
PortfolioOptimizerWorker

consumed by
ExecutionWorker


--------------------------------------------------
EXECUTION EVENTS
--------------------------------------------------

order.request

published by
ExecutionWorker
PortfolioWorker (exit orders)

consumed by
OrderExecutorWorker


ORDER_FILLED

published by
OrderExecutorWorker

consumed by
PortfolioWorker
ExecutionWorker


--------------------------------------------------
PORTFOLIO EVENTS
--------------------------------------------------

portfolio.update

published by
PortfolioWorker

consumed by
ExecutionWorker
PortfolioOptimizerWorker


POSITION_OPENED

published by
PortfolioWorker


POSITION_CLOSED

published by
PortfolioWorker

consumed by
StrategyPerformanceWorker


--------------------------------------------------
STRATEGY PERFORMANCE EVENTS
--------------------------------------------------

strategy.performance

published by
StrategyPerformanceWorker

consumed by
ExecutionWorker
StrategyAllocationWorker


strategy.disabled

published by
StrategyKillSwitchWorker

consumed by
ExecutionWorker


--------------------------------------------------
RISK EVENTS
--------------------------------------------------

risk.close_all

published by
RiskWorker

consumed by
PortfolioWorker


system.halt

published by
KillSwitchWorker

consumed by
ExecutionWorker


--------------------------------------------------
SYSTEM EVENTS
--------------------------------------------------

market.regime

published by
MarketRegimeWorker

consumed by
StrategyAllocationWorker


market.liquidity_regime

published by
LiquidityRegimeWorker

consumed by
StrategyAllocationWorker


--------------------------------------------------
ENGINE MONITORING EVENTS
--------------------------------------------------

analytics.update

published by
AnalyticsWorker


alert.event

published by
AlertWorker


heartbeat

published by
HeartbeatWorker


--------------------------------------------------
END OF DOCUMENT
--------------------------------------------------
