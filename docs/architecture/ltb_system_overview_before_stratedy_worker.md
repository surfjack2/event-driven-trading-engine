# LTB (Live Trading Bot) System Overview

## 1. Project Overview

LTB는 이벤트 기반(Event-Driven) 자동 트레이딩 시스템이다.

주요 목표:

* 실시간 시장 데이터 기반 전략 실행
* 자동 주문 실행
* 포지션 및 리스크 관리 자동화
* 전략 플러그인 구조
* 향후 SOAR Playbook 기반 전략 관리 확장

LTB는 다음 4계층 구조로 설계된다.

```
Engine
API
Web UI
Docs
```

---

# 2. System Architecture

전체 시스템 구조

```
                +----------------------+
                |       Web UI         |
                |   Trading Dashboard  |
                +----------+-----------+
                           |
                        REST API
                           |
        +---------------------------------------+
        |        Admin Console (FastAPI)        |
        |                                       |
        |  /admin/logs                          |
        |  /admin/system                        |
        |  /admin/strategy                      |
        |  /admin/docs                          |
        |                                       |
        |  Swagger = 개발자 콘솔                |
        +----------------+----------------------+
                         |
                      Event Bus
                         |
        +---------------------------------------+
        |               LTB Engine              |
        |---------------------------------------|
        |                                       |
        |  MarketWorker        시장 데이터      |
        |  StrategyWorker      전략 평가        |
        |  ExecutionWorker     주문 생성        |
        |  OrderExecutorWorker 브로커 주문      |
        |  PortfolioWorker     포지션 관리      |
        |  TrailingStopWorker  트레일링 스탑    |
        |  RiskWorker          리스크 관리      |
        |  AnalyticsWorker     통계 분석        |
        |  AlertWorker         알림 시스템      |
        |                                       |
        +---------------------------------------+
                         |
                    Broker API
                         |
                    KIS / Broker
```

---

# 3. Event Driven Architecture

LTB는 Event-Driven Architecture 기반이다.

이벤트 흐름:

```
market.price
    ↓
strategy.signal
    ↓
execution.order
    ↓
order.fill
    ↓
portfolio.update
    ↓
risk.monitor
```

장점

* 높은 확장성
* Worker 분리
* 전략 모듈 확장 가능
* 장애 격리 가능

---

# 4. Current Implemented Components

현재 구현된 핵심 모듈

Engine Core

```
QueueBus (Event Bus)
Runtime Worker Engine
Execution Engine
Portfolio Manager
Trailing Stop
Risk Monitor
Analytics Engine
Alert System
```

Management

```
Admin API (FastAPI)
Swagger Management Console
Internal Docs Viewer
```

---

# 5. Admin Console

Admin Console은 FastAPI 기반 관리 API이다.

관리 API 예시

```
/admin/logs
/admin/docs
/admin/system
/admin/strategy
```

Swagger Console

```
http://localhost:8000/docs
```

Swagger 역할

* API 테스트
* 운영 관리
* 디버깅

---

# 6. Internal Documentation System

운영 문서는 Markdown 기반으로 관리한다.

```
docs/

operations/
strategy/
architecture/
deployment/
```

예시

```
docs/operations/log_inspection.md
docs/operations/docker_commands.md
docs/strategy/turtle.md
docs/architecture/ltb_system.md
```

Docs는 Admin API를 통해 조회 가능하다.

---

# 7. Strategy System Design

전략 시스템은 플러그인 구조로 설계된다.

```
src/ltb/strategy/

strategy_engine.py

strategies/
    volume_breakout.py
    turtle_breakout.py
    momentum.py
```

전략 인터페이스

```
evaluate(market_data)
```

각 전략은 독립 모듈로 구현된다.

---

# 8. Implemented Strategies (Planned)

### Volume Breakout Strategy

조건

* 거래량 급증
* 가격 박스 돌파

목표

* 초기 추세 진입

---

### Turtle Breakout Strategy

조건

* N기간 최고가 돌파

예

```
20-day breakout
```

목표

* 추세 추종

---

### Pullback Continuation Strategy

조건

* 상승 추세
* 눌림목 발생

목표

* 추세 지속 수익 확보

---

# 9. Position Management

포지션 관리 전략

```
ATR Trailing Stop
Panic Exit
Stop Loss
Box Breakdown Exit
```

익절 구조

```
1 ATR → 30%
2 ATR → 30%
3 ATR → 40%
```

---

# 10. Portfolio Limits

포트폴리오 제한

```
동시 종목 수: 5
종목당 최대 진입: 3
손절 2회 발생 시 재진입 금지
```

---

# 11. Future Strategy Playbook (SOAR Integration)

향후 전략 관리 시스템은 SOAR Playbook 구조로 확장될 수 있다.

Playbook 구조

```
Trigger
Condition
Action
Next
```

예

```
market.price
    ↓
volume spike
    ↓
BUY signal
    ↓
risk check
```

Playbook은 YAML 기반으로 관리될 예정이다.

예

```
strategy_playbook.yaml
```

---

# 12. Web UI Roadmap

현재 Swagger는 관리 콘솔 역할만 수행한다.

향후 Web UI는 별도 Dashboard로 구축한다.

예상 구조

```
Trading Dashboard

Dashboard
Portfolio
Logs
Strategy
Docs
System
```

기술 후보

```
FastAPI + Jinja
React Dashboard
```

---

# 13. SonarQube + Local LLM Integration

향후 코드 품질 및 자동 분석을 위해 다음 시스템을 검토 중이다.

```
SonarQube
Local LLM
```

가능한 활용

```
자동 코드 리뷰
보안 취약점 분석
전략 코드 설명 생성
운영 문서 자동 생성
```

---

# 14. Development Roadmap

현재 단계

```
Engine Stabilization
Admin API
Docs System
```

다음 단계

```
Strategy Engine
Strategy Config
Simulation Testing
Paper Trading Integration
Web Dashboard
```

최종 목표

```
Fully automated trading platform
```

---

# 15. Conclusion

LTB는 Event-Driven 기반 자동 트레이딩 시스템으로 설계되었다.

현재 핵심 엔진 구조는 완성되었으며 다음 단계는 전략 시스템 구축이다.
