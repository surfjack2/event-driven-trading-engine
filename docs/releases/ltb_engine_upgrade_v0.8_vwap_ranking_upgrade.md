# LTB Engine Upgrade v0.8

VWAP Ranking Upgrade

Branch
feature/vwap-ranking-upgrade

--------------------------------------------------

Major Changes

Signal System

alpha normalization redesign
signal ranking stability 개선
signal persistence 강화

--------------------------------------------------

Strategy Improvements

VWAP reclaim fake signal filter
VWAP bounce touch cooldown

--------------------------------------------------

Portfolio Improvements

portfolio optimizer scoring 개선
strategy allocation 안정화

--------------------------------------------------

Meta Layer

meta_strategy_worker 추가

전략 enable / disable 자동화

--------------------------------------------------

Quality Layer

trade_quality_filter_worker 추가

--------------------------------------------------

Pipeline 구조

strategy
→ persistence
→ ranking
→ allocation
→ quality
→ intent
→ optimizer
→ execution

--------------------------------------------------

Impact

signal quality 개선
ranking 안정화
portfolio selection 정확도 향상
