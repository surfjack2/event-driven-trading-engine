LTB ENGINE UPGRADE STATUS v0.7
Engine Stabilization and Execution Safeguards
--------------------------------------------------

Commit Reference

9f45292 engine cleanup: remove dead strategy engine, add ATR filter, integrate strategy performance ranking
bcb6512 engine: risk integration, execution safeguards, strategy position limit, order rate control
4f4321d LTB engine upgrade: VWAP alpha ranking, portfolio optimization tuning, execution pipeline stabilization


Current Engine Status

LTB trading engine has transitioned from prototype stage to a stable event-driven multi-worker architecture.

Core characteristics

- event driven architecture
- worker based pipeline
- portfolio level optimization
- strategy performance feedback
- dynamic position sizing
- risk managed execution


Trading Pipeline

MarketWorker
IndicatorWorker
StrategyWorker
SignalDedupWorker
SignalPersistenceWorker
SignalRankingWorker
LiquidityFilterWorker
StrategyAllocationWorker
PositionIntentWorker
CorrelationFilterWorker
PortfolioOptimizerWorker
ExecutionWorker
OrderExecutorWorker
PortfolioWorker
TradeLedgerWorker


Risk Layer Workers

TrailingStopWorker
SignalDecayExitWorker
PositionTimeStopWorker
RiskWorker
StrategyKillSwitchWorker


System Monitoring Workers

AnalyticsWorker
AlertWorker
KillSwitchWorker
HeartbeatWorker


Execution Engine Improvements

execution safeguards

- portfolio heat control
- strategy position limit
- global order rate limit
- ATR based stop distance

dynamic capital allocation

strategy performance → execution multiplier


Strategy Multiplier Model

score >= 2.0 → multiplier 1.4
score >= 1.5 → multiplier 1.2
score >= 1.0 → multiplier 1.0
score >= 0.5 → multiplier 0.7
score < 0.5  → multiplier 0.4


Signal Ranking Model

alpha score components

- trend alignment
- momentum
- liquidity pressure
- volatility penalty

normalization

z-score normalization
range clamp [-3, 3]

ranking output feeds portfolio optimizer


Portfolio Optimization Logic

optimizer_score calculation

optimizer_score =
alpha * 0.6
+ allocation_weight * 0.4
+ momentum factor
+ liquidity factor
- volatility penalty


selection constraints

- max portfolio positions
- strategy quota
- risk exposure


Risk Controls

MAX_PORTFOLIO_HEAT = 0.06

MAX_STRATEGY_POSITIONS = 2

GLOBAL_ORDER_INTERVAL = 0.3 seconds

daily loss protection exists inside RiskEngine


Current Development Plan

1 Mode architecture refinement
2 Strategy tuning
3 Exchange integration (Upbit)
4 CLI backtest interface
5 Key management
6 Web UI
7 Automated trading report


Current Progress

Mode architecture          70%
Strategy tuning            80%
Exchange integration        0%
CLI backtest UI             0%
Key management              0%
Web UI                      0%
Auto trading report         0%


System Scale

workers          : 30+
source files     : 120+
event topics     : 50+


Immediate Next Tasks

1 finalize mode separation (BACKTEST / PAPER / LIVE)
2 remove remaining mock/random market components
3 calibrate alpha scoring model
4 integrate exchange API layer


End of Document
