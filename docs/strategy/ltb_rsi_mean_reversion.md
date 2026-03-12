============================================================
LTB STRATEGY SPEC PACKAGE
Author: System Design Spec
Purpose: Live Trading Bot (LTB) Intraday Strategy Implementation
============================================================

[STRATEGY 1]

NAME
RSI_MEAN_REVERSION

CATEGORY
Mean Reversion

TIMEFRAME
5m

OBJECTIVE
Exploit short-term overbought and oversold conditions using RSI
to capture price reversion back to the mean.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

RSI
period = 14

OPTIONAL

Bollinger Bands
period = 20
std = 2

------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_OVERSOLD

oversold =
RSI < 30


STEP2_PRICE_STABILIZATION

price_stabilization =
last_candle_close > previous_candle_close


STEP3_MEAN_TARGET

target_zone =
RSI >= 50


------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

RSI < 30
AND
price_stabilization == TRUE

THEN

signal = BUY
order_type = MARKET

------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

entry_price * 0.985


TAKE PROFIT

RSI >= 50
OR
entry_price * 1.02


TIME EXIT

max_holding_time = 60 minutes

------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 0.5% account

max_positions = 5

position_size =
(account_equity * risk_per_trade) / stop_distance

------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

ignore if

strong trend detected
or
high volatility news event

recommended universe

large cap stocks
high liquidity instruments

------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

market_data_worker
    ↓
indicator_engine (RSI)
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

    rsi = calculate_rsi(symbol)

    if rsi < 30 and price_reversal_detected:

        signal = BUY

------------------------------------------------------------
BACKTEST REQUIREMENTS
------------------------------------------------------------

metrics

win_rate
profit_factor
max_drawdown

recommended baseline

win_rate > 50%
profit_factor > 1.3

------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

strong trending markets
persistent downtrends

------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = intraday
style = mean_reversion
execution = market
timeframe = 5m

============================================================
END OF STRATEGY SPEC
============================================================
