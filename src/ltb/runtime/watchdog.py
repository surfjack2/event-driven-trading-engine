import threading
import time

from ltb.runtime.queue_bus import QueueBus

# market
from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.market_calendar_worker import MarketCalendarWorker
from ltb.runtime.workers.market_session_worker import MarketSessionWorker
from ltb.runtime.workers.market_regime_worker import MarketRegimeWorker
from ltb.runtime.workers.liquidity_regime_worker import LiquidityRegimeWorker
from ltb.runtime.workers.exposure_worker import ExposureWorker

# scanning
from ltb.runtime.workers.relative_turnover_scanner_worker import RelativeTurnoverScannerWorker
from ltb.runtime.workers.scanner_worker import ScannerWorker
from ltb.runtime.workers.alpha_ranking_worker import AlphaRankingWorker
from ltb.runtime.workers.universe_scanner_worker import UniverseScannerWorker

# ranking
from ltb.runtime.workers.ranking_worker import RankingWorker

# indicators
from ltb.indicator.indicator_worker import IndicatorWorker

# strategy
from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.signal_dedup_worker import SignalDedupWorker
from ltb.runtime.workers.signal_persistence_worker import SignalPersistenceWorker
from ltb.runtime.workers.signal_ranking_worker import SignalRankingWorker
from ltb.runtime.workers.liquidity_filter_worker import LiquidityFilterWorker
from ltb.runtime.workers.strategy_allocation_worker import StrategyAllocationWorker

# intent / portfolio
from ltb.runtime.workers.position_intent_worker import PositionIntentWorker
from ltb.runtime.workers.correlation_filter_worker import CorrelationFilterWorker
from ltb.runtime.workers.portfolio_optimizer_worker import PortfolioOptimizerWorker

# execution
from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker

# portfolio
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trade_ledger_worker import TradeLedgerWorker

# performance
from ltb.runtime.workers.strategy_performance_worker import StrategyPerformanceWorker
from ltb.runtime.workers.strategy_kill_switch_worker import StrategyKillSwitchWorker

# risk
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker
from ltb.runtime.workers.signal_decay_exit_worker import SignalDecayExitWorker
from ltb.runtime.workers.position_time_stop_worker import PositionTimeStopWorker
from ltb.runtime.workers.risk_worker import RiskWorker

# system
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

    t = threading.Thread(
        target=run_worker,
        daemon=True
    )

    t.start()

    return t


def main():

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    workers = [

        # =========================
        # market
        # =========================

        MarketWorker(bus),

        MarketCalendarWorker(bus),
        MarketSessionWorker(bus),

        MarketRegimeWorker(bus),
        LiquidityRegimeWorker(bus),
        ExposureWorker(bus),

        # =========================
        # scanning
        # =========================

        RelativeTurnoverScannerWorker(bus),
        ScannerWorker(bus),
        AlphaRankingWorker(bus),
        UniverseScannerWorker(bus),

        # =========================
        # ranking
        # =========================

        RankingWorker(bus),

        # =========================
        # indicators
        # =========================

        IndicatorWorker(bus),

        # =========================
        # strategy
        # =========================

        StrategyWorker(bus),
        SignalDedupWorker(bus),
        SignalPersistenceWorker(bus),
        SignalRankingWorker(bus),
        LiquidityFilterWorker(bus),
        StrategyAllocationWorker(bus),

        # =========================
        # intent layer
        # =========================

        PositionIntentWorker(bus),
        CorrelationFilterWorker(bus),
        PortfolioOptimizerWorker(bus),

        # =========================
        # execution
        # =========================

        ExecutionWorker(bus),
        OrderExecutorWorker(bus),

        # =========================
        # portfolio
        # =========================

        PortfolioWorker(bus),
        TradeLedgerWorker(bus),

        # =========================
        # performance
        # =========================

        StrategyPerformanceWorker(bus),
        StrategyKillSwitchWorker(bus),

        # =========================
        # risk
        # =========================

        TrailingStopWorker(bus),
        SignalDecayExitWorker(bus),
        PositionTimeStopWorker(bus),
        RiskWorker(bus),

        # =========================
        # analytics / system
        # =========================

        AnalyticsWorker(bus),
        AlertWorker(bus),
        KillSwitchWorker(bus),
        HeartbeatWorker(bus),

    ]

    threads = []

    for worker in workers:
        threads.append(start_worker(worker))

    logger.info("=== ALL WORKERS STARTED ===")

    while True:
        time.sleep(5)
