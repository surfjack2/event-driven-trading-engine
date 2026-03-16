============================================================
LTB GIT HISTORY INSPECTION GUIDE
Purpose: Git History Analysis for Engine Refactoring
Scope: Engine Stabilization / Code Cleanup
============================================================


1. PURPOSE

LTB 프로젝트는 현재 다음 단계에 진입하였다.

Engine Architecture → Engine Stabilization

이 단계에서는 코드 구조 안정화 및 리팩토링이 진행되며
Git History 분석은 다음 목적을 가진다.

- Dead Code 식별
- 리팩토링 중단 상태 확인
- 기존 구조 변경 의도 파악
- 중복 시스템 제거
- 안전한 코드 수정 지원


------------------------------------------------------------
2. WHY GIT HISTORY IS IMPORTANT
------------------------------------------------------------

현재 코드 분석 과정에서 다음과 같은 구조 중복이 발견되었다.

engine.py
engine_process.py

EventBus
QueueBus

MarketWorker
ReplayMarketWorker

이 구조는 다음 두 가지 가능성을 가진다.

Case 1

리팩토링 중간 상태

EventBus → QueueBus 전환
engine.py → engine_process.py 전환

Case 2

구 코드가 제거되지 않고 남아 있는 상태

Dead Code


Git History 분석을 통해 다음을 판단할 수 있다.

- 어떤 파일이 최신 구조인지
- 어떤 코드가 더 이상 사용되지 않는지
- 리팩토링 작업 진행 상태


------------------------------------------------------------
3. GIT LOG PAGER ISSUE
------------------------------------------------------------

git log 명령은 기본적으로 pager(less)를 사용한다.

예

git log

실행 시

git log
↓
less 실행
↓
다음 명령 실행 불가

이 때문에 여러 git 명령을 한 번에 실행하면
첫 번째 log 출력에서 멈추게 된다.

따라서 다음 방법 중 하나를 사용해야 한다.


------------------------------------------------------------
4. SOLUTION
------------------------------------------------------------


방법 1 (추천)

--no-pager 옵션 사용

예

git --no-pager log


방법 2

일시적으로 pager 비활성화

예

GIT_PAGER=cat git log


방법 3

git pager 설정 변경 (비추천)

git config --global core.pager cat


------------------------------------------------------------
5. REQUIRED GIT COMMANDS
------------------------------------------------------------

엔진 구조 분석을 위해 다음 파일들의 git history를 확인한다.

확인 대상

runtime/engine.py
runtime/engine_process.py
runtime/event_bus.py
runtime/queue_bus.py
runtime/workers/market_worker.py


실행 명령


git --no-pager log --oneline -n 30


git --no-pager log -- src/ltb/runtime/engine.py


git --no-pager log -- src/ltb/runtime/engine_process.py


git --no-pager log -- src/ltb/runtime/event_bus.py


git --no-pager log -- src/ltb/runtime/queue_bus.py


git --no-pager log -- src/ltb/runtime/workers/market_worker.py


------------------------------------------------------------
6. GIT BLAME (ADVANCED ANALYSIS)
------------------------------------------------------------

대형 프로젝트에서는 git log보다 git blame이 더 유용할 수 있다.

git blame은 다음 정보를 제공한다.

- 특정 코드 라인을 누가 작성했는지
- 언제 수정되었는지
- 어떤 commit에서 변경되었는지


예

git blame src/ltb/runtime/engine_process.py


이를 통해

- 리팩토링 변경 위치
- 구조 변경 시점
- 코드 작성자 의도

등을 파악할 수 있다.


------------------------------------------------------------
7. EXPECTED OUTCOME
------------------------------------------------------------

Git History 분석을 통해 다음 작업을 수행한다.

Dead Code 제거

가능한 대상

runtime/engine.py
runtime/event_bus.py


Engine 구조 통합

engine_process.py 기반으로 엔진 통합


Event Bus 표준화

QueueBus 기반 구조 유지


MarketWorker 리팩토링

MockMarketWorker
ReplayMarketWorker
LiveMarketWorker

구조 분리


------------------------------------------------------------
8. ENGINE STABILIZATION GOAL
------------------------------------------------------------

현재 LTB 프로젝트는 다음 단계에 있다.

Engine Stabilization Phase

목표

- 중복 코드 제거
- 엔진 구조 단일화
- Mode Architecture 안정화
- Market Source 구조 분리
- Broker Integration 준비


이 작업 완료 후 다음 단계로 진행한다.

Market Integration

- KIS API
- Upbit API

Backtest Infrastructure

CLI Backtest System

Dashboard System


============================================================
END OF DOCUMENT
============================================================
