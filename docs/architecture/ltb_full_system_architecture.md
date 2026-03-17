# LTB Full System Architecture

LTB is a modular event-driven quantitative trading engine.

The system is designed using multiple independent workers connected through an internal event bus.

This architecture allows each component of the trading pipeline to evolve independently while maintaining system stability.

--------------------------------------------------

System Overview

Market Data
↓
Indicator Engine
↓
Strategy Engine
↓
Signal Processing Pipeline
↓
Portfolio Decision Engine
↓
Execution Engine
↓
Risk Management
↓
Analytics and Monitoring

--------------------------------------------------

Architecture Philosophy

The LTB architecture follows three design principles.

1. Event Driven Design

All components communicate through events instead of direct dependencies.

This decouples modules and improves maintainability.

2. Pipeline Signal Processing

Trading signals pass through multiple validation stages before execution.

This prevents weak signals from reaching the execution engine.

3. Separation of Concerns

Signal generation, portfolio decisions and execution logic are separated into different workers.

--------------------------------------------------

Worker Architecture

The engine runs multiple worker threads.

Each worker subscribes to specific events and publishes new events after processing.

Worker Categories

Market Layer

MarketWorker
ReplayMarketWorker

Indicator Layer

IndicatorWorker

Strategy Layer

StrategyWorker

Signal Processing Layer

SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker

Portfolio Decision Layer

StrategyAllocationWorker
TradeQualityFilterWorker
PositionIntentWorker
PortfolioOptimizerWorker

Execution Layer

ExecutionWorker
OrderExecutorWorker

Risk Layer

RiskWorker

Analytics Layer

StrategyPerformanceWorker
AnalyticsWorker

Monitoring Layer

ValidationMonitorWorker
HeartbeatWorker

--------------------------------------------------

Signal Pipeline

Trading signals pass through a validation pipeline before execution.

strategy.signal
↓
dedup.signal
↓
persistent.signal
↓
ranked.signal
↓
allocation.signal
↓
quality.signal
↓
intent.signal
↓
optimized.signal
↓
order.request

Each stage performs additional validation and filtering.

--------------------------------------------------

Signal Ranking Model

Signals are evaluated using an alpha scoring model.

Factors used

VWAP distance
momentum
liquidity
volatility penalty

Alpha values are normalized using tanh scaling.

--------------------------------------------------

Portfolio Decision System

The portfolio decision system ensures that the final trades satisfy portfolio level constraints.

Responsibilities

Signal conflict resolution
Strategy quota enforcement
Portfolio diversification
Position limit control

This stage prevents over-exposure to a single strategy.

--------------------------------------------------

Execution Engine

The execution engine is responsible for translating trading signals into orders.

Key features

ATR based stop distance
portfolio heat control
strategy position limits
signal decay guard

Orders are submitted through the order execution worker.

--------------------------------------------------

Risk Management

Risk control is applied before order submission.

Risk checks include

portfolio heat limits
maximum positions
per strategy exposure
risk engine validation

These checks prevent excessive portfolio risk.

--------------------------------------------------

AI Assisted Development Architecture

The LTB project also includes an optional AI assisted development layer.

This system integrates SonarQube with a Local LLM to analyze the codebase.

Developer Code
↓
Git Repository
↓
SonarQube Analysis
↓
Code Quality Report
↓
LLM Analysis
↓
Insights

Possible outputs

code architecture explanations
security issue detection
automatic documentation
strategy logic analysis

This AI layer is external to the trading engine to maintain deterministic trading behavior.

--------------------------------------------------

Extensibility

The architecture is designed to support future extensions.

Examples

AI assisted strategy analysis
automated strategy diagnostics
market regime classification
advanced portfolio optimization

Because the system is event-driven, new workers can be added without modifying the core pipeline.

--------------------------------------------------

Summary

The LTB architecture demonstrates how a trading engine can be structured using modular event-driven components.

Key characteristics

event-driven system
multi-stage signal pipeline
portfolio-level decision engine
risk controlled execution
extensible architecture
