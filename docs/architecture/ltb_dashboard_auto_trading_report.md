# LTB Dashboard Auto Trading Report (Optional Feature)

## 1. 개요

LTB는 자동 매매 결과를 분석하고 전략 개선에 활용하기 위해  
매 거래일 종료 후 자동으로 매매 성과 리포트를 생성하는 기능을 제공한다.

이 기능은 다음 목적을 가진다.

- 자동 매매 결과 요약
- 전략 성능 평가
- 리스크 분석
- 전략 개선 방향 제시

리포트는 Web Dashboard에서 확인할 수 있으며  
필요 시 파일(PDF / HTML)로 저장할 수 있다.

이 기능은 **필수 기능은 아니며 구조만 설계에 반영하고 이후 구현**한다.

---

# 2. 리포트 생성 시점

리포트 생성 트리거

Market Close Event

또는

Daily Scheduler

예시

US Market Close → 16:00 ET  
KR Market Close → 15:30 KST  
Crypto → Daily 00:00 UTC  

이벤트

market.close

또는

system.daily_report

---

# 3. Report Worker

새 Worker 추가

src/ltb/runtime/workers/trading_report_worker.py

역할

- Trade Ledger 분석
- Portfolio 상태 분석
- Strategy 성능 분석
- 리포트 생성

구독 이벤트

market.close  
system.daily_report  

출력 이벤트

daily.report.generated

---

# 4. 리포트 데이터 소스

리포트는 다음 데이터를 기반으로 생성된다.

TradeLedgerWorker  
PortfolioWorker  
StrategyPerformanceWorker  
RiskWorker  
AnalyticsWorker  

---

# 5. 리포트 내용

## 5.1 Trading Summary

Total Trades  
Winning Trades  
Losing Trades  
Win Rate  
Total PnL  
Average PnL  

예시

Trades : 24  
Win Rate : 62.5%  
Total PnL : +$2140  
Average Trade : +$89  

---

## 5.2 Strategy Performance

전략별 성과

Strategy | Trades | Win Rate | PnL  
Momentum | 10 | 70% | +1200  
VWAP Reclaim | 8 | 62% | +640  
VWAP Bounce | 6 | 50% | +300  

---

## 5.3 Risk Metrics

Max Drawdown  
Average Risk  
Portfolio Heat  
Exposure  

예시

Max Drawdown : -1.8%  
Portfolio Heat Avg : 3.1%  
Exposure Avg : 58%  

---

## 5.4 Best / Worst Trades

Top 3 Winners  
Top 3 Losers  

예시

Best Trade  
TEST026 +$410  

Worst Trade  
TEST031 -$120  

---

## 5.5 Market Regime

Market Regime Distribution

예시

Bull : 40%  
Sideways : 50%  
Bear : 10%  

---

## 5.6 Strategy Insight

자동 분석 결과

예

Momentum 전략이 가장 안정적 수익을 기록  
VWAP Bounce 전략은 변동성 높은 구간에서 손실 증가  

---

## 5.7 개선 제안 (AI 기반 가능)

향후 확장

Strategy tuning suggestion  
Risk parameter suggestion  
Position sizing adjustment  

예

Reduce position size for VWAP Bounce  
Increase filter threshold for low liquidity assets  

---

# 6. 리포트 저장

리포트 저장 위치

reports/daily/

파일 형식

HTML  
JSON  
PDF (optional)

파일 예

report_2026_03_15.html

---

# 7. Dashboard 표시

Dashboard에 Report Panel 추가

TRADING REPORT

구성

Today's Summary  
Strategy Performance  
Risk Metrics  
Best / Worst Trades  

또는

View Full Report

---

# 8. Report Viewer

Dashboard 메뉴

Reports

기능

Daily Reports  
Strategy Reports  
Performance Trends  

---

# 9. 성능 고려

리포트 생성은 엔진 성능에 영향을 주지 않도록  
별도 Worker에서 실행한다.

TradingReportWorker

리포트 생성 시점

Market Close 이후

---

# 10. 향후 확장

가능한 확장 기능

Weekly Report  
Monthly Report  
Strategy Report  
AI Strategy Analysis  

---

# 11. 구현 우선순위

현재 개발 단계에서는 구조만 정의한다.

우선순위

1. Trading Engine 안정화
2. Mode Control 구현
3. Dashboard 기본 기능
4. Trading Report 기능 구현

Auto Trading Report는 **후순위 기능으로 유지한다.**
