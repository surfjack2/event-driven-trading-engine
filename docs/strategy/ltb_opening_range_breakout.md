============================================================
LTB STRATEGY SPEC PACKAGE
============================================================

[STRATEGY 1]

NAME
OPENING_RANGE_BREAKOUT

CATEGORY
Breakout

TIMEFRAME
5m

OBJECTIVE
Capture early momentum by trading breakouts of the opening range.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

OPENING_RANGE

first 15 minutes high and low

VOLUME

volume confirmation

------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_DEFINE_RANGE

opening_high
opening_low


STEP2_BREAKOUT

breakout_up =
price > opening_high

breakout_down =
price < opening_low


STEP3_VOLUME_CONFIRMATION

volume > volume_ma * 1.5

------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

price > opening_high
AND
volume_confirmation

THEN

signal = BUY

------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

below opening_high

TAKE PROFIT

entry_price * 1.03

TIME EXIT

max_holding_time = 60 minutes

------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 1%

max_positions = 3

------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

ignore low volume stocks

------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

market_data_worker
indicator_engine
strategy_signal_worker
risk_manager
execution_worker

------------------------------------------------------------
PSEUDOCODE
------------------------------------------------------------

range = first_15min_range()

if price > range.high:

    signal = BUY

------------------------------------------------------------
BACKTEST REQUIREMENTS
------------------------------------------------------------

profit_factor > 1.5

------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

fake breakouts
sideways markets

------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = intraday
style = breakout
execution = market
timeframe = 5m

============================================================
END OF STRATEGY SPEC
============================================================
