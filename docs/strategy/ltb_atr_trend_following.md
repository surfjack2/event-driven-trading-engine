============================================================
LTB STRATEGY SPEC PACKAGE
Author: System Design Spec
Purpose: Live Trading Bot (LTB) Institutional Trend Strategy
============================================================

[STRATEGY 1]
NAME
ATR_TREND_FOLLOWING

CATEGORY
Trend Following

TIMEFRAME
5m ~ 15m

OBJECTIVE
Capture sustained market trends using volatility expansion
and ATR-based trailing stop.

This strategy follows institutional trend entries rather than
predicting reversals.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

EMA_FAST
Exponential Moving Average

period = 20


EMA_SLOW
Exponential Moving Average

period = 50


ATR
Average True Range

period = 14


VOLUME_MA
Moving average of volume

period = 20


VWAP
Volume Weighted Average Price


------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_TREND_FILTER

trend_up =

EMA_FAST > EMA_SLOW


STEP2_PRICE_CONFIRMATION

price > EMA_FAST


STEP3_ATR_EXPANSION

ATR increasing compared to previous ATR

ATR_current > ATR_previous


STEP4_VOLUME_CONFIRMATION

volume > volume_ma


STEP5_VWAP_CONFIRMATION

price > vwap


------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

EMA_FAST > EMA_SLOW
AND
price > EMA_FAST
AND
ATR expanding
AND
volume > volume_ma
AND
price > vwap

THEN

signal = BUY
order_type = MARKET


------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

ATR TRAILING STOP

stop_price =

highest_price - (ATR * 2)


EMA BREAKDOWN

exit if

price < EMA_FAST


TIME EXIT

exit if position duration > 4 hours


------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 0.5% account

max_positions = 5

max_daily_loss = 3% account


position_size

(account_equity * risk_per_trade) / stop_distance


------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

ignore if

volume < liquidity_threshold

or

ATR too small (low volatility)


recommended universe

top 100~200 volume stocks


------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

market_worker
    ↓

indicator_worker
    ↓

scanner_worker
    ↓

universe_scanner_worker
    ↓

strategy_worker
    ↓

strategy_allocation_worker
    ↓

execution_worker
    ↓

order_executor_worker


------------------------------------------------------------
PSEUDOCODE
------------------------------------------------------------

for symbol in universe:

    ema_fast = ema(symbol, 20)
    ema_slow = ema(symbol, 50)

    atr = atr(symbol)

    if ema_fast <= ema_slow:
        continue

    price_confirm =
        price > ema_fast

    atr_expansion =
        atr_current > atr_previous

    volume_confirm =
        volume > volume_ma

    vwap_confirm =
        price > vwap

    if (
        price_confirm
        and atr_expansion
        and volume_confirm
        and vwap_confirm
    ):

        signal = BUY


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

win_rate > 40%
profit_factor > 1.8


------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

sideways markets

sudden news reversals

false breakouts in low liquidity


------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = intraday
style = trend following
execution = breakout continuation
timeframe = 5m ~ 15m

============================================================
END OF STRATEGY SPEC
============================================================
