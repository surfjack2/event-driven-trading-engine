LTB CLI VALIDATION MONITOR
Operational Usage Guide
--------------------------------------------------

Purpose

Provide instructions for using the LTB Validation Monitor
to diagnose trading engine behavior and system health.


--------------------------------------------------
STARTING THE ENGINE
--------------------------------------------------

Run the engine

python main.py


The validation monitor runs automatically as part
of the engine worker system.


--------------------------------------------------
DASHBOARD REFRESH
--------------------------------------------------

The CLI dashboard refreshes automatically.

Refresh interval

3 seconds


--------------------------------------------------
CLI DASHBOARD SECTIONS
--------------------------------------------------

ENGINE

Displays engine runtime status

mode
uptime
worker count


--------------------------------------------------

EVENT FLOW

Displays runtime event throughput

ticks per second
signals per second
orders per minute


--------------------------------------------------

SIGNAL PIPELINE

Displays signal filtering stages

scanner symbols
strategy signals
ranked signals
optimized signals


--------------------------------------------------

PORTFOLIO

Displays portfolio state

active positions
capital
realized pnl
unrealized pnl


--------------------------------------------------

TRADING STATISTICS

Displays aggregated trading performance

total trades
win rate
profit factor
expectancy
max drawdown


--------------------------------------------------

STRATEGY PERFORMANCE

Displays per-strategy performance

strategy name
trade count
pnl
win rate
profit factor


--------------------------------------------------

SYSTEM HEALTH

Displays engine runtime stability

event queue size
event lag
error count


--------------------------------------------------

MARKET REGIME

Displays market environment state

trend regime
liquidity regime
portfolio exposure


--------------------------------------------------
DIAGNOSTIC WORKFLOW
--------------------------------------------------

Typical troubleshooting procedure

1. Check ENGINE status

Verify engine mode and uptime


2. Check EVENT FLOW

Ensure market data and signals are flowing


3. Check SIGNAL PIPELINE

Confirm signals are progressing through filters


4. Check PORTFOLIO

Verify positions and pnl behavior


5. Check STRATEGY PERFORMANCE

Identify strategy underperformance


6. Check SYSTEM HEALTH

Verify queue stability and error counts


--------------------------------------------------
SUPPORTED MODES
--------------------------------------------------

Validation monitor supports all runtime modes

BACKTEST
PAPER
LIVE


--------------------------------------------------
OPERATIONAL BENEFITS
--------------------------------------------------

Reduces dependency on log inspection

Provides real-time engine diagnostics

Accelerates debugging of trading logic

Improves monitoring during live trading


--------------------------------------------------
END OF DOCUMENT
--------------------------------------------------
