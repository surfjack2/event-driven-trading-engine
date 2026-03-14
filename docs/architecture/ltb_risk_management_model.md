# LTB Risk Management Model

Risk management in LTB is implemented across multiple layers.

Layer 1: Position Sizing
PositionSizer calculates position size using risk based sizing.

Layer 2: Risk Engine
RiskEngine validates:

Maximum open positions
Maximum symbol exposure
Daily loss limits

Layer 3: Portfolio Constraints
PortfolioOptimizerWorker limits total positions.

Layer 4: Correlation Filter
Prevents entering highly correlated symbols simultaneously.

Layer 5: Strategy Kill Switch
StrategyKillSwitchWorker disables underperforming strategies.

Layer 6: Global Kill Switch
KillSwitchWorker closes all positions in emergency scenarios.
