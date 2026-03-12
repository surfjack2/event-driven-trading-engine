# LTB Current Logic Flow

## Engine Runtime Flow

Trading Engine 실행 흐름

Engine Start

Worker Initialization

MarketWorker
IndicatorWorker
StrategyWorker
ExecutionWorker
OrderExecutorWorker
PortfolioWorker
TrailingStopWorker
RiskWorker


---

## Runtime Event Flow

MarketWorker

generate price

↓

IndicatorWorker

calculate indicators

↓

StrategyWorker

evaluate strategies

↓

ExecutionWorker

generate order request

↓

OrderExecutorWorker

execute order

↓

PortfolioWorker

update positions

↓

TrailingStopWorker

manage stop


---

## Risk Control Flow

portfolio.update

↓

RiskWorker

↓

risk check

↓

allow trading


또는

halt trading


---

## Alert Flow

system events

↓

AlertWorker

↓

notifications
