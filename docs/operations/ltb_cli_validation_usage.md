LTB CLI VALIDATION MONITOR
Operational Usage Guide
--------------------------------------------------

Purpose

Provide instructions for running the LTB engine and using the
Validation Monitor CLI dashboard.

The CLI monitor displays engine health, signal pipeline flow,
portfolio statistics, strategy performance, and system diagnostics
in a single screen.


--------------------------------------------------
ENGINE EXECUTION
--------------------------------------------------

The LTB engine is executed from the project root.

Execution command

PYTHONPATH=src python3 main.py [mode]


Supported modes

backtest
paper
live


Examples

PYTHONPATH=src python3 main.py backtest

PYTHONPATH=src python3 main.py paper

PYTHONPATH=src python3 main.py live


--------------------------------------------------
CONSOLE OUTPUT POLICY
--------------------------------------------------

The console is reserved exclusively for the Validation Monitor UI.

All system logs are written to log files.

Log directory

logs/


Examples

logs/engine.log
logs/market.log
logs/strategy.log
logs/trade.log
logs/risk.log


This separation ensures that the CLI monitor remains stable
without log interference.


--------------------------------------------------
CLI DASHBOARD STRUCTURE
--------------------------------------------------

The monitor displays a single page dashboard.

Sections

ENGINE FLOW
SIGNAL PIPELINE
PORTFOLIO
TRADING STATISTICS
STRATEGY PERFORMANCE
MARKET STATE
SYSTEM HEALTH


--------------------------------------------------
DASHBOARD REFRESH
--------------------------------------------------

The CLI dashboard refresh interval is 3 seconds.

The screen is redrawn each refresh cycle to prevent scrolling.


--------------------------------------------------
SUPPORTED RUNTIME MODES
--------------------------------------------------

BACKTEST

Uses replay data or simulated market ticks.


PAPER

Connects to exchange paper trading environment.


LIVE

Connects to real market data and live execution systems.


--------------------------------------------------
OPERATIONAL BENEFITS
--------------------------------------------------

Real-time engine diagnostics.

Reduced dependency on log inspection.

Fast detection of strategy and pipeline failures.

Unified monitoring interface for development and live trading.


--------------------------------------------------
END OF DOCUMENT
--------------------------------------------------
