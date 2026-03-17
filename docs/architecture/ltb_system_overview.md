# LTB System Overview

LTB is an event-driven trading engine built using modular worker components.

Each component runs independently and communicates through an internal event bus.

--------------------------------------------------

Worker Architecture

Workers are responsible for specific stages of the trading pipeline.

Example workers

MarketWorker
IndicatorWorker
StrategyWorker
SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker
StrategyAllocationWorker
TradeQualityFilterWorker
PositionIntentWorker
PortfolioOptimizerWorker
ExecutionWorker

--------------------------------------------------

Event Bus

Workers communicate using an internal event bus.

Example flow

strategy.signal
→ dedup.signal
→ persistent.signal
→ ranked.signal
→ allocation.signal
→ quality.signal
→ intent.signal
→ optimized.signal

--------------------------------------------------

Benefits

- loose coupling between modules
- improved testability
- easier system extension
- isolation of trading logic from infrastructure
