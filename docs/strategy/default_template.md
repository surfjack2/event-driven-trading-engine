============================================================
LTB STRATEGY SPEC PACKAGE
Author: System Design Spec
Purpose: Live Trading Bot (LTB) Strategy Implementation
============================================================

[STRATEGY 1]

NAME
STRATEGY_NAME

CATEGORY
Momentum / Breakout / Trend / MeanReversion

TIMEFRAME
1m / 5m / 15m / 1h / Daily

OBJECTIVE
Describe the core trading objective of the strategy.

Example:
Capture breakout momentum after institutional volume entry.


------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

List all indicators required.

Example

VWAP
RSI
EMA
ATR
Volume MA

Define formulas if necessary.


------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_CONDITION_NAME

condition_expression


STEP2_CONDITION_NAME

condition_expression


STEP3_CONDITION_NAME

condition_expression


STEP4_CONDITION_NAME

condition_expression


------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

condition_1 == TRUE
AND
condition_2 == TRUE
AND
condition_3 == TRUE

THEN

signal = BUY or SELL
order_type = MARKET / LIMIT


------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

define stop logic

example

entry_price * 0.985


TAKE PROFIT

define take profit logic


TIME EXIT

maximum holding time


------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade

example

0.5% account


max_positions


max_daily_loss


position_size_formula

example

(account_equity * risk_per_trade) / stop_distance


------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

Define conditions where strategy should NOT trade.

Example

low liquidity
halted stock
extreme spread
news volatility


recommended universe

example

top volume stocks
index components
scanner results


------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

Define how the strategy fits inside LTB architecture.

Example

market_data_worker
    ↓
indicator_engine
    ↓
strategy_signal_worker
    ↓
risk_manager
    ↓
order_execution_worker


------------------------------------------------------------
PSEUDOCODE
------------------------------------------------------------

for symbol in universe:

    data = get_market_data(symbol)

    indicators = calculate_indicators(data)

    if entry_conditions:

        signal = BUY or SELL


------------------------------------------------------------
BACKTEST REQUIREMENTS
------------------------------------------------------------

metrics

win_rate
profit_factor
max_drawdown
avg_holding_time
expectancy


recommended baseline

example

win_rate > 45%
profit_factor > 1.5


------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

List typical failure conditions.

Example

sideways market
fake breakouts
low liquidity


------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = intraday / swing / trend
style = breakout / momentum / reversion
execution = market / limit
timeframe = 5m / 15m / daily

============================================================
END OF STRATEGY SPEC
============================================================
