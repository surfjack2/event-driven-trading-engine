from ltb.system.logger import logger


class PositionSizer:

    def __init__(self):

        # 총 자본 (예: 테스트용 10,000,000)
        self.capital = 10000000

        # 트레이드당 리스크 비율
        self.risk_per_trade = 0.01

        logger.info("[POSITION SIZER INITIALIZED]")


    def calculate(self, entry_price, stop_price):

        risk_amount = self.capital * self.risk_per_trade

        risk_per_share = abs(entry_price - stop_price)

        if risk_per_share == 0:
            return 0

        qty = int(risk_amount / risk_per_share)

        if qty < 1:
            qty = 1

        logger.info(
            "[POSITION SIZE] capital=%s risk=%s qty=%s",
            self.capital,
            risk_amount,
            qty
        )

        return qty
