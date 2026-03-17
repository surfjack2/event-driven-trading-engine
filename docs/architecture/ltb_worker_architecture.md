# LTB Worker Architecture

LTB uses a multi-worker architecture where each worker is responsible for a specific role.

Workers run as independent threads.

--------------------------------------------------

Worker Categories

Market Workers

MarketWorker
ReplayMarketWorker

Indicator Workers

IndicatorWorker

Strategy Workers

StrategyWorker
SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker

Portfolio Workers

StrategyAllocationWorker
TradeQualityFilterWorker
PositionIntentWorker
PortfolioOptimizerWorker

Execution Workers

ExecutionWorker
OrderExecutorWorker

Risk Workers

RiskWorker

Analytics Workers

StrategyPerformanceWorker
AnalyticsWorker

Monitoring Workers

ValidationMonitorWorker
HeartbeatWorker

--------------------------------------------------

Advantages

Modular architecture

Independent worker responsibilities

Easy debugging

Scalable design
