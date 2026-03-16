LTB CURRENT LOGIC FLOW
======================

Market Data
-----------

MarketWorker
↓
market.price


Indicator Processing
--------------------

IndicatorWorker
↓
market.indicator


Scanner Layer
-------------

RelativeTurnoverScannerWorker
ScannerWorker
UniverseScannerWorker


Ranking Layer
-------------

RankingWorker
AlphaRankingWorker


Strategy Layer
--------------

StrategyWorker
↓
strategy.signal


Signal Processing
-----------------

SignalDedupWorker
↓
SignalPersistenceWorker
↓
SignalRankingWorker


Signal Filtering
----------------

LiquidityFilterWorker
↓
StrategyAllocationWorker


Portfolio Construction
----------------------

PositionIntentWorker
↓
CorrelationFilterWorker
↓
PortfolioOptimizerWorker


Execution
---------

ExecutionWorker
↓
OrderExecutorWorker
↓
ExecutorRouter
↓
ORDER_FILLED


Portfolio Tracking
------------------

PortfolioWorker
↓
POSITION_OPENED
↓
TradeLedgerWorker


Exit Engine
-----------

TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker


Risk Layer
----------

RiskWorker
StrategyKillSwitchWorker


Monitoring
----------

AnalyticsWorker
AlertWorker
HeartbeatWorker


