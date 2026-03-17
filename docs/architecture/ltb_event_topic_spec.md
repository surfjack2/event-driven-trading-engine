# LTB EVENT TOPIC SPECIFICATION
Event Bus Message Contract

본 문서는 LTB Event Bus에서 사용되는 모든 Event Topic의
Payload 구조를 정의한다.

Event는 Worker 간 통신의 유일한 인터페이스이다.

Event Contract 변경 시 반드시 본 문서를 업데이트해야 한다.

--------------------------------------------------
CORE MARKET EVENTS

Topic

market.price

Producer

MarketWorker

Consumers

IndicatorWorker
ValidationMonitorWorker

Payload

{
    symbol
    price
    timestamp
}

--------------------------------------------------

Topic

market.indicator

Producer

IndicatorWorker

Consumers

StrategyWorker
RelativeTurnoverScannerWorker
CorrelationFilterWorker
ExitWorkers

Payload

{
    symbol
    price
    prev_price

    vwap
    vwap_upper
    vwap_lower

    ema
    rsi

    atr
    volatility

    volume
    volume_ma

    price_change
}

--------------------------------------------------
SCANNER EVENTS

Topic

scanner.rtv

Producer

RelativeTurnoverScannerWorker

Consumers

AlphaRankingWorker
RankingWorker

Payload

{
    symbol
    price
    prev_price

    volume
    volume_ma

    turnover
    turnover_ma

    vwap
    atr
}

--------------------------------------------------

Topic

alpha.symbols

Producer

AlphaRankingWorker

Consumers

UniverseScannerWorker

Payload

{
    symbols
}

--------------------------------------------------

Topic

market.universe

Producer

UniverseScannerWorker

Consumers

StrategyWorker

Payload

{
    symbols
}

--------------------------------------------------

Topic

market.ranking

Producer

RankingWorker

Consumers

StrategyWorker

Payload

{
    symbols
}

--------------------------------------------------
STRATEGY EVENTS

Topic

strategy.signal

Producer

StrategyWorker

Consumers

SignalDedupWorker
ValidationMonitorWorker

Payload

{
    symbol
    strategy
    action

    price
    qty

    features
}

features

{
    rsi
    volume
    volume_ma
    volume_ratio

    vwap
    vwap_distance

    ema

    atr

    price_change
    volatility
}

--------------------------------------------------
SIGNAL PIPELINE EVENTS

Topic

dedup.signal

Producer

SignalDedupWorker

Consumers

SignalPersistenceWorker

Payload

strategy.signal payload

--------------------------------------------------

Topic

persistent.signal

Producer

SignalPersistenceWorker

Consumers

SignalRankingWorker

Payload

strategy.signal payload

--------------------------------------------------

Topic

ranked.signal

Producer

SignalRankingWorker

Consumers

StrategyAllocationWorker

Payload

{
    symbol
    strategy

    price
    qty

    alpha_score
    final_score

    features
}

--------------------------------------------------

Topic

allocation.signal

Producer

StrategyAllocationWorker

Consumers

PositionIntentWorker

Payload

ranked.signal payload +

{
    allocation_weight
}

--------------------------------------------------

Topic

intent.signal

Producer

PositionIntentWorker

Consumers

CorrelationFilterWorker

Payload

allocation.signal payload

--------------------------------------------------

Topic

filtered.intent

Producer

CorrelationFilterWorker

Consumers

PortfolioOptimizerWorker

Payload

allocation.signal payload

--------------------------------------------------

Topic

optimized.signal

Producer

PortfolioOptimizerWorker

Consumers

ExecutionWorker

Payload

{
    symbol
    strategy

    price
    qty

    optimizer_score

    allocation_weight
    alpha_score
}

--------------------------------------------------
EXECUTION EVENTS

Topic

order.request

Producer

ExecutionWorker
ExitWorkers

Consumers

OrderExecutorWorker
StrategyWorker
ValidationMonitorWorker

Payload

{
    symbol
    side
    price
    qty
}

--------------------------------------------------

Topic

ORDER_FILLED

Producer

OrderExecutorWorker

Consumers

PortfolioWorker
ExitWorkers
StrategyWorker
ValidationMonitorWorker

Payload

{
    symbol
    side

    price
    qty

    entry_price
    exit_price
}

--------------------------------------------------
PORTFOLIO EVENTS

Topic

portfolio.update

Producer

PortfolioWorker

Consumers

StrategyWorker
CorrelationFilterWorker
PortfolioOptimizerWorker
RiskWorker

Payload

{
    symbol
    position
}

--------------------------------------------------

Topic

POSITION_OPENED

Producer

PortfolioWorker

Consumers

ExitWorkers
TradeLedgerWorker

Payload

{
    symbol
    entry_price
    qty
    strategy
}

--------------------------------------------------

Topic

POSITION_CLOSED

Producer

PortfolioWorker

Consumers

ExitWorkers
TradeLedgerWorker
StrategyAllocationWorker

Payload

{
    symbol
    exit_price
    qty
    strategy
    pnl
}

--------------------------------------------------
ANALYTICS EVENTS

Topic

trade.closed

Producer

TradeLedgerWorker

Consumers

StrategyPerformanceWorker
RiskWorker

Payload

{
    symbol
    strategy
    entry_price
    exit_price
    qty
    pnl
}

--------------------------------------------------

Topic

strategy.performance

Producer

StrategyPerformanceWorker

Consumers

SignalRankingWorker
StrategyAllocationWorker
MetaStrategyWorker
ValidationMonitorWorker

Payload

{
    strategy
    stats
}

stats

{
    trades
    win_rate
    profit_factor
    pnl
    score
}

--------------------------------------------------
RISK EVENTS

Topic

risk.halt

Producer

RiskWorker

Consumers

ExecutionWorker
StrategyWorker

Payload

{
    reason
}

--------------------------------------------------

Topic

risk.resume

Producer

RiskWorker

Consumers

ExecutionWorker
StrategyWorker

Payload

{
    timestamp
}

--------------------------------------------------
SYSTEM EVENTS

Topic

system.alive

Producer

HeartbeatWorker

Consumers

Monitoring Systems

Payload

{
    timestamp
}

--------------------------------------------------

Topic

alert.notification

Producer

AlertWorker

Payload

{
    level
    message
}

--------------------------------------------------
EVENT DESIGN PRINCIPLES

Event Immutability

Event payload는 publish 이후 수정하지 않는다.

--------------------------------------------------

Loose Coupling

Worker는 Event Contract만 의존한다.

--------------------------------------------------

Event Driven Architecture

모든 Worker는 Event 기반으로 동작한다.

--------------------------------------------------

LTB ENGINE CLASSIFICATION

Event Driven Quant Trading Engine
