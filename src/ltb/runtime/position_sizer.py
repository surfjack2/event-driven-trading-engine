from ltb.system.logger import logger


class PositionSizer:

    def __init__(self):

        self.capital = 10_000_000
        self.risk_per_trade = 0.01

        logger.info("[POSITION SIZER INITIALIZED]")


    def size(self, price):

        risk_amount = self.capital * self.risk_per_trade

        qty = int(risk_amount / price)

        if qty < 1:
            qty = 1

        logger.info(
            "[POSITION SIZE] capital=%s risk=%s qty=%s",
            self.capital,
            risk_amount,
            qty
        )

        return qty
