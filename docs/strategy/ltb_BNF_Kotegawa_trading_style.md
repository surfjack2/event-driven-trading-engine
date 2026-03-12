============================================================
LTB STRATEGY SPEC PACKAGE
Strategy Name: BNF_METHOD
Origin: Takashi Kotegawa (BNF) Trading Style
============================================================

STRATEGY CONCEPT

BNF strategy is based on mean reversion and sector correlation.

Core idea

price deviates too far from moving average
→ probability of reversion increases


------------------------------------------------------------
INDICATORS
------------------------------------------------------------

MA25

25 day moving average


PRICE_DEVIATION

deviation =

(price - MA25) / MA25


RSI

period = 14


VOLUME

volume spike detection


------------------------------------------------------------
SETUP TYPE 1
MEAN REVERSION (BNF CORE)
------------------------------------------------------------

ENTRY CONDITION

price_deviation <= -20%

preferred range

-20% ~ -35%

penny stocks

-35% ~ -65%


FILTER

RSI < 30
volume stabilization


ENTRY

BUY


EXIT

price returns near MA25


STOP LOSS

additional drop > 10%


------------------------------------------------------------
SETUP TYPE 2
SECTOR LAGGARD TRADE
------------------------------------------------------------

CONCEPT

sector stocks move together

if one stock lags
→ catch-up move likely


ENTRY CONDITION

sector_index rising
AND

target_stock performance < sector


EXAMPLE

sector move

+5%

target stock

+1%


ENTRY

BUY laggard


EXIT

when price aligns with sector move


------------------------------------------------------------
SETUP TYPE 3
OVERSOLD REBOUND
------------------------------------------------------------

ENTRY CONDITION

large selloff

daily drop

> 10%

RSI < 30


VOLUME

capitulation volume


ENTRY

BUY rebound


EXIT

short-term bounce

5% ~ 15%


------------------------------------------------------------
RISK MANAGEMENT
------------------------------------------------------------

risk_per_trade

0.5% account


max_positions

5


max_daily_loss

3%


position_size

(account_equity * risk_per_trade)
/ stop_distance


------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

avoid

low liquidity
halted stocks
news manipulation


preferred

high volume stocks
high volatility stocks


------------------------------------------------------------
STRATEGY CHARACTERISTICS
------------------------------------------------------------

style

mean_reversion


timeframe

intraday
swing


holding period

2 days ~ 6 days


------------------------------------------------------------
WORKER INTEGRATION (LTB)
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

    ma25 = moving_average(price, 25)

    deviation = (price - ma25) / ma25

    if deviation <= -0.20:

        if rsi < 30:

            signal = BUY


------------------------------------------------------------
STRATEGY TAG
------------------------------------------------------------

type = mean_reversion
origin = BNF
style = contrarian
timeframe = multi-day

============================================================
END
============================================================
