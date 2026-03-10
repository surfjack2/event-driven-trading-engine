import logging
import time

from ltb.runtime.logging_setup import setup_logging

from ltb.runtime.event_bus import EventBus

from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker
from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker

from ltb.execution.kis_executor import KISExecutor


logger = logging.getLogger("ENGINE")


class LTBEngine:

    def __init__(self):

        setup_logging()

        logger.info("=== LTB ENGINE PROCESS STARTED ===")

        self.bus = EventBus()

        logger.info("[EVENT BUS INITIALIZED]")

        self.executor = KISExecutor()

        logger.info("[KIS EXECUTOR INITIALIZED]")

        self.workers = []

        self._init_workers()

    def _init_workers(self):

        self.workers = [

            MarketWorker(self.bus),

            StrategyWorker(self.bus),

            ExecutionWorker(self.bus),

            OrderExecutorWorker(self.bus, self.executor),

            PortfolioWorker(self.bus),

            TrailingStopWorker(self.bus),

            RiskWorker(self.bus),

            AnalyticsWorker(self.bus),

            AlertWorker(self.bus)

        ]

    def start(self):

        for worker in self.workers:

            name = worker.__class__.__name__

            logger.info(f"[STARTING WORKER] {name}")

            worker.start()

        logger.info("=== ALL WORKERS STARTED ===")

        while True:
            time.sleep(1)
