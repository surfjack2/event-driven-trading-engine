import time
from collections import defaultdict, deque

from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.console import Group


class ValidationMonitorWorker:

    REFRESH_INTERVAL = 3

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.mode = str(getattr(context, "mode", "UNKNOWN")).split(".")[-1]
        self.market = str(getattr(context, "market", "UNKNOWN")).split(".")[-1]

        self.start_time = time.time()

        self.counters = defaultdict(int)
        self.pipeline = defaultdict(int)

        self.execution_events = deque(maxlen=20)
        self.ranking_events = deque(maxlen=20)
        self.optimizer_events = deque(maxlen=20)

        self.recent_signals = deque(maxlen=20)
        self.strategy_perf = {}

        self.market_regime = "UNKNOWN"
        self.liquidity_regime = "UNKNOWN"
        self.exposure = 0

        # account stats
        self.account_capital = 0
        self.account_equity = 0
        self.daily_pnl = 0
        self.weekly_pnl = 0
        self.monthly_pnl = 0
        self.open_positions = 0

        # -------------------------
        # subscriptions
        # -------------------------

        bus.subscribe("market.price", self.on_tick)
        bus.subscribe("strategy.signal", self.on_signal)
        bus.subscribe("order.request", self.on_order)
        bus.subscribe("ORDER_FILLED", self.on_fill)

        bus.subscribe("scanner.rtv", self.on_rtv)
        bus.subscribe("market.scanner", self.on_scanner)
        bus.subscribe("market.ranking", self.on_ranking)
        bus.subscribe("dedup.signal", self.on_dedup)
        bus.subscribe("persistent.signal", self.on_persist)
        bus.subscribe("ranked.signal", self.on_ranked)
        bus.subscribe("liquidity.signal", self.on_liquidity)
        bus.subscribe("optimized.signal", self.on_allocated)

        bus.subscribe("ranking.pass", self.on_rank_pass)
        bus.subscribe("ranking.reject", self.on_rank_reject)

        bus.subscribe("optimized.signal", self.on_optimizer)

        bus.subscribe("order.request", self.on_order_request)
        bus.subscribe("execution.block", self.on_execution_block)

        bus.subscribe("strategy.performance", self.on_strategy_perf)

        bus.subscribe("market.regime", self.on_market_regime)
        bus.subscribe("market.liquidity_regime", self.on_liquidity_regime)
        bus.subscribe("portfolio.exposure", self.on_exposure)

        # 🔴 account snapshot
        bus.subscribe("account.snapshot", self.on_account)

    # -------------------------
    # helpers
    # -------------------------

    def fmt(self, v):

        if v is None:
            return "-"

        try:
            return f"{v:.4f}"
        except:
            return v

    def format_uptime(self):

        sec = int(time.time() - self.start_time)

        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60

        return f"{h:02d}:{m:02d}:{s:02d}"

    # -------------------------
    # account
    # -------------------------

    def on_account(self, data):

        self.account_capital = data.get("capital", 0)
        self.account_equity = data.get("equity", 0)
        self.daily_pnl = data.get("daily_pnl", 0)
        self.weekly_pnl = data.get("weekly_pnl", 0)
        self.monthly_pnl = data.get("monthly_pnl", 0)
        self.open_positions = data.get("open_positions", 0)

    # -------------------------
    # engine events
    # -------------------------

    def on_tick(self, data):
        self.counters["ticks"] += 1

    def on_signal(self, signal):

        self.counters["signals"] += 1

        f = signal.get("features", {})

        rec = (
            f"{signal.get('symbol')} {signal.get('strategy')} "
            f"rsi:{self.fmt(f.get('rsi'))} "
            f"vol:{self.fmt(f.get('volume_ratio'))} "
            f"vwap:{self.fmt(f.get('vwap_distance'))} "
            f"move:{self.fmt(f.get('price_change'))}"
        )

        self.recent_signals.append(rec)

    def on_order(self, data):
        self.counters["orders"] += 1

    def on_fill(self, data):
        self.counters["fills"] += 1

    # -------------------------
    # pipeline
    # -------------------------

    def on_rtv(self, data):
        self.pipeline["rtv"] += 1

    def on_scanner(self, data):
        self.pipeline["scanner"] += 1

    def on_ranking(self, data):
        self.pipeline["ranking"] += 1

    def on_dedup(self, data):
        self.pipeline["dedup"] += 1

    def on_persist(self, data):
        self.pipeline["persist"] += 1

    def on_ranked(self, data):
        self.pipeline["ranked"] += 1

    def on_liquidity(self, data):
        self.pipeline["liquidity"] += 1

    def on_allocated(self, data):
        self.pipeline["allocation"] += 1

    # -------------------------
    # ranking
    # -------------------------

    def on_rank_pass(self, data):

        sym = data.get("symbol")
        score = data.get("score", 0)

        if sym:
            self.ranking_events.append(
                f"PASS {sym} score={score:.4f}"
            )

    def on_rank_reject(self, data):

        sym = data.get("symbol")
        reason = data.get("reason")

        if sym:
            self.ranking_events.append(
                f"REJECT {sym} reason={reason}"
            )

    # -------------------------
    # optimizer
    # -------------------------

    def on_optimizer(self, signal):

        sym = signal.get("symbol")
        score = signal.get("optimizer_score")

        if sym:
            self.optimizer_events.append(
                f"{sym} score={self.fmt(score)}"
            )

    # -------------------------
    # execution
    # -------------------------

    def on_order_request(self, order):

        sym = order.get("symbol")

        if sym:
            self.execution_events.append(
                f"ORDER SENT {sym}"
            )

    def on_execution_block(self, data):

        sym = data.get("symbol")
        reason = data.get("reason")

        if sym:
            self.execution_events.append(
                f"BLOCK {sym} reason={reason}"
            )

    # -------------------------
    # strategy performance
    # -------------------------

    def on_strategy_perf(self, data):

        strat = data["strategy"]
        stats = data["stats"]

        self.strategy_perf[strat] = stats

    # -------------------------
    # market
    # -------------------------

    def on_market_regime(self, data):
        self.market_regime = data.get("regime")

    def on_liquidity_regime(self, data):
        self.liquidity_regime = data.get("regime")

    def on_exposure(self, data):
        self.exposure = data.get("exposure", 0)

    # -------------------------
    # layout
    # -------------------------

    def build_layout(self):

        queue_depth = self.bus.queue.qsize()

        uptime = self.format_uptime()

        header = Panel(
            Text(
                f"LTB ENGINE MONITOR | mode={self.mode} | market={self.market} | uptime={uptime}"
            ),
            expand=True
        )

        market_panel = Panel(
            Text(
                f"trend: {self.market_regime} | liquidity: {self.liquidity_regime} | exposure: {self.exposure:.2f}"
            ),
            title="Market Regime"
        )

        account_panel = Panel(
            Group(
                Text(f"capital       {self.account_capital}"),
                Text(f"equity        {self.account_equity}"),
                Text(f"daily pnl     {self.fmt(self.daily_pnl)}"),
                Text(f"weekly pnl    {self.fmt(self.weekly_pnl)}"),
                Text(f"monthly pnl   {self.fmt(self.monthly_pnl)}"),
                Text(f"positions     {self.open_positions}")
            ),
            title="Account"
        )

        engine_panel = Panel(
            Group(
                Text(f"ticks/s      {self.counters['ticks']}"),
                Text(f"signals/s    {self.counters['signals']}"),
                Text(f"orders/s     {self.counters['orders']}"),
                Text(f"fills/s      {self.counters['fills']}"),
                Text(f"queue depth  {queue_depth}")
            ),
            title="Engine Flow"
        )

        pipeline_panel = Panel(
            Group(
                Text(f"rtv         {self.pipeline['rtv']}"),
                Text(f"scanner     {self.pipeline['scanner']}"),
                Text(f"ranking     {self.pipeline['ranking']}"),
                Text(f"dedup       {self.pipeline['dedup']}"),
                Text(f"persist     {self.pipeline['persist']}"),
                Text(f"ranked      {self.pipeline['ranked']}"),
                Text(f"liquidity   {self.pipeline['liquidity']}"),
                Text(f"allocation  {self.pipeline['allocation']}")
            ),
            title="Pipeline"
        )

        ranking_panel = Panel(
            Group(*[Text(f"• {x}") for x in self.ranking_events])
            if self.ranking_events else Text("none"),
            title="Ranking"
        )

        recent_panel = Panel(
            Group(*[Text(f"• {x}") for x in self.recent_signals])
            if self.recent_signals else Text("none"),
            title="Recent Signals"
        )

        optimizer_panel = Panel(
            Group(*[Text(f"• {x}") for x in self.optimizer_events])
            if self.optimizer_events else Text("none"),
            title="Optimizer"
        )

        exec_panel = Panel(
            Group(*[Text(f"• {x}") for x in self.execution_events])
            if self.execution_events else Text("none"),
            title="Execution"
        )

        perf_lines = []

        for strat, s in self.strategy_perf.items():

            perf_lines.append(
                Text(
                    f"{strat} trades={s['trades']} "
                    f"win={s['win_rate']:.2f} "
                    f"pf={s['profit_factor']:.2f} "
                    f"pnl={self.fmt(s['pnl'])}"
                )
            )

        perf_panel = Panel(
            Group(*perf_lines) if perf_lines else Text("none"),
            title="Strategy Performance"
        )

        layout = Layout()

        layout.split_column(
            Layout(header, size=3),
            Layout(market_panel, size=3),
            Layout(name="row1"),
            Layout(name="row2"),
            Layout(name="row3"),
            Layout(name="row4"),
        )

        layout["row1"].split_row(
            Layout(account_panel),
            Layout(engine_panel)
        )

        layout["row2"].split_row(
            Layout(pipeline_panel),
            Layout(ranking_panel)
        )

        layout["row3"].split_row(
            Layout(recent_panel),
            Layout(optimizer_panel)
        )

        layout["row4"].split_row(
            Layout(exec_panel),
            Layout(perf_panel)
        )

        return layout

    def run(self):

        with Live(self.build_layout(), refresh_per_second=2) as live:

            while True:

                time.sleep(self.REFRESH_INTERVAL)

                live.update(self.build_layout())

                self.counters.clear()
                self.pipeline.clear()
