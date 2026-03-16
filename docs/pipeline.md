# LTB Signal Pipeline

market.indicator

↓

strategy_worker

↓

strategy.signal

↓

signal_dedup_worker

↓

dedup.signal

↓

signal_persistence_worker

↓

persistent.signal

↓

signal_ranking_worker

↓

ranked.signal

↓

strategy_allocation_worker

↓

allocation.signal

↓

trade_quality_filter_worker

↓

quality.signal

↓

position_intent_worker

↓

intent.signal

↓

correlation_filter_worker

↓

filtered.intent

↓

portfolio_optimizer_worker

↓

optimized.signal

↓

execution_worker
