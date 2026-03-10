from ltb.strategy.base_strategy import BaseStrategy


class VolumeBreakoutStrategy(BaseStrategy):

    name = "volume_breakout"

    def __init__(self, config):

        self.breakout_price = config["breakout_price"]
        self.position_size = config["position_size"]

    def evaluate(self, event):

        symbol = event["symbol"]
        price = event["price"]

        if price > self.breakout_price:

            return {
                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "qty": self.position_size,
                "strategy": self.name
            }

        return None
