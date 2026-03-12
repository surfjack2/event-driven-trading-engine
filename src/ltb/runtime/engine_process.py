from ltb.system.logger import logger
from ltb.runtime.queue_bus import QueueBus

from ltb.runtime.workers.market_worker import MarketWorker
from ltb.indicator.indicator_worker import IndicatorWorker
from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker
from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker


def run_engine():

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    workers = [

        MarketWorker(bus),
        IndicatorWorker(bus),
        StrategyWorker(bus),
        ExecutionWorker(bus),
        OrderExecutorWorker(bus),
        PortfolioWorker(bus),
        TrailingStopWorker(bus),
        RiskWorker(bus),
        AnalyticsWorker(bus),
        AlertWorker(bus)

    ]

    for worker in workers:

        logger.info(f"[STARTING WORKER] {worker.__class__.__name__}")

        worker.run()

    logger.info("=== ALL WORKERS STARTED ===")
