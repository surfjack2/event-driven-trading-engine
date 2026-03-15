# LTB Auto Trading Report Implementation Design

## 1. 목적

LTB는 자동 매매 결과를 분석하고 전략 개선을 지원하기 위해  
매 거래일 종료 후 자동으로 Trading Report를 생성한다.

이 리포트는 다음 목적을 가진다.

- 매매 성과 분석
- 전략별 성능 비교
- 리스크 분석
- 전략 개선 방향 제시

리포트는 Web Dashboard에서 조회할 수 있으며  
HTML / JSON / PDF 형태로 저장할 수 있다.

---

# 2. 전체 아키텍처

Trading Report 시스템은 다음 구조로 구성된다.

Trading Engine  
↓  
Trade Ledger  
↓  
Analytics Data  
↓  
TradingReportWorker  
↓  
ReportBuilder  
↓  
ReportStorage  
↓  
Dashboard Viewer  

---

# 3. Worker 구조

새 Worker 추가

src/ltb/runtime/workers/trading_report_worker.py

역할

- 거래 기록 수집
- 전략 성능 데이터 수집
- 리스크 데이터 수집
- 리포트 생성

구독 이벤트

market.close  
system.daily_report  

출력 이벤트

daily.report.generated

---

# 4. 데이터 수집 구조

Report Worker는 다음 Worker들의 데이터를 사용한다.

TradeLedgerWorker  
PortfolioWorker  
StrategyPerformanceWorker  
RiskWorker  
AnalyticsWorker  

데이터 흐름

TradeLedger → 거래 기록  
Portfolio → 포지션 상태  
StrategyPerformance → 전략별 성과  
RiskWorker → 리스크 지표  
AnalyticsWorker → 통계

---

# 5. Report Builder

파일

src/ltb/report/report_builder.py

역할

- 데이터 정리
- 통계 계산
- 리포트 포맷 생성

구조

build_summary()  
build_strategy_performance()  
build_risk_metrics()  
build_trade_analysis()  
build_improvement_suggestions()

---

# 6. Report Storage

파일

src/ltb/report/report_storage.py

역할

리포트 저장 및 관리

저장 위치

reports/daily/

파일 형식

JSON  
HTML  
PDF

파일 예

report_2026_03_15.json  
report_2026_03_15.html  

---

# 7. 리포트 데이터 구조

리포트 JSON 구조

{
 "date": "2026-03-15",
 "summary": {
  "total_trades": 24,
  "win_rate": 0.625,
  "total_pnl": 2140,
  "average_trade": 89
 },
 "strategies": [
  {
   "name": "momentum",
   "trades": 10,
   "win_rate": 0.7,
   "pnl": 1200
  },
  {
   "name": "vwap_reclaim",
   "trades": 8,
   "win_rate": 0.62,
   "pnl": 640
  }
 ],
 "risk": {
  "max_drawdown": -0.018,
  "avg_heat": 0.031,
  "avg_exposure": 0.58
 },
 "best_trade": {
  "symbol": "TEST026",
  "pnl": 410
 },
 "worst_trade": {
  "symbol": "TEST031",
  "pnl": -120
 }
}

---

# 8. Dashboard 연동

Dashboard 메뉴

Reports

표시 항목

Today's Summary  
Strategy Performance  
Risk Metrics  
Best / Worst Trades  

또는

View Full Report

---

# 9. CLI 조회 기능

CLI에서도 조회 가능하도록 설계한다.

예

ltb report today

ltb report 2026-03-15

출력 예

Trades: 24  
Win Rate: 62.5%  
PnL: +2140  

Best Trade: TEST026 +410  

---

# 10. 향후 확장

Weekly Report  
Monthly Report  
Strategy Performance Trends  
AI Strategy Analysis  

---

# 11. 구현 우선순위

현재 개발 단계에서는 구조만 정의한다.

우선순위

1. Trading Engine 안정화
2. Mode Control 구조
3. Dashboard 기본 기능
4. Trading Report 구현

Trading Report는 엔진 안정화 이후 구현한다.
