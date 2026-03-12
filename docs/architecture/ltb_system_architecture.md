# LTB System Architecture

## 1. System Overview

LTB (Live Trading Bot)는 Event-Driven Architecture 기반 자동 트레이딩 시스템이다.

목표

- 실시간 시장 데이터 기반 전략 실행
- 자동 주문 실행
- 포지션 관리
- 리스크 관리
- 전략 성능 분석
- Web 기반 운영 및 관리

LTB는 다음 4계층 구조로 설계된다.

Engine
API
Web UI
Docs


------------------------------------------------------------


## 2. High Level Architecture

전체 시스템 구조

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


------------------------------------------------------------


## 3. Event Driven Architecture

LTB는 Event Bus 기반 Worker 구조로 동작한다.

핵심 이벤트 흐름

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


장점

- Worker 간 결합도 감소
- 전략 모듈 확장 가능
- 장애 격리
- 확장성 높은 구조


------------------------------------------------------------


## 4. Engine Worker Architecture

LTB Engine Worker 구성

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


Worker 간 통신은 EventBus로 수행된다.


------------------------------------------------------------


## 5. Worker Responsibilities


### MarketWorker

역할

- 시장 가격 생성 또는 수신
- 가격 이벤트 생성

발행 이벤트

market.price
MARKET_TICK



### IndicatorWorker

역할

- 기술적 지표 계산

계산 지표

RSI
Stochastic
EMA

발행 이벤트

market.indicator



### StrategyWorker

역할

- 전략 평가
- 매매 시그널 생성

구독 이벤트

market.indicator
portfolio.update

발행 이벤트

strategy.signal



### StrategyEngine

역할

- 전략 등록
- 전략 평가 실행

구조

StrategyEngine
 ├ register(strategy)
 └ evaluate(event)



### StrategyLoader

역할

- YAML 기반 전략 설정 로딩
- 활성화된 전략만 로딩

설정 파일

config/strategies.yaml



### ExecutionWorker

역할

- 전략 시그널 처리
- 주문 요청 생성

구독 이벤트

strategy.signal
portfolio.update

발행 이벤트

order.request



### OrderExecutorWorker

역할

- 주문 실행 처리

구독 이벤트

order.request

발행 이벤트

ORDER_FILLED



### PortfolioWorker

역할

- 포지션 상태 관리

구독 이벤트

ORDER_FILLED

발행 이벤트

POSITION_OPENED
POSITION_CLOSED
portfolio.update



### TrailingStopWorker

역할

- 트레일링 스탑 관리

구독 이벤트

POSITION_OPENED
MARKET_TICK

동작

highest_price 갱신
stop_price 계산
price <= stop → SELL



### RiskWorker

역할

- 리스크 상태 모니터링

예정 기능

max open positions
capital exposure limit
daily loss limit
kill switch



### AnalyticsWorker

역할

- 전략 성능 분석
- 거래 통계 분석



### AlertWorker

역할

- 시스템 알림 처리

risk alert
execution alert
system alert


------------------------------------------------------------


## 6. Strategy Architecture

전략 시스템은 플러그인 구조로 설계된다.

위치

src/ltb/strategy/strategies/


전략 인터페이스

evaluate(event)


전략 입력

symbol
price
rsi
stoch
ema


전략 출력

signal = {
 symbol
 action
 price
 qty
 strategy
}


------------------------------------------------------------


## 7. Portfolio Management

포지션 관리 기능

position tracking
portfolio update event
trailing stop


------------------------------------------------------------


## 8. Risk Management

리스크 관리

max open positions
max symbol position
capital usage limit
daily loss limit


향후 추가 예정

kill switch
strategy risk control
account risk limit


------------------------------------------------------------


## 9. Universe System

Universe Builder 존재

현재

static symbol list


향후 확장

KOSPI100
NASDAQ
custom watchlist


------------------------------------------------------------


## 10. Future Expansion

향후 확장 예정 시스템

Strategy Allocation Engine
Strategy Playbook System
Simulation Engine
Paper Trading
Web Dashboard
