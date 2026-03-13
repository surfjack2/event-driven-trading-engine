from ltb.system.logger import logger


class PositionSizer:

    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self.capital = 10000000

        self.base_risk = 0.01
        self.risk_per_trade = self.base_risk

        # 포지션 상한
        self.max_qty = 300

        # 최근 트레이드 기록
        self.recent_trades = []

        logger.info("[POSITION SIZER INITIALIZED]")

        self._initialized = True

    def update_pnl(self, pnl):

        self.recent_trades.append(pnl)

        if len(self.recent_trades) > 5:
            self.recent_trades.pop(0)

        wins = sum(1 for p in self.recent_trades if p > 0)
        losses = sum(1 for p in self.recent_trades if p < 0)

        if losses >= 3:

            self.risk_per_trade = 0.005

        elif wins >= 3:

            self.risk_per_trade = 0.015

        else:

            self.risk_per_trade = self.base_risk

        logger.info(
            "[ADAPTIVE RISK] wins=%s losses=%s risk=%.4f",
            wins,
            losses,
            self.risk_per_trade
        )

    def calculate(self, entry_price, stop_price):

        risk_amount = self.capital * self.risk_per_trade

        risk_per_share = abs(entry_price - stop_price)

        if risk_per_share == 0:
            return 0

        qty = int(risk_amount / risk_per_share)

        qty = min(qty, self.max_qty)

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
