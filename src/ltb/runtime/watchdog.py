import threading
import time

from ltb.runtime.queue_bus import QueueBus

# 기존 workers
from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker

# 새 execution layer
from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker

from ltb.system.logger import logger


def start_worker(worker):

    logger.info("[STARTING WORKER] %s", worker.__class__.__name__)

    thread = threading.Thread(
        target=worker.run,
        daemon=True
    )

    thread.start()

    return thread


def main():

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    workers = [

        # market data
        MarketWorker(bus),

        # strategy
        StrategyWorker(bus),

        # execution layer
        ExecutionWorker(bus),
        OrderExecutorWorker(bus),

        # portfolio
        PortfolioWorker(bus),

        # system workers
        RiskWorker(bus),
        AnalyticsWorker(bus),
        AlertWorker(bus),
    ]

    threads = []

    for worker in workers:
        threads.append(start_worker(worker))

    logger.info("=== ALL WORKERS STARTED ===")

    while True:
        time.sleep(5)
