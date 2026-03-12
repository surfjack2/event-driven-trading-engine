============================================================
LTB STRATEGY SPEC PACKAGE
============================================================

[STRATEGY 1]

NAME
ATR_TREND_FOLLOW

CATEGORY
Trend Following

TIMEFRAME
15m

OBJECTIVE
Follow strong trends using ATR-based breakout and trailing stops.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

ATR
period = 14

EMA
period = 50

------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_TREND_DIRECTION

trend_up =
price > ema50

STEP2_BREAKOUT

price > previous_high

STEP3_VOLATILITY

atr expanding

------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

trend_up
AND
breakout
AND
atr_expanding

THEN

signal = BUY

------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

entry_price - 1 ATR

TRAILING STOP

highest_price - 2 ATR

------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 1%

------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

ignore low volatility periods

------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

market_data_worker
indicator_engine
strategy_worker
risk_worker
execution_worker

------------------------------------------------------------
PSEUDOCODE
------------------------------------------------------------

if trend and breakout:

    enter_trade()

------------------------------------------------------------
BACKTEST REQUIREMENTS
------------------------------------------------------------

profit_factor > 1.6

------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

whipsaw markets

------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = trend
style = breakout
execution = market
timeframe = 15m

============================================================
END OF STRATEGY SPEC
============================================================
