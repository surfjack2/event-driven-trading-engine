LTB VALIDATION MONITOR CLI DESIGN
--------------------------------------------------

Purpose

Provide a real-time terminal dashboard for the LTB trading engine.

The CLI monitor aggregates runtime events and displays
system state information in a single screen.


--------------------------------------------------
CONSOLE DESIGN PRINCIPLE
--------------------------------------------------

The terminal console is dedicated to the Validation Monitor UI.

System logs are written to log files instead of stdout.

This prevents the monitor display from being disrupted by log output.


--------------------------------------------------
DISPLAY STRUCTURE
--------------------------------------------------

The dashboard is rendered as a single page.

Sections

ENGINE FLOW
SIGNAL PIPELINE
PORTFOLIO
TRADING STATISTICS
STRATEGY PERFORMANCE
MARKET STATE
SYSTEM HEALTH


--------------------------------------------------
ENGINE FLOW
--------------------------------------------------

Shows event throughput metrics.

ticks_per_second
signals_per_second
orders_per_minute
fills_per_minute


--------------------------------------------------
SIGNAL PIPELINE
--------------------------------------------------

Displays the number of signals passing through each stage.

scanner
strategy
dedup
persistent
ranked
optimized


--------------------------------------------------
PORTFOLIO
--------------------------------------------------

Displays portfolio status.

positions
capital
realized_pnl
unrealized_pnl
portfolio_heat


--------------------------------------------------
TRADING STATISTICS
--------------------------------------------------

Aggregated trading metrics.

total_trades
win_rate
profit_factor
expectancy
max_drawdown


--------------------------------------------------
STRATEGY PERFORMANCE
--------------------------------------------------

Per-strategy statistics.

strategy
trades
win_rate
profit_factor
pnl


--------------------------------------------------
MARKET STATE
--------------------------------------------------

Market environment indicators.

trend_regime
liquidity_regime
portfolio_exposure


--------------------------------------------------
SYSTEM HEALTH
--------------------------------------------------

Engine diagnostics.

event_queue_size
error_count
worker_restarts


--------------------------------------------------
COLOR INDICATORS
--------------------------------------------------

GREEN

Normal operation.


YELLOW

Warning condition.


RED

Critical condition requiring investigation.


--------------------------------------------------
SCREEN REFRESH MODEL
--------------------------------------------------

The monitor uses a full-screen redraw approach.

Each refresh clears the terminal and redraws the dashboard.

This prevents scrolling and maintains a stable UI layout.


--------------------------------------------------
REFRESH INTERVAL
--------------------------------------------------

Default refresh interval

3 seconds


--------------------------------------------------
END OF DOCUMENT
--------------------------------------------------
