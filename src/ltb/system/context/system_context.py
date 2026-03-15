from ltb.system.context.mode import SystemMode
from ltb.system.context.market import MarketType
from ltb.risk.risk_engine import RiskEngine


class SystemContext:

    def __init__(self, mode=SystemMode.BACKTEST, market=MarketType.US):

        self.mode = mode
        self.market = market

        # broker placeholder
        self.broker = None

        # dynamic capital
        if self.mode == SystemMode.BACKTEST:
            self.capital = 10000000
        else:
            self.capital = 0

        # shared risk engine
        self.risk_engine = RiskEngine(self)

    def set_capital(self, capital):

        self.capital = capital

    def get_capital(self):

        return self.capital

    def is_backtest(self):

        return self.mode == SystemMode.BACKTEST

    def is_paper(self):

        return self.mode == SystemMode.PAPER

    def is_live(self):

        return self.mode == SystemMode.LIVE

    def is_crypto(self):

        return self.market == MarketType.CRYPTO

    def is_stock(self):

        return self.market in (MarketType.US, MarketType.KR)
