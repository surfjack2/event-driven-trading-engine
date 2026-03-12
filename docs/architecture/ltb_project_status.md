# LTB Project Status

## 1. Current Project Phase

현재 프로젝트 단계

Engine Core Prototype


현재 상태

자동매매 엔진 핵심 구조가 동작 가능한 상태이다.



------------------------------------------------------------


## 2. Implemented Components

현재 구현된 핵심 구성 요소

Event Bus
Worker Runtime Engine
Strategy Framework
Execution Pipeline
Portfolio Manager
Trailing Stop System



------------------------------------------------------------


## 3. Working Event Pipeline

현재 정상 동작 확인된 이벤트 흐름

MarketWorker
   ↓
IndicatorWorker
   ↓
StrategyWorker
   ↓
ExecutionWorker
   ↓
OrderExecutorWorker
   ↓
PortfolioWorker
   ↓
TrailingStopWorker


실행 확인 결과

BUY signal
 → order request
 → order filled
 → position opened
 → trailing stop tracking
 → stop triggered
 → SELL


엔진 이벤트 루프 정상 동작 확인됨.



------------------------------------------------------------


## 4. Worker Implementation Status

MarketWorker           implemented
IndicatorWorker        implemented
StrategyWorker         implemented
ExecutionWorker        implemented
OrderExecutorWorker    implemented
PortfolioWorker        implemented
TrailingStopWorker     implemented

RiskWorker             partial
AnalyticsWorker        partial
AlertWorker            partial



------------------------------------------------------------


## 5. Strategy System Status

현재 전략

SimpleMomentumStrategy


현재 목적

엔진 이벤트 흐름 검증


현재 전략 로직

random 기반 BUY signal 생성



------------------------------------------------------------


## 6. Planned Strategy Implementation

향후 구현 예정 전략

Momentum Strategy
Volume Breakout Strategy
Pullback Continuation Strategy
Turtle Breakout Strategy



------------------------------------------------------------


## 7. Risk Engine Status

현재 구현

max open positions
max symbol position
capital usage limit
daily loss limit


향후 추가 예정

strategy risk limits
account loss limit
kill switch
strategy daily loss shutdown



------------------------------------------------------------


## 8. Position Sizing

PositionSizer 구현 존재

기본 구조

capital
risk_per_trade


수량 계산 방식

risk_amount = capital * risk_per_trade
qty = risk_amount / risk_per_share



------------------------------------------------------------


## 9. Portfolio System

현재 기능

position open
position close
portfolio update event


추가 예정 기능

strategy allocation
portfolio exposure control



------------------------------------------------------------


## 10. Strategy Allocation Plan

전략별 자본 배분 구조

기본 초기 배분

30%
30%
40%


운영 정책

일일 전략 성과 분석
성과 높은 전략 배분 증가
성과 낮은 전략 배분 감소


전략 손실 기준

일일 전략 손실률 일정 수준 초과 시
해당 전략 자동 OFF



------------------------------------------------------------


## 11. Account Risk Control Plan

계좌 손실 관리

일일 계좌 손실률 기준 설정


조건 충족 시

자동 매매 중단


운영자 제어

START
STOP
PAUSE
HALT



------------------------------------------------------------


## 12. Next Development Phase

다음 개발 단계

Strategy Implementation
Risk Engine 강화
Strategy Allocation Engine
Analytics System
Web Dashboard 구축



------------------------------------------------------------


## 13. Final Project Direction

LTB는 단순 자동매매 봇이 아니라

Event-Driven Trading Platform을 목표로 한다.


핵심 구성 요소

Trading Engine
Strategy Framework
Risk Engine
Portfolio Management
Analytics
Web Dashboard
