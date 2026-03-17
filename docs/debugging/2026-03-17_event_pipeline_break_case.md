# LTB Debugging Case
## Event Pipeline Break – Allocation → Intent

Author: Jack  
Date: 2026-03-17  
Environment: LTB Engine (Backtest)

---

# 1. 문제 현상

트레이딩 엔진에서 다음과 같은 현상이 발생하였다.

signals > 0  
orders = 0  
fills = 0  

CLI UI 상태

signals 증가  
orders 없음  

즉 신호는 발생하지만 실제 매매가 이루어지지 않았다.

---

# 2. 로그 분석

다음 단계까지는 정상 동작하였다.

StrategyWorker  
↓  
SignalDedupWorker  
↓  
SignalPersistenceWorker  
↓  
SignalRankingWorker  
↓  
StrategyAllocationWorker  

예시 로그

[STRATEGY] signal generated  
[DEDUP] passed  
[PERSISTENCE] confirmed  
[RANKING PASS]  
[ALLOCATION] signal strategy=simple_momentum weight=0.4  

즉 **신호 생성 및 ranking 단계는 정상**이었다.

---

# 3. 문제 위치

문제는 다음 worker 사이에서 발생하였다.

StrategyAllocationWorker  
↓  
PositionIntentWorker  

StrategyAllocationWorker는 다음 이벤트를 publish 하고 있었다.

publish("allocation.signal")

그러나 PositionIntentWorker는 다음 이벤트만 구독하고 있었다.

subscribe("quality.signal")

즉 이벤트 이름이 일치하지 않았다.

---

# 4. 실제 이벤트 흐름

정상 기대 흐름

ranked.signal  
↓  
StrategyAllocationWorker  
↓  
allocation.signal  
↓  
TradeQualityFilterWorker  
↓  
quality.signal  
↓  
PositionIntentWorker  

하지만 실제 엔진에서는 TradeQualityFilterWorker가 pipeline에 없었다.

그래서 실제 흐름은 다음과 같았다.

ranked.signal  
↓  
StrategyAllocationWorker  
↓  
allocation.signal  
✖  
PositionIntentWorker (quality.signal만 구독)

이로 인해 signal pipeline이 완전히 단절되었다.

---

# 5. 영향

다음 worker가 실행되지 않았다.

PositionIntentWorker  
PortfolioOptimizerWorker  
ExecutionWorker  

결과

orders = 0  

---

# 6. 해결 방법

PositionIntentWorker 구독 이벤트 수정

Before

subscribe("quality.signal")

After

subscribe("allocation.signal")

---

# 7. 수정 후 정상 파이프라인

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

# 8. 정상 동작 확인

INTENT 생성 로그

[INTENT] resolved symbol=TEST024 strategy=simple_momentum weight=0.4 alpha=0.909

Execution 로그

[EXECUTION] order request symbol=TEST024 qty=9 heat=0.0 multiplier=1.0

CLI UI

orders 증가  
fills 발생  

---

# 9. 교훈

Event-driven architecture에서 다음 오류는 매우 흔하다.

Event Name Mismatch

worker A publish(event_A)  
worker B subscribe(event_B)

이 경우 pipeline이 완전히 끊어진다.

---

# 10. 예방

Signal pipeline 이벤트를 문서화한다.

ranked.signal  
allocation.signal  
quality.signal  
intent.signal  
optimized.signal  

worker 구현 시 반드시 다음을 확인한다.

publish event name  
subscribe event name  

---

# 11. 상태

Resolved  
Trading pipeline operational
