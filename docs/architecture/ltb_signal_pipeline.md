# LTB Signal Pipeline

The signal pipeline is the core alpha generation path of the LTB trading engine.

Market data flows through several processing layers that progressively filter and rank trading opportunities.

Pipeline Flow:

MarketWorker
    ↓
IndicatorWorker
    ↓
RelativeTurnoverScannerWorker
    ↓
AlphaRankingWorker
    ↓
StrategyWorker
    ↓
SignalDedupWorker
    ↓
SignalRankingWorker
    ↓
LiquidityFilterWorker
    ↓
StrategyAllocationWorker
    ↓
PositionIntentWorker
    ↓
CorrelationFilterWorker
    ↓
PortfolioOptimizerWorker
    ↓
ExecutionWorker
    ↓
OrderExecutorWorker

Each layer performs a specific function:

MarketWorker
Generates market price and volume events.

IndicatorWorker
Calculates indicators such as RSI, EMA, VWAP, ATR.

RelativeTurnoverScannerWorker
Identifies symbols with abnormal turnover relative to moving average.

AlphaRankingWorker
Ranks symbols based on liquidity and volatility driven alpha.

StrategyWorker
Evaluates trading strategies and generates signals.

SignalDedupWorker
Removes duplicate signals within a defined time window.

SignalRankingWorker
Ranks signals across strategies based on scoring models.

LiquidityFilterWorker
Filters signals that do not meet liquidity requirements.

StrategyAllocationWorker
Assigns capital allocation weights based on strategy performance.

PositionIntentWorker
Resolves competing strategy signals for the same symbol.

CorrelationFilterWorker
Prevents correlated positions from entering simultaneously.

PortfolioOptimizerWorker
Selects final signals based on portfolio constraints.

ExecutionWorker
Performs risk validation and generates orders.

OrderExecutorWorker
Sends orders to the broker execution layer.
