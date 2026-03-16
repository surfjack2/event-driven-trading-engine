import time
from ltb.system.logger import logger


class PortfolioWorker:

    TIME_STOP_SECONDS = 3600

    def __init__(self, event_bus, exit_manager):

        self.event_bus = event_bus
        self.exit_manager = exit_manager

        self.positions = {}

        self.event_bus.subscribe(
            "ORDER_FILLED",
            self.handle_fill
        )

        self.event_bus.subscribe(
            "risk.close_all",
            self.handle_close_all
        )

    def run(self):

        logger.info("[PORTFOLIO WORKER STARTED]")

        while True:

            now = time.time()

            for symbol, pos in list(self.positions.items()):

                entry_time = pos.get("entry_time")

                if not entry_time:
                    continue

                hold_time = now - entry_time

                if hold_time > self.TIME_STOP_SECONDS:

                    # 🔴 ExitManager gate
                    if not self.exit_manager.request_exit(symbol):
                        continue

                    logger.info(
                        "[TIME STOP EXIT] symbol=%s hold_time=%s",
                        symbol,
                        hold_time
                    )

                    order = {
                        "symbol": symbol,
                        "side": "SELL",
                        "price": pos["entry_price"],
                        "qty": pos["qty"],
                        "strategy": pos.get("strategy")
                    }

                    self.event_bus.publish("order.request", order)

            time.sleep(5)

    def handle_fill(self, fill):

        symbol = fill["symbol"]
        strategy = fill.get("strategy")

        side = fill.get("side") or fill.get("action")
        price = fill.get("price")

        if side == "BUY":

            position = {
                "symbol": symbol,
                "entry_price": price,
                "qty": fill["qty"],
                "highest_price": price,
                "entry_time": time.time(),
                "strategy": strategy
            }

            self.positions[symbol] = position

            logger.info(
                "[PORTFOLIO] OPEN symbol=%s qty=%s entry=%s",
                symbol,
                position["qty"],
                position["entry_price"]
            )

            self.event_bus.publish(
                "POSITION_OPENED",
                position
            )

            self.event_bus.publish(
                "portfolio.update",
                {
                    "symbol": symbol,
                    "position": position["qty"],
                    "price": price,
                    "strategy": strategy
                }
            )

        elif side == "SELL":

            if symbol in self.positions:

                pos = self.positions.pop(symbol)

                pnl = (price - pos["entry_price"]) * pos["qty"]

                trade = {
                    "symbol": symbol,
                    "entry_price": pos["entry_price"],
                    "exit_price": price,
                    "qty": pos["qty"],
                    "pnl": pnl,
                    "strategy": pos.get("strategy")
                }

                logger.info(
                    "[PORTFOLIO] CLOSE symbol=%s qty=%s pnl=%s",
                    symbol,
                    pos["qty"],
                    pnl
                )

                # 🔴 exit 상태 해제
                self.exit_manager.clear(symbol)

                self.event_bus.publish(
                    "POSITION_CLOSED",
                    trade
                )

                self.event_bus.publish(
                    "portfolio.update",
                    {
                        "symbol": symbol,
                        "position": 0,
                        "price": price,
                        "strategy": pos.get("strategy")
                    }
                )

    def handle_close_all(self, data):

        reason = data.get("reason")

        logger.error(
            "[PORTFOLIO] CLOSE ALL POSITIONS reason=%s",
            reason
        )

        for symbol, pos in list(self.positions.items()):

            if not self.exit_manager.request_exit(symbol):
                continue

            qty = pos["qty"]

            self.event_bus.publish(
                "order.request",
                {
                    "symbol": symbol,
                    "side": "SELL",
                    "price": pos["entry_price"],
                    "qty": qty,
                    "strategy": pos.get("strategy")
                }
            )

            logger.error(
                "[PORTFOLIO] emergency sell symbol=%s qty=%s",
                symbol,
                qty
            )
