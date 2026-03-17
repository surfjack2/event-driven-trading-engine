# LTB Debugging Report
## Signal Pipeline Break – PositionIntentWorker Event Mismatch

Date: 2026-03-17  
Environment: LTB Engine Backtest Mode

---

# 1. 문제 현상

시스템에서 다음 현상이 발생하였다.

- Strategy 신호 정상 발생
- Ranking 정상
- Allocation 정상
- 그러나 매매가 발생하지 않음

Engine 상태

signals > 0  
orders = 0

CLI UI

orders: 0  
fills: 0

---

# 2. 초기 의심

초기 분석에서는 다음 가능성이 검토되었다.

- alpha_score 계산 문제
- strategy 필터 문제
- execution risk block
- optimizer selection 실패

그러나 로그 분석 결과 다음 단계까지는 정상 동작하였다.

Pipeline

StrategyWorker  
↓  
SignalDedupWorker  
↓  
SignalPersistenceWorker  
↓  
SignalRankingWorker  
↓  
StrategyAllocationWorker

즉 신호 생성 및 ranking 단계는 정상이었다.

---

# 3. 실제 원인

PositionIntentWorker가 다음 이벤트만 구독하고 있었다.

subscribe("quality.signal")

그러나 StrategyAllocationWorker는 다음 이벤트를 publish 하고 있었다.

publish("allocation.signal")

즉 pipeline 이벤트가 연결되지 않았다.

실제 흐름

ranked.signal  
↓  
StrategyAllocationWorker  
↓  
allocation.signal  
✖  
PositionIntentWorker (quality.signal만 수신)

이로 인해 다음 단계가 모두 실행되지 않았다.

- PositionIntentWorker
- PortfolioOptimizerWorker
- ExecutionWorker

---

# 4. 해결 방법

PositionIntentWorker의 구독 이벤트를 수정하였다.

기존

subscribe("quality.signal")

수정

subscribe("allocation.signal")

---

# 5. 수정 후 파이프라인

StrategyWorker  
↓  
SignalDedupWorker  
↓  
SignalPersistenceWorker  
↓  
SignalRankingWorker  
↓  
StrategyAllocationWorker  
↓  
PositionIntentWorker  
↓  
PortfolioOptimizerWorker  
↓  
ExecutionWorker

---

# 6. 수정 후 정상 로그

INTENT 생성

[INTENT] resolved symbol=TEST024 strategy=simple_momentum weight=0.4 alpha=0.909

Execution 발생

[EXECUTION] order request symbol=TEST024 qty=9 heat=0.0 multiplier=1.0

---

# 7. CLI 확인

orders > 0  
fills > 0  

Strategy Performance 정상 출력

simple_momentum trades:2

---

# 8. 교훈

Event-driven trading system에서 가장 흔한 오류는

Event Name Mismatch

이다.

특히 다음 구조에서 자주 발생한다.

worker A publish(event_A)  
worker B subscribe(event_B)

이 경우 pipeline이 완전히 단절된다.

---

# 9. 향후 개선

Signal Pipeline Event Map 문서화 필요

예

ranked.signal  
allocation.signal  
quality.signal  
intent.signal  
optimized.signal  

이벤트 흐름을 명시적으로 관리해야 한다.

---

# 10. 상태

Resolution: Completed  
System Status: Trading Operational
