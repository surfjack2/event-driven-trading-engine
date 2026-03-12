# LTB Project Status

## 1. Current Development Stage

현재 LTB 프로젝트는 Engine Core 구축 단계이다.

목표

Event Engine 안정화  
Worker 구조 확립  
Strategy 시스템 구축


---

# 2. Implemented Components

현재 구현 완료

Event Bus  
Market Worker  
Indicator Worker  
Strategy Worker  
Execution Worker  
Order Executor Worker  
Portfolio Worker  
Trailing Stop Worker  


부분 구현

Risk Worker  
Analytics Worker  
Alert Worker  


---

# 3. Engine Runtime Pipeline

현재 실제 동작하는 흐름

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


---

# 4. Current Strategy

현재 전략

SimpleMomentumStrategy


목적

엔진 이벤트 흐름 테스트


---

# 5. Planned Strategies

Momentum Strategy  
Volume Breakout Strategy  
Pullback Strategy  
Turtle Strategy  


---

# 6. Risk System Status

현재

basic risk checks


계획

daily loss control  
strategy risk limits  
kill switch system  


---

# 7. Strategy Allocation Plan

멀티 전략 자본 배분

초기 구조

30%  
30%  
40%


운영 정책

전략 성과 기반 재배분


---

# 8. Dashboard Status

현재

Admin API 기반 관리 콘솔


향후

Trading Dashboard  
Strategy Performance  
Portfolio Monitoring  


---

# 9. Planned Development

다음 단계

Strategy System 확장  
Risk Engine 강화  
Strategy Allocation Engine 구현  
Dashboard 구축  
Backtest Engine 구현  


---

# 10. Long Term Goal

LTB는 단순 자동매매 봇이 아닌

Event Driven Trading Platform 구축을 목표로 한다.
