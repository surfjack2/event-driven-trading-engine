# LTB Detailed Architecture

## 1. Platform Layer

LTB Platform 구성

Web UI
Admin Console
Dashboard

API Layer

Trading Engine

Watchdog

Database
Cache


---

## 2. Trading Engine Structure

Trading Engine 내부 구성

Event Bus

Workers

MarketWorker
IndicatorWorker
StrategyWorker
ExecutionWorker
OrderExecutorWorker
PortfolioWorker
TrailingStopWorker
RiskWorker
AnalyticsWorker
AlertWorker


---

## 3. Data Storage Layer

Primary Database

PostgreSQL

사용 테이블

markets
market_indexes
trades
positions
strategy_stats
alerts
engine_health


Cache

Redis

사용 목적

market data cache
dashboard cache
session


---

## 4. External Integration

Broker API

KIS
Future US Broker

Market Data

Exchange API
News API


---

## 5. System Monitoring

Watchdog

engine heartbeat
worker heartbeat
api health


Monitoring

CPU
RAM
API latency


---

## 6. Deployment Architecture

Container

Docker

Service

Trading Engine Container
API Container
Dashboard Container
Redis
PostgreSQL
