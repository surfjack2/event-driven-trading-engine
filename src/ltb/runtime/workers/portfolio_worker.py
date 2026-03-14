import time
from ltb.system.logger import logger


class PortfolioWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
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
            time.sleep(1)

    def handle_fill(self, fill):

        symbol = fill["symbol"]
        strategy = fill.get("strategy")

        if fill["action"] == "BUY":

            position = {
                "symbol": symbol,
                "entry_price": fill["price"],
                "qty": fill["qty"],
                "highest_price": fill["price"],
                "strategy": strategy
            }

            self.positions[symbol] = position

            logger.info(
                f"[PORTFOLIO] OPEN symbol={symbol} qty={position['qty']} entry={position['entry_price']}"
            )

            self.event_bus.publish(
                "POSITION_OPENED",
                position
            )

            # 🔴 strategy 추가
            self.event_bus.publish(
                "portfolio.update",
                {
                    "symbol": symbol,
                    "position": position["qty"],
                    "strategy": strategy
                }
            )

        elif fill["action"] == "SELL":

            if symbol in self.positions:

                pos = self.positions.pop(symbol)

                pnl = (fill["price"] - pos["entry_price"]) * pos["qty"]

                trade = {
                    "symbol": symbol,
                    "entry_price": pos["entry_price"],
                    "exit_price": fill["price"],
                    "qty": pos["qty"],
                    "pnl": pnl,
                    "strategy": pos.get("strategy")
                }

                logger.info(
                    f"[PORTFOLIO] CLOSE symbol={symbol} qty={pos['qty']} pnl={pnl}"
                )

                self.event_bus.publish(
                    "POSITION_CLOSED",
                    trade
                )

                # 🔴 strategy 추가
                self.event_bus.publish(
                    "portfolio.update",
                    {
                        "symbol": symbol,
                        "position": 0,
                        "strategy": pos.get("strategy")
                    }
                )

    def handle_close_all(self, data):

        reason = data.get("reason")

        logger.error(
            f"[PORTFOLIO] CLOSE ALL POSITIONS reason={reason}"
        )

        for symbol, pos in list(self.positions.items()):

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
                f"[PORTFOLIO] emergency sell symbol={symbol} qty={qty}"
            )
