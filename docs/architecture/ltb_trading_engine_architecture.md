# LTB Trading Engine Architecture

## 1. Engine Design

LTB Trading Engine은 Event-Driven Architecture 기반으로 동작한다.

Worker 기반 구조를 사용하며 Event Bus를 통해 통신한다.

---

## 2. Worker Architecture

Trading Engine Worker

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

---

## 3. Worker Responsibilities

### MarketWorker

시장 데이터 수집

price  
index  
fx  
news  

Event

market.price  

---

### IndicatorWorker

기술적 지표 계산

RSI  
Stochastic  
EMA  

Event

indicator.update  

---

### StrategyWorker

전략 평가

Input

indicator.update  
portfolio.update  

Output

strategy.signal  

---

### ExecutionWorker

주문 생성

Input

strategy.signal  

Output

order.request  

---

### OrderExecutorWorker

브로커 주문 실행

Input

order.request  

Output

ORDER_FILLED  

---

### PortfolioWorker

포지션 관리

Input

ORDER_FILLED  

Output

portfolio.update  

---

### TrailingStopWorker

트레일링 스탑 관리

동작

highest_price update  
stop_price 계산  

가격 ≤ stop → SELL  

---

### RiskWorker

리스크 관리

검사 항목

max open positions  
capital usage  
daily loss  

Kill Switch 조건

daily_loss  
max_drawdown  
api_error_rate  
engine_error  

---

### AnalyticsWorker

전략 성과 분석

수집

trades  
pnl  
strategy performance  

---

### AlertWorker

알림 처리

trade execution  
risk alerts  
system alerts  

---

## 4. Execution Pipeline

strategy.signal  
↓  
ExecutionWorker  
↓  
order.request  
↓  
OrderExecutorWorker  
↓  
ORDER_FILLED  
↓  
PortfolioWorker  
↓  
portfolio.update  
