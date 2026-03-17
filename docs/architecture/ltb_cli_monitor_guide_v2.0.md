# LTB CLI Engine Monitor Guide
Version: V2.0

---

# 1. 개요

LTB 엔진은 실행 시 CLI 기반 모니터링 화면을 제공한다.

이 화면은 단순 로그가 아니라 다음 정보를 실시간으로 통합 표시하는
Trading Engine Monitoring Dashboard 역할을 한다.

표시되는 주요 정보

- 시장 상태
- 전략 신호 발생
- 포트폴리오 후보
- 주문 실행 상태
- 계좌 상태
- 엔진 성능
- Worker 상태

이 문서는 CLI 화면의 각 영역이 의미하는 바를 설명한다.

---

# 2. CLI 화면 전체 구조

CLI 화면은 다음 영역으로 구성된다.

1. Header
2. Market Regime
3. Account
4. Engine Flow
5. Pipeline
6. Ranking
7. Recent Signals
8. Optimizer
9. Execution
10. Strategy Performance
11. Engine Diagnostics
12. Worker Health

---

# 3. Header

예시

LTB ENGINE | mode=LIVE | market=KOSDAQ | uptime=00:23:41

설명

mode  
엔진 실행 모드

- LIVE
- PAPER
- BACKTEST

market  
현재 거래 시장

uptime  
엔진이 실행된 시간

---

# 4. Market Regime

예시

trend: BULL
liquidity: HIGH
exposure: 12%

status: RUNNING
positions: 2

설명

trend  
시장 방향

- BULL
- BEAR
- NEUTRAL

liquidity  
시장 유동성 상태

- LOW
- NORMAL
- HIGH

exposure  
현재 투자 자본 비율

positions  
현재 보유 종목 수

status  
엔진 상태

---

# 5. Account

예시

capital     10,000,000
equity      10,120,000
daily pnl   120,000
drawdown    1.3%

설명

capital  
초기 투자 자본

equity  
현재 총 자산

daily pnl  
오늘 수익

drawdown  
최대 손실률

---

# 6. Engine Flow

예시

ticks    4500
signals  32
orders   5
fills    3

설명

ticks  
수신된 시장 데이터 수

signals  
전략이 생성한 신호 수

orders  
주문 요청 수

fills  
체결 수

이 값은 엔진의 처리 흐름을 보여준다.

---

# 7. Pipeline

예시

rtv        120
ranking    35

설명

rtv  
Relative Turnover Scanner 결과

거래량 급증 종목을 탐지한다.

ranking  
알파 점수 기반 상위 종목 필터

즉

시장 전체 → 유망 종목 추출 단계

---

# 8. Ranking

예시

PASS AAPL
PASS NVDA
REJECT TSLA reason=score<=0

설명

Ranking Worker가 계산한 결과

PASS  
상위 신호

REJECT  
조건 미달 신호

---

# 9. Recent Signals

예시

AAPL vwap_reclaim rsi:61 vol:2.3 move:0.4%

설명

전략이 실제로 생성한 신호

구성 정보

symbol  
종목

strategy  
전략 이름

rsi  
RSI 지표

vol  
거래량 비율

move  
가격 움직임

---

# 10. Optimizer

예시

AAPL
NVDA

설명

Portfolio Optimizer가 선택한 종목

즉

실제 매수 후보

---

# 11. Execution

예시

ORDER SENT AAPL
BLOCK TSLA reason=risk_engine

설명

주문 처리 상태

ORDER SENT  
주문 전송

BLOCK  
리스크 엔진에 의해 차단

차단 이유 예

- max_positions
- portfolio_heat
- risk_engine

---

# 12. Strategy Performance

예시

vwap_reclaim trades=21 win=57% pf=1.42 pnl=340000

설명

전략 성과 정보

trades  
거래 횟수

win  
승률

pf  
Profit Factor

pnl  
총 수익

---

# 13. Engine Diagnostics

예시

event rate    320/s
queue depth   4
latency       0.002

설명

엔진 성능 지표

event rate  
초당 처리 이벤트

queue depth  
이벤트 대기열 길이

latency  
엔진 처리 지연

---

# 14. Worker Health

예시

market_worker 0.4s OK
strategy_worker 0.5s OK
execution_worker 0.6s OK

설명

Worker heartbeat 기반 상태 체크

OK  
정상

LAG  
지연 발생

이 영역은 시스템 장애를 조기 감지하는 역할을 한다.

---

# 15. 결론

LTB CLI Monitor는 단순 로그가 아니라

Trading Engine Control Panel 역할을 한다.

운영자가 다음 상태를 한 화면에서 확인할 수 있다.

- 시장 상태
- 전략 신호
- 포트폴리오 후보
- 주문 실행
- 계좌 상태
- 엔진 성능
- Worker 상태

이 모니터는 LTB 엔진 운영 및 디버깅에 핵심적인 도구이다.
