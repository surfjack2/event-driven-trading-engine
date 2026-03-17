# LTB Trading Engine Design Decisions

This document explains the key engineering decisions made during the design of the LTB trading engine.

The goal of the project was not only to implement trading strategies but also to design a robust trading system architecture.

--------------------------------------------------

Design Objective

The main objective of LTB was to explore how a trading engine can be structured using modular architecture.

Key design goals

- modular system design
- event-driven communication
- pipeline based signal validation
- portfolio level decision making
- controlled risk exposure

--------------------------------------------------

Why Event Driven Architecture

A trading engine contains many independent subsystems.

Examples

market data ingestion  
indicator calculation  
strategy evaluation  
portfolio decisions  
execution  

Using direct function calls between components would tightly couple the system.

Instead, LTB uses an event-driven architecture.

Advantages

loose coupling  
easier testing  
clear processing pipeline  
independent worker modules  

Workers subscribe to events and publish new events after processing.

--------------------------------------------------

Why Multi-Stage Signal Pipeline

Many retail trading bots send signals directly to execution.

This approach can create problems

weak signals reaching execution  
duplicate signals  
overlapping strategy signals  

LTB solves this by introducing a signal validation pipeline.

Signal stages

strategy.signal
dedup.signal
persistent.signal
ranked.signal
allocation.signal
quality.signal
intent.signal
optimized.signal

Each stage performs additional validation.

--------------------------------------------------

Why Separate Portfolio Decision Layer

Trading signals alone should not decide portfolio actions.

The system introduces a dedicated portfolio decision layer.

Responsibilities

strategy allocation  
signal conflict resolution  
position limits  
portfolio diversification  

This ensures that the system manages trades at a portfolio level rather than a signal level.

--------------------------------------------------

Why Portfolio Optimizer

Multiple strategies may generate signals for the same symbol.

Without an optimizer the engine may

open redundant positions  
overexpose a strategy  
ignore stronger signals  

The PortfolioOptimizerWorker selects the best candidate signals.

Criteria include

alpha score  
strategy weight  
momentum  
liquidity  

--------------------------------------------------

Why Risk Management Before Execution

Risk management must occur before sending orders.

The LTB execution engine performs several checks

portfolio heat limit  
max positions  
strategy exposure  
risk engine validation  

These checks prevent excessive portfolio risk.

--------------------------------------------------

Why Modular Workers

Instead of building a single large trading engine loop, LTB splits responsibilities across workers.

Benefits

smaller modules  
clear responsibilities  
easier debugging  
simpler architecture evolution  

Each worker focuses on a single responsibility.

--------------------------------------------------

Why AI Is Not Part of Execution

AI assisted tools are used only for development and analysis.

Examples

SonarQube static analysis  
LLM architecture explanation  
strategy code analysis  

AI components are intentionally kept outside the execution engine.

Reasons

deterministic trading behavior  
reproducible backtests  
reduced operational risk  

--------------------------------------------------

Future Architecture Extensions

Because the system is modular, additional components can be integrated.

Examples

market regime classifier  
advanced portfolio optimizer  
strategy clustering analysis  
AI assisted research tools  

New modules can subscribe to events without modifying the core engine.

--------------------------------------------------

Summary

The LTB project demonstrates how a trading system can be engineered using modular architecture.

Key architectural concepts

event-driven design  
multi-stage signal validation  
portfolio-level decision engine  
risk controlled execution  
extensible worker architecture
