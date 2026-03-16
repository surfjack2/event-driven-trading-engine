# LTB VWAP Ranking Upgrade Architecture

Branch
feature/vwap-ranking-upgrade

본 업그레이드는 LTB Signal Pipeline의 안정성과 신호 품질을 개선하기 위해 수행되었다.

--------------------------------------------------

목표

Signal ranking 안정화
VWAP 전략 신호 품질 개선
Portfolio optimizer 정확도 향상
전략 자동 제어 시스템 도입

--------------------------------------------------

핵심 변경

1. Alpha Normalization 개선

기존

tanh(alpha / 30)

문제

alpha saturation
signal ranking 왜곡

개선

scaled tanh normalization

tanh(alpha / 80)

extreme alpha soft clipping 적용

--------------------------------------------------

2. Portfolio Optimizer Scoring 개선

기존

momentum weight 과도
volatility penalty 과도

개선

score 구조

alpha
allocation_weight
momentum
liquidity
volatility

balanced scoring 적용

--------------------------------------------------

3. Signal Ranking 안정화

signal persistence
ranking stability 개선

signal selection 정확도 향상

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

--------------------------------------------------

결과

signal noise 감소
ranking 안정화
optimizer selection 정확도 상승
