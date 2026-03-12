MarketWorker → market.price

IndicatorWorker
    subscribe market.price
    publish indicator.update

StrategyWorker
    subscribe indicator.update
    publish strategy.signal

ExecutionWorker
    subscribe strategy.signal
    publish order.request

OrderExecutorWorker
    subscribe order.request
    publish ORDER_FILLED

PortfolioWorker
    subscribe ORDER_FILLED
    publish portfolio.update
