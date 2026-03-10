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

            # 먼저 로그
            log.info(
                f"[PORTFOLIO] OPEN symbol={symbol} qty={position['qty']} entry={position['entry_price']}"
            )

            # 포지션 오픈 이벤트
            self.event_bus.publish("POSITION_OPENED", position)

            # ExecutionWorker 상태 업데이트
            self.event_bus.publish(
                "portfolio.update",
                {
                    "symbol": symbol,
                    "position": position["qty"]
                }
            )

        elif fill["action"] == "SELL":

            if symbol in self.positions:

                pos = self.positions.pop(symbol)

                # 먼저 로그
                log.info(
                    f"[PORTFOLIO] CLOSE symbol={symbol} qty={pos['qty']} entry={pos['entry_price']}"
                )

                # 포지션 종료 이벤트
                self.event_bus.publish("POSITION_CLOSED", pos)

                # ExecutionWorker 상태 업데이트
                self.event_bus.publish(
                    "portfolio.update",
                    {
                        "symbol": symbol,
                        "position": 0
                    }
                )
