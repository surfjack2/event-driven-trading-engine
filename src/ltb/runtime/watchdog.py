import threading
import time

from ltb.runtime.queue_bus import QueueBus

from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.scanner_worker import ScannerWorker
from ltb.runtime.workers.universe_scanner_worker import UniverseScannerWorker
from ltb.runtime.workers.ranking_worker import RankingWorker
from ltb.indicator.indicator_worker import IndicatorWorker

from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.signal_ranking_worker import SignalRankingWorker
from ltb.runtime.workers.strategy_allocation_worker import StrategyAllocationWorker

from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trade_ledger_worker import TradeLedgerWorker
from ltb.runtime.workers.strategy_performance_worker import StrategyPerformanceWorker
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker
from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker
from ltb.runtime.workers.killswitch_worker import KillSwitchWorker
from ltb.runtime.workers.heartbeat_worker import HeartbeatWorker

from ltb.system.logger import logger


def start_worker(worker):

    def run_worker():

        while True:

            try:

                worker.run()

            except Exception as e:

                logger.error(
                    f"[WORKER CRASH] {worker.__class__.__name__} error={e}"
                )

                logger.error(
                    f"[WORKER RESTART] restarting {worker.__class__.__name__} in 2s"
                )

                time.sleep(2)

    logger.info(f"[STARTING WORKER] {worker.__class__.__name__}")

    t = threading.Thread(target=run_worker, daemon=True)

    t.start()

    return t


def main():

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    workers = [

        # market data
        MarketWorker(bus),

        # scanning
        ScannerWorker(bus),
        UniverseScannerWorker(bus),

        # symbol ranking
        RankingWorker(bus),

        # indicator calculation
        IndicatorWorker(bus),

        # strategy evaluation
        StrategyWorker(bus),

        # signal quality ranking
        SignalRankingWorker(bus),

        # strategy capital allocation
        StrategyAllocationWorker(bus),

        # execution pipeline
        ExecutionWorker(bus),
        OrderExecutorWorker(bus),

        # portfolio management
        PortfolioWorker(bus),
        TradeLedgerWorker(bus),

        # performance tracking
        StrategyPerformanceWorker(bus),

        # risk & exit
        TrailingStopWorker(bus),
        RiskWorker(bus),

        # analytics
        AnalyticsWorker(bus),

        # alerts
        AlertWorker(bus),

        # emergency protection
        KillSwitchWorker(bus),

        # engine health monitoring
        HeartbeatWorker(bus),

    ]

    threads = []

    for worker in workers:
        threads.append(start_worker(worker))

    logger.info("=== ALL WORKERS STARTED ===")

    while True:
        time.sleep(5)
