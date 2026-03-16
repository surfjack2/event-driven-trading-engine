import time
from collections import defaultdict, deque

from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Group


class ValidationMonitorWorker:

    REFRESH_INTERVAL = 3
    EQUITY_WINDOW = 40
    ROLLING_WINDOW = 20

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.start_time = time.time()

        self.counters = defaultdict(int)

        self.positions = 0
        self.realized_pnl = 0

        self.strategy_stats = {}

        self.market_regime = "unknown"
        self.liquidity_regime = "NORMAL"
        self.exposure = 0

        self.trades = []
        self.recent_trades = deque(maxlen=self.ROLLING_WINDOW)

        self.equity = 0
        self.max_equity = 0
        self.max_drawdown = 0

        self.equity_curve = deque(maxlen=self.EQUITY_WINDOW)

        self.market_leaders = []

        bus.subscribe("market.price", self.on_tick)
        bus.subscribe("strategy.signal", self.on_signal)
        bus.subscribe("order.request", self.on_order)
        bus.subscribe("ORDER_FILLED", self.on_fill)

        bus.subscribe("POSITION_OPENED", self.on_position_open)
        bus.subscribe("POSITION_CLOSED", self.on_position_close)

        bus.subscribe("trade.closed", self.on_trade_closed)
        bus.subscribe("market.ranking", self.on_market_ranking)

        bus.subscribe("market.regime", self.on_market_regime)
        bus.subscribe("market.liquidity_regime", self.on_liquidity_regime)
        bus.subscribe("portfolio.exposure", self.on_exposure)

    def on_tick(self, data):
        self.counters["ticks"] += 1

    def on_signal(self, data):
        self.counters["signals"] += 1

    def on_order(self, data):
        self.counters["orders"] += 1

    def on_fill(self, data):
        self.counters["fills"] += 1

    def on_position_open(self, pos):
        self.positions += 1

    def on_position_close(self, trade):
        self.positions -= 1
        self.realized_pnl += trade.get("pnl", 0)

    def on_trade_closed(self, trade):

        pnl = trade.get("pnl", 0)

        self.trades.append(pnl)
        self.recent_trades.append(pnl)

        self.equity += pnl
        self.equity_curve.append(self.equity)

        if self.equity > self.max_equity:
            self.max_equity = self.equity

        dd = self.max_equity - self.equity
        self.max_drawdown = max(self.max_drawdown, dd)

    def on_market_ranking(self, data):
        self.market_leaders = data.get("symbols", [])[:10]

    def on_market_regime(self, data):
        self.market_regime = data.get("regime")

    def on_liquidity_regime(self, data):
        self.liquidity_regime = data.get("regime")

    def on_exposure(self, data):
        self.exposure = data.get("exposure")

    def trading_stats(self):

        if not self.trades:
            return (0, 0, 0)

        wins = [p for p in self.trades if p > 0]
        losses = [p for p in self.trades if p <= 0]

        win_rate = len(wins) / len(self.trades)

        profit = sum(wins)
        loss = abs(sum(losses))

        pf = profit / loss if loss > 0 else 0

        return (len(self.trades), win_rate, pf)

    def build_layout(self):

        layout = Layout()

        trades, win_rate, pf = self.trading_stats()

        engine_table = Table(title="Engine Flow")

        engine_table.add_column("Metric")
        engine_table.add_column("Value")

        engine_table.add_row("ticks/s", str(self.counters["ticks"]))
        engine_table.add_row("signals/s", str(self.counters["signals"]))
        engine_table.add_row("orders/s", str(self.counters["orders"]))
        engine_table.add_row("fills/s", str(self.counters["fills"]))

        portfolio_table = Table(title="Portfolio")

        portfolio_table.add_column("Metric")
        portfolio_table.add_column("Value")

        portfolio_table.add_row("positions", str(self.positions))
        portfolio_table.add_row("realized pnl", str(self.realized_pnl))

        stats_table = Table(title="Trading Stats")

        stats_table.add_column("Metric")
        stats_table.add_column("Value")

        stats_table.add_row("trades", str(trades))
        stats_table.add_row("win rate", f"{win_rate:.2f}")
        stats_table.add_row("profit factor", f"{pf:.2f}")
        stats_table.add_row("max drawdown", str(self.max_drawdown))

        market_table = Table(title="Market State")

        market_table.add_column("Metric")
        market_table.add_column("Value")

        market_table.add_row("trend", self.market_regime)
        market_table.add_row("liquidity", self.liquidity_regime)
        market_table.add_row("exposure", str(self.exposure))

        leaders = Table(title="Market Leaders")
        leaders.add_column("Symbol")

        for s in self.market_leaders:
            leaders.add_row(s)

        return Group(
            Panel(engine_table),
            Panel(portfolio_table),
            Panel(stats_table),
            Panel(market_table),
            Panel(leaders)
        )

    def run(self):

        with Live(self.build_layout(), refresh_per_second=2) as live:

            while True:

                time.sleep(self.REFRESH_INTERVAL)

                live.update(self.build_layout())

                self.counters.clear()
