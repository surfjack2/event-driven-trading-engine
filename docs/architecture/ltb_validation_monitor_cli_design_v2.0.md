LTB Validation Monitor CLI Architecture
Version: 2.0
Status: Active

Purpose
-------

The Validation Monitor CLI provides real-time operational visibility
into the LTB runtime engine.

The monitor is designed to support:

• live trading validation
• engine diagnostics
• strategy monitoring
• risk state visibility
• pipeline event tracing

The CLI is implemented using the Rich Live Layout system.


Architecture Overview
---------------------

The CLI monitor is composed of multiple runtime panels.

Layout structure:

HEADER

Market Regime

Account | Engine Flow
Pipeline | Ranking
Recent Signals | Optimizer
Execution | Strategy Performance
Engine Diagnostics | Worker Health


Panel Description
-----------------

Account

Displays account level metrics.

capital
equity
daily pnl
weekly pnl
monthly pnl
open positions


Engine Flow

Displays core event flow metrics.

ticks
signals
orders
fills


Pipeline

Displays signal pipeline event counters.

rtv
ranking
dedup
persist
allocation


Ranking

Displays ranking decision results.

ranking pass
ranking reject


Recent Signals

Displays recently generated strategy signals.

symbol
strategy
RSI
volume ratio
VWAP distance
price change


Optimizer

Displays portfolio optimizer selections.


Execution

Displays order routing and execution decisions.


Strategy Performance

Displays aggregated strategy metrics.

trades
win rate
profit factor
pnl


Engine Diagnostics

Displays runtime engine health metrics.

event rate
queue depth
event latency


Worker Health

Displays worker heartbeat monitoring.

Each worker emits periodic heartbeat events.

Worker lag is calculated as:

current_time - last_heartbeat


Future Expansion
----------------

The CLI monitor will be expanded to support:

• strategy sharpe ratio
• trade expectancy
• worker latency histogram
• event queue backlog visualization
