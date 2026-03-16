LTB ENGINE RUNTIME PIPELINE
===========================

Runtime Flow Overview
---------------------

Market Data
↓
Indicator Calculation
↓
Scanner Filtering
↓
Symbol Ranking
↓
Strategy Signal Generation
↓
Signal Processing
↓
Signal Filtering
↓
Portfolio Construction
↓
Execution
↓
Portfolio Tracking
↓
Risk Monitoring


Detailed Runtime Pipeline
-------------------------

1. Market Data

MarketWorker
publishes

market.price


2. Indicator Processing

IndicatorWorker
publishes

market.indicator


3. Strategy Signal

StrategyWorker
publishes

strategy.signal


4. Signal Pipeline

SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker


5. Signal Filtering

LiquidityFilterWorker
StrategyAllocationWorker


6. Portfolio Optimization

PositionIntentWorker
CorrelationFilterWorker
PortfolioOptimizerWorker


7. Execution

ExecutionWorker
OrderExecutorWorker
ExecutorRouter


8. Portfolio Engine

PortfolioWorker
TradeLedgerWorker


9. Exit Engine

TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker


10. Risk Engine

RiskWorker
StrategyKillSwitchWorker


11. Monitoring

AnalyticsWorker
AlertWorker
HeartbeatWorker


Runtime Characteristics
-----------------------

Fully event driven
Worker isolated architecture
Asynchronous execution
Multi-layer risk management


