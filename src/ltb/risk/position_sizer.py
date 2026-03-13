from ltb.system.logger import logger


class PositionSizer:

    def __init__(self):

        self.capital = 10000000
        self.risk_per_trade = 0.01

        # 포지션 최대 자본 비율
        self.max_capital_per_trade = 0.05

        logger.info("[POSITION SIZER INITIALIZED]")


    def calculate(self, entry_price, stop_price):

        risk_amount = self.capital * self.risk_per_trade

        risk_per_share = abs(entry_price - stop_price)

        if risk_per_share == 0:
            return 0

        qty = int(risk_amount / risk_per_share)

        # 자본 기반 cap
        max_position_value = self.capital * self.max_capital_per_trade

        max_qty_cap = int(max_position_value / entry_price)

        qty = min(qty, max_qty_cap)

        if qty < 1:
            qty = 1

        logger.info(
            "[POSITION SIZE] capital=%s risk=%s stop=%s qty=%s",
            self.capital,
            risk_amount,
            risk_per_share,
            qty
        )

        return qty
