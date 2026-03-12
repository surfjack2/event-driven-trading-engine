============================================================
LTB STRATEGY SPEC PACKAGE
============================================================

[STRATEGY 1]

NAME
GAP_FADE_REVERSAL

CATEGORY
Mean Reversion

TIMEFRAME
5m

OBJECTIVE
Trade reversal of extreme opening gaps.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

GAP_PERCENT

gap =
(today_open - yesterday_close) / yesterday_close

VWAP

------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_LARGE_GAP

gap_percent > 3%

STEP2_WEAK_CONTINUATION

price fails to continue trend

STEP3_VWAP_REJECTION

price crosses VWAP

------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

gap_up
AND
vwap_rejection

THEN

signal = SELL

------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

above gap high

TAKE PROFIT

gap fill level

------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 0.5%

------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

avoid earnings announcements

------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

market_data_worker
indicator_engine
strategy_worker
execution_worker

------------------------------------------------------------
PSEUDOCODE
------------------------------------------------------------

if gap > threshold and rejection:

    enter short

------------------------------------------------------------
BACKTEST REQUIREMENTS
------------------------------------------------------------

profit_factor > 1.4

------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

strong trend days

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
