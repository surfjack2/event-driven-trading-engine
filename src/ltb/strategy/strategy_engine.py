class StrategyEngine:

    def __init__(self, market):
        self.market = market

    # ==========================
    # Entry 조건
    # ==========================
    def check_entry(self, symbol):

        price = self.market.get_price(symbol)

        rsi = self.market.get_rsi(symbol)
        macd = self.market.get_macd(symbol)
        stoch = self.market.get_stochastic(symbol)

        # 데이터 부족
        if rsi is None or macd is None:
            return False

        # ----------------------
        # Trend Filter (Turtle)
        # ----------------------

        trend_ok = rsi > 50

        # ----------------------
        # Momentum Filter (BNF)
        # ----------------------

        momentum_ok = stoch is not None and stoch > 60

        # ----------------------
        # 최종 조건
        # ----------------------

        if trend_ok and momentum_ok:
            return True

        return False
