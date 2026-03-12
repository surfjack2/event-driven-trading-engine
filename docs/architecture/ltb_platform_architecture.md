# LTB Platform Architecture

## 1. Overview

LTB는 Event-Driven 기반 자동매매 플랫폼이다.

구성 요소

Trading Engine  
Market Data System  
Risk Management  
Analytics Engine  
Alert System  
Admin Console  
Dashboard  
Database  
Watchdog  

플랫폼 구조

Watchdog  
↓  
Trading Engine  
↓  
Event Bus  
↓  
Workers  

Dashboard / Admin Console  
↓  
API Layer  
↓  
Database  

---

## 2. Platform Components

### Trading Engine

자동매매 핵심 엔진

구성

Strategy  
Risk  
Execution  
Portfolio  

---

### Market Data System

시장 데이터 수집

price  
index  
fx  
news  

MarketWorker가 데이터 허브 역할 수행

---

### Dashboard

운영 모니터링 UI

구성

Market  
System  
Portfolio  
Performance  
Alerts  

표시 데이터

시장 지수  
환율  
뉴스  
전략 성과  
계좌 상태  

---

### Admin Console

FastAPI 기반 관리 콘솔

Top Menu

Dashboard  
Trading  
Reports  
Logs  
AI  
Settings  

기능

전략 관리  
엔진 제어  
로그 조회  
시스템 설정  

---

### Watchdog

시스템 감시 프로세스

감시 대상

engine heartbeat  
worker heartbeat  
api health  

동작

heartbeat lost → engine restart  

---

### Alert System

Alert 종류

Trading Alert  
Risk Alert  
System Alert  
Market Alert  

알림 방식

popup  
telegram  
slack  

---

### Database

Primary DB

PostgreSQL

사용 테이블

markets  
market_indexes  
trades  
positions  
strategy_stats  
alerts  
engine_health  

---

### Cache

Redis

용도

market cache  
dashboard cache  
session data  

---

### DevOps

Container

Docker  

CI/CD

GitHub Actions
