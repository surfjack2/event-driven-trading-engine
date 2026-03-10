from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from datetime import datetime

router = APIRouter(prefix="/ops", tags=["operations"])


# ====================================
# OPS GUIDE PAGE (기존 기능 유지)
# ====================================
@router.get("")
def ops_page():

    return FileResponse(
        "web/ui/ops/ops_guide.html"
    )


# ====================================
# SYSTEM HEALTH
# ====================================
@router.get("/health")
def health():

    return {
        "status": "ok",
        "engine": "running"
    }


# ====================================
# WORKER STATUS
# ====================================
@router.get("/workers")
def workers():

    workers = [
        "MarketWorker",
        "StrategyWorker",
        "ExecutionWorker",
        "OrderExecutorWorker",
        "PortfolioWorker",
        "TrailingStopWorker",
        "RiskWorker",
        "AnalyticsWorker",
        "AlertWorker"
    ]

    return {
        "workers": workers,
        "status": "running"
    }


# ====================================
# ENGINE STATUS
# ====================================
@router.get("/status")
def system_status():

    return {
        "engine": "running",
        "event_bus": "running",
        "market_worker": "running",
        "strategy_worker": "running",
        "execution_worker": "running",
        "portfolio_worker": "running",
        "risk_worker": "running"
    }


# ====================================
# LOG SUMMARY
# ====================================
@router.get("/logs/summary")
def log_summary():

    log_file = "logs/engine.log"

    if not os.path.exists(log_file):
        return {"error": "log file not found"}

    with open(log_file, "r") as f:
        lines = f.readlines()

    last_lines = lines[-200:]

    stats = {
        "market_events": 0,
        "strategy_signals": 0,
        "orders": 0,
        "portfolio_updates": 0,
        "trailing_events": 0
    }

    for line in last_lines:

        if "MARKET" in line:
            stats["market_events"] += 1

        if "STRATEGY" in line:
            stats["strategy_signals"] += 1

        if "ORDER EXECUTOR" in line:
            stats["orders"] += 1

        if "PORTFOLIO" in line:
            stats["portfolio_updates"] += 1

        if "TRAIL" in line:
            stats["trailing_events"] += 1

    return {
        "checked_lines": len(last_lines),
        "stats": stats
    }


# ====================================
# RECENT TRADES (log based)
# ====================================
@router.get("/trades/recent")
def recent_trades():

    log_file = "logs/engine.log"

    if not os.path.exists(log_file):
        return {"trades": []}

    trades = []

    with open(log_file, "r") as f:
        lines = f.readlines()

    for line in lines[-200:]:

        if "executing order" in line:

            trades.append({
                "timestamp": str(datetime.now()),
                "event": line.strip()
            })

    return {
        "recent_trades": trades[-20:]
    }
