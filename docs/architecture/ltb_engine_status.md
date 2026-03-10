# LTB Engine Architecture & Implementation Status

## 1. Overview

LTB (Live Trading Bot)는 **Event-Driven Architecture 기반 자동 트레이딩 시스템**이다.

시스템 목표

* 실시간 시장 데이터 기반 전략 실행
* 자동 주문 처리
* 포지션 관리
* 리스크 관리
* 전략 성능 분석
* Web Dashboard 기반 운영

현재 상태

```
Event Driven Trading Engine
```

구현 진행 상태는 아래 기준으로 표시한다.

```
[✔ IMPLEMENTED]  구현 완료
[~ PARTIAL]      부분 구현
[○ PLANNED]      설계만 존재
```

---

# 2. System Architecture

전체 시스템 구조

```
Browser
   ↓
Web UI
   ↓
Admin API (FastAPI)
   ↓
Event Bus
   ↓
LTB Engine
   ↓
Broker API
```

구현 상태

```
Admin API           [✔ IMPLEMENTED]
Event Bus           [✔ IMPLEMENTED]
LTB Engine          [✔ IMPLEMENTED]
Web UI              [○ PLANNED]
Broker Integration  [~ PARTIAL]
```

---

# 3. Engine Runtime Architecture

LTB Engine은 **Worker 기반 Event-Driven 구조**이다.

현재 Worker 목록

```
MarketWorker
IndicatorWorker
StrategyWorker
ExecutionWorker
OrderExecutorWorker
PortfolioWorker
TrailingStopWorker
RiskWorker
AnalyticsWorker
AlertWorker
```

구현 상태

```
MarketWorker         [✔ IMPLEMENTED]
IndicatorWorker      [✔ IMPLEMENTED]
StrategyWorker       [✔ IMPLEMENTED]
ExecutionWorker      [✔ IMPLEMENTED]
OrderExecutorWorker  [✔ IMPLEMENTED]
PortfolioWorker      [✔ IMPLEMENTED]
TrailingStopWorker   [✔ IMPLEMENTED]
RiskWorker           [~ PARTIAL]
AnalyticsWorker      [~ PARTIAL]
AlertWorker          [~ PARTIAL]
```

---

# 4. Event Bus Architecture

LTB는 내부 EventBus (`QueueBus`)를 통해 Worker 간 통신을 수행한다.

핵심 이벤트 흐름

```
market.price
   ↓
market.indicator
   ↓
strategy.signal
   ↓
order.request
   ↓
ORDER_FILLED
   ↓
portfolio.update
```

구현 상태

```
QueueBus            [✔ IMPLEMENTED]
Event Routing       [✔ IMPLEMENTED]
Error Logging       [✔ IMPLEMENTED]
Async Processing    [○ PLANNED]
```

---

# 5. Worker Responsibilities

## MarketWorker

역할

* 시장 가격 데이터 생성 / 수신
* 가격 이벤트 생성

이벤트

```
market.price
MARKET_TICK
```

구현 상태

```
Market Simulation      [✔ IMPLEMENTED]
Broker Market Feed    [○ PLANNED]
```

---

## IndicatorWorker

역할

* 가격 기반 기술적 지표 계산

지표

```
RSI
Stochastic
EMA
```

출력 이벤트

```
market.indicator
```

구현 상태

```
RSI Calculation      [✔ IMPLEMENTED]
Stochastic           [✔ IMPLEMENTED]
EMA                  [✔ IMPLEMENTED]
Indicator Pipeline   [✔ IMPLEMENTED]
```

---

## StrategyWorker

역할

* 전략 평가
* 매매 시그널 생성

구독 이벤트

```
market.indicator
portfolio.update
```

출력 이벤트

```
strategy.signal
```

구현 상태

```
Strategy Execution     [✔ IMPLEMENTED]
Position Gate          [✔ IMPLEMENTED]
Strategy Plugin Model  [✔ IMPLEMENTED]
```

---

## Strategy Engine

역할

* 전략 관리
* 전략 평가 실행

구조

```
StrategyEngine
   ├ register(strategy)
   └ evaluate(event)
```

구현 상태

```
Strategy Registration  [✔ IMPLEMENTED]
Strategy Evaluation    [✔ IMPLEMENTED]
Multi Strategy Engine  [✔ IMPLEMENTED]
```

---

## Strategy Loader

역할

* YAML 전략 설정 로딩
* 전략 활성화 관리

설정 파일

```
config/strategies.yaml
```

구현 상태

```
Strategy Config Loader   [✔ IMPLEMENTED]
Dynamic Strategy Enable  [✔ IMPLEMENTED]
```

---

## ExecutionWorker

역할

* 전략 시그널 처리
* 주문 요청 생성

구독 이벤트

```
strategy.signal
portfolio.update
```

출력 이벤트

```
order.request
```

구현 상태

```
Signal Processing   [✔ IMPLEMENTED]
Position Gate       [✔ IMPLEMENTED]
Order Request       [✔ IMPLEMENTED]
```

---

## OrderExecutorWorker

역할

* 주문 실행 처리

구독 이벤트

```
order.request
```

출력 이벤트

```
ORDER_FILLED
```

구현 상태

```
Order Queue        [✔ IMPLEMENTED]
Simulated Fill     [✔ IMPLEMENTED]
Broker API         [○ PLANNED]
```

---

## PortfolioWorker

역할

* 포지션 관리

구독 이벤트

```
ORDER_FILLED
```

출력 이벤트

```
POSITION_OPENED
POSITION_CLOSED
portfolio.update
```

구현 상태

```
Position Tracking      [✔ IMPLEMENTED]
Portfolio Update Event [✔ IMPLEMENTED]
```

---

## TrailingStopWorker

역할

* 트레일링 스탑 관리

구독 이벤트

```
POSITION_OPENED
MARKET_TICK
```

동작

```
highest_price 갱신
stop_price 계산
price <= stop → SELL
```

구현 상태

```
Trailing Stop Logic    [✔ IMPLEMENTED]
ATR Stop               [○ PLANNED]
```

---

## RiskWorker

역할

* 리스크 상태 모니터링

현재 기능

```
max open positions
max capital usage
daily loss limit
```

구현 상태

```
Risk Engine          [~ PARTIAL]
Capital Risk Check   [~ PARTIAL]
Kill Switch          [○ PLANNED]
Strategy Risk Limit  [○ PLANNED]
```

---

## AnalyticsWorker

역할

* 전략 성능 분석

예정 기능

```
strategy performance
trade statistics
equity curve
```

구현 상태

```
Worker Skeleton      [~ PARTIAL]
Performance Metrics  [○ PLANNED]
```

---

## AlertWorker

역할

* 시스템 이벤트 알림

대상 이벤트

```
risk
execution
system
```

구현 상태

```
Alert Worker Skeleton   [~ PARTIAL]
Notification System     [○ PLANNED]
```

---

# 6. Strategy Architecture

전략은 **플러그인 구조**로 설계되었다.

경로

```
src/ltb/strategy/strategies/
```

전략 인터페이스

```
evaluate(event)
```

전략 입력

```
symbol
price
rsi
stoch
ema
```

전략 출력

```
signal = {
  symbol
  action
  price
  qty
  strategy
}
```

구현 상태

```
Strategy Framework   [✔ IMPLEMENTED]
Strategy Plugin      [✔ IMPLEMENTED]
```

---

# 7. Current Strategy

현재 테스트 전략

```
SimpleMomentumStrategy
```

목적

```
엔진 이벤트 흐름 검증
```

구현 상태

```
Test Strategy        [✔ IMPLEMENTED]
Real Strategy Logic  [○ PLANNED]
```

---

# 8. Planned Strategy Types

향후 전략

```
Momentum Strategy
Volume Breakout Strategy
Pullback Continuation Strategy
Turtle Breakout Strategy
```

구현 상태

```
Momentum Strategy          [○ PLANNED]
Volume Breakout Strategy   [○ PLANNED]
Pullback Strategy          [○ PLANNED]
Turtle Strategy            [○ PLANNED]
```

---

# 9. Portfolio Rules

현재 기능

```
동시 종목 수 제한
포지션 관리
트레일링 스탑
```

구현 상태

```
Position Tracking   [✔ IMPLEMENTED]
Portfolio Limits    [~ PARTIAL]
```

---

# 10. Risk Controls

현재 리스크 기능

```
max open positions
max symbol position
capital usage limit
daily loss limit
```

구현 상태

```
Basic Risk Engine     [~ PARTIAL]
Daily Loss Control    [~ PARTIAL]
Kill Switch           [○ PLANNED]
Strategy Disable      [○ PLANNED]
```

---

# 11. Position Sizing

PositionSizer 존재

구조

```
capital
risk_per_trade
```

수량 계산

```
risk_amount = capital * risk_per_trade
qty = risk_amount / risk_per_share
```

구현 상태

```
PositionSizer Module     [✔ IMPLEMENTED]
Strategy Allocation      [○ PLANNED]
```

---

# 12. Universe System

UniverseBuilder 존재

현재

```
symbol list
```

확장 예정

```
KOSPI100
NASDAQ
Custom Watchlist
```

구현 상태

```
UniverseBuilder      [✔ IMPLEMENTED]
Market Universe DB   [○ PLANNED]
```

---

# 13. System State Control

시스템 상태

```
START
STOP
PAUSE
HALT
```

HALT 조건

```
risk violation
kill switch
manual operator stop
```

구현 상태

```
Engine Runtime Control  [~ PARTIAL]
Kill Switch System      [○ PLANNED]
```

---

# 14. Planned Extensions

향후 확장

```
Strategy Allocation Engine
Strategy Playbook System
Web Dashboard
Simulation Engine
Paper Trading
```

구현 상태

```
Strategy Allocation Engine  [○ PLANNED]
Strategy Playbook System    [○ PLANNED]
Web Dashboard               [○ PLANNED]
Simulation Engine           [○ PLANNED]
Paper Trading               [○ PLANNED]
```

---

# 15. Conclusion

현재 LTB는 다음 핵심이 구현된 상태이다.

```
Event Bus
Worker Runtime
Strategy Framework
Execution Pipeline
Portfolio Manager
Trailing Stop
```

현재 단계

```
Trading Engine Core Complete
```

다음 단계

```
Strategy Expansion
Risk Engine 강화
Strategy Allocation
Web Dashboard
Analytics System
```
