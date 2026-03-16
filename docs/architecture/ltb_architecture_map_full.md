LTB FULL ARCHITECTURE MAP
=========================

Project
-------
Live Trading Bot (LTB)

Architecture Type
-----------------
Event-driven trading engine

Core System Layers
------------------

1. Market Layer
2. Scanner Layer
3. Strategy Layer
4. Signal Processing Layer
5. Portfolio Optimization Layer
6. Execution Layer
7. Risk Management Layer
8. Analytics Layer
9. Monitoring Layer


Worker Architecture
-------------------

Market Layer
------------
MarketWorker
MarketCalendarWorker
MarketSessionWorker
MarketRegimeWorker
LiquidityRegimeWorker


Scanner Layer
-------------
RelativeTurnoverScannerWorker
ScannerWorker
UniverseScannerWorker
RankingWorker
AlphaRankingWorker


Indicator Layer
---------------
IndicatorWorker


Strategy Layer
--------------
StrategyWorker


Signal Processing
-----------------
SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker


Signal Filtering
----------------
LiquidityFilterWorker
StrategyAllocationWorker


Portfolio Construction
----------------------
PositionIntentWorker
CorrelationFilterWorker
PortfolioOptimizerWorker


Execution Engine
----------------
ExecutionWorker
OrderExecutorWorker


Portfolio Engine
----------------
PortfolioWorker
TradeLedgerWorker


Exit Engine
-----------
TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker


Risk Engine
-----------
RiskWorker
StrategyPerformanceWorker
StrategyKillSwitchWorker


Analytics & Monitoring
----------------------
AnalyticsWorker
AlertWorker
KillSwitchWorker
HeartbeatWorker


System Characteristics
----------------------

Event Bus Architecture
Worker Isolation
Asynchronous Processing
Modular Strategy Engine
Multi-layer Risk Controls


Current Architecture Complexity
-------------------------------

Workers: 30+
Event Topics: 40+
Execution Layers: 7
Exit Systems: 5


Conclusion
----------

LTB is designed as a modular event-driven trading engine.
The architecture supports scalability, strategy isolation,
and risk-layer separation.


