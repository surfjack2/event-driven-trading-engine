# LTB – Live Trading Bot

Event-driven quantitative trading engine built in Python.

LTB implements a modular trading pipeline including signal generation, ranking, portfolio optimization, risk management and execution.

The project focuses on system architecture design rather than short-term trading performance.

--------------------------------------------------

Project Motivation

Most retail trading bots rely on simple rule-based execution.

LTB explores a structured architecture similar to institutional trading systems.

Design goals

- event-driven architecture
- modular strategy pipeline
- signal ranking and filtering
- portfolio optimization
- risk controlled execution

--------------------------------------------------

System Architecture

Market Data
↓
Indicator Engine
↓
Strategy Engine
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
↓
Risk Engine

Each stage runs as an independent worker communicating through an internal event bus.

--------------------------------------------------

Core Components

Strategy Engine

Generates signals using multiple strategies.

Example strategies

- VWAP Reclaim
- VWAP Bounce
- Momentum Breakout

--------------------------------------------------

Signal Ranking

Signals are evaluated using a quantitative alpha model.

Factors

- VWAP distance
- momentum
- liquidity
- volatility penalty

Signals are normalized using tanh scaling.

--------------------------------------------------

Strategy Allocation

Capital is dynamically allocated across strategies.

Allocation considers

- strategy performance
- market regime
- liquidity regime

--------------------------------------------------

Portfolio Optimizer

Resolves conflicts between signals.

Responsibilities

- symbol conflict resolution
- strategy quota control
- portfolio diversification

--------------------------------------------------

Execution Engine

Handles order generation and risk checks.

Features

- ATR based stop calculation
- portfolio heat control
- strategy position limits
- signal decay guard

--------------------------------------------------

Trading Pipeline

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

--------------------------------------------------

Future Architecture Extensions

The LTB engine was designed with extensibility in mind.

Example extension

AI assisted code analysis using SonarQube and Local LLM.

Developer Code
↓
Git Repository
↓
SonarQube Analysis
↓
Code Quality Report
↓
LLM Analysis Layer
↓
Insights

Benefits

- automated code review
- architecture explanation
- strategy logic analysis
- security issue detection

--------------------------------------------------

Repository Structure

src/ltb
runtime/workers
strategy
risk
indicator

docs
architecture
strategy
operations
debugging

--------------------------------------------------

Development Focus

This project demonstrates

- event-driven system design
- modular trading engine architecture
- portfolio level risk management
- extensible system architecture

The emphasis is on engineering architecture rather than short-term trading profitability.

--------------------------------------------------

Author

Jack Go

21 years experience in IT / security engineering
Transitioning into quantitative trading system development

Note

Some strategy implementations and risk models are intentionally removed
from this public repository.

This project focuses on demonstrating the architecture of a
multi strategy event driven trading engine.

