# LTB Runtime Monitoring Guide

이 문서는 LTB (Live Trading Bot) 시스템이 정상적으로 동작하는지 확인하기 위한
운영 모니터링 가이드이다.

이 가이드는 향후 **Admin Console / Web UI에서 상태를 확인하는 기준 문서**로 사용된다.

---

# 1. 시스템 이벤트 흐름

LTB는 이벤트 기반 구조로 동작한다.

Market Data
→ Strategy Engine
→ Execution Engine
→ Order Executor
→ Portfolio Manager
→ Risk Engine
→ Exit / Trailing Stop

정상 동작 시 로그 흐름은 다음과 같다.

MARKET
STRATEGY
EXECUTION
ORDER
PORTFOLIO
TRAIL

---

# 2. 핵심 운영 체크 항목

운영 중 확인해야 하는 주요 항목

1. Market data 수신 여부
2. Strategy signal 발생 여부
3. Execution signal 처리 여부
4. Order 실행 여부
5. Portfolio 상태 업데이트
6. Trailing stop 작동 여부
7. Risk monitoring 상태

---

# 3. 로그 기반 확인 방법

전체 트레이딩 흐름 확인

tail -f logs/engine.log | grep -E "MARKET|STRATEGY|EXECUTION|ORDER|PORTFOLIO|TRAIL"

주문 시스템 확인

tail -f logs/engine.log | grep -E "ORDER EXECUTOR|KIS"

포지션 상태 확인

tail -f logs/engine.log | grep PORTFOLIO

트레일링 스탑 확인

tail -f logs/engine.log | grep TRAIL

에러 확인

tail -f logs/engine.log | grep -E "ERROR|WARN"

---

# 4. 정상 동작 기준

다음 패턴이 반복되면 정상이다.

MARKET pushed price
STRATEGY signal generated
EXECUTION processing signal
ORDER EXECUTOR executing order
PORTFOLIO updated position
TRAIL INIT
TRAIL STOP HIT
PORTFOLIO updated position = 0

---

# 5. 향후 Web UI 모니터링 항목

Admin Console / Web UI에서는 다음 항목을 표시한다.

Market Status
Strategy Status
Active Positions
Order Execution Status
Risk Monitoring
Recent Trades

---

# 6. 향후 확장

향후 다음 기능이 추가될 예정이다.

Strategy Performance Dashboard
PnL Monitoring
Strategy별 성능 분석
AI 기반 시장 분석
SOAR Playbook 기반 전략 관리

---
