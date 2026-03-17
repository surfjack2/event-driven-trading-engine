LTB Engine State Machine
Version: 2.0
Status: Architecture Reference


Purpose
-------

This document defines the operational state machine of the LTB
trading engine.

The state machine describes how the engine transitions between
different runtime states during system startup, market operation,
and risk events.

This provides a clear operational model for both system behavior
and monitoring tools.


High Level State Model
----------------------

The LTB engine operates through a sequence of states.

ENGINE_START
    │
    ▼
SYSTEM_READY
    │
    ▼
MARKET_WAIT
    │
    ▼
TRADING_ACTIVE
    │
    ▼
TRADING_HALTED
    │
    ▼
SYSTEM_SHUTDOWN


State Descriptions
------------------


ENGINE_START

The engine process is started.

Initialization steps:

• load configuration
• initialize event bus
• start workers
• initialize logging
• load strategies


SYSTEM_READY

The system is fully initialized.

The engine is waiting for market session signals.


MARKET_WAIT

The system is running but the market is not yet open.

Workers active:

• market data listener
• scanner
• indicator engine
• monitoring CLI


TRADING_ACTIVE

Normal trading operations.

Enabled components:

• strategy engine
• signal ranking
• portfolio optimizer
• execution engine

All trading signals may be processed and executed.


TRADING_HALTED

Trading has been halted by the risk engine or kill switch.

Typical triggers:

• daily loss limit exceeded
• system halt command
• critical runtime error

Actions:

• no new trades allowed
• open positions may be closed
• monitoring remains active


SYSTEM_SHUTDOWN

Engine shutdown sequence.

Typical steps:

• stop event ingestion
• close open positions
• flush logs
• terminate workers


State Transitions
-----------------

ENGINE_START → SYSTEM_READY

Occurs after successful initialization.


SYSTEM_READY → MARKET_WAIT

Occurs when system initialization is complete.


MARKET_WAIT → TRADING_ACTIVE

Triggered when market session worker detects
market open.


TRADING_ACTIVE → TRADING_HALTED

Triggered by:

risk_worker
strategy_kill_switch_worker
system halt event


TRADING_HALTED → SYSTEM_SHUTDOWN

Manual operator decision or system shutdown.


Operational Notes
-----------------

The Validation Monitor CLI reflects the current
engine state.

Example indicators:

status: RUNNING
status: HALTED (daily_loss_limit)


Future Expansion
----------------

Possible future states:

RESEARCH_MODE

Replay-based research environment.


SIMULATION_MODE

Paper trading environment without real execution.


Implementation Status
---------------------

The LTB engine currently implements the core behavior
described in this document through multiple runtime
workers.

This document formalizes the conceptual model.
