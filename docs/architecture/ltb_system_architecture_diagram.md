# LTB System Architecture Diagram

This document visualizes the overall architecture of the LTB trading engine.

The system is built using a modular event-driven pipeline.

Each component runs as an independent worker and communicates through an internal event bus.

--------------------------------------------------

System Architecture Diagram

```mermaid
flowchart TD

Market[Market Worker]
Indicator[Indicator Worker]

Strategy[Strategy Worker]

Dedup[Signal Dedup Worker]
Persist[Signal Persistence Worker]
Ranking[Signal Ranking Worker]

Allocation[Strategy Allocation Worker]
Quality[Trade Quality Filter Worker]
Intent[Position Intent Worker]
Optimizer[Portfolio Optimizer Worker]

Execution[Execution Worker]
OrderExec[Order Executor Worker]

Risk[Risk Worker]

Analytics[Analytics Worker]
Monitor[Validation Monitor Worker]

Market --> Indicator
Indicator --> Strategy

Strategy --> Dedup
Dedup --> Persist
Persist --> Ranking

Ranking --> Allocation
Allocation --> Quality
Quality --> Intent
Intent --> Optimizer

Optimizer --> Execution
Execution --> OrderExec

Execution --> Risk

Execution --> Analytics
Analytics --> Monitor
