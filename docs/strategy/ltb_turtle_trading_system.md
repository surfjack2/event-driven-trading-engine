============================================================
LTB STRATEGY SPEC
Strategy Name: TURTLE_TREND
Origin: Turtle Trading System
============================================================

CONCEPT

Trend Following Strategy

Buy strength
Sell weakness


------------------------------------------------------------
INDICATORS
------------------------------------------------------------

DONCHIAN_CHANNEL

Upper = highest high (N)
Lower = lowest low (N)

Short-term N = 20
Long-term N = 55


ATR

ATR period = 20


------------------------------------------------------------
ENTRY RULES
------------------------------------------------------------

SYSTEM_1

BUY

price > 20 day high

SELL

price < 20 day low


SYSTEM_2

BUY

price > 55 day high

SELL

price < 55 day low


------------------------------------------------------------
EXIT RULES
------------------------------------------------------------

SYSTEM_1 EXIT

long exit

price < 10 day low

short exit

price > 10 day high


SYSTEM_2 EXIT

long exit

price < 20 day low

short exit

price > 20 day high


------------------------------------------------------------
POSITION SIZING
------------------------------------------------------------

N = ATR(20)

risk_per_trade

1% account


position_size

(account_equity * risk_per_trade)
/ (ATR * multiplier)


------------------------------------------------------------
PYRAMIDING
------------------------------------------------------------

add position every

0.5 ATR move


max_units

4


------------------------------------------------------------
STOP LOSS
------------------------------------------------------------

initial_stop

2 ATR


------------------------------------------------------------
MARKET FILTER
------------------------------------------------------------

prefer

high volatility markets
strong trends


avoid

sideways markets


------------------------------------------------------------
WORKER FLOW
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
STRATEGY TAG
------------------------------------------------------------

type = trend_following
style = breakout
timeframe = multi-day

============================================================
END
============================================================
