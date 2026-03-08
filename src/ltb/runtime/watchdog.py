import threading
import time

from ltb.runtime.queue_bus import QueueBus

from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker
from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker

from ltb.system.logger import logger


def start_worker(worker):

    logger.info(f"[STARTING WORKER] {worker.__class__.__name__}")

    t = threading.Thread(target=worker.run, daemon=True)
    t.start()

    return t


def main():

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    workers = [

        MarketWorker(bus),

        StrategyWorker(bus),

        ExecutionWorker(bus),

        OrderExecutorWorker(bus),

        PortfolioWorker(bus),

        TrailingStopWorker(bus),

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
