from ltb.system.logger import logger
from ltb.runtime.queue_bus import QueueBus

from ltb.system.context.system_context import SystemContext

from ltb.runtime.workers.market_worker import MarketWorker
from ltb.runtime.workers.replay_market_worker import ReplayMarketWorker

from ltb.indicator.indicator_worker import IndicatorWorker
from ltb.runtime.workers.strategy_worker import StrategyWorker
from ltb.runtime.workers.execution_worker import ExecutionWorker
from ltb.runtime.workers.order_executor_worker import OrderExecutorWorker
from ltb.runtime.workers.portfolio_worker import PortfolioWorker
from ltb.runtime.workers.trailing_stop_worker import TrailingStopWorker
from ltb.runtime.workers.risk_worker import RiskWorker
from ltb.runtime.workers.analytics_worker import AnalyticsWorker
from ltb.runtime.workers.alert_worker import AlertWorker


def run_engine(context: SystemContext):

    logger.info("=== LTB ENGINE PROCESS STARTED ===")

    bus = QueueBus()

    # -----------------------------
    # MARKET SOURCE 분기
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

        market_worker,
        IndicatorWorker(bus),
        StrategyWorker(bus),
        ExecutionWorker(bus, context),
        OrderExecutorWorker(bus, context),
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
