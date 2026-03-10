class StrategyEngine:

    def __init__(self, market, portfolio=None):

        self.market = market
        self.portfolio = portfolio

    # ==========================
    # Entry 조건
    # ==========================
    def check_entry(self, symbol):

        # ----------------------
        # 포지션 보유 여부 체크
        # ----------------------

        if self.portfolio:

            pos = self.portfolio.get_position(symbol)

            if pos and pos > 0:
                return False

        # ----------------------
        # 시장 데이터 조회
        # ----------------------

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
