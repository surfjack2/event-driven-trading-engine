import random


class MarketManager:

    def __init__(self, universe):

        self.universe = universe

    def set_universe(self, universe):

        self.universe = universe

    def get_price(self, symbol):

        return random.uniform(45000, 65000)
