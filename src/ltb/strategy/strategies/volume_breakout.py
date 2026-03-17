from ltb.strategy.base_strategy import BaseStrategy


class VolumeBreakoutStrategy(BaseStrategy):

    def __init__(self, config):

        self.breakout_price = config[""]
        self.position_size = config[""]

    def evaluate(self, event):

        symbol = event["symbol"]

        if price > self.breakout_price:

            return {
            }

        return None
