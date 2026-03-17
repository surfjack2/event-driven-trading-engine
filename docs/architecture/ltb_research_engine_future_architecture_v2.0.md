LTB Research Engine Future Architecture
Version: 2.0
Status: Design Proposal (Future Expansion)


Purpose
-------

This document describes a future architecture for expanding the LTB platform
from a live trading engine into a quantitative research platform.

The goal is to enable large-scale strategy experimentation and evaluation
without impacting the stability of the live trading engine.

This architecture is not part of the current implementation and is recorded
as a long-term design reference.


Current System Scope
--------------------

The current LTB platform is designed primarily for live trading.

Core capabilities include:

• event-driven trading engine
• real-time market data processing
• strategy execution
• signal ranking
• portfolio optimization
• execution routing
• runtime monitoring CLI


The current system typically operates a small number of strategies
(2–5 live strategies).


Motivation for Research Engine
------------------------------

Future development may require large scale strategy experimentation.

Example scenarios:

• testing 100+ strategies simultaneously
• parameter optimization
• historical market replay
• statistical evaluation of strategies

To support these workflows safely, research execution must be isolated
from the live trading engine.


Architecture Separation
-----------------------

The future platform architecture is divided into two major layers.


LTB Platform

LIVE TRADING ENGINE
RESEARCH ENGINE


The live engine remains responsible for real-time trading,
while the research engine operates independently on historical data.


Research Engine High Level Architecture
---------------------------------------

Historical Market Data
        │
        ▼
Replay Engine
        │
        ▼
Indicator Engine
        │
        ▼
Strategy Pool (100+ strategies)
        │
        ▼
Signal Capture
        │
        ▼
Trade Simulation
        │
        ▼
Performance Evaluation
        │
        ▼
Research Result Storage


Replay Engine
-------------

The replay engine simulates historical market data as if it were
real-time market events.

This allows reuse of the same event-driven pipeline used by the
live trading engine.


Strategy Pool
-------------

The research engine runs a large pool of strategies simultaneously.

Each strategy operates on the same replayed market data stream.

Each strategy maintains its own independent simulated portfolio.


Trade Simulation
----------------

Trades are executed in a simulated environment.

The simulator handles:

• order execution logic
• slippage assumptions
• transaction costs
• position tracking
• PnL calculation


Strategy Evaluation Metrics
---------------------------

Each strategy is evaluated using statistical metrics.

Typical metrics include:

• win rate
• profit factor
• expectancy
• maximum drawdown
• sharpe ratio
• trade count


Meta Strategy Allocation
------------------------

In future iterations, a meta-strategy layer may allocate capital
dynamically to the best performing strategies.

Example concept:

capital allocation ∝ strategy score


Integration with Live Engine
----------------------------

The research engine does not execute live trades.

Instead, research results inform the selection of strategies
that are deployed in the live trading engine.


Future Possibilities
--------------------

Potential future capabilities include:

• automated strategy discovery
• machine learning strategy ranking
• parameter search
• strategy evolution
• multi-market research


Implementation Status
---------------------

This architecture is not implemented in the current LTB platform.

The document exists as a design reference for future development.
