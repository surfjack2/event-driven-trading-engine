class BaseStrategy:

    name = "base"

    def evaluate(self, market_event):

        raise NotImplementedError
