# LTB Logging Policy

## 1. 목적

LTB(Live Trading Bot)의 로그 정책은 다음 목적을 가진다.

- 트레이딩 이벤트 기록
- 시스템 상태 추적
- 장애 분석
- 운영 모니터링

로그는 **운영 로그(operational logs)**와 **모니터링 로그(monitoring logs)**로 구분한다.

---

# 2. 로그 분류

## 2.1 Trading Log (거래 로그)

트레이딩 이벤트는 반드시 기록되어야 한다.

다음 이벤트는 **INFO 레벨 이상으로 기록한다.**

ENGINE START  
API SESSION CONNECTED  
ORDER REQUEST  
ORDER FILLED  
PORTFOLIO OPEN  
PORTFOLIO CLOSE  
TRAILING STOP TRIGGERED  
COOLDOWN START  

이 로그는 **거래 기록 및 사고 분석에 사용된다.**

---

## 2.2 Risk Log (리스크 이벤트)

리스크 관련 이벤트는 **WARNING 레벨 이상**으로 기록한다.

예:

global position limit reached  
risk engine blocked order  
daily loss limit reached  
kill switch triggered  

---

## 2.3 System Log (시스템 로그)

시스템 상태 로그는 운영 추적용이다.

예:

WORKER STARTED  
ENGINE PROCESS STARTED  
WORKER CRASH  
WORKER RESTART  
API RECONNECT  

---

## 2.4 Monitoring Log (모니터링 로그)

모니터링 로그는 **DEBUG 레벨**로 기록한다.

예:

cooldown active  
position gate  
indicator values  
scanner trigger  
ranking update  
market tick  

이 로그는 **실시간 모니터링 및 디버깅 목적**이다.

운영 환경에서는 기본적으로 출력하지 않는다.

---

# 3. 로그 레벨 정책

DEBUG  → 모니터링 및 디버깅  
INFO   → 거래 및 시스템 이벤트  
WARNING → 리스크 이벤트  
ERROR  → 시스템 오류  

---

# 4. 로그 출력 정책

LTB는 다음 두 가지 로그 출력을 사용한다.

## 4.1 파일 로그

파일 로그는 모든 이벤트를 기록한다.

logs/engine.log

설정:

level: DEBUG  
rotation: enabled  
max size: 10MB  
backup count: 10  

최대 저장 용량:

100MB

---

## 4.2 콘솔 로그

콘솔 로그는 운영 모니터링을 위한 것이다.

출력 레벨:

INFO  
WARNING  
ERROR  

예:

ORDER REQUEST  
PORTFOLIO OPEN  
PORTFOLIO CLOSE  

---

# 5. 로그 로테이션 정책

로그는 RotatingFileHandler를 사용한다.

설정:

maxBytes = 10MB  
backupCount = 10  

로그 구조:

logs/  
    engine.log  
    engine.log.1  
    engine.log.2  
    ...  
    engine.log.10  

---

# 6. 운영 모니터링 방법

운영 중 실시간 로그 확인:

tail -f logs/engine.log

또는

docker logs -f <container>

---

# 7. 중요 이벤트 모니터링

중요 트레이딩 이벤트만 확인할 경우:

grep -E "PORTFOLIO|ORDER|FILLED"

예:

PYTHONPATH=src python3 main.py 2>&1 | grep -E "PORTFOLIO|ORDER"

---

# 8. 로그 보존 정책

로그 보존 기간:

최대 100MB

로그 백업은 별도로 수행하지 않는다.

필요 시 운영 환경에서 로그 수집 시스템을 사용한다.

예:

ELK Stack  
Grafana Loki  
CloudWatch  

---

# 9. 향후 확장 계획

향후 다음 로그 분리가 가능하다.

logs/  
   engine.log  
   trading.log  
   risk.log  

현재 버전에서는 단일 로그 파일 정책을 사용한다.

---

# 10. 정책 적용 범위

이 정책은 다음 모듈에 적용된다.

runtime workers  
execution engine  
risk engine  
portfolio manager  
strategy engine  

