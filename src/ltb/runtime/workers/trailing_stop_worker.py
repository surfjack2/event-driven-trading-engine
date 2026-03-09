import time

from ltb.system.logger import logger


class TrailingStopWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        self.trail_percent = 0.05

        self.bus.subscribe("portfolio.update", self.on_position_update)

        self.bus.subscribe("market.price", self.on_price)


    def run(self):

        logger.info("[TRAILING STOP WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_position_update(self, data):

        symbol = data["symbol"]
        position = data["position"]
        price = data["price"]

        if position <= 0:

            # 포지션 제거 (안전 삭제)
            self.positions.pop(symbol, None)

            return

        if symbol not in self.positions:

            stop_price = price * (1 - self.trail_percent)

            self.positions[symbol] = {
                "entry": price,
                "stop": stop_price,
                "qty": position
            }

            logger.info(
                "[TRAIL INIT] %s entry=%s stop=%s",
                symbol,
                price,
                stop_price
            )


    def on_price(self, event):

        symbol = event["symbol"]
        price = event["price"]

        # 안전 접근 (KeyError 방지)
        pos = self.positions.get(symbol)

        if not pos:
            return

        stop = pos["stop"]

        # stop 이동
        new_stop = price * (1 - self.trail_percent)

        if new_stop > stop:

            pos["stop"] = new_stop

            logger.info(
                "[TRAIL MOVE] %s new_stop=%s",
                symbol,
                new_stop
            )

        # stop hit
        if price < pos["stop"]:

            logger.info(
                "[TRAIL STOP HIT] %s price=%s stop=%s",
                symbol,
                price,
                pos["stop"]
            )

            order = {
                "symbol": symbol,
                "side": "SELL",
                "price": price,
                "qty": pos["qty"]
            }

            self.bus.publish("order.request", order)

            # 포지션 제거 (안전 삭제)
            self.positions.pop(symbol, None)
