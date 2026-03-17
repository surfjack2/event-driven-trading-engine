# LTB Project Summary (For Recruiters)

This document provides a short overview of the LTB project for technical reviewers and recruiters.

The goal is to quickly explain the purpose, architecture and engineering scope of the project.

--------------------------------------------------

Project Overview

LTB (Live Trading Bot) is an event-driven quantitative trading engine implemented in Python.

The system was designed to explore how a trading platform can be structured using modular architecture similar to institutional trading systems.

The project demonstrates system engineering concepts including

event-driven architecture
multi-stage signal processing
portfolio level decision making
risk controlled execution

--------------------------------------------------

Key Architecture Features

Event Driven System

The trading engine is composed of multiple independent workers communicating through an internal event bus.

This design reduces coupling between components and improves system scalability.

--------------------------------------------------

Signal Processing Pipeline

Trading signals pass through a validation pipeline before execution.

Pipeline stages

strategy.signal
dedup.signal
persistent.signal
ranked.signal
allocation.signal
quality.signal
intent.signal
optimized.signal
order.request

Each stage filters weak signals and improves decision quality.

--------------------------------------------------

Portfolio Decision Layer

Instead of executing signals directly, the system introduces a portfolio decision layer.

Responsibilities

strategy allocation
signal conflict resolution
portfolio diversification
position limits

This design prevents overexposure to individual strategies.

--------------------------------------------------

Execution and Risk Management

The execution engine converts signals into orders while applying risk controls.

Key risk checks

portfolio heat limits
maximum positions
strategy exposure
ATR based stop distance

--------------------------------------------------

System Components

Major engine components

MarketWorker
IndicatorWorker
StrategyWorker
SignalRankingWorker
StrategyAllocationWorker
PositionIntentWorker
PortfolioOptimizerWorker
ExecutionWorker
RiskWorker

Each component runs independently and communicates through events.

--------------------------------------------------

AI Assisted Development Architecture

The project also explores integrating static code analysis and AI tools.

Architecture

Developer Code
↓
Git Repository
↓
SonarQube Analysis
↓
Code Quality Report
↓
Local LLM Analysis
↓
Architecture Insights

This system assists development by generating explanations, documentation and security analysis.

The AI layer remains external to the trading engine to maintain deterministic trading behavior.

--------------------------------------------------

Engineering Focus

The project emphasizes engineering architecture rather than trading profitability.

Key focus areas

system architecture design
modular trading engine implementation
portfolio level decision logic
risk controlled execution

--------------------------------------------------

Technical Stack

Language

Python

Architecture

event-driven worker architecture

Key system concepts

multi-stage signal pipeline
portfolio optimizer
risk controlled execution

--------------------------------------------------

Author Background

Jack

21 years experience in IT and security engineering

Currently transitioning into quantitative trading system development.
