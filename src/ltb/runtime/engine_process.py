from ltb.system.logger import logger
from ltb.runtime.queue_bus import QueueBus

from ltb.system.context.system_context import SystemContext

from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.replay_market_worker import ReplayMarketWorker

from ltb.indicator.indicator_worker import IndicatorWorker
from ltb.runtime.workers.strategy_worker import StrategyWorker

from ltb.runtime.workers.signal_dedup_worker import SignalDedupWorker
from ltb.runtime.workers.signal_persistence_worker import SignalPersistenceWorker
from ltb.runtime.workers.signal_ranking_worker import SignalRankingWorker
from ltb.runtime.workers.strategy_allocation_worker import StrategyAllocationWorker
from ltb.runtime.workers.trade_quality_filter_worker import TradeQualityFilterWorker
from ltb.runtime.workers.position_intent_worker import PositionIntentWorker
from ltb.runtime.workers.portfolio_optimizer_worker import PortfolioOptimizerWorker

from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker

from ltb.runtime.workers.trade_ledger_worker import TradeLedgerWorker
from ltb.runtime.workers.strategy_performance_worker import StrategyPerformanceWorker

from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker

from ltb.runtime.workers.validation_monitor_worker import ValidationMonitorWorker
from ltb.runtime.workers.heartbeat_worker import HeartbeatWorker

import threading


def run_engine(context: SystemContext):

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    # -----------------------------
    # MARKET SOURCE
    # -----------------------------

    if context.is_backtest():

        logger.info("[ENGINE MODE] BACKTEST")

        if not context.data_file:
            raise RuntimeError("BACKTEST mode requires data_file")

        market_worker = ReplayMarketWorker(
            bus,
            context.data_file,
            context.replay_speed
        )

    elif context.is_paper():

        logger.info("[ENGINE MODE] PAPER")

        market_worker = MarketWorker(bus, context)

    elif context.is_live():

        logger.info("[ENGINE MODE] LIVE")

        market_worker = MarketWorker(bus, context)

    else:

        raise RuntimeError("Unknown system mode")

    workers = [

        # market
        market_worker,

        # indicator
        IndicatorWorker(bus),

        # strategy
        StrategyWorker(bus),

        # signal pipeline
        SignalDedupWorker(bus),
        SignalPersistenceWorker(bus),
        SignalRankingWorker(bus),

        # allocation pipeline
        StrategyAllocationWorker(bus),
        TradeQualityFilterWorker(bus),
        PositionIntentWorker(bus),
        PortfolioOptimizerWorker(bus),

        # execution
        ExecutionWorker(bus, context),
        OrderExecutorWorker(bus, context),

        # portfolio
        PortfolioWorker(bus),
        TrailingStopWorker(bus),

        # trade accounting
        TradeLedgerWorker(bus, context),
        StrategyPerformanceWorker(bus),

        # risk
        RiskWorker(bus),

        # analytics
        AnalyticsWorker(bus),

        # alerts
        AlertWorker(bus),

        # monitoring
        ValidationMonitorWorker(bus, context),
        HeartbeatWorker(bus)

    ]

    threads = []

    for worker in workers:

        logger.info(f"[STARTING WORKER] {worker.__class__.__name__}")

        t = threading.Thread(
            target=worker.run,
            name=worker.__class__.__name__,
            daemon=True
        )

        t.start()

        threads.append(t)

    logger.info("=== ALL WORKERS STARTED ===")

    for t in threads:
        t.join()
