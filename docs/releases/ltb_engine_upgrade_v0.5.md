# LTB Engine Upgrade v0.5

## 1. Upgrade Overview

This upgrade introduces a major improvement in the LTB trading engine pipeline.
The system moves closer to an institutional-grade architecture by introducing
portfolio construction layers, improved strategy allocation, and runtime stability.

Main goals of this upgrade:

- Stabilize execution pipeline
- Improve strategy signal quality
- Introduce portfolio construction layer
- Enable market regime based exposure control
- Improve VWAP-based strategy logic

---

## 2. Architecture Changes

Previous simplified pipeline:

market  
→ indicator  
→ strategy  
→ ranking  
→ execution  

New pipeline after upgrade:

market  
→ indicator  
→ strategy  
→ signal ranking  
→ liquidity filter  
→ strategy allocation  
→ position intent resolution  
→ portfolio optimizer  
→ execution  

This change introduces a dedicated **portfolio construction layer** between strategy
signals and the execution engine.

---

## 3. New Runtime Workers

The following workers were introduced or integrated into the pipeline:

- PositionIntentWorker  
  Resolves multiple strategy signals for the same symbol.

- PortfolioOptimizerWorker  
  Selects optimal signals based on allocation weight and volatility.

- CorrelationFilterWorker  
  Reduces correlated risk between positions.

- MarketCalendarWorker  
  Handles market open/close and holiday awareness.

- MarketSessionWorker  
  Controls trading phases such as premarket, open session, and closing session.

---

## 4. Risk & Exposure Improvements

Dynamic exposure management was introduced using market regime detection.

New components:

- MarketRegimeWorker  
  Detects market condition (bull / bear / sideways).

- ExposureWorker  
  Adjusts maximum portfolio exposure dynamically based on market regime.

Example exposure configuration:

bull market → higher exposure  
sideways market → moderate exposure  
bear market → reduced exposure

---

## 5. Strategy Improvements

VWAP-based strategies were refined.

Updated strategies:

- VWAP Reclaim Band Strategy
- VWAP Band Bounce Strategy

Enhancements include:

- better lower-band detection
- stronger volume confirmation
- improved signal validation

These improvements aim to reduce noise signals and increase trade quality.

---

## 6. Execution Stability Improvements

Execution pipeline improvements include:

- worker restart safety via watchdog
- order cooldown protection
- strategy-level position limits
- global exposure limits
- improved pending order tracking

This significantly reduces race conditions and duplicate order risks.

---

## 7. Current Engine Status

After this upgrade the LTB system now includes:

- event-driven worker architecture
- multi-strategy execution engine
- portfolio construction layer
- dynamic exposure management
- VWAP institutional-style strategies

The engine is now structurally ready for advanced liquidity-based scanners.

---

## 8. Next Development Phase

Next upgrades planned:

- Relative Turnover Scanner
- Liquidity Regime Detection
- Market session based scanner control
- advanced capital allocation model
- long-term position filtering based on fundamentals

These upgrades will significantly improve symbol selection and trading performance.

