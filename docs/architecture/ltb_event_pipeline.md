# LTB Event Pipeline

The LTB engine processes trading signals through a multi-stage pipeline.

Each stage refines signals before execution.

--------------------------------------------------

Signal Flow

Strategy Engine
↓
Signal Deduplication
↓
Signal Persistence
↓
Signal Ranking
↓
Strategy Allocation
↓
Trade Quality Filter
↓
Position Intent Resolution
↓
Portfolio Optimizer
↓
Execution Engine

--------------------------------------------------

Design Rationale

Breaking the system into multiple stages provides

- signal validation
- noise reduction
- portfolio level decision making

--------------------------------------------------

Advantages

Separation of concerns

signal generation
portfolio decision
execution

Each component can evolve independently.
