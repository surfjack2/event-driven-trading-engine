# LTB FULL EVENT TOPOLOGY MAP
Worker ↔ Event ↔ Worker

LTB는 Event Bus 기반 Event Driven Trading Engine이다.

모든 Worker는 Event Topic을 통해 통신하며
Producer / Consumer 구조로 연결된다.

--------------------------------------------------

CORE EVENT BUS

QueueBus

역할

Event routing
Worker decoupling
Async pipeline execution

--------------------------------------------------

MARKET DATA FLOW

Broker API
    │
    ▼
MarketWorker
    │
    ▼
market.price
    │
    ▼
IndicatorWorker
    │
    ▼
market.indicator

--------------------------------------------------

SCANNER FLOW

market.indicator
    │
    ▼
RelativeTurnoverScannerWorker
    │
    ▼
scanner.rtv

scanner.rtv
    │
    ▼
AlphaRankingWorker
    │
    ▼
alpha.symbols

alpha.symbols
    │
    ▼
UniverseScannerWorker
    │
    ▼
market.universe

--------------------------------------------------

RANKING FLOW

scanner.rtv
    │
    ▼
RankingWorker
    │
    ▼
market.ranking

--------------------------------------------------

STRATEGY FLOW

market.indicator
market.ranking
market.universe
        │
        ▼
StrategyWorker
        │
        ▼
strategy.signal

--------------------------------------------------

SIGNAL PIPELINE

strategy.signal
        │
        ▼
SignalDedupWorker
        │
        ▼
dedup.signal

dedup.signal
        │
        ▼
SignalPersistenceWorker
        │
        ▼
persistent.signal

persistent.signal
        │
        ▼
SignalRankingWorker
        │
        ▼
ranked.signal

ranked.signal
        │
        ▼
StrategyAllocationWorker
        │
        ▼
allocation.signal

allocation.signal
        │
        ▼
TradeQualityFilterWorker
        │
        ▼
quality.signal

quality.signal
        │
        ▼
PositionIntentWorker
        │
        ▼
intent.signal

intent.signal
        │
        ▼
CorrelationFilterWorker
        │
        ▼
filtered.intent

filtered.intent
        │
        ▼
PortfolioOptimizerWorker
        │
        ▼
optimized.signal

--------------------------------------------------

EXECUTION FLOW

optimized.signal
        │
        ▼
ExecutionWorker
        │
        ▼
order.request

order.request
        │
        ▼
OrderExecutorWorker
        │
        ▼
ORDER_FILLED

--------------------------------------------------

PORTFOLIO FLOW

ORDER_FILLED
        │
        ▼
PortfolioWorker
        │
        ├─ POSITION_OPENED
        └─ POSITION_CLOSED

--------------------------------------------------

EXIT SYSTEM

market.indicator
POSITION_OPENED
        │
        ▼
TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker
        │
        ▼
order.request

--------------------------------------------------

RISK SYSTEM

portfolio.update
trade.closed
        │
        ▼
RiskWorker
        │
        ├─ risk.halt
        └─ risk.resume

--------------------------------------------------

ANALYTICS SYSTEM

trade.closed
portfolio.update
        │
        ▼
TradeLedgerWorker
        │
        ▼
strategy.performance

strategy.performance
        │
        ▼
StrategyPerformanceWorker
        │
        ▼
strategy.performance.update

--------------------------------------------------

META STRATEGY LAYER

strategy.performance
        │
        ▼
MetaStrategyWorker
        │
        ├─ strategy.disabled
        └─ strategy.enabled

--------------------------------------------------

SYSTEM MONITORING

system events
        │
        ▼
AnalyticsWorker

AlertWorker

KillSwitchWorker

HeartbeatWorker

ValidationMonitorWorker

--------------------------------------------------

DATA STORAGE

Tick Storage

Trade Journal

Performance Metrics

Event Log

--------------------------------------------------

SYSTEM CHARACTERISTICS

Architecture

Event Driven
Multi Worker
Async Queue

--------------------------------------------------

ENGINE LOOPS

Market Loop
1s

Strategy Loop
3s

System Loop
5~10s

--------------------------------------------------

WORKER COUNT

Market Layer
Indicator Layer
Scanner Layer
Strategy Layer
Portfolio Layer
Execution Layer
Risk Layer
Analytics Layer
System Layer

총 Worker 수

40+

--------------------------------------------------

LTB ENGINE CLASSIFICATION

Event Driven Quant Trading Engine

--------------------------------------------------
