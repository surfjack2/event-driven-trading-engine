# LTB Master Architecture

## 1. System Overview

LTB는 Event-Driven 기반 자동매매 플랫폼이다.

핵심 목표

- 멀티 전략 자동매매
- 리스크 관리 자동화
- 전략 성과 기반 자본 배분
- 확장 가능한 플랫폼 구조


전체 플랫폼 구성

Trading Engine  
Web UI / Dashboard  
Admin API  
Database  
Cache  
Watchdog  
Broker API  


---

# 2. Platform Architecture

전체 구조

Web UI / Dashboard
        ↓
Admin API (FastAPI)
        ↓
Event Bus
        ↓
Trading Engine Workers
        ↓
Broker API
        ↓
Database / Cache


Platform Layer

Dashboard  
Admin Console  
Reports  
Logs  


API Layer

Admin API  
Strategy API  
Docs API  


Trading Layer

Strategy Engine  
Execution Engine  
Risk Engine  


Infrastructure

PostgreSQL  
Redis  
Watchdog  


---

# 3. Trading Engine Architecture

LTB 엔진은 Worker 기반 Event Engine 구조이다.

Worker 구성

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


각 Worker는 Event Bus 기반으로 통신한다.


---

# 4. Core Event Flow

엔진 이벤트 흐름

market.price
↓
indicator.update
↓
strategy.signal
↓
order.request
↓
ORDER_FILLED
↓
portfolio.update


---

# 5. Worker Responsibilities

MarketWorker

시장 데이터 수집

price  
index  
fx  
news  


IndicatorWorker

기술적 지표 계산

RSI  
Stochastic  
EMA  


StrategyWorker

전략 평가

StrategyEngine을 통해 전략 실행

출력

strategy.signal


ExecutionWorker

전략 신호 처리

position check  
risk check  
order creation  


OrderExecutorWorker

브로커 주문 실행

Broker API 호출


PortfolioWorker

포지션 상태 관리

portfolio.update 이벤트 생성


TrailingStopWorker

포지션 트레일링 스탑 관리

highest price update  
stop price 계산  


RiskWorker

리스크 모니터링

daily loss  
capital usage  
position limits  


AnalyticsWorker

전략 성과 분석

trade 기록  
pnl 계산  


AlertWorker

시스템 알림

trade alerts  
risk alerts  
system alerts  


---

# 6. Strategy System

전략 시스템은 Plugin 구조로 설계된다.

StrategyEngine

strategy modules 실행

예

momentum  
volume breakout  
turtle  


전략 인터페이스

evaluate(event)


---

# 7. Strategy Capital Allocation

LTB는 멀티 전략 자본 배분 구조를 사용한다.

기본 배분

30%
30%
40%

전략 성과 기반 재배분

일일 전략 성과 분석  
성과 낮은 전략 자동 off  
자본 다른 전략으로 재배분


---

# 8. Risk Management

Risk Engine 구성

risk_manager  
position_size_manager  
portfolio_risk_manager  
kill_switch  


Kill Switch 감시 항목

daily_loss  
max_drawdown  
loss_streak  
api_error_rate  
engine_error  


조건 충족 시

halt trading  
close positions  
alert admin  


---

# 9. Execution Fallback

주문 실패 처리

limit order fail → market order fallback

price fetch fail → cached price


---

# 10. Watchdog System

Watchdog는 시스템 상태를 감시한다.

감시 대상

engine heartbeat  
worker heartbeat  
api error  


문제 발생 시

engine restart  
emergency stop  


---

# 11. Database Architecture

Primary Database

PostgreSQL


주요 테이블

markets  
market_indexes  
trades  
positions  
strategy_stats  
alerts  
engine_health  


Cache

Redis


용도

market cache  
dashboard cache  
session cache  


---

# 12. Multi Market Architecture

LTB는 멀티 시장 확장을 고려하여 설계되었다.

지원 시장

KRX  
US  
CRYPTO  


DB 구조

markets table


---

# 13. AI Code Analysis

LTB는 SonarQube + Local LLM을 통해 코드 분석을 수행할 수 있다.

목적

코드 품질 분석  
보안 취약점 탐지  
전략 코드 설명 생성  
자동 문서 생성


구조

Developer Code
↓
Git
↓
SonarQube
↓
LLM Analysis
↓
Report


---

# 14. Future Architecture

향후 확장

Backtest Engine  
Strategy Optimization  
AI Strategy Assistant  
Distributed Trading  


---

# 15. Design Principles

LTB 설계 원칙

Event Driven Architecture  
Worker Isolation  
Loose Coupling  
Strategy Plugin Architecture  
Scalable Platform
