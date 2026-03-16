LTB WORKER EVENT MAP
Architecture

Event-driven trading engine

MARKET DATA LAYER

MarketWorker
↓ publish
market.price

IndicatorWorker
subscribe market.price
↓ publish
market.indicator




SCANNER LAYER

RelativeTurnoverScannerWorker
subscribe market.indicator
↓ publish
scanner.candidate

ScannerWorker
subscribe scanner.candidate
↓ publish
scanner.filtered

UniverseScannerWorker
subscribe scanner.filtered
↓ publish
universe.updated




RANKING LAYER

RankingWorker
subscribe universe.updated
↓ publish
ranking.symbols

AlphaRankingWorker
subscribe ranking.symbols
↓ publish
ranking.alpha




STRATEGY ENGINE

StrategyWorker
subscribe ranking.alpha
subscribe market.indicator
↓ publish
strategy.signal




SIGNAL PROCESSING PIPELINE

SignalDedupWorker
subscribe strategy.signal
↓ publish
dedup.signal

SignalPersistenceWorker
subscribe dedup.signal
↓ publish
persistent.signal

SignalRankingWorker
subscribe persistent.signal
↓ publish
ranked.signal




SIGNAL FILTERING

LiquidityFilterWorker
subscribe ranked.signal
↓ publish
liquidity.signal

StrategyAllocationWorker
subscribe liquidity.signal
↓ publish
filtered.intent




PORTFOLIO CONSTRUCTION

PositionIntentWorker
subscribe filtered.intent
↓ publish
position.intent

CorrelationFilterWorker
subscribe position.intent
↓ publish
position.filtered

PortfolioOptimizerWorker
subscribe position.filtered
↓ publish
order.request




EXECUTION ENGINE

ExecutionWorker
subscribe order.request
↓ publish
execution.order

OrderExecutorWorker
subscribe execution.order
↓ publish
ORDER_FILLED

ExecutorRouter
handles
- mock execution
- future broker execution




PORTFOLIO ENGINE

PortfolioWorker
subscribe ORDER_FILLED

BUY fill
↓ publish
POSITION_OPENED

SELL fill
↓ publish
POSITION_CLOSED




TRADE ACCOUNTING

TradeLedgerWorker
subscribe POSITION_OPENED
subscribe POSITION_CLOSED
↓ publish
trade.closed




EXIT ENGINE

TrailingStopWorker
subscribe POSITION_OPENED
subscribe market.indicator
↓ publish
order.request

SignalDecayExitWorker
subscribe POSITION_OPENED
subscribe market.indicator
↓ publish
order.request

PositionTimeStopWorker
subscribe POSITION_OPENED
↓ publish
order.request




RISK ENGINE

RiskWorker
subscribe portfolio.update
↓ publish
risk.alert

StrategyKillSwitchWorker
subscribe strategy.performance
↓ publish
strategy.disabled

KillSwitchWorker
subscribe risk.alert
↓ publish
risk.close_all




MONITORING & ANALYTICS

AnalyticsWorker
subscribe trade.closed
↓ publish
analytics.stats

AlertWorker
subscribe risk.alert
↓ alert

HeartbeatWorker
periodic system health monitoring




SYSTEM SUMMARY

Workers: 30+

Event Topics: 40+

Pipeline Layers

1 Market Data
2 Indicator
3 Scanner
4 Ranking
5 Strategy
6 Signal Processing
7 Portfolio Construction
8 Execution
9 Portfolio Tracking
10 Risk Control
11 Monitoring

Design Characteristics

Event-driven architecture
Worker isolation
Asynchronous execution
Multi-layer exit engine
Multi-layer risk system
