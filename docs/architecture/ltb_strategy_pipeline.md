# LTB Strategy Pipeline

Strategies operate after alpha selection.

Strategies included:

simple_momentum
vwap_reclaim
vwap_bounce

StrategyWorker evaluates strategies on each market indicator event.

Generated signals pass through the following layers:

SignalDedupWorker
Prevents duplicate signals.

SignalRankingWorker
Ranks signals by strategy-specific scoring.

LiquidityFilterWorker
Ensures sufficient liquidity.

StrategyAllocationWorker
Applies dynamic capital weighting.

PositionIntentWorker
Resolves conflicts between strategies.
