class StrategyEngine:

    def __init__(self, market, config):
        self.market = market
        self.config = config

    def check_entry(self, symbol):

        indicators = self.config.get("indicators", {})

        rsi_threshold = indicators.get("rsi_threshold", 50)
        stochastic_threshold = indicators.get("stochastic_threshold", 60)

        rsi = self.market.get_rsi(symbol)
        stoch = self.market.get_stochastic(symbol)

        if rsi is None or stoch is None:
            return False

        trend_ok = rsi > rsi_threshold
        momentum_ok = stoch > stochastic_threshold

        return trend_ok and momentum_ok
