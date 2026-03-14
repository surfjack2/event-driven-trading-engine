# LTB Execution Model

ExecutionWorker is responsible for transforming optimized signals into actual trade orders.

Key Responsibilities:

Signal Validation
Risk validation through RiskEngine.

Portfolio Limits
Maximum open positions.
Maximum strategy exposure.

Strategy Performance Scaling
Position sizing multiplier based on strategy score.

Dynamic Position Sizing
Uses ATR stop distance to calculate risk per trade.

Execution Pipeline

optimized.signal
    ↓
ExecutionWorker
    ↓
RiskEngine validation
    ↓
PositionSizer calculation
    ↓
order.request
    ↓
OrderExecutorWorker
