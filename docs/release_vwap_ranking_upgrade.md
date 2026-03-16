# Release
feature/vwap-ranking-upgrade

--------------------------------------------------

Signal System

alpha normalization redesign
signal ranking stabilization
signal persistence 개선

--------------------------------------------------

Strategy Improvements

VWAP reclaim fake signal filter
VWAP bounce touch cooldown

--------------------------------------------------

Portfolio Improvements

portfolio optimizer scoring redesign
strategy allocation rebalance

--------------------------------------------------

Risk Improvements

exit manager integration
signal decay exit stabilization
time stop 개선

--------------------------------------------------

Meta Layer

meta_strategy_worker 추가
strategy enable / disable 자동화

--------------------------------------------------

Quality Layer

trade_quality_filter_worker 추가

--------------------------------------------------

Pipeline

strategy
→ persistence
→ ranking
→ allocation
→ quality
→ intent
→ optimizer
→ execution
