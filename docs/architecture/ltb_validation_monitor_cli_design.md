LTB VALIDATION MONITOR CLI DESIGN
--------------------------------------------------

Purpose

Provide a real-time diagnostic dashboard for the LTB engine.

The monitor aggregates runtime events and displays system state,
signal pipeline health, portfolio statistics, strategy performance,
and system diagnostics in a single CLI page.

The dashboard refreshes automatically every 3 seconds.


--------------------------------------------------
DISPLAY STRUCTURE
--------------------------------------------------

The CLI monitor displays a single page with the following sections:

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

Displays event throughput.

Metrics

ticks_per_second
signals_per_second
orders_per_minute
fills_per_minute


--------------------------------------------------
SIGNAL PIPELINE
--------------------------------------------------

Displays the number of signals passing through each layer.

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

Displays aggregated trading performance.

total_trades
win_rate
profit_factor
expectancy
max_drawdown


--------------------------------------------------
STRATEGY PERFORMANCE
--------------------------------------------------

Displays per-strategy performance.

strategy_name
trades
win_rate
profit_factor
pnl


--------------------------------------------------
MARKET STATE
--------------------------------------------------

Displays market environment.

trend_regime
liquidity_regime
portfolio_exposure


--------------------------------------------------
SYSTEM HEALTH
--------------------------------------------------

Displays engine diagnostics.

event_queue_size
error_count
worker_restarts


--------------------------------------------------
COLOR CODING
--------------------------------------------------

The CLI dashboard uses color indicators.

GREEN
normal operation

YELLOW
warning condition

RED
critical condition


Example thresholds

profit_factor

GREEN  > 1.5
YELLOW 1.2 – 1.5
RED    < 1.2


win_rate

GREEN  > 0.50
YELLOW 0.40 – 0.50
RED    < 0.40


portfolio_heat

GREEN  < 0.05
YELLOW 0.05 – 0.08
RED    > 0.08


event_queue_size

GREEN  < 1000
YELLOW 1000 – 3000
RED    > 3000


--------------------------------------------------
REFRESH INTERVAL
--------------------------------------------------

The dashboard refresh interval is 3 seconds.


--------------------------------------------------
SUPPORTED MODES
--------------------------------------------------

The monitor supports all engine modes.

BACKTEST
PAPER
LIVE


--------------------------------------------------
BENEFITS
--------------------------------------------------

Provides a real-time overview of the trading engine.

Eliminates the need for extensive log inspection.

Accelerates debugging and system validation.

Supports both development and live trading monitoring.

--------------------------------------------------
END OF DOCUMENT
