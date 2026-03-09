# LTB Log Inspection Guide

프로젝트: LTB (Live Trading Bot)

목적: 시스템 실행 중 오류 / 예외 / 이상동작을 빠르게 확인하기 위한 운영 가이드

---

# 1. 컨테이너 실시간 로그 확인

docker logs -f kis_trader

확인 항목

BUS ERROR  
Python Traceback  
Worker crash  
Runtime exception

---

# 2. 최근 로그 확인

docker logs --tail 100 kis_trader

또는

docker logs --tail 50 kis_trader

---

# 3. ERROR / WARNING 검색

docker logs kis_trader 2>&1 | grep -E "ERROR|WARNING"

---

# 4. BUS ERROR 검색

docker logs kis_trader 2>&1 | grep "BUS ERROR"

---

# 5. Python Traceback 검색

docker logs kis_trader 2>&1 | grep -i traceback

---

# 6. Exception 검색

docker logs kis_trader 2>&1 | grep -i exception

또는

docker logs kis_trader 2>&1 | grep -i error

---

# 7. engine.log 실시간 확인

tail -f logs/engine.log

확인 항목

STRATEGY  
EXECUTION  
PORTFOLIO  
TRAIL STOP  
RISK ENGINE  

---

# 8. engine.log 에러 검색

grep -E "ERROR|WARNING" logs/engine.log

---

# 9. 주문 흐름 확인

docker logs kis_trader | grep EXECUTION

또는

docker logs kis_trader | grep -E "EXECUTION|ORDER EXECUTOR|KIS"

정상 흐름

STRATEGY  
→ EXECUTION  
→ ORDER EXECUTOR  
→ KIS  
→ PORTFOLIO  

---

# 10. 포지션 상태 확인

docker logs kis_trader | grep PORTFOLIO

정상 흐름

position = 0  
BUY  
position = 1  
SELL  
position = 0  

---

# 11. Trailing Stop 확인

docker logs kis_trader | grep TRAIL

정상 로그

TRAIL INIT  
TRAIL MOVE  
TRAIL STOP HIT  

---

# 12. Risk Engine 확인

docker logs kis_trader | grep RISK

---

# 13. 컨테이너 상태 확인

docker ps

정상 상태

Up

문제 상태

Restarting  
Exited  

---

# 14. 로그 파일 크기 확인

ls -lh logs/

---

# 15. 운영 편의 alias

alias ltbcheck='docker logs kis_trader 2>&1 | grep -E "ERROR|WARNING|BUS|Traceback"'

사용

ltbcheck

---

# 16. 정상 로그 패턴

STRATEGY received  
EXECUTION processing signal  
ORDER EXECUTOR executing  
PORTFOLIO updated  
TRAIL STOP HIT  

---

# 17. 즉시 대응 필요 로그

BUS ERROR  
Traceback  
Exception  
KeyError  
ModuleNotFoundError  

---

# 18. 권장 운영 로그 모니터링

터미널 1

docker logs -f kis_trader

터미널 2

tail -f logs/engine.log

터미널 3

docker logs kis_trader 2>&1 | grep -E "ERROR|WARNING|BUS"
