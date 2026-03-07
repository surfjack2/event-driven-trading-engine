class ATRStop:

    def __init__(self, market, period=14, multiplier=2):

        self.market = market
        self.period = period
        self.multiplier = multiplier

    def calculate_stop(self, symbol, entry_price):

        atr = self.market.get_atr(symbol, self.period)

        if atr is None:
            return entry_price * 0.975

        stop_price = entry_price - (atr * self.multiplier)

        return stop_price
