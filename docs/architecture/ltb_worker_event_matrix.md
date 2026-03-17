# LTB WORKER EVENT MATRIX
Worker ↔ Event Contract Map

본 문서는 LTB 엔진의 Worker 간 Event Contract를 정의한다.

각 Worker는 다음 두 가지 역할을 가진다.

SUBSCRIBE
이벤트 소비

PUBLISH
이벤트 생성

이 문서는 엔진의 이벤트 흐름을 빠르게 이해하기 위한 핵심 문서이다.

--------------------------------------------------
EVENT BUS

QueueBus

역할

Worker 간 비동기 이벤트 전달
이벤트 기반 파이프라인 구성

--------------------------------------------------
MARKET DATA LAYER

Worker

MarketWorker

Subscribe

Broker API

Publish

market.price

--------------------------------------------------

IndicatorWorker

Subscribe

market.price

Publish

market.indicator

--------------------------------------------------
SCANNER LAYER

RelativeTurnoverScannerWorker

Subscribe

market.indicator

Publish

scanner.rtv

--------------------------------------------------

AlphaRankingWorker

Subscribe

scanner.rtv

Publish

alpha.symbols

--------------------------------------------------

UniverseScannerWorker

Subscribe

alpha.symbols

Publish

market.universe

--------------------------------------------------

RankingWorker

Subscribe

scanner.rtv

Publish

market.ranking

--------------------------------------------------
STRATEGY LAYER

StrategyWorker

Subscribe

market.indicator
market.ranking
market.universe
portfolio.update
ORDER_FILLED

Publish

strategy.signal

--------------------------------------------------
SIGNAL PIPELINE

SignalDedupWorker

Subscribe

strategy.signal

Publish

dedup.signal

--------------------------------------------------

SignalPersistenceWorker

Subscribe

dedup.signal

Publish

persistent.signal

--------------------------------------------------

SignalRankingWorker

Subscribe

persistent.signal
strategy.performance

Publish

ranked.signal
ranking.pass
ranking.reject

--------------------------------------------------

StrategyAllocationWorker

Subscribe

ranked.signal
POSITION_CLOSED
strategy.performance
market.regime
market.liquidity_regime

Publish

allocation.signal
strategy.disabled

--------------------------------------------------

PositionIntentWorker

Subscribe

allocation.signal

Publish

intent.signal

--------------------------------------------------

CorrelationFilterWorker

Subscribe

intent.signal
market.indicator
portfolio.update

Publish

filtered.intent

--------------------------------------------------

PortfolioOptimizerWorker

Subscribe

filtered.intent
portfolio.update

Publish

optimized.signal

--------------------------------------------------
EXECUTION LAYER

ExecutionWorker

Subscribe

optimized.signal

Publish

order.request

--------------------------------------------------

OrderExecutorWorker

Subscribe

order.request

Publish

ORDER_FILLED

--------------------------------------------------
PORTFOLIO LAYER

PortfolioWorker

Subscribe

ORDER_FILLED

Publish

portfolio.update
POSITION_OPENED
POSITION_CLOSED

--------------------------------------------------
EXIT SYSTEM

TrailingStopWorker

Subscribe

POSITION_OPENED
market.indicator

Publish

order.request

--------------------------------------------------

SignalDecayExitWorker

Subscribe

POSITION_OPENED
POSITION_CLOSED
market.indicator
ORDER_FILLED

Publish

order.request

--------------------------------------------------

PositionTimeStopWorker

Subscribe

POSITION_OPENED
POSITION_CLOSED
market.indicator
ORDER_FILLED

Publish

order.request

--------------------------------------------------
RISK LAYER

RiskWorker

Subscribe

portfolio.update
trade.closed

Publish

risk.halt
risk.resume

--------------------------------------------------
ANALYTICS LAYER

TradeLedgerWorker

Subscribe

POSITION_OPENED
POSITION_CLOSED

Publish

trade.closed
strategy.performance

--------------------------------------------------

StrategyPerformanceWorker

Subscribe

trade.closed

Publish

strategy.performance

--------------------------------------------------
SYSTEM LAYER

AnalyticsWorker

Subscribe

system events

Publish

analytics.report

--------------------------------------------------

AlertWorker

Subscribe

alert events

Publish

alert.notification

--------------------------------------------------

KillSwitchWorker

Subscribe

risk.halt

Publish

system.shutdown

--------------------------------------------------

HeartbeatWorker

Subscribe

system heartbeat

Publish

system.alive

--------------------------------------------------

ValidationMonitorWorker

Subscribe

market.price
strategy.signal
order.request
ORDER_FILLED
ranking.pass
ranking.reject
strategy.performance

Publish

monitor.display

--------------------------------------------------
ENGINE CHARACTERISTICS

Architecture

Event Driven
Multi Worker
Async Queue
Loose Coupling

--------------------------------------------------

ENGINE WORKER COUNT

Market Layer
Indicator Layer
Scanner Layer
Strategy Layer
Signal Pipeline
Execution Layer
Portfolio Layer
Risk Layer
Analytics Layer
System Layer

Total Workers

40+

--------------------------------------------------

ENGINE CLASSIFICATION

Event Driven Quant Trading Engine
