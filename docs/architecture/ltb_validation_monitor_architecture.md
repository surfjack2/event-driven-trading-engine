LTB VALIDATION MONITOR ARCHITECTURE
--------------------------------------------------

Overview

The Validation Monitor provides a real-time diagnostic interface
for the LTB trading engine.

It aggregates runtime events and renders a terminal dashboard
for monitoring engine health and trading activity.


--------------------------------------------------
ARCHITECTURE POSITION
--------------------------------------------------

The monitor operates as a runtime worker within the engine.

Worker name

ValidationMonitorWorker


Integration location

Runtime worker pipeline.


--------------------------------------------------
EVENT SOURCES
--------------------------------------------------

The monitor subscribes to multiple event topics.

market.price
strategy.signal
persistent.signal
ranked.signal
optimized.signal

ORDER_FILLED

POSITION_OPENED
POSITION_CLOSED

strategy.performance

market.regime
market.liquidity_regime
portfolio.exposure


--------------------------------------------------
DATA COLLECTION MODEL
--------------------------------------------------

The monitor maintains in-memory counters for:

event throughput
signal pipeline counts
portfolio state
strategy performance


--------------------------------------------------
DISPLAY LAYER
--------------------------------------------------

The CLI dashboard renders a single page terminal interface.

Sections include

Engine flow
Signal pipeline
Portfolio metrics
Trading statistics
Strategy performance
Market state
System diagnostics


--------------------------------------------------
CONSOLE OUTPUT POLICY
--------------------------------------------------

The console output is reserved exclusively for the monitor UI.

System logs are written to log files.

This design ensures that the monitor screen remains stable
and free from log interference.


--------------------------------------------------
REFRESH MECHANISM
--------------------------------------------------

The dashboard refreshes at a fixed interval.

Default

3 seconds


Rendering model

Full screen redraw.


--------------------------------------------------
SUPPORTED MODES
--------------------------------------------------

BACKTEST

Replay or simulated market data.


PAPER

Paper trading with exchange API.


LIVE

Live market execution.


--------------------------------------------------
END OF DOCUMENT
--------------------------------------------------
