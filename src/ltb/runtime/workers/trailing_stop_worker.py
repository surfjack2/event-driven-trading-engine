import logging
import time

log = logging.getLogger(__name__)


class TrailingStopWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
        self.positions = {}

        # 5% trailing stop
        self.trailing_pct = 0.05

        # 이벤트 구독
        self.event_bus.subscribe("POSITION_OPENED", self.handle_position)
        self.event_bus.subscribe("MARKET_TICK", self.handle_price)

    def run(self):

        log.info("[TRAILING STOP WORKER STARTED]")

        while True:
            time.sleep(1)

    def handle_position(self, position):

        symbol = position["symbol"]

        self.positions[symbol] = position

        log.info(f"[TRAILING] tracking {symbol}")

    def handle_price(self, tick):

        symbol = tick["symbol"]
        price = tick["price"]

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]

        # 최고가 갱신
        if price > pos["highest_price"]:

            pos["highest_price"] = price

            log.info(f"[TRAILING] new high {price}")

        stop_price = pos["highest_price"] * (1 - self.trailing_pct)

        log.info(
            f"[TRAILING] price={price} high={pos['highest_price']} stop={stop_price}"
        )

        if price <= stop_price:

            log.info(f"[TRAILING] STOP TRIGGERED {price}")

            self.event_bus.publish(
                "ORDER_REQUEST",
                {
                    "symbol": symbol,
                    "action": "SELL",
                    "price": price,
                },
            )

            del self.positions[symbol]
