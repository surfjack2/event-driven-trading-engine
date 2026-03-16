import time
import os
from collections import defaultdict
from ltb.system.logger import logger


class ValidationMonitorWorker:

    REFRESH_INTERVAL = 3

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.start_time = time.time()

        # engine counters
        self.counters = defaultdict(int)

        # pipeline counters
        self.pipeline = defaultdict(int)

        # portfolio state
        self.positions = 0
        self.realized_pnl = 0

        # strategy stats
        self.strategy_stats = {}

        # market state
        self.market_regime = "unknown"
        self.liquidity_regime = "NORMAL"
        self.exposure = 0

        # system health
        self.error_count = 0
        self.queue_size = 0

        # event subscriptions
        self.bus.subscribe("market.price", self.on_tick)
        self.bus.subscribe("strategy.signal", self.on_signal)
        self.bus.subscribe("order.request", self.on_order)
        self.bus.subscribe("ORDER_FILLED", self.on_fill)

        self.bus.subscribe("persistent.signal", self.on_persist)
        self.bus.subscribe("ranked.signal", self.on_rank)
        self.bus.subscribe("optimized.signal", self.on_optimized)

        self.bus.subscribe("POSITION_OPENED", self.on_position_open)
        self.bus.subscribe("POSITION_CLOSED", self.on_position_close)

        self.bus.subscribe("strategy.performance", self.on_strategy_perf)

        self.bus.subscribe("market.regime", self.on_market_regime)
        self.bus.subscribe("market.liquidity_regime", self.on_liquidity_regime)
        self.bus.subscribe("portfolio.exposure", self.on_exposure)

    # -----------------------------
    # event handlers
    # -----------------------------

    def on_tick(self, data):
        self.counters["ticks"] += 1

    def on_signal(self, data):
        self.counters["signals"] += 1
        self.pipeline["strategy"] += 1

    def on_order(self, data):
        self.counters["orders"] += 1

    def on_fill(self, data):
        self.counters["fills"] += 1

    def on_persist(self, data):
        self.pipeline["persist"] += 1

    def on_rank(self, data):
        self.pipeline["ranked"] += 1

    def on_optimized(self, data):
        self.pipeline["optimized"] += 1

    def on_position_open(self, pos):
        self.positions += 1

    def on_position_close(self, trade):

        self.positions -= 1

        pnl = trade.get("pnl", 0)
        self.realized_pnl += pnl

    def on_strategy_perf(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        self.strategy_stats[strategy] = stats

    def on_market_regime(self, data):
        self.market_regime = data.get("regime")

    def on_liquidity_regime(self, data):
        self.liquidity_regime = data.get("regime")

    def on_exposure(self, data):
        self.exposure = data.get("exposure")

    # -----------------------------
    # rendering
    # -----------------------------

    def color(self, value, good, warn):

        if value >= good:
            return f"\033[92m{value}\033[0m"

        if value >= warn:
            return f"\033[93m{value}\033[0m"

        return f"\033[91m{value}\033[0m"

    def render(self):

        os.system("clear")

        uptime = int(time.time() - self.start_time)

        print("======================================================")
        print(" LTB ENGINE VALIDATION MONITOR")
        print(
            f" mode={self.context.mode} uptime={uptime}s"
        )
        print("======================================================")

        print("\nENGINE FLOW")
        print("--------------------------------------")

        ticks = self.counters["ticks"]
        signals = self.counters["signals"]
        orders = self.counters["orders"]
        fills = self.counters["fills"]

        print(f"ticks/s     {ticks}")
        print(f"signals/s   {signals}")
        print(f"orders/min  {orders}")
        print(f"fills/min   {fills}")

        print("\nSIGNAL PIPELINE")
        print("--------------------------------------")

        print(f"strategy    {self.pipeline['strategy']}")
        print(f"persist     {self.pipeline['persist']}")
        print(f"ranked      {self.pipeline['ranked']}")
        print(f"optimized   {self.pipeline['optimized']}")

        print("\nPORTFOLIO")
        print("--------------------------------------")

        print(f"positions       {self.positions}")
        print(f"realized pnl    {self.realized_pnl}")

        print("\nSTRATEGY PERFORMANCE")
        print("--------------------------------------")

        for strategy, stats in self.strategy_stats.items():

            trades = stats.get("trades")
            win_rate = stats.get("win_rate")
            pf = stats.get("profit_factor")
            pnl = stats.get("pnl")

            print(
                f"{strategy:20} trades={trades} win={win_rate:.2f} pf={pf:.2f} pnl={pnl}"
            )

        print("\nMARKET STATE")
        print("--------------------------------------")

        print(f"trend regime      {self.market_regime}")
        print(f"liquidity regime  {self.liquidity_regime}")
        print(f"exposure          {self.exposure}")

        print("\n(refresh every 3 seconds)")
        print("======================================================")

        # reset interval counters
        self.counters["ticks"] = 0
        self.counters["signals"] = 0
        self.counters["orders"] = 0
        self.counters["fills"] = 0

        self.pipeline.clear()

    # -----------------------------
    # worker loop
    # -----------------------------

    def run(self):

        logger.info("[VALIDATION MONITOR WORKER STARTED]")

        while True:

            time.sleep(self.REFRESH_INTERVAL)

            self.render()
