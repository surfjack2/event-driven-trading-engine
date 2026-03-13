from ltb.system.logger import logger
import time


class TrailingStopWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus

        self.positions = {}
        self.atr = {}

        # ATR multiplier
        self.atr_multiplier = 2

        self.event_bus.subscribe("POSITION_OPENED", self.handle_position)
        self.event_bus.subscribe("POSITION_CLOSED", self.handle_close)

        self.event_bus.subscribe("MARKET_TICK", self.handle_price)
        self.event_bus.subscribe("market.indicator", self.handle_indicator)

    def run(self):

        logger.info("[TRAILING STOP WORKER STARTED]")

        while True:
            time.sleep(1)

    def handle_position(self, position):

        symbol = position["symbol"]

        self.positions[symbol] = {
            "qty": position["qty"],
            "entry_price": position["entry_price"],
            "highest_price": position["entry_price"]
        }

        logger.info(
            f"[TRAILING] tracking symbol={symbol} qty={position['qty']} entry={position['entry_price']}"
        )

    def handle_close(self, position):

        symbol = position["symbol"]

        if symbol in self.positions:

            del self.positions[symbol]

            logger.info(f"[TRAILING] stop tracking {symbol}")

    def handle_indicator(self, event):

        symbol = event["symbol"]
        atr = event.get("atr")

        if atr is None:
            return

        self.atr[symbol] = atr

    def handle_price(self, tick):

        symbol = tick["symbol"]
        price = tick["price"]

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]

        # highest price update
        if price > pos["highest_price"]:

            pos["highest_price"] = price

            logger.info(f"[TRAILING] new high {price}")

        atr = self.atr.get(symbol)

        if atr is None:
            return

        stop_price = pos["highest_price"] - atr * self.atr_multiplier

        logger.info(
            f"[TRAILING] price={price} high={pos['highest_price']} atr={atr} stop={stop_price}"
        )

        if price <= stop_price:

            logger.info(f"[ATR STOP TRIGGERED] {symbol} price={price} stop={stop_price}")

            order = {
                "symbol": symbol,
                "side": "SELL",
                "price": price,
                "qty": pos["qty"]
            }

            self.event_bus.publish("order.request", order)
