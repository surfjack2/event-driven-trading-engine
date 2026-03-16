# LTB Architecture

Live Trading Bot (LTB)는 이벤트 기반 멀티 워커 구조의 트레이딩 엔진이다.

Core 개념
- Event driven runtime
- Worker based pipeline
- Strategy modular system
- Portfolio optimizer
- Risk engine

--------------------------------------------------

Runtime Layer
runtime.engine
runtime.watchdog
queue_bus

역할
이벤트 버스 관리
워커 실행
시스템 상태 관리

--------------------------------------------------

Market Layer
market_worker
indicator_worker
scanner_worker

역할
시장 데이터 수집
지표 계산
종목 스캔

--------------------------------------------------

Strategy Layer
strategy_worker
strategy_engine
strategy_loader

전략
simple_momentum
vwap_reclaim
vwap_bounce

역할
전략 평가
신호 생성

--------------------------------------------------

Signal Pipeline
signal_dedup_worker
signal_persistence_worker
signal_ranking_worker

역할
중복 신호 제거
신호 지속성 확인
신호 랭킹 계산

--------------------------------------------------

Allocation Layer
strategy_allocation_worker

역할
전략별 자본 배분

--------------------------------------------------

Quality Layer
trade_quality_filter_worker

역할
저품질 진입 제거

--------------------------------------------------

Portfolio Layer
position_intent_worker
correlation_filter_worker
portfolio_optimizer_worker
portfolio_worker

역할
포지션 후보 생성
상관관계 필터
최종 포트폴리오 선택

--------------------------------------------------

Execution Layer
execution_worker
order_executor_worker

역할
주문 실행
체결 관리

--------------------------------------------------

Risk Layer
risk_worker
risk_kill_switch
exposure_worker
position_sizer

역할
리스크 관리

--------------------------------------------------

Meta Layer
strategy_performance_worker
meta_strategy_worker

역할
전략 자동 enable / disable
