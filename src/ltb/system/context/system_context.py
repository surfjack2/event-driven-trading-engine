from ltb.system.context.mode import SystemMode
from ltb.system.context.market import MarketType


class SystemContext:

    def __init__(self, mode=SystemMode.BACKTEST, market=MarketType.US):

        self.mode = mode
        self.market = market

        # broker placeholder
        self.broker = None

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
