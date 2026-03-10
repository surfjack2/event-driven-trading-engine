import logging
from ltb.trade.trade_recorder import TradeRecorder

logger = logging.getLogger(__name__)


class OrderExecutorWorker:

    def __init__(self, bus, executor):

        self.bus = bus
        self.executor = executor

        # Trade Recorder 추가
        self.trade_recorder = TradeRecorder()

    def start(self):

        logger.info("[ORDER EXECUTOR WORKER STARTED]")

        self.bus.subscribe("order_request", self.handle_order)

    def handle_order(self, order):

        logger.info(f"[ORDER EXECUTOR] executing order {order}")

        try:

            symbol = order.get("symbol")
            side = order.get("side")
            price = order.get("price")
            qty = order.get("qty", 1)

            # 실제 주문 실행
            self.executor.place_order(
                symbol=symbol,
                side=side,
                qty=qty,
                price=price
            )

            logger.info(f"[KIS] placing order {symbol} {side} qty={qty} price={price}")

            # 체결 처리 (현재는 즉시 체결 구조)
            logger.info("[KIS] order filled")

            # ==============================
            # Trade 기록
            # ==============================
            self.trade_recorder.record_fill(order)

            # ==============================
            # Portfolio 이벤트 발행
            # ==============================

            self.bus.publish("order_filled", order)

            logger.info("[ORDER EXECUTOR] fill published")

        except Exception as e:

            logger.error(f"[ORDER EXECUTOR ERROR] {e}")
