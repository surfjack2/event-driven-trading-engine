============================================================
LTB STRATEGY SPEC PACKAGE
Author: System Design Spec
Purpose: Live Trading Bot (LTB) Institutional Intraday Strategy
============================================================

[STRATEGY 1]
NAME
OPENING_RANGE_BREAKOUT

CATEGORY
Momentum / Breakout

TIMEFRAME
1m ~ 5m

OBJECTIVE
Capture institutional breakout momentum after the opening
range is established in the first minutes of market open.

This strategy exploits early session volatility and
institutional liquidity entering the market.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

OPENING RANGE

Opening range is defined as the price range during the
first 5 minutes after market open.

opening_high
opening_low


VWAP

VWAP = Σ(price * volume) / Σ(volume)

Used to confirm institutional bias.

Only long trades when price > VWAP.


VOLUME_MA

moving average of volume

period = 20 candles


ATR

Average True Range

Used for stop loss sizing and volatility filter.

period = 14


------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_OPENING_RANGE_BUILD

During market open

09:00 ~ 09:05

Track

opening_high
opening_low


STEP2_RANGE_COMPLETION

After 09:05

Opening range becomes fixed.


STEP3_BREAKOUT_DETECTION

breakout =

price > opening_high


STEP4_VOLUME_CONFIRMATION

volume > volume_ma


STEP5_VWAP_FILTER

price > vwap


STEP6_ATR_EXPANSION

ATR increasing compared to previous periods

ATR expansion confirms volatility expansion.


------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

time >= 09:05
AND
price > opening_high
AND
volume > volume_ma
AND
price > vwap
AND
ATR expanding

THEN

signal = BUY
order_type = MARKET


------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

entry_price - (ATR * 1.5)


TAKE PROFIT

entry_price + (ATR * 3)


VWAP EXIT

exit if price falls below VWAP


TIME EXIT

exit if position duration > 60 minutes


------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 0.5% account

max_positions = 3

max_daily_loss = 3% account


position_size

(account_equity * risk_per_trade) / stop_distance


------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

ignore if

volume < liquidity_threshold

or

market volatility too low


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

    if time < 09:05:

        update_opening_range()

    else:

        breakout = price > opening_high

        volume_confirm =
            volume > volume_ma

        vwap_confirm =
            price > vwap

        atr_expansion =
            atr_current > atr_previous

        if breakout
        and volume_confirm
        and vwap_confirm
        and atr_expansion:

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

win_rate > 45%
profit_factor > 1.7


------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

false breakout during low liquidity

range fakeouts during news spikes

midday low volatility


------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = intraday
style = breakout
execution = momentum
timeframe = 1m ~ 5m

============================================================
END OF STRATEGY SPEC
============================================================
