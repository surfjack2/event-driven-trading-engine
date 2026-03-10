import logging
import time

log = logging.getLogger(__name__)


class PortfolioWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
        self.positions = {}

        # 이벤트 구독
        self.event_bus.subscribe("ORDER_FILLED", self.handle_fill)

    def run(self):

        log.info("[PORTFOLIO WORKER STARTED]")

        # worker thread 유지용 루프
        while True:
            time.sleep(1)

    def handle_fill(self, fill):

        symbol = fill["symbol"]

        if fill["action"] == "BUY":

            position = {
                "symbol": symbol,
                "entry_price": fill["price"],
                "qty": fill["qty"],
                "highest_price": fill["price"],
            }

            self.positions[symbol] = position

            self.event_bus.publish("POSITION_OPENED", position)

            log.info(f"[PORTFOLIO] position opened {position}")

        elif fill["action"] == "SELL":

            if symbol in self.positions:

                pos = self.positions.pop(symbol)

                self.event_bus.publish("POSITION_CLOSED", pos)

                log.info(f"[PORTFOLIO] position closed {pos}")
