============================================================
LTB STRATEGY SPEC PACKAGE
Author: System Design Spec
Purpose: Live Trading Bot (LTB) Intraday Strategy Implementation
============================================================

[STRATEGY 1]
NAME
VWAP_VOLUME_BREAKOUT

CATEGORY
Momentum / Breakout

TIMEFRAME
5m

OBJECTIVE
Detect institutional entry signals via volume spike and VWAP support,
then enter breakout momentum trades.

------------------------------------------------------------
INDICATOR REQUIREMENTS
------------------------------------------------------------

VWAP
VWAP = Σ(price * volume) / Σ(volume)
reset: intraday

VOLUME_MA
moving average of volume
period = 20 candles

AVG_BODY
average candle body size
period = 20 candles

------------------------------------------------------------
SIGNAL CONDITIONS
------------------------------------------------------------

STEP1_VOLUME_SPIKE

volume_spike =
current_volume > volume_ma * 2


STEP2_MOMENTUM_CANDLE

momentum_candle =
candle_body > avg_body * 1.5


STEP3_PULLBACK

pullback_detected if

price retrace <= 50% of impulse move
AND
pullback candles <= 3
AND
volume decreasing


STEP4_VWAP_SUPPORT

low_price >= vwap
OR
abs(price - vwap) <= 0.3%


STEP5_BREAKOUT

current_price > impulse_high
AND
current_volume > previous_volume


------------------------------------------------------------
ENTRY LOGIC
------------------------------------------------------------

IF

volume_spike == TRUE
AND
momentum_candle == TRUE
AND
pullback_detected == TRUE
AND
vwap_support == TRUE
AND
breakout == TRUE

THEN

signal = BUY
order_type = MARKET


------------------------------------------------------------
EXIT LOGIC
------------------------------------------------------------

STOP LOSS

entry_price * 0.985


TAKE PROFIT

entry_price * 1.03


TIME EXIT

max_holding_time = 30 minutes


------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade = 0.5% account

max_positions = 3

max_daily_loss = 3% account

position_size =
(account_equity * risk_per_trade) / stop_distance


------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

ignore if

volume < minimum_liquidity_threshold

or

halted stock

or

spread too wide


recommended universe

top volume stocks


------------------------------------------------------------
WORKER INTEGRATION
------------------------------------------------------------

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

    data = get_5m_data(symbol)

    vwap = calc_vwap(data)
    volume_ma = moving_average(data.volume, 20)
    avg_body = moving_average(data.body, 20)

    volume_spike = data.volume[-1] > volume_ma * 2

    momentum_candle = data.body[-1] > avg_body * 1.5

    pullback_detected = detect_pullback(data)

    vwap_support =
        data.low[-1] >= vwap
        or abs(data.close[-1] - vwap) <= 0.003

    breakout =
        data.close[-1] > impulse_high
        and data.volume[-1] > data.volume[-2]

    if (
        volume_spike
        and momentum_candle
        and pullback_detected
        and vwap_support
        and breakout
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

win_rate > 45%
profit_factor > 1.5


------------------------------------------------------------
KNOWN WEAKNESSES
------------------------------------------------------------

sideways markets
fake breakout traps
news driven spikes


------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = intraday
style = momentum
execution = breakout
timeframe = 5m

============================================================
END OF STRATEGY SPEC
============================================================
