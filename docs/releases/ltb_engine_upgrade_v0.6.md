# LTB Engine Upgrade v0.6

## Release Summary

Version 0.6 focuses on stabilizing the signal pipeline and improving execution safety.

This release introduces improvements to signal filtering, ranking, exit logic, and strategy allocation.

---

# Major Changes

## Signal Pipeline Improvements

New worker introduced:

SignalPersistenceWorker

Updated pipeline:

strategy.signal  
→ dedup.signal  
→ ranked.signal  
→ allocation.signal  
→ optimized.signal

Purpose

- filter transient signals
- improve signal reliability
- stabilize signal ranking

---

# Ranking Model Improvements

SignalRankingWorker updated.

New scoring model includes:

- momentum factor
- VWAP displacement
- volume ratio
- price expansion
- volatility penalty

Goal

Improve alpha signal selection quality.

---

# Exit Logic Stabilization

Exit logic improved to prevent premature exits.

Changes

- minimum hold time enforcement
- pending order guard
- prevention of duplicate exit triggers

Affected workers

- TrailingStopWorker
- SignalDecayExitWorker

---

# Strategy Allocation Improvements

Strategy allocation logic updated.

Features

- dynamic weight allocation
- strategy performance feedback
- automatic strategy disable on large drawdown

Worker

StrategyAllocationWorker

---

# Infrastructure Updates

Watchdog worker updated to improve worker lifecycle stability.

Workers can now recover automatically from runtime failures.

---

# Repository Changes

Added

- SignalPersistenceWorker

Removed

- tree.txt

Updated

- signal ranking logic
- strategy worker pipeline
- exit logic workers
- watchdog worker configuration

---

# Next Release Roadmap

Next development phase will focus on observability and operational tooling.

Planned features

- analytics event worker
- metrics storage layer
- CLI monitoring dashboard
- web monitoring dashboard
- macro data integration
- news and filings monitoring
- alert management system

---

# Version Notes

Version 0.6 represents a major stabilization milestone for the LTB trading engine.

Core architecture is now considered stable.

Future releases will focus primarily on monitoring, analytics, and operational tools.
