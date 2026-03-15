from ltb.system.logger import logger
from ltb.execution.kis_executor import KISExecutor


class ExecutorRouter:

    def __init__(self, context):

        self.context = context

        # LIVE broker
        self.kis = None

        if context.is_live():
            self.kis = KISExecutor()
            logger.info("[EXECUTOR ROUTER] KIS executor initialized")

    def execute(self, order):

        # =========================
        # BACKTEST / PAPER
        # =========================

        if self.context.is_backtest() or self.context.is_paper():

            logger.info("[EXECUTOR ROUTER] mock execution %s", order)

            return {
                "symbol": order["symbol"],
                "action": order["side"],
                "price": order["price"],
                "qty": order.get("qty", 1),
                "strategy": order.get("strategy")
            }

        # =========================
        # LIVE
        # =========================

        if self.context.is_live():

            logger.info("[EXECUTOR ROUTER] live execution %s", order)

            fill = self.kis.place_order(
                order["symbol"],
                order["side"],
                order.get("qty", 1),
                order["price"]
            )

            return {
                "symbol": fill["symbol"],
                "action": fill["side"],
                "price": fill["price"],
                "qty": fill["qty"],
                "strategy": order.get("strategy")
            }

        return None
