class StrategyScanner:

    def __init__(self, market):

        self.market = market

    def scan(self, universe):

        candidates = []

        for symbol in universe:

            price = self.market.get_price(symbol)

            if price is None:
                continue

            if price % 2 < 1:
                candidates.append(symbol)

        return candidates
