LTB Remaining Development Roadmap

Phase 1 — Core Engine Stabilization

1. Mode Structure Refactor

목표

BACKTEST
PAPER
LIVE

구조 분리

필요 작업

ExecutionRouter 분리
MarketWorker 조건 실행
ReplayMarketWorker 통합
BrokerExecutionAdapter

2. Strategy Tuning

현재 전략

simple_momentum
vwap_reclaim
vwap_bounce

튜닝 작업

ATR multiplier
RSI threshold
VWAP band width
volume ratio
alpha scoring

추가 전략 후보

breakout strategy
mean reversion
opening range breakout
volatility expansion
Phase 2 — Market Integration

3. Upbit Structure

구현

Upbit WebSocket market stream
Orderbook
Trade stream
Ticker stream

Worker

UpbitMarketWorker
UpbitExecutionAdapter
UpbitAccountWorker

4. CLI Backtest UI

CLI 인터페이스

backtest run
strategy select
date range
symbol filter

결과 출력

PnL
Sharpe ratio
Max drawdown
Win rate
Trade distribution
Phase 3 — Trading Infrastructure

5. API Key Management

구현

API key storage
environment variable
secure config

기능

API validation
connection test
account balance check

6. Web UI

구성

FastAPI backend
React dashboard

화면

portfolio view
open positions
PnL chart
strategy status
risk metrics
Phase 4 — Analytics & Reporting

7. Auto Trading Report

자동 생성

daily report
weekly report
monthly report

포함 내용

strategy performance
portfolio heat
trade distribution
risk metrics
drawdown analysis

출력

PDF
HTML
Dashboard
Phase 5 — Advanced Systems

8. Additional Features

추가 개발

Multi-market support
Portfolio heat control
Strategy auto-disable
Machine learning signal ranking
Risk adaptive sizing
Final Target

LTB → Full Autonomous Trading Engine

구성

Market ingestion
Strategy execution
Portfolio management
Risk control
Analytics
Auto reporting
Web monitoring
