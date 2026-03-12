# LTB Event Flow Architecture

## 1. Overview

LTB Trading Engine은 Event Bus 기반으로 Worker 간 이벤트를 전달한다.

Worker는 특정 이벤트를 구독하여 동작한다.

---

## 2. Core Event Flow

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

## 3. Market Data Flow

Market API  
↓  
MarketWorker  
↓  
EventBus  
↓  
IndicatorWorker  

---

## 4. Indicator Flow

market.price  
↓  
IndicatorWorker  
↓  
indicator.update  

지표

RSI  
Stochastic  
EMA  

---

## 5. Strategy Flow

indicator.update  
↓  
StrategyWorker  
↓  
StrategyEngine  
↓  
strategy.signal  

Signal 구조

symbol  
action  
price  
qty  
strategy  

---

## 6. Execution Flow

strategy.signal  
↓  
ExecutionWorker  
↓  
order.request  
↓  
OrderExecutorWorker  
↓  
ORDER_FILLED  

---

## 7. Portfolio Flow

ORDER_FILLED  
↓  
PortfolioWorker  
↓  
portfolio.update  

---

## 8. Risk Monitoring Flow

portfolio.update  
↓  
RiskWorker  
↓  
risk.check  

조건

daily_loss  
max_drawdown  
loss_streak  

---

## 9. Alert Flow

system events  
↓  
AlertWorker  
↓  
notifications  

---

## 10. Dashboard Data Flow

MarketWorker  
↓  
Redis Cache  
↓  
Dashboard UI
