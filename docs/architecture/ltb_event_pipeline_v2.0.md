# LTB Event Pipeline Architecture
Version: V2.0

---

# 1. 개요

LTB 엔진은 Event Driven Architecture 기반으로 동작한다.

모든 데이터 흐름은 EventBus를 통해 전달되며,
각 Worker는 특정 이벤트를 구독하고 처리한 뒤 다음 단계 이벤트를 발행한다.

이 구조는 다음 장점을 가진다.

- 높은 모듈 분리도
- 전략 교체 용이
- 병렬 처리 가능
- 시스템 안정성 향상

---

# 2. 전체 Pipeline 구조

전체 이벤트 흐름은 다음과 같다.

Market Data
→ Indicator
→ Strategy Engine
→ Signal Pipeline
→ Allocation Pipeline
→ Portfolio Optimizer
→ Execution Engine
→ Portfolio / Risk
→ Analytics / Monitoring

---

# 3. Detailed Event Flow

## 3.1 Market Data

Worker

MarketWorker
ReplayMarketWorker

Event

market.price

역할

실시간 시장 데이터를 수신한다.

---

## 3.2 Indicator Layer

Worker

IndicatorWorker

Event

market.indicator

역할

기술 지표 계산

예

- RSI
- EMA
- VWAP
- ATR
- Volume MA

---

# 4. Strategy Engine

Worker

StrategyWorker

Input Event

market.indicator

Output Event

strategy.signal

역할

전략 로직 실행

예

- vwap_reclaim
- simple_momentum
- vwap_bounce

Signal은 다음 정보를 포함한다.

symbol  
price  
strategy  
features

---

# 5. Signal Processing Pipeline

## 5.1 Signal Deduplication

Worker

SignalDedupWorker

Event

strategy.signal
→ dedup.signal

역할

중복 신호 제거

---

## 5.2 Signal Persistence

Worker

SignalPersistenceWorker

Event

dedup.signal
→ persistent.signal

역할

일시적인 신호 제거

연속 신호 확인

---

## 5.3 Alpha Ranking

Worker

SignalRankingWorker

Event

persistent.signal
→ ranked.signal

역할

신호 점수 계산

alpha score 기반 ranking 수행

---

# 6. Allocation Pipeline

## 6.1 Strategy Allocation

Worker

StrategyAllocationWorker

Event

ranked.signal
→ allocation.signal

역할

전략별 자본 배분

---

## 6.2 Trade Quality Filter

Worker

TradeQualityFilterWorker

Event

allocation.signal
→ quality.signal

역할

저품질 거래 제거

예

- liquidity 부족
- volatility 과다
- fake VWAP reclaim

---

## 6.3 Position Intent Resolution

Worker

PositionIntentWorker

Event

quality.signal
→ intent.signal

역할

종목별 최적 전략 선택

---

# 7. Portfolio Optimization

Worker

PortfolioOptimizerWorker

Event

intent.signal
→ optimized.signal

역할

포트폴리오 구성

조건

- max positions
- strategy quota
- optimizer score

---

# 8. Execution Engine

Worker

ExecutionWorker

Event

optimized.signal
→ order.request

역할

실제 주문 생성

Risk control

- portfolio heat
- position sizing
- strategy exposure

---

# 9. Order Execution

Worker

OrderExecutorWorker

Event

order.request
→ broker API

역할

브로커 API 주문 전송

예

KIS API

---

# 10. Portfolio Management

Worker

PortfolioWorker

Event

ORDER_FILLED

역할

포지션 상태 업데이트

---

# 11. Risk Management

Worker

RiskWorker

역할

리스크 제어

예

- kill switch
- max exposure
- drawdown control

---

# 12. Exit Management

Worker

TrailingStopWorker

역할

자동 청산

예

- trailing stop
- ATR stop
- signal decay exit

---

# 13. Analytics

Worker

AnalyticsWorker

역할

전략 성과 분석

---

# 14. Monitoring

Worker

ValidationMonitorWorker

역할

엔진 상태 모니터링

표시 정보

- 시장 상태
- 전략 신호
- 주문 상태
- 계좌 정보
- 엔진 성능

---

# 15. EventBus Architecture

LTB는 Queue 기반 EventBus를 사용한다.

특징

- multi worker thread
- event queue
- topic 기반 subscribe

장점

- loose coupling
- scalability
- 안정성

---

# 16. 핵심 설계 특징

LTB 엔진은 다음 설계 원칙을 따른다.

Event Driven Architecture

Worker Isolation

Pipeline Processing

Risk First Design

---

# 17. 결론

LTB Event Pipeline은 다음 구조를 가진다.

Market
→ Indicator
→ Strategy
→ Signal Processing
→ Allocation
→ Portfolio Optimization
→ Execution
→ Portfolio / Risk
→ Monitoring

이 구조는 Quant Trading Engine에서 일반적으로 사용되는
Event Driven Trading Architecture와 동일한 설계 패턴을 따른다.
