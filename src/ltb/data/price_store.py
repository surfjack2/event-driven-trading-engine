from collections import defaultdict


class PriceStore:

    def __init__(self, history_limit=500):

        self.history_limit = history_limit
        self.history = defaultdict(list)

    def add_price(self, symbol, price):

        data = self.history[symbol]

        data.append(price)

        if len(data) > self.history_limit:
            data.pop(0)

    def get_history(self, symbol):

        return self.history[symbol]
