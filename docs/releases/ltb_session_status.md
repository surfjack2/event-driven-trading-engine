LTB PROJECT SESSION STATE
=========================

Project
-------
Live Trading Bot (LTB)

Architecture
------------
Event-driven trading engine

Core components
---------------
Market Engine
Scanner Engine
Strategy Engine
Signal Engine
Portfolio Engine
Execution Engine
Risk Engine
Analytics Engine


Workers (major)
---------------
MarketWorker
MarketCalendarWorker
MarketSessionWorker
MarketRegimeWorker
LiquidityRegimeWorker
ExposureWorker
ScannerWorker
UniverseScannerWorker
RankingWorker
IndicatorWorker
StrategyWorker

SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker

LiquidityFilterWorker
StrategyAllocationWorker
PositionIntentWorker
CorrelationFilterWorker
PortfolioOptimizerWorker

ExecutionWorker
OrderExecutorWorker

PortfolioWorker
TradeLedgerWorker

TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker

RiskWorker
StrategyPerformanceWorker
StrategyKillSwitchWorker

AnalyticsWorker
AlertWorker
KillSwitchWorker
HeartbeatWorker


Exit systems
------------
1. TrailingStopWorker
2. SignalDecayExitWorker
3. PositionTimeStopWorker
4. PortfolioWorker time safety
5. RiskWorker kill switch


Current Mode
------------
BACKTEST


Market Data
-----------
Currently random market generator (MarketWorker)


Execution
---------
mock execution via ExecutorRouter


Capital
-------
Backtest capital = 10,000,000


Known TODO
----------
Replace MarketWorker with real market data
Implement broker API (KIS)
Account capital sync
Backtest dataset integration


Project State
-------------
Core engine architecture complete
Signal pipeline working
Execution pipeline working
Portfolio engine working
Risk engine working


Next Step
---------
Integrate real market data
