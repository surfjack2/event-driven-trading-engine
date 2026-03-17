import time
from collections import defaultdict, deque

from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.console import Group

from ltb.system.format_utils import num, pct


class ValidationMonitorWorker:

    REFRESH_INTERVAL = 3
    WORKER_LAG_LIMIT = 5

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

        self.system_status = "RUNNING"

        # diagnostics
        self.event_counter = 0
        self.event_rate = 0
        self.last_diag_time = time.time()

        # latency
        self.event_latency = deque(maxlen=50)

        # worker heartbeat
        self.worker_heartbeat = {}

        # drawdown
        self.equity_peak = 0
        self.max_drawdown = 0

        # account
        self.account_capital = 0
        self.account_equity = 0
        self.daily_pnl = 0
        self.weekly_pnl = 0
        self.monthly_pnl = 0
        self.open_positions = 0

        # --------------------------------------------------
        # subscriptions
        # --------------------------------------------------

        bus.subscribe("market.price", self.on_tick)
        bus.subscribe("strategy.signal", self.on_signal)
        bus.subscribe("order.request", self.on_order)
        bus.subscribe("ORDER_FILLED", self.on_fill)

        bus.subscribe("scanner.rtv", self.on_rtv)
        bus.subscribe("market.ranking", self.on_ranking)

        bus.subscribe("ranking.pass", self.on_rank_pass)
        bus.subscribe("ranking.reject", self.on_rank_reject)

        bus.subscribe("optimized.signal", self.on_optimizer)

        bus.subscribe("order.request", self.on_order_request)
        bus.subscribe("execution.block", self.on_execution_block)

        bus.subscribe("strategy.performance", self.on_strategy_perf)

        bus.subscribe("market.regime", self.on_market_regime)
        bus.subscribe("market.liquidity_regime", self.on_liquidity_regime)

        bus.subscribe("portfolio.exposure", self.on_exposure)

        bus.subscribe("account.snapshot", self.on_account)

        bus.subscribe("system.halt", self.on_system_halt)

        bus.subscribe("worker.heartbeat", self.on_worker_heartbeat)

    # --------------------------------------------------

    def format_uptime(self):

        sec = int(time.time() - self.start_time)

        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60

        return f"{h:02d}:{m:02d}:{s:02d}"

    # --------------------------------------------------
    # diagnostics
    # --------------------------------------------------

    def update_diagnostics(self):

        now = time.time()
        elapsed = now - self.last_diag_time

        if elapsed >= 1:

            self.event_rate = int(self.event_counter / elapsed)

            self.event_counter = 0
            self.last_diag_time = now

    # --------------------------------------------------

    def update_drawdown(self):

        equity = self.account_equity

        if equity > self.equity_peak:
            self.equity_peak = equity

        if self.equity_peak > 0:

            dd = (self.equity_peak - equity) / self.equity_peak

            if dd > self.max_drawdown:
                self.max_drawdown = dd

    # --------------------------------------------------

    def record_latency(self):

        now = time.time()
        self.event_latency.append(now)

    # --------------------------------------------------
    # worker heartbeat
    # --------------------------------------------------

    def on_worker_heartbeat(self, data):

        worker = data.get("worker")
        ts = time.time()

        if worker:
            self.worker_heartbeat[worker] = ts

    # --------------------------------------------------
    # risk
    # --------------------------------------------------

    def on_system_halt(self, data):

        reason = data.get("reason")
        self.system_status = f"HALTED ({reason})"

    # --------------------------------------------------
    # account
    # --------------------------------------------------

    def on_account(self, data):

        self.account_capital = data.get("capital", 0)
        self.account_equity = data.get("equity", 0)

        self.daily_pnl = data.get("daily_pnl", 0)
        self.weekly_pnl = data.get("weekly_pnl", 0)
        self.monthly_pnl = data.get("monthly_pnl", 0)

        self.open_positions = data.get("open_positions", 0)

        self.update_drawdown()

    # --------------------------------------------------

    def on_tick(self, data):

        self.counters["ticks"] += 1
        self.event_counter += 1
        self.record_latency()

    def on_signal(self, signal):

        self.counters["signals"] += 1
        self.event_counter += 1
        self.record_latency()

        f = signal.get("features", {})

        rec = (
            f"{signal.get('symbol')} {signal.get('strategy')} "
            f"rsi:{num(f.get('rsi'))} "
            f"vol:{num(f.get('volume_ratio'))} "
            f"move:{pct(f.get('price_change'))}"
        )

        self.recent_signals.append(rec)

    def on_order(self, data):

        self.counters["orders"] += 1
        self.event_counter += 1
        self.record_latency()

    def on_fill(self, data):

        self.counters["fills"] += 1
        self.event_counter += 1
        self.record_latency()

    # --------------------------------------------------
    # pipeline
    # --------------------------------------------------

    def on_rtv(self, data):
        self.pipeline["rtv"] += 1

    def on_ranking(self, data):
        self.pipeline["ranking"] += 1

    # --------------------------------------------------
    # ranking
    # --------------------------------------------------

    def on_rank_pass(self, data):

        sym = data.get("symbol")

        if sym:
            self.ranking_events.append(f"PASS {sym}")

    def on_rank_reject(self, data):

        sym = data.get("symbol")
        reason = data.get("reason")

        if sym:
            self.ranking_events.append(f"REJECT {sym} reason={reason}")

    # --------------------------------------------------
    # optimizer
    # --------------------------------------------------

    def on_optimizer(self, signal):

        sym = signal.get("symbol")

        if sym:
            self.optimizer_events.append(sym)

    # --------------------------------------------------
    # execution
    # --------------------------------------------------

    def on_order_request(self, order):

        sym = order.get("symbol")

        if sym:
            self.execution_events.append(f"ORDER SENT {sym}")

    def on_execution_block(self, data):

        sym = data.get("symbol")
        reason = data.get("reason")

        if sym:
            self.execution_events.append(f"BLOCK {sym} reason={reason}")

    # --------------------------------------------------
    # strategy performance
    # --------------------------------------------------

    def on_strategy_perf(self, data):

        strat = data["strategy"]
        stats = data["stats"]

        self.strategy_perf[strat] = stats

    # --------------------------------------------------
    # market
    # --------------------------------------------------

    def on_market_regime(self, data):
        self.market_regime = data.get("regime")

    def on_liquidity_regime(self, data):
        self.liquidity_regime = data.get("regime")

    def on_exposure(self, data):
        self.exposure = data.get("exposure", 0)

    # --------------------------------------------------
    # layout
    # --------------------------------------------------

    def build_layout(self):

        queue_depth = self.bus.queue.qsize()

        uptime = self.format_uptime()

        latency = 0

        if len(self.event_latency) > 1:
            latency = self.event_latency[-1] - self.event_latency[0]

        header = Panel(
            Text(
                f"LTB ENGINE | mode={self.mode} | market={self.market} | uptime={uptime}"
            ),
            expand=True
        )

        market_panel = Panel(
            Text(
                f"trend: {self.market_regime} | liquidity: {self.liquidity_regime} | exposure: {pct(self.exposure)}\n"
                f"status: {self.system_status} | positions: {self.open_positions}"
            ),
            title="Market Regime"
        )

        account_panel = Panel(
            Group(
                Text(f"capital     {num(self.account_capital)}"),
                Text(f"equity      {num(self.account_equity)}"),
                Text(f"daily pnl   {num(self.daily_pnl)}"),
                Text(f"drawdown    {pct(self.max_drawdown)}"),
            ),
            title="Account"
        )

        engine_panel = Panel(
            Group(
                Text(f"ticks    {self.counters['ticks']}"),
                Text(f"signals  {self.counters['signals']}"),
                Text(f"orders   {self.counters['orders']}"),
                Text(f"fills    {self.counters['fills']}")
            ),
            title="Engine Flow"
        )

        pipeline_panel = Panel(
            Group(
                Text(f"rtv        {self.pipeline['rtv']}"),
                Text(f"ranking    {self.pipeline['ranking']}")
            ),
            title="Pipeline"
        )

        ranking_panel = Panel(
            Group(*[Text(x) for x in self.ranking_events])
            if self.ranking_events else Text("none"),
            title="Ranking"
        )

        signals_panel = Panel(
            Group(*[Text(x) for x in self.recent_signals])
            if self.recent_signals else Text("none"),
            title="Recent Signals"
        )

        optimizer_panel = Panel(
            Group(*[Text(x) for x in self.optimizer_events])
            if self.optimizer_events else Text("none"),
            title="Optimizer"
        )

        execution_panel = Panel(
            Group(*[Text(x) for x in self.execution_events])
            if self.execution_events else Text("none"),
            title="Execution"
        )

        perf_lines = []

        for strat, s in self.strategy_perf.items():

            perf_lines.append(
                Text(
                    f"{strat} trades={s['trades']} "
                    f"win={pct(s['win_rate'])} "
                    f"pf={num(s['profit_factor'])} "
                    f"pnl={num(s['pnl'])}"
                )
            )

        perf_panel = Panel(
            Group(*perf_lines) if perf_lines else Text("none"),
            title="Strategy Performance"
        )

        diagnostics_panel = Panel(
            Group(
                Text(f"event rate    {self.event_rate}/s"),
                Text(f"queue depth   {queue_depth}"),
                Text(f"latency       {num(latency)}"),
            ),
            title="Engine Diagnostics"
        )

        worker_lines = []

        now = time.time()

        for w, ts in self.worker_heartbeat.items():

            lag = now - ts

            status = "OK"

            if lag > self.WORKER_LAG_LIMIT:
                status = "LAG"

            worker_lines.append(
                Text(f"{w} {num(lag)}s {status}")
            )

        worker_panel = Panel(
            Group(*worker_lines) if worker_lines else Text("none"),
            title="Worker Health"
        )

        layout = Layout()

        layout.split_column(
            Layout(header, size=3),
            Layout(market_panel, size=4),
            Layout(name="row1"),
            Layout(name="row2"),
            Layout(name="row3"),
            Layout(name="row4"),
            Layout(name="row5"),
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
            Layout(signals_panel),
            Layout(optimizer_panel)
        )

        layout["row4"].split_row(
            Layout(execution_panel),
            Layout(perf_panel)
        )

        layout["row5"].split_row(
            Layout(diagnostics_panel),
            Layout(worker_panel)
        )

        return layout

    # --------------------------------------------------

    def run(self):

        with Live(self.build_layout(), refresh_per_second=2) as live:

            while True:

                time.sleep(self.REFRESH_INTERVAL)

                self.update_diagnostics()

                live.update(self.build_layout())

                self.counters.clear()
